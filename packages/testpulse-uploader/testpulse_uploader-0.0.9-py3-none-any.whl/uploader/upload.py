import json
import logging
from typing import Optional
import requests

from pathlib import Path
from uploader.urls import ENDPOINT_UPLOAD_RESULTS, TESTPULSE_RECEIVER

from uploader.domain import TestRun

logger = logging.getLogger(__name__)

LOCAL_URL = 'http://localhost:8080'


def upload_test_results(zip: Path, testRun: TestRun) -> Optional[bool]:
    files = {'file': open(zip, 'rb')}

    data = {
        "commitId": testRun.commit,
        "repository": testRun.repository,
    }

    if testRun.test_configuration:
        data['testConfiguration'] = json.dumps(testRun.test_configuration)

    if testRun.github_run_id:
        data['githubRunID'] = testRun.github_run_id

    headers = {
        "Authorization": f"Bearer {testRun.token}",
    }

    url = LOCAL_URL if testRun.localhost else TESTPULSE_RECEIVER
    url = url + ENDPOINT_UPLOAD_RESULTS

    logging.debug(f'Making request to {url}')

    req = requests.post(url=url,
                        files=files,
                        data=data,
                        headers=headers)
    if req.status_code != 200:
        logging.error(f'Something went wrong: {req.text}')
        return False
    return True
