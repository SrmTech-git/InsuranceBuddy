"""
insurance-rag test suite
Run from project root:
    python tests/test_suite.py
    python tests/test_suite.py --skip-api   # skip the live Haiku call
"""

import sys
import unittest
from pathlib import Path

# Make src/ importable regardless of where this file is run from
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# =============================================================================
# 1. UNIT TESTS — pure Python, no DB, no API
# =============================================================================

class TestStatesModule(unittest.TestCase):
    """Verify states.py is the single source of truth used everywhere."""

    def setUp(self):
        from states import STATE_MAP
        from ingest_batch import STATE_FOLDER_MAP
        from chat import _STATE_NAME_MAP
        self.canonical = STATE_MAP
        self.folder_map = STATE_FOLDER_MAP
        self.name_map = _STATE_NAME_MAP

    def test_state_map_nonempty(self):
        self.assertGreater(len(self.canonical), 0)

    def test_ingest_batch_uses_canonical_map(self):
        self.assertIs(self.folder_map, self.canonical,
                      "STATE_FOLDER_MAP in ingest_batch should be the same object as STATE_MAP")

    def test_chat_uses_canonical_map(self):
        self.assertIs(self.name_map, self.canonical,
                      "_STATE_NAME_MAP in chat should be the same object as STATE_MAP")

    def test_all_known_states_present(self):
        expected = {"OH", "IN", "IL", "KY", "MN", "VA", "MI", "GA", "TN", "IA", "WI"}
        actual = set(self.canonical.values())
        self.assertEqual(expected, actual)

    def test_keys_are_lowercase(self):
        for key in self.canonical:
            self.assertEqual(key, key.lower(), f"Key '{key}' should be lowercase")

    def test_values_are_uppercase(self):
        for val in self.canonical.values():
            self.assertEqual(val, val.upper(), f"Value '{val}' should be uppercase")
            self.assertEqual(len(val), 2, f"State code '{val}' should be 2 characters")

    def test_xlsx_header_map_derived_from_canonical(self):
        """ingest_xlsx must derive its header map from STATE_MAP, not hardcode it."""
        from ingest_xlsx import _HEADER_TO_STATE
        # Same set of state codes
        self.assertEqual(set(_HEADER_TO_STATE.values()), set(self.canonical.values()))
        # Title-cased keys ("Ohio") match the spreadsheet column headers
        for header, code in _HEADER_TO_STATE.items():
            self.assertEqual(header, header.title(),
                             f"Header '{header}' should be Title Case")
            self.assertEqual(self.canonical.get(header.lower()), code,
                             f"Header '{header}' code mismatch with STATE_MAP")


class TestAbbreviations(unittest.TestCase):
    def setUp(self):
        from abbreviations import expand_abbreviations
        self.expand = expand_abbreviations

    def test_single_abbreviation(self):
        result = self.expand("Does Ohio require UM coverage?")
        self.assertIn("uninsured motorist coverage", result)
        self.assertNotIn(" UM ", result)

    def test_multiple_abbreviations(self):
        result = self.expand("What are the BI and PD limits?")
        self.assertIn("bodily injury coverage", result)
        self.assertIn("property damage coverage", result)

    def test_no_change_plain_text(self):
        q = "What is the minimum coverage requirement?"
        self.assertEqual(self.expand(q), q)

    def test_case_insensitive_match(self):
        # lowercase 'um' in a sentence — should still expand
        result = self.expand("Is um coverage required in Ohio?")
        self.assertIn("uninsured motorist coverage", result)

    def test_uim_expansion(self):
        result = self.expand("UIM limits in Indiana")
        self.assertIn("underinsured motorist coverage", result)

    def test_whole_word_only(self):
        # "CLUE" inside "CLUED" should not expand
        result = self.expand("I was CLUED in on the policy details")
        # "CLUED" should NOT be touched — 'CLUE' only matches as whole word
        self.assertNotIn("comprehensive loss underwriting exchange", result)


