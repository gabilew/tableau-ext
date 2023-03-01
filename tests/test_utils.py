import os
from logging import exception
from unittest import TestCase, mock

from tableau_ext.utils import prepared_env


class TestUtils(TestCase):
    def test_prepared_env(self) -> None:
        envs = {
            "TEST_TOKEN_SECRET": "a",
            "TEST_TOKEN_NAME": "b",
            "TEST_BASE_URL": "c",
            "TEST_API_VERSION": "d",
            "TEST_SITE_ID": "e",
        }

        with mock.patch.dict(os.environ, envs):
            config = prepared_env("TEST")

            assert len(config) == 5
            assert config["TOKEN_SECRET"] == "a"

    def test_prepared_env_failure(self) -> None:
        with mock.patch.dict(os.environ, {}) and self.assertRaises(Exception) as ctx:
            prepared_env("TEST")

        self.assertTrue("These env variables are missing" in str(ctx.exception))
