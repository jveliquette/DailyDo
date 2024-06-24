from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from .utils import Document
from todos.models import TodoItem, TodoList


class TestTodoItemCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.todolist = TodoList.objects.create(name="TodoList 1")
        self.response = self.client.get("/todos/items/create/")
        self.content = self.response.content.decode("utf-8")
        self.document = Document()
        self.document.feed(self.content)

    def test_todo_item_create_resolves_to_todo_item_create(self):
        path = reverse("todo_item_create")
        self.assertEqual(
            path,
            "/todos/items/create/",
            msg="Could not resolve path name 'todo_item_create' to '/todos/items/create/",
        )

    def test_accounts_todo_item_create_returns_200(self):
        self.assertEqual(
            self.response.status_code,
            200,
            msg="Did not get the create todoitem page",
        )

    def test_page_has_fundamental_five(self):
        self.assertTrue(
            self.document.has_fundamental_five(),
            msg="The response did not have the fundamental five",
        )

    def test_form_is_post(self):
        form = self.document.select("html", "body", "main", "div", "form")
        self.assertIsNotNone(
            form,
            msg=(
                "Did not find the form at the path "
                "html > body > main > div > form"
            ),
        )
        self.assertIn(
            "method",
            form.attrs,
            msg="Did not find 'method' for the form",
        )
        self.assertEqual(
            form.attrs.get("method").lower(),
            "post",
            msg="Form was not a post form",
        )

    def test_form_has_task_input(self):
        form = self.document.select("html", "body", "main", "div", "form")
        inputs = form.get_all_children("input")
        name = None
        for input in inputs:
            if input.attrs.get("name") == "task":
                name = input
                break
        self.assertIsNotNone(
            name,
            msg="Could not find the task input",
        )

    def test_form_has_due_date_input(self):
        form = self.document.select("html", "body", "main", "div", "form")
        inputs = form.get_all_children("input")
        name = None
        for input in inputs:
            if input.attrs.get("name") == "due_date":
                name = input
                break
        self.assertIsNotNone(
            name,
            msg="Could not find the due_date input",
        )

    def test_form_has_is_completed_checkbox(self):
        form = self.document.select("html", "body", "main", "div", "form")
        inputs = form.get_all_children("input")
        name = None
        for input in inputs:
            if input.attrs.get("name") == "is_completed":
                name = input
                break
        self.assertIsNotNone(
            name,
            msg="Could not find the is_completed input",
        )

    def test_form_has_list_select(self):
        form = self.document.select("html", "body", "main", "div", "form")
        inputs = form.get_all_children("select")
        name = None
        for input in inputs:
            if input.attrs.get("name") == "list":
                name = input
                break
        self.assertIsNotNone(
            name,
            msg="Could not find the list select",
        )

    def test_form_has_button(self):
        form = self.document.select("html", "body", "main", "div", "form")
        buttons = form.get_all_children("button")
        found_button = None
        for button in buttons:
            if button.inner_text().strip().lower() == "create":
                found_button = button
                break
        self.assertIsNotNone(
            found_button,
            msg="Could not find the 'Create' button",
        )

    def test_todo_item_create_works(self):
        response = self.client.post(
            reverse("todo_item_create"),
            {
                "task": "ZZZZZZ",
                "due_date": "01/01/1969",
                "list": self.todolist.pk,
            },
        )
        try:
            todoitem = TodoItem.objects.get(task="ZZZZZZ")
            self.assertTrue(todoitem)
        except:
            self.fail("Did not create a new todo item")

    def test_create_redirects_to_detail(self):
        response = self.client.post(
            reverse("todo_item_create"),
            {
                "task": "ZZZZZZ",
                "due_date": "01/01/1969",
                "list": self.todolist.pk,
            },
        )
        self.assertEqual(
            response.headers.get("Location"),
            reverse("todo_list_detail", args=[self.todolist.id]),
            msg="Create does not redirect to detail",
        )

    def test_detail_view_has_link_to_create(self):
        response = self.client.get(reverse("todo_list_list"))
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        html = document.select("html")
        links = html.get_all_children("a")
        create_link = None
        for link in links:
            if link.attrs.get("href") == reverse("todo_item_create"):
                create_link = link
                break
        self.assertIsNotNone(
            create_link,
            msg="Could not find the create link for todos on the list view",
        )
