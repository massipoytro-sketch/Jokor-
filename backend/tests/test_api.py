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
    assert not any(item['code'] == 'EU' for item in payload['regions'])


def test_region_detail():
    response = client().get('/api/regions/ME')
    assert response.status_code == 200
    assert response.get_json()['region']['group'] == 'GLOBAL'


def test_game_info():
    response = client().get('/api/game-info')
    assert response.status_code == 200
    payload = response.get_json()['data']
    assert payload['game'] == 'Free Fire'
    assert {mode['id'] for mode in payload['modes']} == {'br', 'cs'}
    assert len(payload['ranks']) >= 8


def test_catalog():
    response = client().get('/api/catalog')
    assert response.status_code == 200
    payload = response.get_json()['data']
    assert len(payload['regions']) >= 6
    assert {mode['id'] for mode in payload['modes']} == {'br', 'cs'}


def test_service_registry():
    response = client().get('/api/services')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is True
    assert payload['count'] >= 24
    assert any(item['id'] == 'leaderboards' for item in payload['data'])
    assert any(item['id'] == 'player-intelligence' for item in payload['data'])


def test_service_filter():
    response = client().get('/api/services?status=provider-dependent')
    assert response.status_code == 200
    assert all(item['status'] == 'provider-dependent' for item in response.get_json()['data'])


def test_service_detail_and_missing_service():
    response = client().get('/api/services/player-profile')
    assert response.status_code == 200
    assert response.get_json()['data']['group'] == 'player'

    response = client().get('/api/services/not-real')
    assert response.status_code == 404
    assert response.get_json()['error']['code'] == 'SERVICE_NOT_FOUND'


def test_player_intelligence_validation_and_safe_fallback():
    response = client().get('/api/player/IND/not-a-uid/intelligence')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'INVALID_REQUEST'

    response = client().get('/api/player/IND/123456789/intelligence')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is False
    assert payload['data']['profile_completeness'] == 0
    assert payload['data']['available_sections'] == []


def test_player_comparison_returns_real_br_and_explicit_cs_unavailable():
    response = client().get('/api/player/IND/123456789/compare/987654321')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is False
    assert payload['comparison']['br']['win_rate']['delta_a_minus_b'] is None
    assert payload['comparison']['cs']['available'] is False
    assert payload['players']['a']['uid'] == '123456789'
    assert payload['players']['b']['uid'] == '987654321'


def test_invalid_uid():
    response = client().get('/api/player/IND/not-a-uid')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'INVALID_UID'


def test_unsupported_region_is_rejected():
    response = client().get('/api/player/EU/123456789')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'INVALID_REGION'


def test_system_metrics():
    response = client().get('/api/system/metrics')
    assert response.status_code == 200
    assert response.get_json()['success'] is True


def test_health_detail():
    response = client().get('/api/system/health-detail')
    assert response.status_code == 200
    assert response.get_json()['data']['status'] == 'healthy'
