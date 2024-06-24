from django.test import TestCase
from django.db import models


class TestTodoListModel(TestCase):
    def test_todolist_model_exists(self):
        try:
            from todos.models import TodoList  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models.TodoList'")

    def test_todolist_model_has_char_name_field(self):
        try:
            from todos.models import TodoList

            name = TodoList.name
            self.assertIsInstance(
                name.field,
                models.CharField,
                msg="TodoList.name should be a character field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoList'")
        except AttributeError:
            self.fail("Could not find 'TodoList.name'")

    def test_todolist_model_has_name_with_max_length_200_characters(self):
        try:
            from todos.models import TodoList

            name = TodoList.name
            self.assertEqual(
                name.field.max_length,
                100,
                msg="The max length of TodoList.name should be 100",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoList'")
        except AttributeError:
            self.fail("Could not find 'TodoList.name'")

    def test_todolist_model_has_name_that_is_not_nullable(self):
        try:
            from todos.models import TodoList

            name = TodoList.name
            self.assertFalse(
                name.field.null,
                msg="TodoList.name should not be nullable",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoList'")
        except AttributeError:
            self.fail("Could not find 'TodoList.name'")

    def test_todolist_model_has_name_that_is_not_blank(self):
        try:
            from todos.models import TodoList

            name = TodoList.name
            self.assertFalse(
                name.field.blank,
                msg="TodoList.name should not be allowed a blank value",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models.TodoList'")
        except AttributeError:
            self.fail("Could not find 'TodoList.name'")

    def test_todolist_model_has_created_on_field(self):
        try:
            from todos.models import TodoList

            created_on = TodoList.created_on
            self.assertIsInstance(
                created_on.field,
                models.DateTimeField,
                msg="TodoList.created_on should be a date time field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoList'")
        except AttributeError:
            self.fail("Could not find 'TodoList.created_on'")

    def test_todolist_model_has_created_on_automatically_set(self):
        try:
            from todos.models import TodoList

            created_on = TodoList.created_on
            self.assertTrue(
                created_on.field.auto_now_add,
                msg="TodoList.created_on should automatically set the date",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoList'")
        except AttributeError:
            self.fail("Could not find 'TodoList.created_on'")
