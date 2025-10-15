# components/cicd_dispatcher.py
from langflow.custom import CustomComponent
import requests, os

class CICDDispatcher(CustomComponent):
    display_name = "CI/CD Dispatcher"
    description = "Triggers GitHub Actions/CodePipeline/Jenkins based on config."

    def build(self, provider: str, **kwargs):
        if provider == "github":
            # expects: repo, workflow_file, ref, token, inputs (dict)
            url = f"https://api.github.com/repos/{kwargs['repo']}/actions/workflows/{kwargs['workflow_file']}/dispatches"
            r = requests.post(url,
                              headers={"Authorization": f"Bearer {kwargs['token']}",
                                       "Accept": "application/vnd.github+json"},
                              json={"ref": kwargs.get("ref", "main"), "inputs": kwargs.get("inputs", {})})
            return {"ok": r.status_code in (201, 204), "status": r.status_code, "body": r.text}
        # add CodePipeline/Jenkins branches similarly
        return {"ok": False, "error": "Unsupported provider"}

