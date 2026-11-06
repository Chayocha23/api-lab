# API Testing Lab

ITCS386 — Software Verification and Validation

This lab uses Python, pytest, and requests to test the QuickPizza API.

## 1. Requirements

- Python 3.10 or newer
- pytest
- requests
- pytest-html

Install the required packages:

```bash
pip install -r requirements.txt
```

## 2. Running the Tests

Run all tests:

```bash
pytest -v
```

Generate an HTML test report:

```bash
pytest -v --html=report.html --self-contained-html
```

The HTML report shows the test results and execution time.

## 3. Input Space Partitioning — Step A1

**Operation:** POST /api/ratings

The request uses `pizza_id` and `stars` in the JSON body and an authentication token in the header.

The following table shows the input domain model and the tests that cover each block.

| Characteristic | Block | Test Value | Test Name |
|---|---|---|---|
| C1: Value of stars | Below 1 | 0 | test_stars_out_of_range[0] |
| C1: Value of stars | 1 to 5 (base) | 3 | test_base_choice_is_saved |
| C1: Value of stars | Above 5 | 6 | test_stars_out_of_range[6] |
| C2: Type of stars | Whole number (base) | 3 | test_base_choice_is_saved |
| C2: Type of stars | Decimal | 3.5 | test_a2_base_choice_variations[decimal-3.5-True-True-valid] |
| C2: Type of stars | Text | "3" | test_a2_base_choice_variations |
| C2: Type of stars | Missing | No stars field | test_a2_base_choice_variations |
| C3: Pizza | Exists (base) | New pizza | test_base_choice_is_saved |
| C3: Pizza | Does not exist | 999999999 | test_a2_base_choice_variations |
| C4: Token | User's own (base) | Valid token | test_base_choice_is_saved |
| C4: Token | None | No header | test_a2_base_choice_variations |
| C4: Token | Wrong length | token short | test_a2_base_choice_variations |

**Base choice:** 3 stars as a whole number, an existing pizza, and a valid user token.

For base choice coverage, one characteristic is changed at a time while the others remain at their base values.

- Base choice coverage: 9 tests
- All combinations coverage: 72 tests

## 4. Boundary Value Testing — Step A3

**Operation:** PUT /api/ratings/{id}

The valid range is 1 to 5 stars.

The tests use four boundary values: 0, 1, 5, and 6.

Valid updates should save the new rating. Invalid updates should return an error and keep the original rating unchanged.

Test file: `test_update_rating.py`

## 5. Rating Ownership — Step A4

These tests check that another user cannot read, update, or delete a rating owned by someone else.

The owner should still be able to read the original rating after each unauthorized attempt.

Test file: `test_rating_owner.py`

## 6. Known Defect — Step 0.16

A request that excludes all three pizza tools returns HTTP 500 with an empty response body instead of HTTP 400 with an error message.

The test is marked with `pytest.mark.xfail(strict=True)` because this is a known defect.

More details are recorded in `RESULTS.md`.

## 7. Test Results

- `RESULTS.md` contains the test results, defect report, and reflection answers.
- `report.html` contains the full pytest execution report.
