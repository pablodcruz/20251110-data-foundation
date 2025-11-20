# Cumulative for the module

<details><summary>Learning Objectives</summary>

# Learning Objectives
After completing this module, associates should be able to:

- Explain why automated testing is critical in data and AI projects
- Describe the roles of Python’s built-in `unittest` framework and the third-party `pytest` framework
- Write basic unit tests for metrics, preprocessing functions, and ETL steps
- Use `unittest.TestCase` and assertion methods to structure tests
- Use pytest features such as simple `assert` statements, fixtures, and parametrized tests
- Organize tests into a `tests/` folder so they can be discovered and run from the command line
- Run test suites with `python -m unittest` and with `pytest`

</details>

<details><summary>Description</summary>

# What is Testing in Python?

Testing is the practice of writing **code that checks other code**.

In data and AI work, it is easy for bugs to hide inside:

- metric calculations  
- feature engineering steps  
- data cleaning and ETL pipelines  
- model input/output shapes  

Small mistakes can silently produce wrong numbers, train bad models, or corrupt datasets.

Python provides two main ways to write automated tests:

1. **`unittest`** – the **built-in** testing framework  
   - Class-based (`unittest.TestCase`)  
   - Uses assertion methods like `assertEqual`, `assertAlmostEqual`, `assertRaises`  
   - Common in older codebases and still widely used in enterprise environments  

2. **`pytest`** – a very popular **third-party** framework  
   - Function-based tests using plain `assert`  
   - Powerful fixtures and parametrization for data-heavy testing  
   - Often preferred for modern data and ML projects because the tests are shorter and easier to read  

In this module, you will see both, with a focus on examples that feel natural for analytics, ETL, and machine learning workflows.

</details>

<details><summary>Real World Application</summary>

# Real World Application for Testing

In real AI and data engineering projects, automated tests are used to:

- **Validate metrics and loss functions**  
  Make sure accuracy, precision/recall, or custom scores are computed correctly.

- **Protect data cleaning and feature engineering**  
  Ensure steps like imputing missing values, scaling features, and encoding categories behave as expected and do not change the original data accidentally.

- **Test ETL pipelines**  
  Verify that “bronze → silver → gold” transformations create the right columns, types, and row counts.

- **Check model interfaces**  
  Confirm that prediction functions accept the expected shapes and return outputs of the right size and type.

- **Support CI/CD**  
  In many teams, every pull request triggers a test run in GitHub Actions, Jenkins, or Azure DevOps. A failing test can block a broken model or pipeline from going to production.

Good tests give data teams confidence to refactor code, upgrade libraries, and experiment without constantly worrying about breaking something subtle.

</details>

<details><summary>Implementation</summary>

# Implementation

## Installing pytest

If `pytest` is not already available in your environment, install it with:

```bash
pip install pytest
```

`unittest` is part of the Python standard library, so it does not need to be installed.

---

## 1. Testing a Simple Metric Function with `unittest`

Imagine a small utility in `metrics.py` that computes accuracy:

```python
# metrics.py
def accuracy(predictions, labels):
    if len(predictions) != len(labels):
        raise ValueError("predictions and labels must have same length")

    correct = sum(p == y for p, y in zip(predictions, labels))
    return correct / len(labels)
```

A `unittest`-style test file:

```python
# test_metrics_unittest.py
import unittest
from metrics import accuracy

class TestAccuracy(unittest.TestCase):

    def test_perfect_accuracy(self):
        preds = [1, 0, 1]
        labels = [1, 0, 1]
        self.assertEqual(accuracy(preds, labels), 1.0)

    def test_partial_accuracy(self):
        preds = [1, 1, 0, 0]
        labels = [1, 0, 0, 0]
        self.assertAlmostEqual(accuracy(preds, labels), 0.75)

    def test_mismatched_lengths_raises(self):
        preds = [1, 0]
        labels = [1]
        with self.assertRaises(ValueError):
            accuracy(preds, labels)

if __name__ == "__main__":
    unittest.main()
```

Run all unittest tests:

```bash
python -m unittest
```

---

## 2. Testing the Same Logic with `pytest`

The same tests written in pytest style:

```python
# test_metrics_pytest.py
from metrics import accuracy
import pytest

def test_perfect_accuracy():
    assert accuracy([1, 0, 1], [1, 0, 1]) == 1.0

def test_partial_accuracy():
    assert accuracy([1, 1, 0, 0], [1, 0, 0, 0]) == 0.75

def test_mismatched_lengths_raises():
    with pytest.raises(ValueError):
        accuracy([1, 0], [1])
```

Run all pytest tests:

```bash
pytest
```

---

## 3. Using pytest Fixtures for Data / AI Workflows

Fixtures are great for creating **reusable data objects** like NumPy arrays or pandas DataFrames.

