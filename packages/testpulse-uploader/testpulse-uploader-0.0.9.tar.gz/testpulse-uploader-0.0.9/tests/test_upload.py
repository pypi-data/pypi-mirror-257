from argparse import Namespace
import os
import responses

from pathlib import Path
from unittest import mock
from uploader.domain import TestRun
from uploader.upload import upload_test_results
from uploader.urls import ENDPOINT_UPLOAD_RESULTS, TESTPULSE_RECEIVER

env_variables_mocked = {
    "GITHUB_REPOSITORY": "testpulse/myrepo",
    "GITHUB_SHA": "0289dbc9db2214d7b3e2a115987c3067b4400f25",
    "GITHUB_REF": "refs/remotes/origin/main",
    "TESTPULSE_TOKEN": "MYVERYLONGANDIMPOSSIBLETOGUESSTOKEN",
    "GITHUB_ACTIONS": "True",
}

url = TESTPULSE_RECEIVER + ENDPOINT_UPLOAD_RESULTS


@responses.activate
@mock.patch.dict(os.environ, env_variables_mocked)
def test_simple_false():
    # Register via 'Response' object
    rsp1 = responses.Response(
        method="POST",
        url=url,
        status=404
    )
    responses.add(rsp1)

    testRun = TestRun()
    resp2 = upload_test_results(zip=Path('tests/fixtures/test_results.zip'),
                                testRun=testRun)

    assert resp2 is False


@responses.activate
@mock.patch.dict(os.environ, env_variables_mocked)
def test_simple_true():
    # Register via 'Response' object
    rsp1 = responses.Response(
        method="POST",
        url=url,
        status=200
    )
    responses.add(rsp1)

    testRun = TestRun()
    resp2 = upload_test_results(zip=Path('tests/fixtures/test_results.zip'),
                                testRun=testRun)

    assert resp2 is True
