from django.test import TestCase
from django.db import models


class TestTodoItemModel(TestCase):
    def test_todoitem_model_exists(self):
        try:
            from todos.models import TodoItem  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models.TodoItem'")

    def test_todoitem_model_has_char_task_field(self):
        try:
            from todos.models import TodoItem

            task = TodoItem.task
            self.assertIsInstance(
                task.field,
                models.CharField,
                msg="TodoItem.task should be a character field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.task'")

    def test_todoitem_model_has_task_with_max_length_200_characters(self):
        try:
            from todos.models import TodoItem

            task = TodoItem.task
            self.assertEqual(
                task.field.max_length,
                100,
                msg="The max length of TodoItem.task should be 100",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.task'")

    def test_todoitem_model_has_task_that_is_not_nullable(self):
        try:
            from todos.models import TodoItem

            task = TodoItem.task
            self.assertFalse(
                task.field.null,
                msg="TodoItem.task should not be nullable",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.task'")

    def test_todoitem_model_has_task_that_is_not_blank(self):
        try:
            from todos.models import TodoItem

            task = TodoItem.task
            self.assertFalse(
                task.field.blank,
                msg="TodoItem.task should not be allowed a blank value",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.task'")

    def test_todoitem_model_has_due_date_field(self):
        try:
            from todos.models import TodoItem

            due_date = TodoItem.due_date
            self.assertIsInstance(
                due_date.field,
                models.DateTimeField,
                msg="TodoItem.due_date should be a date time field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.due_date'")

    def test_todoitem_model_has_due_date_that_is_nullable(self):
        try:
            from todos.models import TodoItem

            due_date = TodoItem.due_date
            self.assertTrue(
                due_date.field.null,
                msg="TodoItem.due_date should be nullable",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.due_date'")

    def test_todoitem_model_has_due_date_that_is_blank(self):
        try:
            from todos.models import TodoItem

            due_date = TodoItem.due_date
            self.assertTrue(
                due_date.field.blank,
                msg="TodoItem.due_date should be allowed a blank value",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.due_date'")

    def test_todoitem_model_has_is_completed_field(self):
        try:
            from todos.models import TodoItem

            is_completed = TodoItem.is_completed
            self.assertIsInstance(
                is_completed.field,
                models.BooleanField,
                msg="TodoItem.is_completed should be a boolean field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.is_completed'")

    def test_todoitem_model_has_is_completed_with_default_value_false(self):
        try:
            from todos.models import TodoItem

            is_completed = TodoItem.is_completed
            self.assertFalse(
                is_completed.field.default,
                msg="TodoItem.due_date should have a default value of False",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.is_completed'")

    def test_todoitem_model_has_list_field(self):
        try:
            from todos.models import TodoItem

            list = TodoItem.list
            self.assertIsInstance(
                list.field,
                models.ForeignKey,
                msg="TodoItem.list should be a ForeignKey field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.list'")

    def test_todoitem_model_has_list_with_related_name_items(self):
        try:
            from todos.models import TodoItem

            list = TodoItem.list
            self.assertEqual(
                list.field._related_name,
                "items",
                msg="TodoItem.list should have a related name of items",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail("Could not find 'todos.models.TodoItem'")
        except AttributeError:
            self.fail("Could not find 'TodoItem.list'")

    def test_todoitem_model_has_foreign_key_with_todolist(self):
        try:
            from todos.models import TodoItem, TodoList

            list = TodoItem.list
            self.assertEqual(
                list.field.related_model,
                TodoList,
                msg="TodoItem.list should have a foreign key with the TodoList model",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'todos.models'")
        except ImportError:
            self.fail(
                "Could not find 'todos.models.TodoItem' or 'todos.models.TodoList'"
            )
        except AttributeError:
            self.fail("Could not find 'TodoItem.list'")
