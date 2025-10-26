from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_plans():
    response = client.get("/plans/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert any(plan["id"] == "broker" for plan in data)


def test_create_advertiser_and_property_flow():
    advertiser_payload = {
        "name": "Imobiliária Centro",
        "email": "contato@centro.com",
        "advertiser_type": "agency",
        "plan_id": "agency",
        "document": "11222333000181",
        "document_status": "active",
        "metadata": {"cnpj": "11222333000181"},
    }
    response = client.post("/advertisers/", json=advertiser_payload)
    assert response.status_code == 201, response.text
    advertiser_data = response.json()
    advertiser_id = advertiser_data["id"]

    property_payload = {
        "advertiser_id": advertiser_id,
        "title": "Cobertura com vista panorâmica",
        "description": "Cobertura duplex com 4 suítes",
        "price": 2500000,
        "address": "Av. Paulista, 1000",
        "bedrooms": 4,
        "bathrooms": 5,
        "area_m2": 320,
        "amenities": ["Piscina", "Churrasqueira"],
    }
    response = client.post("/properties/", json=property_payload)
    assert response.status_code == 201, response.text
    property_data = response.json()
    property_id = property_data["id"]

    analytics_response = client.get(f"/analytics/properties/{property_id}")
    assert analytics_response.status_code == 200
    analytics_data = analytics_response.json()
    assert analytics_data["views"] == 0

    metric_response = client.post(f"/properties/{property_id}/metrics/views")
    assert metric_response.status_code == 200
    assert metric_response.json()["views"] == 1


def test_create_broker_requires_creci():
    payload = {
        "name": "Marcos Lima",
        "email": "marcos@example.com",
        "advertiser_type": "broker",
        "plan_id": "broker",
        "document": "987654",
        "document_status": "active",
        "metadata": {},
    }
    response = client.post("/advertisers/", json=payload)
    assert response.status_code == 400
    assert "CRECI" in response.json()["detail"]

