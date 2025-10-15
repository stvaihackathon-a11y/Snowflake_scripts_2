# components/notifier.py
from langflow.custom import CustomComponent
import requests, json

class Notifier(CustomComponent):
    display_name = "Notifier (Slack)"
    description = "Sends a Slack message with results."

    def build(self, slack_webhook: str, title: str, summary: dict):
        text = f"*{title}*\n```{json.dumps(summary, indent=2)[:2800]}```"
        r = requests.post(slack_webhook, json={"text": text})
        return {"ok": r.status_code == 200}
