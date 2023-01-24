from fastapi.testclient import TestClient
from main import main2

client = TestClient(main2.app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_read_main2():
    response = client.post("/post/color")
    assert response.json() == "red"


test_read_main2()
