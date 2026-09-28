# Live proof ledger

The first StudioNet deployment at `0x205D00D4cb08C225Faa4a1Bd6405A54B36290372` uses the initial source revision and is **superseded** by the added address-typed read methods. Its deployment transaction `0x070098d8234556e11ac4330914d3b4dfd5cde605cefcb05da25b77e26f585522` finalized with execution success. It is not evidence for the revised source. A submitted assessment transaction `0xf645e7754114f01e23c34ea19b46807b821e5ec6bd3a4b78130b005cbf16edf8` could not be verified because the StudioNet RPC failed during receipt retrieval; it is **not** counted as a proof.

The address-safe revision deployed at `0x4c536B2fECf4DFfBA8Ecf7be8Ef0B29ec4Ba78c8` (tx `0x58382067c08f66b342117c46f0492562ee9646b6d239b11b9fecc1480b3fd136`) and finalized with leader `SUCCESS` and `MAJORITY_AGREE`. Its onchain code SHA-256 matched the then-published source (`518063c714de6fa4f7a1794cb55180fc311cd66adf20b3cfd28f8fd8aab6be04`). The program was created, given two modules and sealed, then enrolled. This revision is now also **superseded** by the GitHub Contents API adapter. Do not cite it as matching the adapter source.

The first GitHub Contents adapter revision deployed at `0x25D94C9cDD83D1f9e2E5191868dAae864a0aEd9E` (tx `0xa8c656ff116204eebbeb81e9372edad49ef045de7c0c00d0ce076c0d3e2ca709`). The demonstration assessment `0xc5c0c8b17a8749fdc92dbb9017464573fbed25ab8625881de79b5eb95c03172c` executed and recorded `INCONCLUSIVE`: both GitHub API requests failed, their source statuses were `0`, and the learner index did not advance. This is a fail-closed result, **not** proof of successful semantic routing. This revision is superseded by a retry with explicit GitHub API headers and fetch-error diagnostics.

The header-fix revision deployed at `0x9a293be1da1ACeEea1729Aa5261D49d0F5ECcaC1` (tx `0x1858fb86a8c685b509e3b223775d7cfe5a5ffb399b9a8a6dd6afbcb46973e9f0`). Assessment tx `0x5968fc7c0aed95816b594624ea4953948ffb935dbedf5fa97b8ee95d1c5e9647` finalized with leader `SUCCESS` but recorded `INCONCLUSIVE`. Its stdout showed `Only base64 data is allowed`: GitHub wraps base64 content in line breaks, which strict decoding rejected. This revision is superseded by whitespace-normalizing decoding; do **not** cite the assessment as a PASS.

No whitespace-fix deployment or positive assessment is claimed until its finalized receipt shows execution success and the Explorer source matches the published contract.

Required proof matrix:

| Case | Expected effect | Explorer transaction |
| --- | --- | --- |
| Deployment | Source available at new address | Pending |
| Program + sealed rubrics | Immutable criteria configuration | Pending |
| Learner enrollment | Index 0 | Pending |
| Method work meets both criteria | ADVANCE to index 1 | Pending |
| Incomplete reproduction work | RETRY, index remains 1 | Pending |
| Complete reproduction work | COMPLETE, index 2 | Pending |
| Hash mismatch | INCONCLUSIVE, no advancement | Pending |

Do not reuse the `DynamicResearchCommons` or `DynamicLearningPath` Explorer transactions as proof for this architecture.
