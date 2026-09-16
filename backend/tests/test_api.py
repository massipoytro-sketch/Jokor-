from app import app


def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_health():
    response = client().get('/api/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'
    assert response.headers.get('X-Request-ID')


def test_regions():
    response = client().get('/api/regions')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['count'] >= 10
    assert any(item['code'] == 'IND' for item in payload['regions'])


def test_region_detail():
    response = client().get('/api/regions/EU')
    assert response.status_code == 200
    assert response.get_json()['region']['group'] == 'EUROPE'


def test_game_info():
    response = client().get('/api/game-info')
    assert response.status_code == 200
    payload = response.get_json()['data']
    assert payload['game'] == 'Free Fire'
    assert {mode['id'] for mode in payload['modes']} == {'br', 'cs'}
    assert len(payload['ranks']) >= 8


def test_invalid_uid():
    response = client().get('/api/player/IND/not-a-uid')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'INVALID_UID'


def test_unknown_player_provider_is_safe():
    response = client().get('/api/player/IND/123456789')
    assert response.status_code == 200
    assert response.get_json()['success'] is False
    assert response.get_json()['error'] == 'DATA_SOURCE_NOT_CONFIGURED'


def test_system_metrics():
    response = client().get('/api/system/metrics')
    assert response.status_code == 200
    assert response.get_json()['success'] is True


def test_health_detail():
    response = client().get('/api/system/health-detail')
    assert response.status_code == 200
    assert response.get_json()['data']['status'] == 'healthy'
