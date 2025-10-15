# components/notifier.py
from langflow.custom import CustomComponent
import requests, os, json

class Notifier(CustomComponent):
    display_name = "Notifier"
    description = "Sends Slack/Email notification with results."

    def build(self, channel_webhook: str, title: str, summary: dict):
        text = f"*{title}*\n```{json.dumps(summary, indent=2)[:2800]}```"
        r = requests.post(channel_webhook, json={"text": text})
        return {"ok": r.status_code == 200}

