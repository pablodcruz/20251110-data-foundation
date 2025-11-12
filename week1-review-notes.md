# Week 1 — Python Fundamentals, Git, and Agile

## Learning Outcomes

By the end of this week you will be able to:

* Explain SDLC & Agile, write clear user stories with acceptance criteria, and run daily stand-ups.
* Use Git professionally: branch, commit, push/pull, open PRs, resolve conflicts, and follow Conventional Commits.
* Set up a Python 3.11+ environment with `venv`, run scripts, use the REPL and Jupyter.
* Write Python that uses variables, expressions, **casting**, control flow, **functions (incl. lambdas)**, core data structures, and **namespaces/scope (LEGB)**.
* Describe and use **data types** including strings, numbers, **range**, lists, tuples, sets, dicts, **binary types** (bytes/bytearray), booleans, and `NoneType`.
* Build simple programs using **iterators** and idiomatic loops.

---

## Admin & Setup

* **Tooling**

  * Python 3.11+ (verify: `python --version` or `python3 --version`)
  * VS Code + extensions: *Python*, *Pylance*, *Jupyter*
  * Git + a GitHub account

* **Project bootstrap**

  ```bash
  git clone <your-repo-url> data-foundations
  cd data-foundations

  # virtual env
  python -m venv .venv
  # Windows (PowerShell): .\.venv\Scripts\Activate.ps1
  # Windows (Git Bash):   source .venv/Scripts/activate
  # macOS/Linux:
  source .venv/bin/activate

  python -m pip install --upgrade pip
  pip install jupyter pandas
  ```

---

## Python Orientation

### Full-Stack Overview (context)

* **Frontend** (web/mobile UI) + **Backend** (APIs, services, databases) + **Data** (ETL, analytics, warehousing).
* Why Python in data foundations: fast iteration, rich ecosystem, glue language for ETL/SQL.

### Interpreter vs Compiler

* **Interpreter** executes line-by-line (Python CPython bytecode VM).
* **Compiler** translates to machine code ahead of time (e.g., C/C++).
* Python typically **interpreted** (with bytecode step); REPL enables rapid feedback.

### REPL/Jupyter

* REPL: `python` (or `python -i`) for quick experiments.
* Jupyter: literate notebooks for demos/EDA; keep “production” logic in `.py` modules.

---

## SDLC (Software Development Life Cycle)

* **Phases**: Requirements → Design → Implementation → Testing → Deployment → Maintenance
* **Waterfall**: sequential; simple but rigid.
* **Agile**: iterative; frequent feedback and prioritization.

### Agile for Developers

* **Values**: Individuals & interactions; Working software; Customer collaboration; Responding to change.
* **Scrum roles**: PO, SM, Dev Team.
* **Ceremonies**: Planning, Daily Stand-up (≤15m), Review, Retro.
* **User story**: *As a* `<role>` *I want* `<goal>` *so that* `<benefit>`; include **Acceptance Criteria**.
* **Story pointing**: relative sizing (Fibonacci).

---

## Git Fundamentals

### Source Control Management (SCM)

* **VCS**: track changes & history.
* **CVCS**: centralized (single server).
* **DVCS**: distributed (e.g., **Git**); full history per clone.

### File states & everyday commands

```bash
git init                         # initialize repository
git remote add origin <URL>      # link remote
git status
git add <path>                   # stage changes
git commit -m "feat: initial commit"
git branch                       # list branches
git checkout -b feat/basics      # create & switch
git push -u origin feat/basics   # first push
git pull                         # fetch+merge current branch
git merge <branch>               # merge into current branch
git log --oneline --graph
```

**Conventional Commits**: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:` (e.g., `feat(core): add cli basics`).

**Quick exercises** (Git katas):

* Init a repo, add a file, create a feature branch, open a PR.
* Create a merge conflict with a partner and resolve it.
* Add a `.gitignore` for Python:

  ```
  __pycache__/
  *.pyc
  .venv/
  .env
  .DS_Store
  Thumbs.db
  ```

---

## Python Basics

### Syntax & Style

* Indentation is semantic (meaning) (4 spaces).
* Snake_case; docstrings with triple quotes; comments with `#`.

### What is Python? Why Python?

* Batteries-included stdlib, strong community, great for data/AI/automation.

### Variables and Data Types

* Strongly typed, dynamically bound.
* Built-ins: `int`, `float`, `bool`, `str`, `list`, `tuple`, `set`, `dict`, `NoneType`.