class TestParseFilename(unittest.TestCase):
    def setUp(self):
        from ingest import parse_filename
        self.parse = parse_filename

    def test_full_format(self):
        path = r"data\raw\regulatory\ohio\ORC3937 (Rev. 01/2020) Uninsured Motorist Coverage.pdf"
        meta = self.parse(path)
        self.assertTrue(meta["form_number"].startswith("ORC3937"))
        self.assertIn("2020", meta["edition_date"])
        self.assertIn("Uninsured", meta["description"])
        self.assertTrue(meta["parsed"])

    def test_no_edition_date(self):
        path = r"data\raw\educational\GL Overview General Liability.txt"
        meta = self.parse(path)
        # No form number in this path — should still parse description
        self.assertEqual(meta["edition_date"], "")

    def test_no_form_number(self):
        path = r"data\raw\educational\inland_marine_overview.txt"
        meta = self.parse(path)
        self.assertEqual(meta["form_number"], "")
        self.assertFalse(meta["parsed"])

    def test_oac_format(self):
        path = r"data\raw\regulatory\ohio\OAC3901-1 (04/2019) Filing Rules.pdf"
        meta = self.parse(path)
        self.assertTrue(meta["form_number"].upper().startswith("OAC"))
        self.assertTrue(meta["parsed"])

    def test_display_filename_no_directory(self):
        path = r"C:\Users\shann\insurance-rag\data\raw\regulatory\ohio\ORC3937.18 (Rev. 01/2020) UM Coverage.pdf"
        meta = self.parse(path)
        # filename field should be just the basename, not the full path
        self.assertNotIn("\\", meta["filename"])
        self.assertNotIn("Users", meta["filename"])


class TestDetectFormNumber(unittest.TestCase):
    def setUp(self):
        from chat import detect_form_number, detect_bare_section
        self.detect = detect_form_number
        self.detect_bare = detect_bare_section

    def test_orc_with_dot(self):
        result = self.detect("What does ORC 3937.18 say?")
        self.assertEqual(result, "ORC3937.18")

    def test_orc_no_space(self):
        result = self.detect("Tell me about ORC3937.18")
        self.assertEqual(result, "ORC3937.18")

    def test_oac_with_dash(self):
        result = self.detect("What is OAC 3901-1-54?")
        self.assertEqual(result, "OAC3901-1-54")

    def test_no_form_number(self):
        result = self.detect("Does Ohio require uninsured motorist coverage?")
        self.assertIsNone(result)

    def test_bare_section_dot(self):
        result = self.detect_bare("What does 3937.18 require?")
        self.assertEqual(result, "3937.18")

    def test_bare_section_dash(self):
        result = self.detect_bare("Explain section 3901-1-54")
        self.assertEqual(result, "3901-1-54")

    def test_bare_integer_ignored(self):
        # A lone integer (no dots or dashes) should not match
        result = self.detect_bare("What is the 12 month rule?")
        self.assertIsNone(result)


class TestIsInventoryQuery(unittest.TestCase):
    def setUp(self):
        from chat import is_inventory_query
        self.check = is_inventory_query

    def test_what_forms_do_we_have(self):
        self.assertTrue(self.check("What forms do we have?"))

    def test_list_all_documents(self):
        self.assertTrue(self.check("List all documents"))

    def test_show_me_forms(self):
        self.assertTrue(self.check("Show me all forms available"))

    def test_what_do_we_have(self):
        self.assertTrue(self.check("What do we have in the database?"))

    def test_which_forms(self):
        self.assertTrue(self.check("Which forms cover UM?"))

    def test_normal_question_not_inventory(self):
        self.assertFalse(self.check("Does Ohio require UM coverage?"))

    def test_specific_statute_not_inventory(self):
        self.assertFalse(self.check("What does ORC 3937.18 say about UM?"))


