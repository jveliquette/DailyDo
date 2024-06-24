from django.test import SimpleTestCase


class TestDjangoProjectAndApp(SimpleTestCase):
    def test_brain_two_project_created(self):
        try:
            from brain_two.settings import INSTALLED_APPS  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find the Django project 'brain_two'")

    def test_todos_app_created(self):
        try:
            from todos.apps import TodosConfig  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find the Django app 'todos'")

    def test_todos_app_installed(self):
        try:
            from brain_two.settings import INSTALLED_APPS

            self.assertIn("todos.apps.TodosConfig", INSTALLED_APPS)
        except ModuleNotFoundError:
            self.fail("Could not find 'todos' installed in 'brain_two'")
