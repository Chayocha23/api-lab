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

### Step A3 — Boundary Values for an Update

**Operation:** PUT /api/ratings/{id}

**Testing Technique:** Boundary Value Analysis (BVA)

The valid range of rating stars is 1 to 5. Four boundary values were selected to test values immediately outside and at the valid limits.

| Stars | Boundary Type | Expected Status | Expected Stored Value | Result |
|---|---|---|---|---|
| 0 | Below minimum | 400 | Original stars | PASSED |
| 1 | Minimum valid | 200 | 1 | PASSED |
| 5 | Maximum valid | 200 | 5 | PASSED |
| 6 | Above maximum | 400 | Original stars | PASSED |

**Command:** `pytest -v`

**Result:** 29 passed, 1 xfailed in 40.20s.

All four boundary-value tests passed. Valid updates
saved the new stars, while invalid updates preserved
the original rating.

### Step A4 — Who May Change a Rating

**Testing Objective:** Verify that another authenticated user cannot read, update, or delete a rating owned by a different user.

**Test Setup:**
- User A creates a rating with 3 stars.
- User B logs in using a separate account.
- User B attempts to read, update, and delete User A's rating.
- User A reads the rating afterward to verify that the original data remains unchanged.

| Operation | Expected Status | Actual Status | Result |
|---|---|---|---|
| GET (Read) | 400–499 | 404 | PASSED |
| PUT (Update) | 400–499 | 400 | PASSED |
| DELETE | 400–499 | 400 | PASSED |

**Command:** `pytest -v -s test_rating_owner.py`

**Result:** 3 passed in 9.52s.

**Conclusion:** All three authorization tests passed. Unauthorized access attempts were rejected, and the original rating remained unchanged.

## Part B — Reflection

### 1. API Testing vs Unit Testing

**Question:** Your tests talk to a real server over the internet. Name two kinds of failure that they can find and a unit test with stubs cannot. Then give one reason to write unit tests with stubs as well.

**Answer:**

API tests can find problems with the connection between the client and the real server. They can also find problems when the server does not save or update data correctly.

Unit tests with stubs are still useful because they are faster and help us find problems in specific parts of the code.

### 2. Why Each Test Creates a New User

**Question:** Why does every test create its own user with a new name, rather than use the public token? How will you apply the same idea to the shared shop or hotel in Project 2?

**Answer:**

Each test creates a new user to avoid using the same data as other tests. If we use a public token, other people might change the data and affect our test results.

For Project 2, I will create separate users and test data for each test so they do not affect each other.

### 3. Why We Use One Session

**Question:** Explain in your own words why the tests send every request through one session. If you did Step 0.12, describe what happened in your three runs.

**Answer:**

Using one session helps us reuse the same connection instead of starting a new connection for every request. It also keeps the session settings the same, which makes the tests easier to manage.

*Step 0.12 results: To be added if completed.*

### 4. Bug Found in Step 0.16

**Question:** Which block of the excluded tools revealed the defect in Step 0.16? Why is a 500 with an empty body worse for an app that calls the API than a 400 with a message? Why does the test stay in the suite as xfail instead of being deleted?

**Answer:**

Block B4 found the bug when all three tools were excluded.

The API returned 500 with an empty response instead of 400 with an error message. This is a problem because the app cannot tell the user what went wrong.

We keep the test as xfail because the bug is still there. If the bug gets fixed later, the test will help us notice the change.

### 5. Base Choice Coverage

**Question:** How many tests does base choice coverage need for the model in Step A1, and how many would all combinations coverage need? Show how you counted.

**Answer:**

There are four characteristics in Step A1:

- C1 has 3 blocks.
- C2 has 4 blocks.
- C3 has 2 blocks.
- C4 has 3 blocks.

For base choice coverage:

1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = **9 tests**

For all combinations coverage:

3 × 4 × 2 × 3 = **72 tests**

Base choice coverage needs fewer tests because we start with one normal case and change only one characteristic at a time.

### 6. Rating Ownership

**Question:** In Step A4, which status codes did you get when the other user read, changed and deleted the rating? Which codes would you expect? Is the difference a defect? Explain.

**Answer:**

These are the results from my tests:

| Action | Actual Status |
|---|---|
| Read rating | 404 |
| Update rating | 400 |
| Delete rating | 400 |

I expected 403 Forbidden because the other user should not have permission to access or change the rating.

I don't think this is necessarily a bug because the API still blocked all three actions, and the original rating was not changed. The exact expected status codes would depend on the API rules.

### 7. Made-Up Token

**Question:** Create madeup.txt with a made-up token of 16 characters and use it to read ratings. What comes back? Is this a defect, and what could a stranger do with it on a real system?

**Command:**

```bash
curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings
```

**Answer:**

I tested the API using a made-up token (`0000000000000000`). The server returned **200 OK** and showed a list of ratings instead of rejecting the token.

I think this is a security defect because the API allowed an invalid token to read data. On a real system, a stranger might be able to see information that they should not have access to.

I only used the token to read the ratings and did not create, update, or delete anything.

### 8. API Testing vs Web Page Testing

**Question:** Name one thing that an API test checks better than a test through the web pages, and one thing that only a test through the web pages can check.

**Answer:**

API tests are better for checking status codes and JSON responses directly.

Web page tests can check how the website looks and whether buttons and other parts of the page work correctly.