# Cumulative for Python Test

<details><summary>Learning Objectives</summary>

# Learning Objectives
After completing this module, associates should be able to:

- Explain why automated testing matters in software development
- Understand the differences between Python’s built-in `unittest` framework and the third-party `pytest` framework
- Write basic test cases using `unittest.TestCase`
- Write pytest-style test functions using simple `assert` statements
- Run test suites using the Python CLI and the pytest CLI
- Organize tests into files and folders that each framework can automatically discover
- Use fixtures in pytest and setup/teardown methods in unittest

</details>

<details><summary>Description</summary>

# What is Testing in Python?

Testing is the process of verifying that your code behaves the way you expect. It helps catch errors early, prevents regressions, and makes your code easier to maintain.

---

## 1. `unittest` (Built-in Testing Framework)

`unittest` is Python’s **standard library** testing framework modeled after Java’s JUnit.  
It uses:

- Classes (`unittest.TestCase`)
- Methods that begin with `test_`
- Assertions like `self.assertEqual`

unittest is included with Python — no installation required.

---

## 2. `pytest` (3rd-party but extremely popular)

`pytest` is a **lightweight, powerful testing framework** that focuses on:

- Simple tests using `assert`
- Automatic test discovery
- Detailed assertion introspection
- Rich plugins and fixtures

Many modern Python teams prefer pytest because tests are cleaner and easier to write.

</details>

<details><summary>Real World Application</summary>

# Real World Application for Testing

Testing is used in almost every part of software development:

### ✔️ Backend systems  
Ensure API routes, services, and business rules work correctly.

### ✔️ Data engineering  
Validate transformations, ETL logic, and ensure schemas are correct.

### ✔️ Machine learning workflows  
Verify feature extraction, metrics, models, and pipelines.

### ✔️ DevOps / CI-CD  
GitHub Actions, Jenkins, and Azure DevOps run tests automatically before deployment.

### ✔️ Enterprise applications  
Large companies rely on testing to prevent bugs and regressions across large teams.

Knowing both unittest and pytest prepares developers for real-world professional workflows.

</details>

<details><summary>Implementation</summary>

# Implementation

## Creating Tests With `unittest`

### 1. Create a test file  
`test_example.py`:

```python
import unittest
from my_app import add_numbers

class TestAddNumbers(unittest.TestCase):

    def test_add_two_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add_numbers(-1, 1), 0)

if __name__ == "__main__":
    unittest.main()
````

### 2. Running unittest tests

```bash
python -m unittest
```

or run a specific test file:

```bash
python -m unittest test_example.py
```

---

## Creating Tests With `pytest`

### 1. Install pytest

```bash
pip install pytest
```

### 2. Write a test file

`test_example.py`:

```python
from my_app import add_numbers

def test_add_two_numbers():
    assert add_numbers(2, 3) == 5

def test_add_negative():
    assert add_numbers(-1, 1) == 0
```

### 3. Run all tests

```bash
pytest
```

### 4. Verbose mode

```bash
pytest -v
```

---

## Comparing `unittest` and `pytest`

| Feature            | unittest                           | pytest                 |
| ------------------ | ---------------------------------- | ---------------------- |
| Included in Python | ✔️ Yes                             | ❌ No (pip install)     |
| Test style         | Class-based                        | Function-based         |
| Assertions         | Many methods (`assertEqual`, etc.) | Just `assert`          |
| Fixtures           | Setup/teardown methods             | Very powerful fixtures |
| Popularity         | Common in older codebases          | Most popular today     |

---

## Using Fixtures (pytest)

Fixtures allow reusable setup logic:

```python
import pytest

@pytest.fixture
def sample_numbers():
    return [1, 2, 3]

def test_length(sample_numbers):
    assert len(sample_numbers) == 3
```

---

## Setup/Teardown (unittest)

```python
import unittest

class TestStuff(unittest.TestCase):

    def setUp(self):
        self.data = [1, 2, 3]

    def tearDown(self):
        self.data = None

    def test_length(self):
        self.assertEqual(len(self.data), 3)
```

These patterns appear frequently in enterprise-level testing.

</details>

<details><summary>Summary</summary>

# Summary

* Python supports two major testing styles: the built-in `unittest` framework and the third-party `pytest` framework.
* `unittest` uses classes, setup methods, and many assertion helper methods.
* `pytest` uses simple functions, plain `assert`, and a powerful fixture system.
* Both frameworks support automatic test discovery based on naming conventions.
* Tests can be run through `python -m unittest` or `pytest`, depending on the framework used.
* Automated testing is essential for catching bugs, preventing regressions, and supporting CI/CD pipelines.

</details>

<details><summary>Practice Questions</summary>

[Practice Questions](./Quiz.gift)

</details>