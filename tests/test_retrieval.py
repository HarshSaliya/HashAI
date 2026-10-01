import pytest

from tests.cases import RETRIEVAL

TOP_K = 3


@pytest.mark.parametrize("question,expected", RETRIEVAL)
def test_expected_chunk_is_retrieved(embedder, question, expected):
    rows = embedder.search(question, limit=TOP_K)
    hits = [r["content"] for r in rows]
    assert any(expected in h for h in hits), (
        f"{expected!r} not in top {TOP_K} for {question!r}"
    )


def test_search_respects_limit(embedder):
    assert len(embedder.search("databases", limit=2)) == 2


def test_results_are_ordered_by_distance(embedder):
    rows = embedder.search("What databases has he worked with?", limit=5)
    distances = [r["distance"] for r in rows]
    assert distances == sorted(distances)


def test_context_joins_every_chunk(embedder):
    rows = embedder.search("databases", limit=3)
    context = embedder.build_context(rows)
    for row in rows:
        assert row["content"] in context
