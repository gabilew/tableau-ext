import os
from unittest.mock import patch
import unittest

from tableau_ext.utils import prepared_env

class TestUtils(unittest.TestCase):
    def test_prepared_env(self) -> None:
        envs = {
            'TEST_TOKEN_SECRET': 'a',
            'TEST_TOKEN_NAME': 'b',
            'TEST_BASE_URL': 'c',
            'TEST_API_VERSION': 'd',
            'TEST_SITE_ID': 'e',
        }

        with unittest.mock.patch.dict(os.environ, envs):
            config = prepared_env("TEST")

            assert len(config) == 5
            assert config["TOKEN_SECRET"] == 'a'
        
        with unittest.mock.patch.dict(os.environ, {}) and self.assertRaises(Exception):
            config = prepared_env("TEST")
