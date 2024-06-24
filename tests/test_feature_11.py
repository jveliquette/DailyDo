from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from .utils import Document
from todos.models import TodoList


class TestTodoListDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.todolist = TodoList.objects.create(name="Original Name")
        self.response = self.client.get(f"/todos/{self.todolist.pk}/delete/")
        self.content = self.response.content.decode("utf-8")
        self.document = Document()
        self.document.feed(self.content)

    def test_todo_list_edit_resolves_to_todo_list_delete(self):
        path = reverse("todo_list_delete", args=[self.todolist.pk])
        self.assertEqual(
            path,
            f"/todos/{self.todolist.pk}/delete/",
            msg="Could not resolve path name 'todo_list_delete' to '/todos/<int:pk>/delete/'",
        )

    def test_todo_list_update_returns_200(self):
        self.assertEqual(
            self.response.status_code,
            200,
            msg="Did not get the delete todolist page",
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

    def test_form_has_button(self):
        form = self.document.select("html", "body", "main", "div", "form")
        buttons = form.get_all_children("button")
        found_button = None
        for button in buttons:
            if button.inner_text().strip().lower() == "delete":
                found_button = button
                break
        self.assertIsNotNone(
            found_button,
            msg="Could not find the 'Delete' button",
        )

    def test_todo_list_delete_works(self):
        todolist = TodoList.objects.create(name="TodoList 1")
        response = self.client.post(
            reverse("todo_list_delete", args=[todolist.pk])
        )
        with self.assertRaises(
            TodoList.DoesNotExist, msg="TodoList was not deleted"
        ):
            TodoList.objects.get(pk=todolist.pk)

    def test_delete_redirects_to_list(self):
        todolist = TodoList.objects.create(name="TodoList 2")
        response = self.client.post(
            reverse("todo_list_delete", args=[todolist.pk]),
        )
        self.assertEqual(
            response.headers.get("Location"),
            reverse("todo_list_list"),
            msg="Delete does not redirect to list view",
        )

    def test_list_view_has_link_to_delete(self):
        response = self.client.get(
            reverse("todo_list_detail", args=[self.todolist.pk])
        )
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        html = document.select("html")
        links = html.get_all_children("a")
        create_link = None
        for link in links:
            if link.attrs.get("href") == reverse(
                "todo_list_delete", args=[self.todolist.pk]
            ):
                create_link = link
                break
        self.assertIsNotNone(
            create_link,
            msg="Could not find the delete link for todos on the list view",
        )
