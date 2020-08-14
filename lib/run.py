import kopf
from kube_utils import KubeUtils
from notifiers import Notifier


@kopf.on.create(
    "apps",
    "v1",
    "deployments",
    annotations={"dinner-bell.io/slack-channel": kopf.PRESENT},
)
@kopf.on.update(
    "apps",
    "v1",
    "deployments",
    annotations={"dinner-bell.io/slack-channel": kopf.PRESENT},
)
def deployment_create(body, **kwargs):
    channel = body.metadata.annotations.get("dinner-bell.io/slack-channel")
    timeout = body.metadata.annotations.get("dinner-bell.io/timeout-seconds", None)
    k = KubeUtils(timeout=timeout)
    deployment = body.metadata.name
    namespace = body.metadata.namespace
    custom_message = body.metadata.annotations.get(
        "dinner-bell.io/custom-message", None
    )
    notifier = Notifier(channel, deployment, namespace, custom_message=custom_message)
    notifier.send_initalize_message()
    success, status = k.wait_for_deployment(namespace, deployment, channel)
    if success:
        notifier.send_success_message(status)
    elif not success:
        notifier.send_failure_message(status)
