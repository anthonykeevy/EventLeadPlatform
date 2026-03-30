from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def api_client():
    with TestClient(app) as client:
        yield client


def _valid_definition_payload():
    return {
        "definition": {
            "schemaVersion": "1.0",
            "formId": "story-6-1-form",
            "theme": {
                "primaryColor": "#0055FF",
                "backgroundColor": "#FFFFFF",
                "fontFamily": "Inter",
            },
            "canvasSettings": {
                "width": 500,
                "height": 400,
                "gridSize": 8,
            },
            "pages": [
                {
                    "id": "page-1",
                    "title": "Page 1",
                    "components": [
                        {
                            "id": "component-a",
                            "type": "text",
                            "props": {"label": "Name"},
                            "position": {"x": 20, "y": 20},
                            "style": {"width": 120, "height": 60},
                        },
                        {
                            "id": "component-b",
                            "type": "email",
                            "props": {"label": "Email"},
                            "position": {"x": 180, "y": 20},
                            "style": {"width": 120, "height": 60},
                        },
                    ],
                }
            ],
        }
    }


def test_t1_endpoint_available_in_openapi_and_returns_200(api_client):
    openapi = api_client.get("/openapi.json")
    assert openapi.status_code == 200
    assert "/api/form-validate" in openapi.json()["paths"]

    response = api_client.post("/api/form-validate", json=_valid_definition_payload())
    assert response.status_code == 200


def test_t2_valid_payload_returns_expected_clean_contract(api_client):
    response = api_client.post("/api/form-validate", json=_valid_definition_payload())
    assert response.status_code == 200

    body = response.json()
    assert body["valid"] is True
    assert body["schemaErrors"] == []
    assert body["boundaryViolations"] == []
    assert body["collisions"] == []
    assert body["summary"]["errorCount"] == 0
    assert body["summary"]["warningCount"] == 0


def test_t3_schema_invalid_payload_returns_structured_schema_errors(api_client):
    payload = _valid_definition_payload()
    del payload["definition"]["formId"]

    response = api_client.post("/api/form-validate", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["valid"] is False
    assert len(body["schemaErrors"]) > 0
    assert body["boundaryViolations"] == []
    assert body["collisions"] == []
    assert body["summary"]["errorCount"] == len(body["schemaErrors"])

    sample = body["schemaErrors"][0]
    assert set(sample.keys()) == {"path", "message", "code"}


def test_t4_boundary_violation_returns_direction_flags(api_client):
    payload = _valid_definition_payload()
    payload["definition"]["pages"][0]["components"][0]["position"] = {"x": -10, "y": 10}
    payload["definition"]["pages"][0]["components"][1]["position"] = {"x": 450, "y": 360}
    payload["definition"]["pages"][0]["components"][1]["style"] = {"width": 100, "height": 80}

    response = api_client.post("/api/form-validate", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["valid"] is False
    assert len(body["boundaryViolations"]) >= 2

    violations_by_component = {
        item["componentId"]: item["violations"] for item in body["boundaryViolations"]
    }
    assert violations_by_component["component-a"]["left"] is True
    assert violations_by_component["component-b"]["right"] is True
    assert violations_by_component["component-b"]["bottom"] is True


def test_t5_collision_violation_returns_component_relationships(api_client):
    payload = _valid_definition_payload()
    payload["definition"]["pages"][0]["components"][1]["position"] = {"x": 90, "y": 40}

    response = api_client.post("/api/form-validate", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["valid"] is False
    assert len(body["collisions"]) == 1
    collision = body["collisions"][0]
    assert collision["componentAId"] == "component-a"
    assert collision["componentBId"] == "component-b"
    assert collision["overlapArea"] > 0


def test_t6_deterministic_for_identical_payload(api_client):
    payload = _valid_definition_payload()
    payload["definition"]["pages"][0]["components"][1]["position"] = {"x": 90, "y": 40}

    response_1 = api_client.post("/api/form-validate", json=deepcopy(payload))
    response_2 = api_client.post("/api/form-validate", json=deepcopy(payload))

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_1.json() == response_2.json()


def test_t7_malformed_json_parseable_payload_returns_controlled_response(api_client):
    payload = {"definition": "this is not an object"}
    response = api_client.post("/api/form-validate", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["valid"] is False
    assert body["boundaryViolations"] == []
    assert body["collisions"] == []
    assert len(body["schemaErrors"]) == 1
    assert "definition" in body["schemaErrors"][0]["path"]


def test_story_621_url_rating_paragraph_types_accepted(api_client):
    """Story 6.2.1: validator must accept url, rating, and paragraph components."""
    payload = _valid_definition_payload()
    comps = payload["definition"]["pages"][0]["components"]
    base_y = 120
    extra = [
        ("c-url", "url", {"label": "Site", "urlPrefix": "https://"}),
        ("c-rating", "rating", {"label": "Score", "ratingMax": 5, "ratingStyle": "stars"}),
        ("c-paragraph", "paragraph", {"label": "Note", "content": "Hello"}),
    ]
    for i, (cid, ctype, props) in enumerate(extra):
        comps.append(
            {
                "id": cid,
                "type": ctype,
                "props": props,
                "position": {"x": 20, "y": base_y + i * 72},
                "style": {"width": 200, "height": 56},
            }
        )
    response = api_client.post("/api/form-validate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert body["schemaErrors"] == []
