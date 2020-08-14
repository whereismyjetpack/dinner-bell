from kubernetes import client, config
from time import sleep, time
import os


class KubeUtils:
    def __init__(self, timeout=None):
        if not timeout:
            self.deployment_timeout = int(os.environ.get("TIMEOUT_SECONDS", 90))
        else:
            self.deployment_timeout = int(timeout)
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException:
            config.load_kube_config()

    def get_deployment_status(self, namespace, deployment):
        # Simply returns a deployment status
        api_instance = client.AppsV1Api()
        resp = api_instance.read_namespaced_deployment(deployment, namespace)
        return resp.status

    def wait_for_deployment(self, namespace, deployment, channel):
        # Waits for a deployment to finish
        # Returns True for success, False for failure, along with status from kubernetes
        start_time = time()
        while True:
            status = self.get_deployment_status(namespace, deployment)
            if time() >= start_time + self.deployment_timeout:
                return False, status
            if status.ready_replicas == status.replicas:
                return True, status
                break
            else:
                sleep(2)
