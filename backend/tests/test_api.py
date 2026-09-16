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
    assert 'IND' in response.get_json()['regions']


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
