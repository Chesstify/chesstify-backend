def test_hello(test_client):
    response = test_client.get('/hello')
    assert response.status_code == 200
    assert response.data == b'Hello World!'
