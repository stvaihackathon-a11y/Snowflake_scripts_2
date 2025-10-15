# components/pipeline_status_poller.py
from langflow.custom import CustomComponent
import requests, time

class PipelineStatusPoller(CustomComponent):
    display_name = "Pipeline Status Poller (GitHub)"
    description = "Polls the latest workflow run until completed."

    def build(self, repo_slug: str, workflow_file: str, token: str,
              timeout_sec: int = 180, poll_every_sec: int = 5):
        hdr = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
        list_url = f"https://api.github.com/repos/{repo_slug}/actions/workflows/{workflow_file}/runs?per_page=1"
        deadline = time.time() + timeout_sec
        last_status = {}
        while time.time() < deadline:
            r = requests.get(list_url, headers=hdr)
            if r.status_code != 200:
                time.sleep(poll_every_sec); continue
            runs = r.json().get("workflow_runs", [])
            if not runs:
                time.sleep(poll_every_sec); continue
            run = runs[0]
            last_status = {"status": run["status"], "conclusion": run["conclusion"], "html_url": run["html_url"]}
            if run["status"] == "completed":
                break
            time.sleep(poll_every_sec)
        return {"done": last_status.get("status") == "completed", **last_status}
