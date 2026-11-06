
import uuid


def new_user():
    return {
        "username": "lab-" + uuid.uuid4().hex[:12],
        "password": "Pizza-2026"
    }


# A duplicate username is refused with status 400.
def test_duplicate_username_is_refused(api):
    user = new_user()

    res = api.post("/api/users", json=user)
    assert res.status_code == 201

    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}


# Logging in with a wrong password is refused with status 401.
def test_wrong_password_is_refused(api):
    user = new_user()

    res = api.post("/api/users", json=user)
    assert res.status_code == 201

    wrong_user = {
        "username": user["username"],
        "password": "WrongPassword"
    }

    res = api.post("/api/users/token/login", json=wrong_user)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# An empty username is refused with status 400.
def test_empty_username_is_refused(api):
    user = new_user()
    user["username"] = ""

    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
