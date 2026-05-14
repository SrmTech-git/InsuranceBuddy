# Eval Report — 2026-05-14_12-43-51

**Summary:** 19/21 cases passed (90%)

- Average source recall:   0.95
- Average content recall:  0.98

## Per-case results

| Result | Case ID | Source recall | Content recall | Notes |
|---|---|---|---|---|
| ✅ PASS | `regression-pap-part-c` | 1.00 | 1.00 | - |
| ✅ PASS | `regression-duty-to-cooperate` | 1.00 | 0.67 | missing content phrases: ['investigation'] |
| ✅ PASS | `regression-other-insurance-clause` | 1.00 | 1.00 | - |
| ✅ PASS | `regression-cg-20-10` | 1.00 | 1.00 | - |
| ✅ PASS | `regression-dec-package` | 1.00 | 1.00 | - |
| ❌ FAIL | `regression-late-notice` | 0.00 | 1.00 | missing sources: ['Exclusions and Conditions Overview'] |
| ✅ PASS | `form-lookup-acord-25` | 1.00 | 1.00 | - |
| ✅ PASS | `form-lookup-acord-130` | 1.00 | 1.00 | - |
| ✅ PASS | `statute-lookup-orc-3937-18` | 1.00 | 1.00 | - |
| ✅ PASS | `multi-form-comparison` | 1.00 | 1.00 | - |
| ✅ PASS | `form-as-context` | 1.00 | 1.00 | - |
| ❌ FAIL | `cross-state-comparison` | 1.00 | 1.00 | system refused but case expected info |
| ✅ PASS | `concept-ho3-coverage` | 1.00 | 1.00 | - |
| ✅ PASS | `concept-eo-insurance` | 1.00 | 1.00 | - |
| ✅ PASS | `concept-treaty-vs-facultative` | 1.00 | 1.00 | - |
| ✅ PASS | `concept-admitted-vs-surplus` | 1.00 | 1.00 | - |
| ✅ PASS | `concept-bad-faith` | 1.00 | 1.00 | - |
| ✅ PASS | `concept-fnol` | 1.00 | 1.00 | - |
| ✅ PASS | `ohio-um-requirement` | 1.00 | 1.00 | - |
| ✅ PASS | `should-refuse-nonexistent-form` | 1.00 | 1.00 | - |
| ✅ PASS | `should-refuse-no-state-content` | 1.00 | 1.00 | - |

## Failed cases — detail

### `regression-late-notice`
**Query:** What happens if I give late notice of a claim?
- Source recall: 0.00
- Content recall: 1.00
- Notes: missing sources: ['Exclusions and Conditions Overview']

### `cross-state-comparison`
**Query:** Compare uninsured motorist requirements between Ohio and Indiana
- Source recall: 1.00
- Content recall: 1.00
- Notes: system refused but case expected info

