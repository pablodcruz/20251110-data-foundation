# Week 2 — Python Advanced

## Learning Outcomes

By the end of this week you will be able to:

* Organize code into reusable **modules** and packages.
* Handle **exceptions** gracefully using `try/except/finally`.
* Read, write, and manage files in multiple formats.
* Use **logging** and **pylint** for professional-grade code quality.
* Install and manage dependencies with **pip**.
* Employ advanced built-ins such as **collections.Counter**, **namedtuple**, and **OrderedDict**.
* Write and run **unit tests** using `unittest` or `pytest`.
* Perform data analysis and visualization with **NumPy**, **pandas**, and **matplotlib**.

---

## 🧱 Modules and Standard Library Essentials

### Python Modules & Imports

A **module** is any `.py` file that defines reusable code.
A **package** is a folder containing an `__init__.py` file, allowing it to be imported as a module.

```python
# utils.py
def greet(name):
    return f"Hello, {name}"

# main.py
import utils
print(utils.greet("Pablo"))

# This will only run if you execute: python math_utils.py
if __name__ == "__main__":
    print("Running tests...")
    print(add(2, 3))
    print(subtract(10, 5))
```

* `import` loads the module once per interpreter session.
* `from module import func` imports specific members.
* Use `if __name__ == "__main__":` to make files both runnable and importable.
* Prefer **absolute imports** for clarity: `from myproject.utils import greet`.

---

## 🔢 **Math Module (Built-in Mathematical Functions)**

### Definition

The **`math`** module provides access to common mathematical operations and constants that go beyond basic `+`, `-`, `*`, `/`.
It interfaces with the C standard library, making these functions both **fast** and **precise**.

### Use Cases

* Perform scientific or statistical computations accurately.
* Avoid reinventing formulas (square roots, logs, trigonometry, rounding).
* Common in analytics, finance, geometry, and machine-learning preprocessing.

### Common Constants

| Constant   | Meaning        |
| ---------- | -------------- |
| `math.pi`  | 3.14159…       |
| `math.e`   | Euler’s number |
| `math.inf` | Infinity       |
| `math.nan` | Not-a-Number   |

### Common Functions

| Category           | Example                              | Description             |
| ------------------ | ------------------------------------ | ----------------------- |
| **Rounding**       | `math.ceil(3.2)` → `4`               | Round up                |
|                    | `math.floor(3.7)` → `3`              | Round down              |
| **Powers & Roots** | `16 ** 0.5` → `4.0`                  | Square root (preferred) |
|                    | `math.pow(2, 3)` → `8.0`             | Always returns float    |
| **Trigonometry**   | `math.sin(math.radians(30))` → `0.5` | Works with radians      |
| **Logarithms**     | `math.log(100, 10)` → `2.0`          | Log base 10             |
|                    | `math.log2(8)` → `3.0`               | Log base 2              |

### Example Program

```python
import math

radius = 5
area = math.pi * math.pow(radius, 2)
circumference = 2 * math.pi * radius
print(f"Area={area:.2f}, Circumference={circumference:.2f}")
```

---

## 🧾 **Logging Module**

### Definition

`logging` is a flexible framework for tracking events and messages while a program runs.
Unlike `print()`, logs can be filtered by severity, timestamped, and saved to files.

### Use Cases

* Trace errors in production without exposing output to the console.
* Maintain historical audit trails.
* Monitor ETL or API pipelines.

### Configuration Example

```python
import logging

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(fmt)

fh = logging.FileHandler("debug.log")
fh.setLevel(logging.INFO)
fh.setFormatter(fmt)

logger.handlers.clear()
logger.addHandler(ch)
logger.addHandler(fh)

logger.info("Program started")
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Division by zero occurred!")
```

### Logging Levels

| Level    | Purpose                                             |
| -------- | --------------------------------------------------- |
| DEBUG    | Detailed developer messages                         |
| INFO     | Normal operation updates                            |
| WARNING  | Something unexpected happened but program continues |
| ERROR    | Serious issue but not fatal                         |
| CRITICAL | Program cannot continue                             |

