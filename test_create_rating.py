
import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


@pytest.mark.parametrize(
    "case,stars,include_stars,valid_pizza,token_type",
    [
        ("decimal", 3.5, True, True, "valid"),
        ("text", "3", True, True, "valid"),
        ("missing", None, False, True, "valid"),
        ("invalid_pizza", 3, True, False, "valid"),
        ("no_token", 3, True, True, "none"),
        ("short_token", 3, True, True, "short"),
    ],
)
def test_a2_base_choice_variations(
    api, auth, pizza_id,
    case, stars, include_stars, valid_pizza, token_type
):
    body = {
        "pizza_id": pizza_id if valid_pizza else 999999999
    }

    if include_stars:
        body["stars"] = stars

    headers = {
        "valid": auth,
        "none": {},
        "short": {"Authorization": "token short"},
    }[token_type]

    res = api.post("/api/ratings", json=body, headers=headers)

    
    expected_status = {
        "decimal": 400,
        "text": 400,
        "missing": 400,
        "invalid_pizza": 400,
        "no_token": 401,
        "short_token": 401,
    }

    assert res.status_code == expected_status[case]


    expected_errors = {
        "missing": STARS_ERROR,
        "invalid_pizza": "pizza ID 999999999 not found",
        "no_token": "authentication failed",
        "short_token": "authentication failed",
    }

    if case in expected_errors:
        assert res.json() == {"error": expected_errors[case]}
    else:
        assert "error" in res.json()


