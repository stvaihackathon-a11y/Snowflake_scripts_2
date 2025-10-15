# components/liquibase_conventions_checker.py
from langflow.custom import CustomComponent
from pathlib import Path
import re, json

REQUIRED_HEADERS = ["--changeset", "--rollback"]  # simplify example

class LiquibaseConventionsChecker(CustomComponent):
    display_name = "Liquibase Conventions Checker"
    description = "Lint DDL files for Liquibase headers, naming rules, and rollback presence."

    def build(self, repo_root: str, ddl_path: str = "liquibase_scripts/ddl"):
        issues = []
        files = list(Path(repo_root, ddl_path).rglob("*.sql"))
        for f in files:
            text = f.read_text(encoding="utf-8", errors="ignore")
            if not all(h in text for h in REQUIRED_HEADERS):
                issues.append({"file": str(f), "error": "Missing Liquibase headers/rollback"})
            # Add more checks: naming patterns, forbidden statements, etc.
            if re.search(r"\bDROP\s+TABLE\b", text, re.I) and "--rollback" not in text:
                issues.append({"file": str(f), "error": "DROP TABLE without rollback"})
        ok = len(issues) == 0
        return {"ok": ok, "issues": issues, "checked_files": [str(f) for f in files]}