### Casting (type conversions)

```python
int("42")         # 42
float("3.14")     # 3.14
str(10)           # "10"
bool("")          # False; non-empty strings/collections → True
```

### User Input and Output

```python
name = input("Name: ")
print(f"Hello, {name}!")
```

### Comments

* Single line `# ...`; block by convention with multiple `#` lines; docstrings for modules/classes/functions.

---

## Python Data Types

### Namespaces & Scope (LEGB)

* **L**ocal → **E**nclosing → **G**lobal → **B**uilt-ins (Python's predefined names) lookup order.

```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)  # local
    inner()
```

### Booleans & NoneType

```python
is_ready = True
nothing = None
```

### Numbers

* `int` (unbounded), `float` (IEEE 754), `complex` (optional), `Decimal` (from `decimal`) for precision-critical work.

### Strings

* Immutable sequences; slicing; methods (`split`, `join`, `replace`, `startswith`, f-strings).

### Lists & Tuples

* Lists mutable; tuples immutable; both ordered.

### Range

```python
for i in range(3):  # 0,1,2
    ...
```

### Sets & Dictionaries

* Sets: unique items; Dicts: key→value mappings.

### Binary Types

```python
b = b"hello"                # bytes
ba = bytearray(b)           # mutable bytes
mv = memoryview(b)          # zero-copy slices
```

### Casting refresher

* `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, `bytes()`.

### Datetime (quick)

```python
from datetime import datetime, timedelta
now = datetime.now()
yesterday = now - timedelta(days=1)
```

---

## Flow Control Statements

```python
# If-Else
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

# While
n = 3
while n > 0:
    n -= 1

# For (incl. range & iterables)
for item in ["a", "b", "c"]:
    ...
```

---

## Functions & Arrays

### Functions

```python
def clean(name: str) -> str:
    return name.strip().title()

# Lambda (small anonymous function)
title = lambda s: s.strip().title()
```

### “Arrays” in Python

* Use **lists** for general-purpose dynamic arrays.
* Optional: `array` module (`from array import array`) for typed, compact numeric arrays.

### Iterators

```python
it = iter([10, 20, 30])
print(next(it))  # 10
for x in it:
    print(x)     # 20, 30
```

---

## Classes & Inheritance (OOP Primer)

### Classes & Objects

```python
class Person:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def greet(self) -> str:
        return f"Hi, I'm {self.name}"
```

### OOP Concepts & Inheritance

```python
class Employee(Person):                  # inheritance
    def __init__(self, id: int, name: str, role: str):
        super().__init__(id, name)
        self.role = role

    def greet(self) -> str:              # overriding
        return f"{super().greet()} and I work as {self.role}"
```

### Iterators (protocol) & Scope recap

* Iterator protocol: `__iter__()` returns iterator; iterator implements `__next__()`.
* Scope recap: prefer local variables; avoid unnecessary `global`/`nonlocal`.

---

## Lab Starters

### basics_cli.py

```python
name = input("Name: ").strip()
age = int(input("Age: ").strip())
print(f"Hello {name}! Next year you'll be {age + 1}.")
```

### datatypes_playground.py

```python
s = "data foundations"
assert s[:4] == "data"
nums = [3,1,4]; nums.append(1); assert 1 in nums
coords = (40.7, -74.0)
flags = {"etl", "sql", "python"}
cfg = {"retries": 3, "timeout": 5.0}
b = b"abc"; ba = bytearray(b); ba[0] = 65  # 'A'
r = range(3); assert list(r) == [0,1,2]
```

### flow_funcs.py

```python
def grade(score: int) -> str:
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    return "D"

title = lambda s: s.strip().title()  # example lambda

from array import array
arr = array("i", [1,2,3])  # typed int array
```

### oop_basics.py

```python
class Person:
    def __init__(self, pid: int, name: str):
        self.pid, self.name = pid, name
    def greet(self) -> str: return f"Hi, I'm {self.name}"

class Employee(Person):
    def __init__(self, pid: int, name: str, role: str):
        super().__init__(pid, name); self.role = role
    def greet(self) -> str: return f"{super().greet()} and I work as {self.role}"

emps = [Employee(1,"Ada","Engineer"), Employee(2,"Alan","Researcher")]
for e in emps: print(e.greet())
```

---

## Stretch (optional)

* Add a small iterator class (custom `__iter__`/`__next__`).
* Use `array("f")` to store floats and compare memory footprint vs list.
* Add a `Decimal` example for currency rounding.
