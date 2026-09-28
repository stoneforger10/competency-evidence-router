import base64
import hashlib
import json


RUBRIC = "Criterion method: ordered steps. Criterion evidence: measured observation with unit."
PASS = "First heat water, then measure. The measured temperature was 44 C."
FAIL = "I intend to do the experiment next week."
REPRO = "Criterion reproduction: describe repeat and result. Criterion comparison: compare with original."


def h(text):
    return hashlib.sha256(text.encode()).hexdigest()


def addr(value):
    from genlayer import Address
    return Address("0x" + value.hex())


def setup(c, vm, owner, learner):
    vm.sender = owner
    c.create_program("lab", "Lab skills")
    c.add_module("lab", "method", "https://rubric.example.org/method", h(RUBRIC), "method,evidence")
    c.add_module("lab", "repeat", "https://rubric.example.org/repeat", h(REPRO), "reproduction,comparison")
    c.seal_program("lab")
    vm.sender = learner
    c.enroll("lab")


def test_semantic_pass_advances_and_replay_fails(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy("contracts/CompetencyEvidenceRouter.py")
    setup(c, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_web(r"rubric\.example\.org/method", {"status": 200, "body": RUBRIC})
    direct_vm.mock_web(r"work\.example\.org/pass", {"status": 200, "body": PASS})
    direct_vm.mock_llm(r".*Judge only whether the work.*", json.dumps({"met": {"method": True, "evidence": True}, "decision": "PASS"}))
    c.submit_work("lab", "first", "https://work.example.org/pass", h(PASS))
    progress = json.loads(c.get_progress("lab", addr(direct_bob)))
    report = json.loads(c.get_attempt("lab", addr(direct_bob), "first"))
    assert progress["index"] == 1
    assert report["outcome"] == "ADVANCE"
    assert all(s["hash_match"] for s in report["sources"])
    with direct_vm.expect_revert("unique attempt required"):
        c.submit_work("lab", "first", "https://work.example.org/pass", h(PASS))


def test_missing_criterion_retries_without_advance(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy("contracts/CompetencyEvidenceRouter.py")
    setup(c, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_web(r"rubric\.example\.org/method", {"status": 200, "body": RUBRIC})
    direct_vm.mock_web(r"work\.example\.org/fail", {"status": 200, "body": FAIL})
    direct_vm.mock_llm(r".*Judge only whether the work.*", json.dumps({"met": {"method": False, "evidence": False}, "decision": "FAIL"}))
    c.submit_work("lab", "first", "https://work.example.org/fail", h(FAIL))
    assert json.loads(c.get_progress("lab", addr(direct_bob)))["index"] == 0
    assert json.loads(c.get_attempt("lab", addr(direct_bob), "first"))["outcome"] == "RETRY"


def test_hash_mismatch_fails_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy("contracts/CompetencyEvidenceRouter.py")
    setup(c, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_web(r"rubric\.example\.org/method", {"status": 200, "body": RUBRIC})
    direct_vm.mock_web(r"work\.example\.org/pass", {"status": 200, "body": PASS})
    c.submit_work("lab", "first", "https://work.example.org/pass", h("tampered"))
    report = json.loads(c.get_attempt("lab", addr(direct_bob), "first"))
    assert report["outcome"] == "INCONCLUSIVE"
    assert report["sources"][1]["hash_match"] is False
    assert json.loads(c.get_progress("lab", addr(direct_bob)))["index"] == 0


def test_owner_and_enrollment_boundaries(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy("contracts/CompetencyEvidenceRouter.py")
    direct_vm.sender = direct_alice
    c.create_program("lab", "Lab skills")
    with direct_vm.prank(direct_bob), direct_vm.expect_revert("program owner required"):
        c.add_module("lab", "method", "https://rubric.example.org/method", h(RUBRIC), "method")
    with direct_vm.expect_revert("sealed program and new learner required"):
        c.enroll("lab")


def test_contradictory_model_output_does_not_advance(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy("contracts/CompetencyEvidenceRouter.py")
    setup(c, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_web(r"rubric\.example\.org/method", {"status": 200, "body": RUBRIC})
    direct_vm.mock_web(r"work\.example\.org/pass", {"status": 200, "body": PASS})
    direct_vm.mock_llm(r".*Judge only whether the work.*", json.dumps({"met": {"method": False, "evidence": False}, "decision": "PASS"}))
    c.submit_work("lab", "contradiction", "https://work.example.org/pass", h(PASS))
    assert json.loads(c.get_my_attempt("lab", "contradiction"))["outcome"] == "INCONCLUSIVE"
    assert json.loads(c.get_my_progress("lab"))["index"] == 0


def test_pinned_github_contents_are_decoded_before_assessment(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy("contracts/CompetencyEvidenceRouter.py")
    rubric_url = "https://api.github.com/repos/example/fixtures/contents/rubric.txt?ref=commit"
    work_url = "https://api.github.com/repos/example/fixtures/contents/work.txt?ref=commit"
    direct_vm.sender = direct_alice
    c.create_program("lab", "Lab skills")
    c.add_module("lab", "method", rubric_url, h(RUBRIC), "method,evidence")
    c.add_module("lab", "repeat", "https://rubric.example.org/repeat", h(REPRO), "reproduction,comparison")
    c.seal_program("lab")
    direct_vm.sender = direct_bob
    c.enroll("lab")
    for url, body in ((rubric_url, RUBRIC), (work_url, PASS)):
        value = base64.b64encode(body.encode()).decode()
        encoded = value[:32] + "\n" + value[32:] + "\n"
        direct_vm.mock_web(url.replace("?", r"\?"), {"status": 200, "body": json.dumps({"encoding": "base64", "content": encoded})})
    direct_vm.mock_llm(r".*Judge only whether the work.*", json.dumps({"met": {"method": True, "evidence": True}, "decision": "PASS"}))
    c.submit_work("lab", "api-pass", work_url, h(PASS))
    report = json.loads(c.get_my_attempt("lab", "api-pass"))
    assert report["sources"][0]["sha256"] == h(RUBRIC)
    assert report["sources"][1]["sha256"] == h(PASS)
    assert report["outcome"] == "ADVANCE"
