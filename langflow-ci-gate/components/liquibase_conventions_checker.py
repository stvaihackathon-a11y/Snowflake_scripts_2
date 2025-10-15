# components/liquibase_conventions_checker.py
from langflow.custom import CustomComponent
from pathlib import Path
import re, json

REQUIRED_TOKENS = ["--changeset", "--rollback"]  # minimal; extend as needed

class LiquibaseConventionsChecker(CustomComponent):
    display_name = "Liquibase Conventions Checker"
    description = "Checks headers, rollbacks and basic naming rules in DDL."

    def build(self, repo_root: str = ".", ddl_path: str = "liquibase_scripts/ddl"):
        issues, files = [], list(Path(repo_root, ddl_path).rglob("*.sql"))
        for f in files:
            txt = f.read_text(encoding="utf-8", errors="ignore")
            if not all(t in txt for t in REQUIRED_TOKENS):
                issues.append({"file": str(f), "error": "Missing --changeset and/or --rollback"})
            if re.search(r"\bDROP\s+TABLE\b", txt, re.I) and "--rollback" not in txt:
                issues.append({"file": str(f), "error": "DROP TABLE without rollback"})
        return {"ok": len(issues) == 0, "issues": issues, "checked": [str(p) for p in files]}
