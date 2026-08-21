import uuid


def test_create_tender(client, test_user_id):
    """Тест: создание тендера"""
    response = client.post(
        "/tenders",
        json={
            "title": "Новый тендер",
            "description": "Описание тендера",
            "created_by": str(test_user_id)
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Новый тендер"
    assert data["status"] == "draft"
    assert data["created_by"] == str(test_user_id)


def test_get_tender(client, test_tender):
    """Тест: получение тендера по ID"""
    response = client.get(f"/tenders/{test_tender.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_tender.id)
    assert data["title"] == test_tender.title
    assert data["description"] == test_tender.description


def test_get_tender_not_found(client):
    """Тест: получение несуществующего тендера"""
    fake_id = uuid.uuid4()
    response = client.get(f"/tenders/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tender not found"


def test_update_status_draft_to_active(client, test_tender, test_user_id):
    """Тест: обновление статуса DRAFT -> ACTIVE (валидный переход)"""
    response = client.patch(
        f"/tenders/{test_tender.id}/status",
        json={
            "status": "active",
            "reason": "Переход в активный",
            "changed_by": str(test_user_id)
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"


def test_update_status_active_to_won(client, test_tender, test_user_id):
    """Тест: обновление статуса ACTIVE -> WON (валидный переход)"""
    # сначала делаем тендер активным
    client.patch(
        f"/tenders/{test_tender.id}/status",
        json={
            "status": "active",
            "reason": "Переход в активный",
            "changed_by": str(test_user_id)
        }
    )

    # потом меняем на вон
    response = client.patch(
        f"/tenders/{test_tender.id}/status",
        json={
            "status": "won",
            "reason": "Победа в тендере",
            "changed_by": str(test_user_id)
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "won"


def test_update_status_invalid_transition(client, test_tender, test_user_id):
    """Тест: невалидный переход DRAFT -> WON (должен вернуть 400)"""
    # пытаемся изменить драфт -> вон (невалидно)
    response = client.patch(
        f"/tenders/{test_tender.id}/status",
        json={
            "status": "won",
            "reason": "Победа без активации",
            "changed_by": str(test_user_id)
        }
    )
    assert response.status_code == 400
    assert "Cannot change" in response.json()["detail"]


def test_get_history(client, test_tender, test_user_id):
    """Тест: получение истории изменений"""
    # меняем статус
    client.patch(
        f"/tenders/{test_tender.id}/status",
        json={
            "status": "active",
            "reason": "Переход в активный",
            "changed_by": str(test_user_id)
        }
    )

    # получаем историю
    response = client.get(f"/tenders/{test_tender.id}/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["old_status"] == "draft"
    assert data[0]["new_status"] == "active"
    assert data[0]["reason"] == "Переход в активный"


def test_get_history_tender_not_found(client):
    """Тест: история для несуществующего тендера"""
    fake_id = uuid.uuid4()
    response = client.get(f"/tenders/{fake_id}/history")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tender not found"


def test_update_status_tender_not_found(client, test_user_id):
    """Тест: обновление статуса несуществующего тендера"""
    fake_id = uuid.uuid4()
    response = client.patch(
        f"/tenders/{fake_id}/status",
        json={
            "status": "active",
            "reason": "Переход в активный",
            "changed_by": str(test_user_id)
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Tender not found"