# Live proof ledger

The first StudioNet deployment at `0x205D00D4cb08C225Faa4a1Bd6405A54B36290372` uses the initial source revision and is **superseded** by the added address-typed read methods. Its deployment transaction `0x070098d8234556e11ac4330914d3b4dfd5cde605cefcb05da25b77e26f585522` finalized with execution success. It is not evidence for the revised source. A submitted assessment transaction `0xf645e7754114f01e23c34ea19b46807b821e5ec6bd3a4b78130b005cbf16edf8` could not be verified because the StudioNet RPC failed during receipt retrieval; it is **not** counted as a proof.

No revised deployment or lifecycle transaction is claimed until its finalized receipt shows execution success and the Explorer source matches the published contract.

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
