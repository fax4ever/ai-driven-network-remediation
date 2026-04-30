def test_hello(chatbot_client):
    response = chatbot_client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}
