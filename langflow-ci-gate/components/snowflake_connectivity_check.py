# components/snowflake_connectivity_check.py
from langflow.custom import CustomComponent
import snowflake.connector

class SnowflakeConnectivityCheck(CustomComponent):
    display_name = "Snowflake Connectivity Check"
    description = "Ensures Snowflake login/role/warehouse/db/schema are valid."

    def build(self, account: str, user: str, password: str,
              warehouse: str, database: str, schema: str, role: str):
        cnx = snowflake.connector.connect(
            account=account, user=user, password=password,
            warehouse=warehouse, database=database, schema=schema, role=role
        )
        with cnx.cursor() as cur:
            cur.execute("SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();")
            meta = cur.fetchone()
            cur.execute("SELECT 1")
            ok = cur.fetchone()[0] == 1
        cnx.close()
        return {"ok": ok, "context": {"role": meta[0], "warehouse": meta[1], "database": meta[2], "schema": meta[3]}}
