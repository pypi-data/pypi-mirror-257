import json
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTTPClient:
    def __init__(self):
        self.session = requests.Session()

    def post(self, url, data, headers=None):
        headers = headers or {"Content-Type": "application/json"}
        try:
            response = self.session.post(url, data=json.dumps(data), headers=headers)
            logger.info(f"Request to {url} completed with status code {response.status_code}.")
            return response
        except requests.RequestException as e:
            logger.error(f"Request to {url} failed: {e}")
            return None  # Возможно, стоит рассмотреть повторную генерацию исключения после логирования.

    def close(self):
        self.session.close()
        logger.info("HTTP session closed.")
