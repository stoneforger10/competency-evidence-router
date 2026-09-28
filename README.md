# CompetencyEvidenceRouter

One representative GenLayer primitive replacing the parallel `DynamicResearchCommons` and `DynamicLearningPath` graph-ordering submissions. **Do not submit those two domain variants separately.** This contract does not propose graph edges or advance an owner-controlled graph head. It routes each enrolled learner according to a validator-checked assessment of externally fetched work against a fetched rubric.

## Problem and boundary

A deterministic contract can check a hash, but cannot judge whether a piece of work meets natural-language rubric criteria. Here, the program owner fixes a short module sequence and each module's public HTTPS rubric URL, SHA-256 hash, and 1–5 criterion IDs. The program is sealed before learners enroll. A learner supplies a public work URL and its SHA-256 hash. The contract fetches **both** bodies itself, verifies full-response hashes, and asks the model to assess each criterion. Validators independently refetch both bodies and rerun the assessment; the complete decision-bearing report must match exactly.

This assesses the submitted artifact, **not authorship, credential identity, scientific truth, or independent source authority**. A learner could submit someone else's public work. Applications needing identity assurance must add an external authenticated assessment source before treating `COMPLETE` as a credential.

## State and consensus

```text
owner: create_program → add_module × 2–6 → seal_program
learner: enroll → submit_work
                     │
                     ├─ fetched rubric/work unavailable, altered or ambiguous → INCONCLUSIVE
                     ├─ at least one criterion unmet → RETRY (same module)
                     ├─ all criteria met → ADVANCE (next module)
                     └─ all criteria met on last module → COMPLETE
```

`submit_work` is the consequential nondeterministic operation. The leader and every validator fetch the same content-addressed rubric and work, verify HTTP 200, full-body SHA-256 match, UTF-8 completeness and rubric criterion presence, and independently derive the exact Boolean criterion vector and PASS/FAIL/UNKNOWN decision. A deterministic consistency rule rejects PASS with any unmet criterion and FAIL with all met. Consensus requires exact equality of context, source statuses/hashes, criterion vector, outcome and report root. Disagreement does not create an attempt or move progress.

Attempts are keyed by program, learner address and attempt ID and are immutable. The learner's on-chain index only advances on consensus-backed PASS. Failed or inconclusive attempts are recorded without advancement. The program is sealed, so rubric commitments and module order cannot change under an enrolled learner. The cap is six modules and sixteen attempts per learner.

## Demo and limitations

`examples/` contains a two-module rubric and three public demonstration submissions: a method pass, a reproduction fail and a reproduction pass. They are synthetic educational artifacts, not independently authored research. Pin their URLs to the exact published commit before registering them. The contract accepts plain HTTPS text or GitHub Contents API responses with base64-encoded file content; for the API it hashes the **decoded file**, not the JSON wrapper. `LIVE_PROOFS.md` records only executed and verified chain transactions; historical graph-submission transactions are **not** evidence for this contract.

Risks: HTTPS availability, mutable redirects, prompt injection inside fetched documents, model disagreement, and work plagiarism. Hash mismatch and ambiguity fail closed. The report root is an audit commitment, not a proof that the work is original. See `SECURITY.md`.

## Run

```powershell
python -m pip install genvm-linter genlayer-test
genvm-lint check contracts/CompetencyEvidenceRouter.py
python -m pytest tests/direct -q
genlayer network set studionet
genlayer deploy --contract contracts/CompetencyEvidenceRouter.py
```

For each write, wait for `genlayer receipt <tx>` and check both `FINALIZED` **and** leader execution `SUCCESS`; finality alone is not execution success. Then compare `genlayer code <address>` byte-for-byte with the deployed GitHub revision. StudioNet is gasless but rate-limited.

API: `create_program`, `add_module`, `seal_program`, `enroll`, `submit_work`, `get_program`, `get_progress`, `get_my_progress`, `get_attempt`, `get_my_attempt`.

Live StudioNet source and the finalized ADVANCE → RETRY → COMPLETE proof matrix are in [LIVE_PROOFS.md](LIVE_PROOFS.md). Use [SUBMISSION.md](SUBMISSION.md) for a single representative Builder submission; do not resubmit the two earlier graph-domain variants.