---

# 🧩 **JSON Module**

### Definition

The **`json`** module encodes (serializes) and decodes (deserializes) data between Python objects and JSON format.

### Use Cases

* JSON is the standard for APIs and web services.
* Portable between Python, JavaScript, Java, etc.
* Great for lightweight storage and ETL workflows.

### Example

```python
import json

# Python dict → JSON string
data = {"name": "Ada", "active": True, "city": "Santo Domingo"}
json_str = json.dumps(data, indent=2, ensure_ascii=False)
print(json_str)

# Write JSON to file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Read JSON from file
with open("data.json", encoding="utf-8") as f:
    result = json.load(f)
print(result["name"])
```

### Common Parameters

* `indent`: pretty-printing
* `sort_keys`: alphabetically sort keys
* `ensure_ascii`: control encoding of Unicode characters

### Gotchas

* JSON supports only basic types: dict, list, str, int, float, bool, None.
* Custom classes must be converted manually using `__dict__` or a custom encoder.
---

## 🔍 **Regex (Regular Expressions)**

### Definition

Regular expressions allow **pattern matching** and **text extraction**.
Python’s `re` module provides the tools to match complex string patterns.

### Use Cases

* Validate input formats (emails, phone numbers, IDs).
* Extract structured data from messy text.
* Replace or split text efficiently.

### Common Functions

| Function       | Purpose                          |
| -------------- | -------------------------------- |
| `re.match()`   | Match pattern at start of string |
| `re.search()`  | Find first occurrence            |
| `re.findall()` | Find all matches as list         |
| `re.sub()`     | Replace text                     |

### Common Patterns

| Pattern | Meaning                                                              |
| ------- | -------------------------------------------------------------------- |
| `\d`    | Digit                                                                |
| `\w`    | Word character                                                       |
| `\s`    | Whitespace                                                           |
| `.`     | Any character *(except newline; use `re.DOTALL` to include newline)* |
| `+`     | One or more                                                          |
| `*`     | Zero or more                                                         |
| `?`     | Optional                                                             |
| `^`     | Start of string                                                      |
| `$`     | End of string                                                        |

### Example: Email Extraction

```python
import re
text = "Emails: ada@lab.com, alan@lab.com"
pattern = r"[\w\.-]+@[\w\.-]+"
result = re.findall(pattern, text)
print(result)
```

### Example: Validation

```python
pattern = r"^[A-Za-z0-9_-]{3,16}$"
username = "user_01"
if re.match(pattern, username):
    print("Valid username!")
```

---

# 📦 **pip and pylint**

### pip (Package Installer for Python)

**Definition:** Tool for installing and managing Python packages.

#### Use Cases

* Install reusable libraries.
* Manage project dependencies via `requirements.txt`.

```bash
pip install requests
pip install pandas==2.2.0
pip uninstall requests
pip list
pip freeze > requirements.txt
pip install -r requirements.txt
python -m pip install --upgrade pip
```

### pylint (Code Linter)

**Definition:** Static analysis tool that enforces style and detects errors.

#### Use Cases
* Helps maintain readable, consistent code.
* Detects syntax mistakes, unused variables, or bad naming.

```bash
pylint my_script.py
```

Output Example:

```
my_script.py:1:0: C0114: Missing module docstring
my_script.py:3:4: C0103: Variable name "x" doesn't conform to snake_case
```

#### Fixing Issues

Follow PEP 8 conventions:

* Functions and variables → `snake_case`
* Classes → `PascalCase`
* Use docstrings `"""Explain what this does"""`
---

## ⚙️ Advanced Collections

# 🧮 **collections.Counter**

### Definition

`Counter` is a subclass of `dict` that counts occurrences of hashable items.

### Use Cases

* Simplifies frequency counting (e.g., word counts, votes, etc.)
* Provides convenient arithmetic on counts.

### Example

