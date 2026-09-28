# Security scope

Only public, non-sensitive work may be submitted; fetched text and exact hashes become visible in consensus execution. Never submit private student data. The contract judges artifact-to-rubric fit, not authorship. No token payout or transferable credential is implemented.

Owner controls module registration but cannot edit a sealed program. Learners control their own enrollment and attempts; an attempt is permanently bound to the learner address, module index, program, URL, hashes and unique ID. Replay and cross-learner reads cannot change progress. Network, hash, decoding, rubric omission and ambiguous model results become `INCONCLUSIVE` without advancement. Validators independently recompute all consequential fields. Prompt injection is mitigated by treating fetched documents as data and constraining the output vector, but cannot be eliminated categorically.

URL validation is syntactic only. Deployment operators should constrain the GenVM network egress policy; do not rely on this contract as an SSRF firewall. A redirected response is accepted only if its final body matches the precommitted SHA-256. Source availability is not guaranteed. Exact validator comparison can lead to liveness failure when model judgments diverge; this is safer than accepting a unilateral PASS.
