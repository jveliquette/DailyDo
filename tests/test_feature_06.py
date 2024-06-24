from django.contrib import admin
from django.test import TestCase


class TestTodoItemAdmin(TestCase):
    def test_todoitem_registered_with_admin(self):
        try:
            from todos.models import TodoItem

            self.assertTrue(
                admin.site.is_registered(TodoItem),
                msg="todos.models.TodoItem is not registered with the admin",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
