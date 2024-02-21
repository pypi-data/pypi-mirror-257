from argparse import Namespace
import os
from typing import Dict, Optional

from uploader.exceptions import NotInCI


class TestRun:
    def __init__(self, args: Optional[Namespace] = None) -> None:
        self.args = args

    @property
    def localhost(self) -> Optional[str]:
        if self.args:
            return self.args.localhost
        return None

    @property
    def operating_system(self) -> Optional[str]:
        if self.args:
            return self.args.operating_system
        return None

    @property
    def language_version(self) -> Optional[str]:
        if self.args:
            return self.args.language_version
        return None

    @property
    def test_framework_version(self) -> Optional[str]:
        if self.args:
            return self.args.test_framework_version
        return None

    @property
    def github_run_id(self) -> Optional[str]:
        if self.args:
            return self.args.github_run_id
        return None

    @property
    def repository(self) -> str:
        if 'GITHUB_REPOSITORY' in os.environ:
            return os.environ['GITHUB_REPOSITORY']
        raise NotInCI("GITHUB_REPOSITORY")

    @property
    def commit(self) -> str:
        if 'GITHUB_SHA' in os.environ:
            return os.environ['GITHUB_SHA']
        raise NotInCI("GITHUB_SHA")

    @property
    def ref(self) -> str:
        if 'GITHUB_REF' in os.environ:
            return os.environ['GITHUB_REF']
        raise NotInCI("GITHUB_REF")

    @property
    def token(self) -> str:
        if 'TESTPULSE_TOKEN' in os.environ:
            return os.environ['TESTPULSE_TOKEN']
        raise NotInCI("TESTPULSE_TOKEN")

    @property
    def test_configuration(self) -> Dict[str, str]:
        tc = {}
        if self.language_version:
            tc['languageVersion'] = self.language_version
        if self.operating_system:
            tc['operatingSystem'] = self.operating_system
        if self.test_framework_version:
            tc['testFrameworkVersion'] = self.test_framework_version

        return tc


class TokenVerification:
    @property
    def token(self) -> str:
        if 'TESTPULSE_TOKEN' in os.environ:
            return os.environ['TESTPULSE_TOKEN']
        raise NotInCI("TESTPULSE_TOKEN")