Example: testing a data cleaning function in `cleaning.py`:

```python
# cleaning.py
import pandas as pd

def drop_missing_target(df, target_col):
    """Return a new DataFrame with rows removed where target_col is null."""
    return df.dropna(subset=[target_col])
```

pytest tests with a fixture:

```python
# test_cleaning.py
import pytest
import pandas as pd
from cleaning import drop_missing_target

@pytest.fixture
def raw_df():
    return pd.DataFrame(
        {
            "feature": [1.0, 2.0, None, 4.0],
            "target":  [0,   1,   None, 0],
        }
    )

def test_drop_missing_target_removes_null_rows(raw_df):
    cleaned = drop_missing_target(raw_df, "target")
    assert cleaned["target"].isna().sum() == 0
    assert len(cleaned) == 3  # one row with null target removed

def test_drop_missing_target_does_not_modify_original(raw_df):
    before = raw_df.copy()
    drop_missing_target(raw_df, "target")
    # Original should stay unchanged
    assert raw_df.equals(before)
```

---

## 4. Parametrized Tests for Edge Cases

Data and AI code often needs to handle many edge cases (empty arrays, all zeros, class imbalance, etc.).
`@pytest.mark.parametrize` lets you test multiple scenarios in one function.

Example: scaling a NumPy array in `preprocessing.py`:

```python
# preprocessing.py
import numpy as np

def normalize_vector(x):
    x = np.asarray(x, dtype=float)
    norm = np.linalg.norm(x)
    if norm == 0:
        return x
    return x / norm
```

Parametrized pytest tests:

```python
# test_preprocessing.py
import numpy as np
import pytest
from preprocessing import normalize_vector

@pytest.mark.parametrize(
    "vector, expected_norm",
    [
        ([1, 0, 0], 1.0),
        ([3, 4], 1.0),
        ([0, 0, 0], 0.0),
    ],
)
def test_normalize_vector_norm_is_expected(vector, expected_norm):
    result = normalize_vector(vector)
    norm = np.linalg.norm(result)
    assert norm == pytest.approx(expected_norm, rel=1e-6)
```

---

## 5. Testing Simple ETL Steps

Example: verify that a “bronze → silver” transformation adds required columns.

```python
# transform.py
import pandas as pd

def add_total_column(df):
    """Assumes df has 'price' and 'quantity' columns."""
    df = df.copy()
    df["total"] = df["price"] * df["quantity"]
    return df
```

pytest test:

```python
# test_transform.py
import pandas as pd
from transform import add_total_column

def test_add_total_column_computes_correct_values():
    df = pd.DataFrame(
        {
            "price": [10.0, 5.0],
            "quantity": [2, 3],
        }
    )

    result = add_total_column(df)

    assert "total" in result.columns
    assert list(result["total"]) == [20.0, 15.0]
```

---

## 6. Organizing Tests in a Data / AI Project

A common layout:

```python
project/
    my_app/
        __init__.py
        metrics.py
        cleaning.py
        preprocessing.py
        transform.py
    tests/
        __init__.py # Optional: needed for unittest discovery in some cases
        test_metrics_pytest.py
        test_cleaning.py
        test_preprocessing.py
        test_transform.py
```

From the **project root**, you can then run:

```bash
pytest
```

or, if using unittest-style tests:

```bash
python -m unittest
```

This structure scales nicely as models, pipelines, and utilities grow.

## 7. Test Structure: Arrange → Act → Assert

The Arrange-Act-Assert pattern is widely used. Using AAA keeps tests readable and structured:

* **Arrange** — set up inputs
* **Act** — call the function being tested
* **Assert** — verify the output

### 🐍 AAA in pytest (example)

```python
def test_normalize_vector():
    # Arrange
    vector = [3, 4]

    # Act
    result = normalize_vector(vector)

    # Assert
    assert pytest.approx(np.linalg.norm(result)) == 1.0
```

</details>

<details><summary>Summary</summary>

# Summary

* Automated tests are critical in data and AI projects to protect metrics, preprocessing, ETL steps, and model interfaces from subtle bugs.
* Python provides two major testing frameworks:

  * **`unittest`** – built in, class-based, uses assertion methods.
  * **`pytest`** – external, function-based, uses simple `assert`, fixtures, and parametrization.
* `unittest` tests often live in classes that inherit from `unittest.TestCase`, with methods beginning with `test_`.
* pytest tests are plain functions; fixtures and `@pytest.mark.parametrize` make it easy to test many data scenarios.
* Both frameworks can be run from the command line and integrated into CI/CD pipelines.
* A clear `tests/` folder structure keeps growing data/ML projects maintainable and testable.

</details>

<details><summary>Practice Questions</summary>

[Practice Questions](./Quiz.gift)

</details>