from django.contrib import admin
from django.test import TestCase


class TestTodoListAdmin(TestCase):
    def test_todolist_registered_with_admin(self):
        try:
            from todos.models import TodoList

            self.assertTrue(
                admin.site.is_registered(TodoList),
                msg="todos.models.TodoList is not registered with the admin",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
