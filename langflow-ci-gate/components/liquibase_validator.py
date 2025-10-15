# components/liquibase_validator.py
from langflow.custom import CustomComponent
import subprocess, json, os, tempfile, textwrap

class LiquibaseValidator(CustomComponent):
    display_name = "Liquibase Validate & Dry-Run"
    description = "Runs `liquibase validate` and `updateSQL` against Snowflake JDBC (no changes applied)."

    def build(self,
              changelog_file: str,
              url: str,  # e.g., "jdbc:snowflake://<acct>.snowflakecomputing.com"
              username: str,
              password: str,
              warehouse: str,
              database: str,
              schema: str,
              role: str = "SYSADMIN"):
        env = os.environ.copy()
        env.update({
            "LIQUIBASE_URL": url,
            "LIQUIBASE_USERNAME": username,
            "LIQUIBASE_PASSWORD": password,
            "SNOWFLAKE_WAREHOUSE": warehouse,
            "SNOWFLAKE_DATABASE": database,
            "SNOWFLAKE_SCHEMA": schema,
            "SNOWFLAKE_ROLE": role
        })
        # validate
        v = subprocess.run(["liquibase", "--changelog-file", changelog_file, "validate"],
                           capture_output=True, text=True, env=env)
        # dry-run SQL
        d = subprocess.run(["liquibase", "--changelog-file", changelog_file, "updateSQL"],
                           capture_output=True, text=True, env=env)
        return {
            "validate_ok": v.returncode == 0,
            "validate_stdout": v.stdout,
            "validate_stderr": v.stderr,
            "dryrun_sql": d.stdout,
            "dryrun_ok": d.returncode == 0
        }

