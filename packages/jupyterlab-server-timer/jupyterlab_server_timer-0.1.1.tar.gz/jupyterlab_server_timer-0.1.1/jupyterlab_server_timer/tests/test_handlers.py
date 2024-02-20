import json


async def test_get_example(jp_fetch):
    # When
    response = await jp_fetch("jupyterlab-server-timer", "get-life-span")

    # Then
    assert response.code == 200
    payload = json.loads(response.body)
    assert "comment" in payload and payload["comment"] == "Server life span."
