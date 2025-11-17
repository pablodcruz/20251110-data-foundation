
## 1️⃣ Logfile Whodunnit (File I/O + Parsing + Collections)

**Story:**
There was a security breach at 23:00 yesterday. You’re given a web server log file and must figure out who likely caused it.

**You get:**
A text file `access.log` with lines like:

```text
2025-11-15T22:58:01Z  192.168.0.10   /login        200
2025-11-15T22:59:10Z  192.168.0.13   /admin        403
2025-11-15T23:00:05Z  192.168.0.77   /transfer     200
...
```

**Task:**

1. Write a script `find_intruder.py` that:

   * Reads `access.log`.
   * Finds all requests **between 22:55:00 and 23:05:00**.
   * Groups requests by IP address.
2. Flag any IP that:

   * Hit more than **N** unique endpoints (e.g. N=5) in that window **and**
   * Had at least one successful request with status `200` to `/transfer` or `/admin`.

**Output:**
Print a small report like:

```text
Suspected IPs:
- 192.168.0.77 (7 endpoints, accessed /transfer with 200)
```
