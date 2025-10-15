import pytest
from components.liquibase_conventions_checker import LiquibaseConventionsChecker
from pathlib import Path
import tempfile

def test_conventions_checker_with_good_file():
    tmpdir = tempfile.mkdtemp()
    file_path = Path(tmpdir) / "good_table.sql"
    file_path.write_text("--changeset author:id\nCREATE TABLE TEST(ID INT);\n--rollback DROP TABLE TEST;")

    checker = LiquibaseConventionsChecker()
    result = checker.build(repo_root=tmpdir, ddl_path=".")
    assert result["ok"] is True
    assert len(result["issues"]) == 0

def test_conventions_checker_with_missing_header():
    tmpdir = tempfile.mkdtemp()
    file_path = Path(tmpdir) / "bad_table.sql"
    file_path.write_text("CREATE TABLE TEST(ID INT);")
    checker = LiquibaseConventionsChecker()
    result = checker.build(repo_root=tmpdir, ddl_path=".")
    assert result["ok"] is False
    assert "Missing" in result["issues"][0]["error"]

