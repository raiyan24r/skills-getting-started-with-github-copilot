from src.app import activities


def test_get_activities_returns_seeded_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload) == 9
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_success_adds_participant(client):
    email = "newstudent@mergington.edu"

    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    existing_email = activities["Chess Club"]["participants"][0]

    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": existing_email}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_success_removes_participant(client):
    email = activities["Programming Class"]["participants"][0]

    response = client.delete(
        "/activities/Programming%20Class/participants", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Programming Class"
    }
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_enrolled_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants", params={"email": "absent@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