```python
from collections import Counter
words = ["data", "python", "data", "etl"]
c = Counter(words)
print(c)              # Counter({'data': 2, 'python': 1, 'etl': 1})
print(c.most_common(1))  # [('data', 2)]
```

### Useful Methods

| Method           | Description                          |
| ---------------- | ------------------------------------ |
| `elements()`     | Iterator over elements               |
| `most_common(n)` | Top `n` frequent elements            |
| `subtract()`     | Subtract counts from another counter |

### Example — Word Frequency

```python
sentence = "data is life and data drives insight"
counts = Counter(sentence.split())
for word, count in counts.items():
    print(word, count)
```

---

# 🧱 **namedtuple**

### Definition

A **`namedtuple`** is an immutable, lightweight object for grouping data with named fields.

### Use Cases

* Provides attribute access (`p.x` instead of `p[0]`).
* Uses less memory than a class.
* Perfect for read-only data records.

### Example

```python
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(p.x + p.y)
```

### Comparison to Class

```python
class PointClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

`namedtuple` automatically adds `__init__`, `__repr__`, and `__eq__` — no boilerplate.
#### Unpacking

```python
x, y = p
print(x, y)
```

---

## 🧭 **OrderedDict**

### Definition

A **dictionary subclass** that remembers the **insertion order** of keys.
(From Python 3.7+, all dicts maintain order, but OrderedDict still provides explicit methods.)

### Use Cases

* Useful for ordered serialization, deterministic output, and LRU (Least Recently Used) cache-like behavior.

### Example

```python
from collections import OrderedDict
menu = OrderedDict()
menu['coffee'] = 2.5
menu['tea'] = 2.0
menu['sandwich'] = 5.0

for item, price in menu.items():
    print(item, price)
```

### Reordering

```python
menu.move_to_end('coffee')  # send to end
print(menu)
```

---

## 🧾 Exceptions and File Handling

### 🧠 Core ideas

* **Exceptions are classes**. They signal errors and unwind the call stack until handled.
* **Hierarchy:** `BaseException` > `Exception` > specific errors (e.g., `ValueError`, `TypeError`).

---

### 🔧 Handling errors

```python
try:
    x = int(user_input)
except ValueError as e:            # handle specific error
    print("Not a number:", e)
else:                              # runs only if no exception
    print("Converted:", x)
finally:                           # always runs
    print("Done")
```

* **Multiple exceptions:**

```python
try:
    risky()
except (ValueError, TypeError) as e:
    ...
```

* **Re-raise or chain:**

```python
try:
    risky()
except KeyError as e:
    raise ValueError("Bad config") from e  # keeps original cause
```

---

### 🚨 Raising your own

```python
def percent(p):
    if not (0 <= p <= 100):
        raise ValueError("p must be 0..100")
    return p / 100
```

---

### 🧩 Custom exception types

```python
class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass
```

---

### 📚 Common exceptions (know these)

| Exception           | Typical cause                       |
| ------------------- | ----------------------------------- |
| `ValueError`        | Bad value (right type, wrong value) |
| `TypeError`         | Wrong type / wrong arg count        |
| `KeyError`          | Missing dict key                    |
| `IndexError`        | List/tuple index out of range       |
| `AttributeError`    | Missing attribute on object         |
| `ZeroDivisionError` | Division by zero                    |
| `FileNotFoundError` | Missing file                        |
| `IOError`/`OSError` | I/O, filesystem errors              |
| `TimeoutError`      | Operation timed out                 |
| `AssertionError`    | Failed `assert`                     |

---

### ✅ Best practices

* Catch **specific** exceptions; keep handlers **small**.
* Only handle what you can **recover** from; let the rest bubble up.
* Use **`finally`/context managers** for cleanup.
* Prefer **logging** over `print` for errors.
* Provide **clear messages** when raising exceptions.


### Exception Handling

```python
try:
    value = int(input("Enter a number: "))
    print(10 / value)
except ValueError:
    print("That was not a valid integer!")
