# API lab results

## Part 0

- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: The Happy Hawaii

### Step 0.16 — Bug Hunt Checkpoint

#### Input Space Partitioning

**Characteristic:** Number of excluded tools (out of three available tools).

| Block | Number of excluded tools | Test coverage |
|---|---|---|
| B1 | 0 | Covered by [] |
| B2 | 1 | Covered by ["Knife"] and ["Scissors"] |
| B3 | 2 | Covered by ["Knife", "Scissors"] |
| B4 | 3 | Covered by ["Knife", "Pizza cutter", "Scissors"]; defect found (XFAIL) |

All four input blocks have been tested. Block B4 revealed a defect when all three tools were excluded.

**Step 0.16.5 — Expected Failure**

The failing test was separated from the parametrized tests and marked with `pytest.mark.xfail(strict=True)` to document the known defect.

**Test result:** 16 passed, 1 xfailed in 20.10s.

The expected failure remains in the test suite so the defect can be detected when the application behavior changes.

## Defect report

- **Title:** HTTP 500 Internal Server Error when all pizza tools are excluded.
- **Request:** POST /api/pizza with JSON body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}` and a valid Authorization token.
- **Expected result:** HTTP 400 Bad Request with a JSON error message explaining that no pizza can satisfy the request.
- **Actual result:** HTTP 500 Internal Server Error with an empty response body (Content-Length: 0). The behavior was reproduced using pytest and curl.
- **Severity:** Medium — The API fails to handle an invalid request gracefully and returns an unexpected server error instead of a meaningful client error.

## Part A — Input Space Partitioning for Ratings

### Step A1: Input Domain Model

**Operation:** POST /api/ratings

The request contains `pizza_id` and `stars` in the JSON body and an authentication token in the header.

| Characteristic | Blocks | Values in the tests |
|---|---|---|
| C1 Value of stars | Below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of stars | Whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3 Pizza | Exists (base), does not exist | A new pizza, 999999999 |
| C4 Token | The user's own (base), none, wrong length | From auth, no header, token short |

**Base choice:** 3 stars as a whole number, an existing pizza, and the logged-in user's token.

The model divides the input domain into blocks. Base choice coverage tests the base combination first, then changes one characteristic at a time while keeping the others at their base values.

### Step A1 — Test Execution Result

**Command:** `pytest -v`

**Result:** 19 passed, 1 xfailed in 25.38s.

- Base choice (3 stars, valid pizza, valid token): PASSED
- Stars below minimum (0): PASSED
- Stars above maximum (6): PASSED

All three Step A1 test cases passed. The previously identified defect from Step 0.16 remains marked as an expected failure (XFAIL).

### Step A2 — Base Choice Coverage

**Operation:** POST /api/ratings

Six additional test cases were designed using Base Choice Coverage. Each test changes one characteristic from the base choice while keeping the other characteristics at their base values.

| Test Case | Characteristic | Test Value | Expected Status | Result |
|---|---|---|---|---|
| Decimal stars | C2 | 3.5 | 400 | PASSED |
| Text stars | C2 | "3" | 400 | PASSED |
| Missing stars | C2 | No stars field | 400 | PASSED |
| Invalid pizza | C3 | 999999999 | 400 | PASSED |
| No token | C4 | No Authorization header | 401 | PASSED |
| Short token | C4 | token short | 401 | PASSED |

**Command:** `pytest -v`

**Result:** 25 passed, 1 xfailed in 28.93s.

All six Step A2 test cases passed. The previously identified defect from Step 0.16 remains marked as an expected failure (XFAIL).

## Part B

1.
2.
3.
4.
5.
6.
7.
8.