class TestDetectStates(unittest.TestCase):
    def setUp(self):
        from chat import detect_states
        self.detect = detect_states

    def test_full_name_ohio(self):
        self.assertIn("OH", self.detect("Does Ohio require UM coverage?"))

    def test_full_name_indiana(self):
        self.assertIn("IN", self.detect("What are Indiana's BI minimums?"))

    def test_uppercase_abbr(self):
        self.assertIn("OH", self.detect("What does OH require for PIP?"))

    def test_lowercase_abbr_ignored(self):
        # "oh" lowercase should NOT match as Ohio
        result = self.detect("Oh, I see the policy has changed")
        self.assertNotIn("OH", result)

    def test_multiple_states(self):
        result = self.detect("Compare Ohio and Indiana requirements")
        self.assertIn("OH", result)
        self.assertIn("IN", result)

    def test_no_state(self):
        result = self.detect("What is general liability coverage?")
        self.assertEqual(result, [])

    def test_all_supported_states(self):
        queries = {
            "Illinois": "IL",
            "Kentucky": "KY",
            "Minnesota": "MN",
            "Virginia": "VA",
            "Michigan": "MI",
            "Georgia": "GA",
            "Tennessee": "TN",
            "Iowa": "IA",
            "Wisconsin": "WI",
        }
        for name, code in queries.items():
            with self.subTest(state=name):
                self.assertIn(code, self.detect(f"What does {name} require?"))


class TestBuildStateFilter(unittest.TestCase):
    def setUp(self):
        from chat import _build_state_filter
        self.build = _build_state_filter

    def test_no_states(self):
        self.assertIsNone(self.build([]))

    def test_single_state(self):
        result = self.build(["OH"])
        self.assertEqual(result, {"state": "OH"})

    def test_two_states(self):
        result = self.build(["IN", "OH"])
        self.assertIn("$or", result)
        self.assertEqual(len(result["$or"]), 2)
        state_values = {c["state"] for c in result["$or"]}
        self.assertEqual(state_values, {"IN", "OH"})


class TestMergeFilters(unittest.TestCase):
    def setUp(self):
        from chat import _merge_filters
        self.merge = _merge_filters

    def test_all_none(self):
        self.assertIsNone(self.merge(None, None))

    def test_one_filter_one_none(self):
        f = {"form_number": "ORC3937.18"}
        self.assertEqual(self.merge(f, None), f)

    def test_two_filters(self):
        f1 = {"form_number": "ORC3937.18"}
        f2 = {"state": "OH"}
        result = self.merge(f1, f2)
        self.assertIn("$and", result)
        self.assertIn(f1, result["$and"])
        self.assertIn(f2, result["$and"])

    def test_single_filter_no_and_wrap(self):
        f = {"state": "IN"}
        result = self.merge(None, f, None)
        # Should return the filter directly, not wrapped in $and
        self.assertNotIn("$and", result)
        self.assertEqual(result, f)


class TestComparisonRouting(unittest.TestCase):
    """detect_collection comparison fast-path — no API call needed."""
    def setUp(self):
        from chat import detect_collection, COLLECTION_REGISTRY
        self.detect = detect_collection
        self.all_collections = list(COLLECTION_REGISTRY.keys())

    def test_vs_returns_all_collections(self):
        result = self.detect("UM coverage in Ohio vs Indiana")
        self.assertEqual(sorted(result), sorted(self.all_collections))

    def test_compare_returns_all_collections(self):
        result = self.detect("Compare Ohio and Indiana BI limits")
        self.assertEqual(sorted(result), sorted(self.all_collections))

    def test_difference_between_returns_all_collections(self):
        result = self.detect("What is the difference between UM and UIM?")
        self.assertEqual(sorted(result), sorted(self.all_collections))


# =============================================================================
# 2. DB INTEGRATION TESTS — ChromaDB only, no API
# =============================================================================

class TestDatabase(unittest.TestCase):
    def setUp(self):
        from db import get_collection
        self.get_collection = get_collection

    def test_regulatory_collection_exists(self):
        col = self.get_collection("regulatory")
        self.assertIsNotNone(col)

    def test_educational_collection_exists(self):
        col = self.get_collection("educational")
        self.assertIsNotNone(col)

    def test_regulatory_has_vectors(self):
        col = self.get_collection("regulatory")
        count = col.count()
        self.assertGreater(count, 0, "regulatory collection should have at least 1 vector")

    def test_educational_has_vectors(self):
        col = self.get_collection("educational")
        count = col.count()
        self.assertGreater(count, 0, "educational collection should have at least 1 vector")


