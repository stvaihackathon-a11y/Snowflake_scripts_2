# components/liquibase_validator.py
from langflow.custom import CustomComponent
import subprocess, os

class LiquibaseValidator(CustomComponent):
    display_name = "Liquibase Validate & Dry-Run"
    description = "Runs liquibase validate and updateSQL (no changes)."

    def build(self, changelog_file: str):
        # relies on liquibase & snowflake JDBC present in PATH/image
        v = subprocess.run(["liquibase","--changelog-file",changelog_file,"validate"],
                           capture_output=True, text=True)
        d = subprocess.run(["liquibase","--changelog-file",changelog_file,"updateSQL"],
                           capture_output=True, text=True)
        return {
            "validate_ok": v.returncode == 0,
            "validate_stdout": v.stdout, "validate_stderr": v.stderr,
            "dryrun_ok": d.returncode == 0,
            "dryrun_sql": d.stdout[:200000]  # trim for UI
        }