except ZeroDivisionError:
    print("Cannot divide by zero.")
finally:
    print("End of computation.")
```

* `try`: code that might fail
* `except`: catch and handle specific errors
* `finally`: always runs (cleanup, closing files, etc.)
* Use `raise` to propagate or define custom errors.

### File I/O Basics

```python
# Writing
with open("output.txt", "w") as f:
    f.write("Hello Data Foundations!\n")

# Reading
with open("output.txt") as f:
    print(f.read())
```

* Always use `with open()` — it automatically closes files.
* Modes: `'r'` = read, `'w'` = write (overwrite), `'a'` = append, `'rb'` = binary.

---

## 🧪 Unit Testing Overview

### unittest Example

```python
import unittest
from math import sqrt

class TestMath(unittest.TestCase):
    def test_square_root(self):
        self.assertEqual(sqrt(16), 4)

    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            10 / 0

if __name__ == "__main__":
    unittest.main()
```

### pytest Example

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
```

Run tests:

```bash
pytest -v
```

| Feature    | unittest         | pytest         |
| ---------- | ---------------- | -------------- |
| Setup      | Class-based      | Function-based |
| Assertions | `self.assert*()` | plain `assert` |
| Simplicity | Verbose          | Concise        |

---

## 📊 **Data Visualization and Analysis Overview (NumPy, pandas, matplotlib)**

### Definition

Data analysis and visualization are the backbone of **data engineering** and **data science** workflows.
Python’s **NumPy**, **pandas**, and **matplotlib** together form the foundation of most analytical systems — from data pipelines to machine learning models.

### Purpose

* Perform **numeric computation**, **array transformations**, and **data aggregation** efficiently.
* Clean, transform, and explore data in **tabular form**.
* Create meaningful **visualizations** to interpret trends, distributions, and relationships.
* Bridge ETL → analytics → visualization, forming the foundation for later GenAI or dashboard integration.

---


## 🧮 **NumPy (Numerical Python)**

### Definition

**NumPy** provides a fast and memory-efficient way to handle large arrays and perform vectorized mathematical operations.
It’s the foundation for nearly every data and AI framework (pandas, TensorFlow, PyTorch, scikit-learn).

### Key Features

* **ndarray**: the core multidimensional array type.
* **Vectorized operations**: perform math on entire arrays without loops.
* **Broadcasting**: automatic alignment of shapes for arithmetic.
* **Statistical methods**: mean, std, sum, median, var.
* **Integration with C/C++ and Fortran** for speed.

### Example 1 — Basic Operations

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])
print("Mean:", arr.mean())
print("Standard deviation:", arr.std())
print("Sum:", arr.sum())

# Vectorized operation
print("Scaled:", arr * 2)
```

### Example 2 — 2D Arrays and Slicing

```python
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[0, 1])  # 2
print(matrix[:, 1])  # column 2
```

### Example 3 — Random Numbers and Broadcasting

```python
randoms = np.random.randn(5, 3)
print(randoms)
print(randoms * np.array([1, 2, 3]))  # broadcasting
```

### Common Use Cases

* Large-scale numeric computation (e.g., matrix multiplication)
* Statistical summaries for ETL validation
* Basis for ML preprocessing

---

## 🧾 **pandas (Data Manipulation and Cleaning)**

### Definition

**pandas** is a high-level library for **data manipulation and analysis** built on NumPy. It introduces two core structures:

* `Series` — a 1D labeled array.
* `DataFrame` — a 2D labeled data table.

### Purpose

* Handle **structured/tabular data** (like Excel sheets or SQL tables).
* Clean, filter, and transform datasets.
* Merge/join multiple data sources.
* Export and import data (CSV, JSON, SQL, Excel, Parquet).

### Example 1 — Creating DataFrames

```python
import pandas as pd

data = {
    "name": ["Ada", "Alan", "Grace"],
    "score": [95, 88, 92],
    "active": [True, False, True]
}
df = pd.DataFrame(data)
print(df)
```

### Example 2 — Reading and Cleaning Data

```python
df = pd.read_csv('data.csv')
print(df.head())  # first 5 rows

