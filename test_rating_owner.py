
# Step A4: Who May Change a Rating


# Another user must not read the owner's rating.
def test_other_user_cannot_read_rating(
    api, auth, other_auth, rating
):
    path = f"/api/ratings/{rating['id']}"

    res = api.get(path, headers=other_auth)

    print(f"\nREAD status: {res.status_code}")
    assert 400 <= res.status_code <= 499

    # The owner can still read the original rating.
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating


# Another user must not update the owner's rating.
def test_other_user_cannot_update_rating(
    api, auth, other_auth, rating
):
    path = f"/api/ratings/{rating['id']}"

    res = api.put(
        path,
        json={"stars": 5},
        headers=other_auth,
    )

    print(f"\nUPDATE status: {res.status_code}")
    assert 400 <= res.status_code <= 499

    # The original rating must remain unchanged.
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating


# Another user must not delete the owner's rating.
def test_other_user_cannot_delete_rating(
    api, auth, other_auth, rating
):
    path = f"/api/ratings/{rating['id']}"

    res = api.delete(path, headers=other_auth)

    print(f"\nDELETE status: {res.status_code}")
    assert 400 <= res.status_code <= 499

    # The owner must still have the rating.
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating
