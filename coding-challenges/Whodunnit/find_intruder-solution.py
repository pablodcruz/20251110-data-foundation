#!/usr/bin/env python3

"""
Simple Logfile Whodunnit

Reads access.log, looks at requests between 22:55:00 and 23:05:00,
groups by IP, and flags IPs that:
- hit more than N unique endpoints in that window
- AND had at least one 200 to /transfer or /admin
"""

LOG_FILE = "access.log"
WINDOW_START = "22:55:00"
WINDOW_END = "23:05:00"
THRESHOLD = 5  # must hit more than this many unique endpoints

SENSITIVE_ENDPOINTS = {"/transfer", "/admin"}


def parse_line(line):
    """
    Example line:
    2025-11-15T22:58:01Z  192.168.0.10   /login        200

    Returns (time_str, ip, endpoint, status_int) or None if malformed.
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split()
    if len(parts) < 4:
        return None

    ts_str, ip, endpoint, status_str = parts[:4]

    # Extract time-of-day part: "2025-11-15T22:58:01Z" -> "22:58:01"
    # We split on 'T' and then strip the trailing 'Z'
    try:
        date_part, time_part = ts_str.split("T")
        time_part = time_part.rstrip("Z")
    except ValueError:
        return None

    try:
        status = int(status_str)
    except ValueError:
        return None

    return time_part, ip, endpoint, status


def time_in_window(time_str, start_str, end_str):
    """
    Compare HH:MM:SS strings lexicographically.
    Works because the format is fixed-width.
    """
    return start_str <= time_str <= end_str


def main():
    # Data structures:
    # ip -> set of endpoints
    endpoints_by_ip = {}
    # ip -> set of sensitive endpoints that returned 200
    sensitive_hits_by_ip = {}

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_line(line) # parse_line
            if parsed is None:
                continue

            time_str, ip, endpoint, status = parsed

            # Filter by time window
            if not time_in_window(time_str, WINDOW_START, WINDOW_END):
                continue

            # Track unique endpoints
            if ip not in endpoints_by_ip:
                endpoints_by_ip[ip] = set()
            endpoints_by_ip[ip].add(endpoint)

            # Track sensitive successful hits
            if status == 200 and endpoint in SENSITIVE_ENDPOINTS:
                if ip not in sensitive_hits_by_ip:
                    sensitive_hits_by_ip[ip] = set()
                sensitive_hits_by_ip[ip].add(endpoint)

    # Find suspects
    suspects = []
    for ip, endpoints in endpoints_by_ip.items():
        unique_count = len(endpoints)
        has_sensitive_200 = ip in sensitive_hits_by_ip and len(sensitive_hits_by_ip[ip]) > 0

        if unique_count > THRESHOLD and has_sensitive_200:
            suspects.append((ip, unique_count, sensitive_hits_by_ip[ip]))

    # Print report
    print("Suspected IPs:")
    if not suspects:
        print("- (none)")
    else:
        for ip, unique_count, sensitive_paths in sorted(suspects):
            paths_list = ", ".join(sorted(sensitive_paths))
            print(f"- {ip} ({unique_count} endpoints, accessed {paths_list} with 200)")


if __name__ == "__main__":
    main()