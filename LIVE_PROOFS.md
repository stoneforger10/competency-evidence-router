# Live proof ledger

The first StudioNet deployment at `0x205D00D4cb08C225Faa4a1Bd6405A54B36290372` uses the initial source revision and is **superseded** by the added address-typed read methods. Its deployment transaction `0x070098d8234556e11ac4330914d3b4dfd5cde605cefcb05da25b77e26f585522` finalized with execution success. It is not evidence for the revised source. A submitted assessment transaction `0xf645e7754114f01e23c34ea19b46807b821e5ec6bd3a4b78130b005cbf16edf8` could not be verified because the StudioNet RPC failed during receipt retrieval; it is **not** counted as a proof.

The address-safe revision deployed at `0x4c536B2fECf4DFfBA8Ecf7be8Ef0B29ec4Ba78c8` (tx `0x58382067c08f66b342117c46f0492562ee9646b6d239b11b9fecc1480b3fd136`) and finalized with leader `SUCCESS` and `MAJORITY_AGREE`. Its onchain code SHA-256 matched the then-published source (`518063c714de6fa4f7a1794cb55180fc311cd66adf20b3cfd28f8fd8aab6be04`). The program was created, given two modules and sealed, then enrolled. This revision is now also **superseded** by the GitHub Contents API adapter. Do not cite it as matching the adapter source.

The first GitHub Contents adapter revision deployed at `0x25D94C9cDD83D1f9e2E5191868dAae864a0aEd9E` (tx `0xa8c656ff116204eebbeb81e9372edad49ef045de7c0c00d0ce076c0d3e2ca709`). The demonstration assessment `0xc5c0c8b17a8749fdc92dbb9017464573fbed25ab8625881de79b5eb95c03172c` executed and recorded `INCONCLUSIVE`: both GitHub API requests failed, their source statuses were `0`, and the learner index did not advance. This is a fail-closed result, **not** proof of successful semantic routing. This revision is superseded by a retry with explicit GitHub API headers and fetch-error diagnostics.

The header-fix revision deployed at `0x9a293be1da1ACeEea1729Aa5261D49d0F5ECcaC1` (tx `0x1858fb86a8c685b509e3b223775d7cfe5a5ffb399b9a8a6dd6afbcb46973e9f0`). Assessment tx `0x5968fc7c0aed95816b594624ea4953948ffb935dbedf5fa97b8ee95d1c5e9647` finalized with leader `SUCCESS` but recorded `INCONCLUSIVE`. Its stdout showed `Only base64 data is allowed`: GitHub wraps base64 content in line breaks, which strict decoding rejected. This revision is superseded by whitespace-normalizing decoding; do **not** cite the assessment as a PASS.

## Current deployment — matching source

StudioNet contract: [0x5F66D8d221b0D678Bfc767B8095b36d5435e4649](https://explorer-studio.genlayer.com/address/0x5F66D8d221b0D678Bfc767B8095b36d5435e4649).

`gen_getContractCode` bytes equal `contracts/CompetencyEvidenceRouter.py` at commit `3bf70d3` byte-for-byte. SHA-256: `92645bd307a19091e53c1ac058fd8ae4f83889c08f3ff67ee41ef77c544a8d29`. Every transaction below was checked through `eth_getTransactionByHash`: `FINALIZED`, `MAJORITY_AGREE`, leader execution `SUCCESS`.

| Case | Verified effect | Explorer transaction |
| --- | --- | --- |
| Deployment | Source matches pinned repository file | [0xd957…3e7f](https://explorer-studio.genlayer.com/tx/0xd957930a336a90af3458145d26d54e6b06364fdf40a81711e73e5f8c0ea83e7f) |
| Program creation | `lab-api-v3` initialized | [0x7038…419c](https://explorer-studio.genlayer.com/tx/0x70383c0e6f90c92c396afaf434ccd5c826f5a124cb7097e236b5741a9bf0419c) |
| Method rubric | Pinned URL and decoded-file SHA-256 registered | [0xd945…8f70](https://explorer-studio.genlayer.com/tx/0xd9455007a3660bf1b4b32600353e3fa8332af4c25c8576b1cfd4007dfb9c8f70) |
| Reproduction rubric | Second pinned URL and SHA-256 registered | [0x83fc…7a8d](https://explorer-studio.genlayer.com/tx/0x83fc8c7f9d36e07c235e044c403db702b58d053f7351e6b9aa8402d7fc977a8d) |
| Program seal | Rubric configuration made immutable | [0x4ec9…4874](https://explorer-studio.genlayer.com/tx/0x4ec9670e443eb581bbbaf365f4a7543d2b35a0371ac48d7512d1265f021f4874) |
| Learner enrollment | Index 0, ACTIVE | [0xd984…b252](https://explorer-studio.genlayer.com/tx/0xd984fb40c046484aa15d48899a9febc93b05f16869b44e673ab445629521b252) |
| Method assessment | Both fetched sources HTTP 200 and hash-matched; `method=true`, `evidence=true`, PASS → ADVANCE | [0xfb16…1650](https://explorer-studio.genlayer.com/tx/0xfb16a40371637b6de9038913c61582bf7a94af9ba6541668568ba2dc79751650) |
| Incomplete reproduction | Both sources matched; `reproduction=false`, `comparison=false`, FAIL → RETRY; index remains 1 | [0x4769…b7ba](https://explorer-studio.genlayer.com/tx/0x47691d04642a3d37ee1892f62c163c24e8db980836c740bee2c5fb921201b7ba) |
| Complete reproduction | Both sources matched; `reproduction=true`, `comparison=true`, PASS → COMPLETE; index 2 | [0x3fc6…816b](https://explorer-studio.genlayer.com/tx/0x3fc6fab41dc5de5536339ac53cb1b22d7013d34e815d6a9c1df25c4a4357816b) |

The final `get_my_progress("lab-api-v3")` returned `{"attempts":3,"index":2,"state":"COMPLETE"}`. A hash-mismatch path is covered by direct tests, **not** claimed as an onchain proof.

Do not reuse the `DynamicResearchCommons` or `DynamicLearningPath` Explorer transactions as proof for this architecture.
