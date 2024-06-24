from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from .utils import Document
from todos.models import TodoList


class TestTodoListCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get("/todos/create/")
        self.content = self.response.content.decode("utf-8")
        self.document = Document()
        self.document.feed(self.content)

    def test_todo_list_create_resolves_to_accounts_todo_list_create(self):
        path = reverse("todo_list_create")
        self.assertEqual(
            path,
            "/todos/create/",
            msg="Could not resolve path name 'todo_list_create' to '/todos/create/",
        )

    def test_accounts_todo_list_create_returns_200(self):
        self.assertEqual(
            self.response.status_code,
            200,
            msg="Did not get the create todolist page",
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

    def test_form_has_name_input(self):
        form = self.document.select("html", "body", "main", "div", "form")
        inputs = form.get_all_children("input")
        name = None
        for input in inputs:
            if input.attrs.get("name") == "name":
                name = input
                break
        self.assertIsNotNone(
            name,
            msg="Could not find the name input",
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

    def test_todo_list_create_works(self):
        response = self.client.post(
            reverse("todo_list_create"),
            {
                "name": "ZZZZZZ",
            },
        )
        self.assertEqual(
            response.status_code,
            302,
            msg="TodoList creation does not seem to work",
        )

    def test_create_redirects_to_detail(self):
        response = self.client.post(
            reverse("todo_list_create"),
            {
                "name": "ZZZZZZ",
            },
        )
        todolist = TodoList.objects.get(name="ZZZZZZ")
        self.assertEqual(
            response.headers.get("Location"),
            reverse("todo_list_detail", args=[todolist.id]),
            msg="Create does not redirect to detail",
        )

    def test_list_view_has_link_to_create(self):
        response = self.client.get(reverse("todo_list_list"))
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        html = document.select("html")
        links = html.get_all_children("a")
        create_link = None
        for link in links:
            if link.attrs.get("href") == reverse("todo_list_create"):
                create_link = link
                break
        self.assertIsNotNone(
            create_link,
            msg="Could not find the create link for todos on the list view",
        )
