def test_health_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_ask_returns_answer_and_session_id(client):
    res = client.post("/ask", json={"question": "What databases has he worked with?"})
    assert res.status_code == 200
    body = res.json()
    assert "PostgreSQL" in body["answer"] or "MongoDB" in body["answer"]
    assert body["session_id"]


def test_ask_reuses_given_session_id(client):
    res = client.post("/ask", json={"question": "Does he know Docker?", "session_id": "abc-123"})
    assert res.status_code == 200
    assert res.json()["session_id"] == "abc-123"


def test_ask_rejects_empty_question(client):
    res = client.post("/ask", json={"question": ""})
    assert res.status_code == 422


def test_ask_rejects_too_long_question(client):
    res = client.post("/ask", json={"question": "a" * 501})
    assert res.status_code == 422
