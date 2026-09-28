# Live proof ledger

No deployment or transaction is claimed here until its finalized receipt shows execution success and the Explorer source matches the published contract.

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
