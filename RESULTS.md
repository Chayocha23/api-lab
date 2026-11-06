# API lab results

## Part 0

- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: The Happy Hawaii
- Step 0.16, blocks of "how many of the three tools are excluded":

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

## Part A

- Step A4, status codes when the other user reads, changes and deletes:

## Part B

1.
2.
3.
4.
5.
6.
7.
8.