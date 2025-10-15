import pytest
from components.liquibase_validator import LiquibaseValidator
import subprocess

def test_liquibase_validator_mock(monkeypatch):
    def mock_run(cmd, capture_output, text):
        class Result:
            def __init__(self, rc=0): self.returncode = rc; self.stdout = "OK"; self.stderr = ""
        return Result(0)

    monkeypatch.setattr(subprocess, "run", mock_run)
    validator = LiquibaseValidator()
    result = validator.build(changelog_file="liquibase_scripts/changelog-root.xml")
    assert result["validate_ok"] is True
    assert result["dryrun_ok"] is True
    assert "OK" in result["validate_stdout"]