# Clean column names and missing data
df.columns = [c.strip().lower() for c in df.columns]
df = df.dropna(subset=['score'])
```

### Example 3 — Filtering and Aggregation

```python
active_df = df[df['active']]
print(active_df[['name', 'score']])

print(df['score'].mean())  # Average
print(df.groupby('active')['score'].mean())
```

### Example 4 — Exporting Data

```python
df.to_json('output.json', orient='records', indent=2)
```

### Common Operations Cheat Sheet

| Task              | Code                            |
| ----------------- | ------------------------------- |
| Select column     | `df['col']`                     |
| Filter rows       | `df[df['col'] > 10]`            |
| Sort values       | `df.sort_values('col')`         |
| Group & aggregate | `df.groupby('key').mean()`      |
| Add new column    | `df['new'] = df['a'] + df['b']` |
| Drop column       | `df.drop('col', axis=1)`        |

---

## 📈 **matplotlib (Data Visualization)**

### Definition

**matplotlib** is the primary plotting library for Python. It produces static, animated, and interactive visualizations in notebooks and apps.

### Purpose

* Visualize trends, comparisons, and distributions.
* Create professional-quality charts for reports or dashboards.
* Support exploratory data analysis during ETL validation.

### Example 1 — Line Plot

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.figure(figsize=(6,4))
plt.plot(x, y, marker='o', color='blue', linestyle='--')
plt.title('Simple Line Plot')
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.grid(True)
plt.show()
```

### Example 2 — Bar and Histogram

```python
categories = ['A', 'B', 'C']
values = [10, 30, 20]
plt.bar(categories, values, color=['skyblue', 'salmon', 'limegreen'])
plt.title('Category Distribution')
plt.show()

# Histogram
import numpy as np
samples = np.random.randn(1000)
plt.hist(samples, bins=30, color='purple', alpha=0.7)
plt.title('Normal Distribution')
plt.show()
```

### Example 3 — pandas Integration

```python
import pandas as pd

sales = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr'],
    'revenue': [200, 220, 250, 300]
})

sales.plot(kind='bar', x='month', y='revenue', legend=False, color='orange', title='Monthly Revenue')
plt.ylabel('USD (thousands)')
plt.show()
```

### Example 4 — Subplots and Advanced Visualization

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(x, y, 'r--', label='Growth')
axes[0].legend()

axes[1].bar(categories, values, color='cyan')
axes[1].set_title('Bar Chart Example')
plt.tight_layout()
plt.show()
```

---

## 🧠 **Putting It Together: Data Workflow Example**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Generate synthetic data
np.random.seed(42)
data = {
    'day': np.arange(1, 8),
    'sales': np.random.randint(80, 150, size=7),
    'temperature': np.random.randint(60, 90, size=7)
}
df = pd.DataFrame(data)

# 2. Basic analytics
print(df.describe())

# 3. Correlation
print(df.corr())

# 4. Visualization
plt.scatter(df['temperature'], df['sales'], color='tomato')
plt.title('Sales vs Temperature')
plt.xlabel('Temperature (°F)')
plt.ylabel('Sales')
plt.show()
```

---

### Discussion Points

* How can we use visualization to identify patterns or anomalies in ETL output?
* Why is NumPy preferred for numeric performance?
* What operations in pandas map to SQL concepts like SELECT, WHERE, and GROUP BY?

### Summary

| Library        | Core Role           | Typical Tasks                                  |
| -------------- | ------------------- | ---------------------------------------------- |
| **NumPy**      | Numerical computing | Vectorized math, statistics, random data       |
| **pandas**     | Data manipulation   | Reading CSVs, filtering, joining, summarizing  |
| **matplotlib** | Visualization       | Plotting trends, categories, and distributions |

* These three libraries underpin nearly all **data pipelines**, **ETL transformations**, and **AI model pre-processing** workflows. 