class TestRetrieve(unittest.TestCase):
    def setUp(self):
        from retrieve import list_all_forms, find_form, query
        self.list_all_forms = list_all_forms
        self.find_form = find_form
        self.query = query

    def test_list_regulatory_forms_nonempty(self):
        forms = self.list_all_forms("regulatory")
        self.assertGreater(len(forms), 0)

    def test_list_educational_forms_nonempty(self):
        forms = self.list_all_forms("educational")
        self.assertGreater(len(forms), 0)

    def test_forms_have_required_keys(self):
        forms = self.list_all_forms("regulatory")
        required_keys = {"form_number", "edition_date", "description", "filename", "chunk_count"}
        for form in forms[:5]:  # spot check first 5
            self.assertTrue(required_keys.issubset(form.keys()), f"Missing keys in: {form}")

    def test_find_known_orc_form(self):
        result = self.find_form("ORC3937.18", "regulatory")
        self.assertIsNotNone(result, "ORC3937.18 should exist in the regulatory collection")

    def test_find_nonexistent_form_returns_none(self):
        result = self.find_form("DOESNOTEXIST999", "regulatory")
        self.assertIsNone(result)

    def test_semantic_query_returns_results(self):
        results = self.query("uninsured motorist coverage", n_results=5, collection_name="regulatory")
        docs = results["documents"][0]
        self.assertGreater(len(docs), 0, "Should return at least one result")

    def test_state_filter_ohio(self):
        from retrieve import query
        results = query(
            "uninsured motorist coverage",
            n_results=5,
            filters={"state": "OH"},
            collection_name="regulatory",
        )
        metas = results["metadatas"][0]
        for meta in metas:
            self.assertEqual(meta.get("state"), "OH", f"Expected state=OH, got: {meta.get('state')}")

    def test_educational_query(self):
        results = self.query("what is inland marine coverage", n_results=3, collection_name="educational")
        docs = results["documents"][0]
        self.assertGreater(len(docs), 0)


# =============================================================================
# 3. API INTEGRATION TEST — requires live Anthropic API key
# =============================================================================

class TestAskEndToEnd(unittest.TestCase):
    """Full pipeline tests — skipped if --skip-api flag is passed."""

    def setUp(self):
        from chat import ask, detect_collection
        self.ask = ask
        self.detect_collection = detect_collection

    def test_llm_routes_regulatory_question(self):
        result = self.detect_collection("Does Ohio require uninsured motorist coverage by law?")
        self.assertIn("regulatory", result)

    def test_llm_routes_educational_question(self):
        result = self.detect_collection("What is inland marine coverage and how does it work?")
        self.assertIn("educational", result)

    def test_ask_ohio_um_requirement(self):
        answer = self.ask("Does Ohio require uninsured motorist coverage?")
        self.assertIsInstance(answer, str)
        self.assertGreater(len(answer), 50, "Answer should be a non-trivial response")
        # Should reference Ohio or UM somehow
        lower = answer.lower()
        self.assertTrue(
            any(kw in lower for kw in ["ohio", "uninsured", "motorist", "3937"]),
            f"Answer doesn't seem relevant: {answer[:200]}"
        )

    def test_ask_educational_question(self):
        answer = self.ask("What is inland marine coverage?")
        self.assertIsInstance(answer, str)
        self.assertGreater(len(answer), 50)
        self.assertIn("inland marine", answer.lower())

    def test_ask_multi_state_query(self):
        answer = self.ask("What are Ohio's BI liability minimums?")
        self.assertIsInstance(answer, str)
        self.assertGreater(len(answer), 50)


# =============================================================================
# Runner
# =============================================================================

if __name__ == "__main__":
    skip_api = "--skip-api" in sys.argv
    if skip_api:
        sys.argv.remove("--skip-api")
        # Monkey-patch the API test class to skip all its tests
        for name in dir(TestAskEndToEnd):
            if name.startswith("test_"):
                setattr(
                    TestAskEndToEnd,
                    name,
                    unittest.skip("--skip-api flag set")(getattr(TestAskEndToEnd, name)),
                )

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Load in display order
    for cls in [
        TestStatesModule,
        TestAbbreviations,
        TestParseFilename,
        TestDetectFormNumber,
        TestIsInventoryQuery,
        TestDetectStates,
        TestBuildStateFilter,
        TestMergeFilters,
        TestComparisonRouting,
        TestDatabase,
        TestRetrieve,
        TestAskEndToEnd,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
