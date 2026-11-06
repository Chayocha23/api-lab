
import pytest


@pytest.mark.parametrize(
    "stars, expected_status",
    [
        (0, 400),
        (1, 200),
        (5, 200),
        (6, 400),
    ],
)
def test_update_rating_boundary_values(
    api, auth, rating, stars, expected_status
):
    rating_id = rating["id"]
    original_stars = rating["stars"]

    path = f"/api/ratings/{rating_id}"

    # Update the rating with the boundary value.
    res = api.put(
        path,
        json={"stars": stars},
        headers=auth,
    )

    assert res.status_code == expected_status

    # Read the rating back to verify its stored value.
    read_res = api.get(path, headers=auth)
    assert read_res.status_code == 200

    if expected_status == 200:
        # Valid update: the new stars must be saved.
        assert read_res.json()["stars"] == stars
    else:
        # Invalid update: the original stars must remain.
        assert read_res.json()["stars"] == original_stars
