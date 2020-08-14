from slack import WebClient
from slack.errors import SlackApiError
import os


class Notifier:
    def __init__(self, channel, deployment, namespace, custom_message=None):
        self.client = WebClient(token=os.environ.get("SLACK_TOKEN"))
        self.slack_username = os.environ.get("SLACK_USERNAME", "dinner-bell")
        self.custom_message = custom_message
        self.channel = channel
        self.deployment = deployment
        self.namespace = namespace

    def send_message(self, message):
        text = f"{message}"
        blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": f"{message}"}}]
        try:
            resp = self.client.chat_postMessage(
                channel=self.channel,
                text=text,
                as_user=False,
                blocks=blocks,
                username=self.slack_username,
            )
        except SlackApiError as e:
            print(e)

    def send_initalize_message(self):
        text = f":arrows_counterclockwise: Deployment *{self.deployment}* is progressing"
        self.send_message(text)

    def send_success_message(self, status):
        text = f":bellhop_bell: _Ding!_ Deployment *{self.deployment}* is Ready!"
        if self.custom_message:
            text = text + f"\n{self.custom_message}"
        self.send_message(text)

    def send_failure_message(self, status):
        text = (
            f":boom: Deployment *{self.deployment}* Timed out waiting for Ready Status"
        )
        self.send_message(text)
