# components/cicd_dispatcher.py
from langflow.custom import CustomComponent
import requests

class CICDDispatcher(CustomComponent):
    display_name = "CI/CD Dispatcher (GitHub)"
    description = "Calls workflow_dispatch to run Liquibase deploy."

    def build(self, repo_slug: str, workflow_file: str, ref: str,
              token: str, env: str, changelog: str, context_tags: str = ""):
        url = f"https://api.github.com/repos/{repo_slug}/actions/workflows/{workflow_file}/dispatches"
        body = {"ref": ref, "inputs": {
            "env": env, "branch": ref, "changelog": changelog, "context_tags": context_tags
        }}
        r = requests.post(url,
            headers={"Authorization": f"Bearer {token}",
                     "Accept": "application/vnd.github+json"},
            json=body)
        return {"ok": r.status_code in (201, 204), "status": r.status_code, "response": r.text}
