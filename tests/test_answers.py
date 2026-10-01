import pytest

from tests.cases import ANSWER, REFUSAL, REFUSAL_PHRASES


def ask(embedder, llm, question):
    rows = embedder.search(question)
    return llm.generate(embedder.build_context(rows), question)


@pytest.mark.parametrize("question,expected", ANSWER)
def test_answer_contains_the_facts(embedder, llm, question, expected):
    answer = ask(embedder, llm, question)
    for word in expected:
        assert word.lower() in answer.lower(), (
            f"{word!r} missing from answer to {question!r}: {answer}"
        )


@pytest.mark.parametrize("question,must_not_contain", REFUSAL)
def test_refuses_what_is_not_in_the_resume(embedder, llm, question, must_not_contain):
    answer = ask(embedder, llm, question).lower()

    assert any(p in answer for p in REFUSAL_PHRASES), (
        f"expected a refusal for {question!r}, got: {answer}"
    )
    if must_not_contain:
        assert must_not_contain.lower() not in answer, (
            f"answered {question!r} from outside the resume: {answer}"
        )
