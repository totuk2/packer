from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_packer_api_response():
    response = client.post("/", json={
                                              "items": {
                                              "item1": {
                                                "name": "item1",
                                                "quantity": 2,
                                                "width": 2,
                                                "hight": 4,
                                                "depth": 3,
                                                "weight": 2
                                              }
                                            },
                                              "bins": {
                                              "box2": {
                                                "name": "box1",
                                                "width": 10,
                                                "hight": 10,
                                                "depth": 10,
                                                "max_weight": 10
                                              }
                                              }
                                            })

    assert response.json() == {"0": {
                                  "name": "box1",
                                  "width": 10,
                                  "height": 10,
                                  "depth": 10,
                                  "max_weight": 10,
                                  "items": [
                                    {
                                      "name": "item1",
                                      "width": 2,
                                      "height": 4,
                                      "depth": 3,
                                      "weight": 2,
                                      "rotation_type": 0,
                                      "position": [
                                        0,
                                        0,
                                        0
                                      ]
                                    },
                                    {
                                      "name": "item1",
                                      "width": 2,
                                      "height": 4,
                                      "depth": 3,
                                      "weight": 2,
                                      "rotation_type": 0,
                                      "position": [
                                        2,
                                        0,
                                        0
                                      ]
                                    }
                                  ],
                                  "efficacy": 0.048
                                }}
