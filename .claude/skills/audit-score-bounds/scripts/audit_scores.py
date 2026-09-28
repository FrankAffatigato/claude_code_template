#!/usr/bin/env python3
"""Audit stored keyword/niche scores in the local SQLite DB for the
0-100 integer invariant documented in CLAUDE.md's Conventions section.

Usage: python audit_scores.py [path-to-db]
Exit code: 0 if no violations (or no DB yet), 1 if violations found.
"""
import os
import re
import sqlite3
import sys

SCORE_COLUMN_PATTERN = re.compile(r"(score|volume|competition)", re.IGNORECASE)


def resolve_db_path(explicit):
    if explicit:
        return explicit
    url = os.environ.get("DATABASE_URL", "")
    if url.startswith("sqlite:///"):
        return url[len("sqlite:///"):]
    return "./niche_scout.db"


def find_score_columns(conn):
    tables = [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    ]
    columns = []
    for table in tables:
        for col in conn.execute(f"PRAGMA table_info({table})"):
            col_name = col[1]
            if SCORE_COLUMN_PATTERN.search(col_name):
                columns.append((table, col_name))
    return columns


def audit_column(conn, table, column):
    violations = []
    query = f"SELECT rowid, {column}, typeof({column}) FROM {table} WHERE {column} IS NOT NULL"
    for rowid, value, sql_type in conn.execute(query):
        if sql_type == "real":
            violations.append(
                f"{table}.{column} row {rowid}: stored as REAL ({value!r}), must be INTEGER"
            )
        elif sql_type != "integer":
            violations.append(
                f"{table}.{column} row {rowid}: stored as {sql_type} ({value!r}), must be INTEGER"
            )
        elif not (0 <= value <= 100):
            violations.append(f"{table}.{column} row {rowid}: {value!r} is outside 0-100")
    return violations


def main():
    db_path = resolve_db_path(sys.argv[1] if len(sys.argv) > 1 else None)
    if not os.path.exists(db_path):
        print(f"No database file found at {db_path} -- nothing to audit yet.")
        return 0

    conn = sqlite3.connect(db_path)
    try:
        score_columns = find_score_columns(conn)
        if not score_columns:
            print("No score-like columns found in any table -- nothing to audit yet.")
            return 0

        violations = []
        for table, column in score_columns:
            violations.extend(audit_column(conn, table, column))

        if not violations:
            checked = ", ".join(f"{t}.{c}" for t, c in score_columns)
            print(f"OK: {len(score_columns)} score column(s) checked ({checked}), all 0-100 integers.")
            return 0

        print(f"{len(violations)} violation(s) found:")
        for v in violations:
            print(f"  - {v}")
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
