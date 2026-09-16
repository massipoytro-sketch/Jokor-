from app import app


def test_derive_stats_calculates_rates():
    client = app.test_client()
    response = client.post("/api/tools/derive-stats", json={
        "stats": {"matches": 20, "wins": 5, "kills": 60, "deaths": 30, "headshots": 18}
    })
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["metrics"]["win_rate_pct"] == 25.0
    assert payload["metrics"]["kd_ratio"] == 2.0
    assert payload["metrics"]["headshot_rate_pct"] == 30.0


def test_derive_stats_rejects_negative_values():
    client = app.test_client()
    response = client.post("/api/tools/derive-stats", json={"stats": {"kills": -1}})
    assert response.status_code == 400
    assert response.get_json()["error"] == "INVALID_STAT_VALUE"


def test_derive_stats_returns_null_for_missing_counters():
    client = app.test_client()
    response = client.post("/api/tools/derive-stats", json={"stats": {"kills": 10}})
    assert response.status_code == 200
    metrics = response.get_json()["metrics"]
    assert metrics["kd_ratio"] is None
    assert metrics["win_rate_pct"] is None
