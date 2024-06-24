import os
from unittest import TestCase


class TestInstallation(TestCase):
    def test_virtual_environment_activated(self):
        value = os.environ.get("VIRTUAL_ENV")
        if len(value) == 0:
            self.fail("No activated virtual environment")

    def test_django_installed(self):
        try:
            import django
        except ModuleNotFoundError:
            self.fail("Could not find 'django' installed in the environment")

    def test_black_installed(self):
        try:
            import black  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'black' installed in the environment")

    def test_flake8_installed(self):
        try:
            import flake8  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'flake8' installed in the environment")

    def test_djlint_installed(self):
        try:
            import djlint  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'djlint' installed in the environment")
