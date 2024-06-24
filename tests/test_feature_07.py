from django.test import TestCase, Client

from .utils import Document
from todos.models import TodoList


class TestTodoListView(TestCase):
    def test_can_get_todos_urlpatterns(self):
        try:
            from todos.urls import urlpatterns  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find module 'todos.urls'")
        except ImportError:
            self.fail("Could not find 'todos.urls.urlpatterns'")

    def test_list_response_is_200(self):
        client = Client()
        response = client.get("/todos/")
        self.assertEqual(
            response.status_code,
            200,
            msg="Did not get a 200 OK for the path todos/",
        )

    def test_page_has_fundamental_five(self):
        client = Client()
        response = client.get("/todos/")
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        self.assertTrue(
            document.has_fundamental_five(),
            msg="The response did not have the fundamental five",
        )

    def test_list_html_has_main_tag(self):
        client = Client()
        response = client.get("/todos/")
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        self.assertIsNotNone(
            document.select("html", "body", "main"),
            msg="The response did not have a main tag as a direct child of the body",  # noqa: E501
        )

    def test_main_tag_has_a_div_tag(self):
        client = Client()
        response = client.get("/todos/")
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        self.assertIsNotNone(
            document.select("html", "body", "main", "div"),
            msg="The response did not have a div tag as a direct child of the main",  # noqa: E501
        )

    def test_div_tag_has_an_h1_tag_with_content_my_todos(self):
        client = Client()
        response = client.get("/todos/")
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        h1 = document.select("html", "body", "main", "div", "h1")
        self.assertIsNotNone(
            h1,
            msg="The response did not have an h1 tag as a direct child of the div",  # noqa: E501
        )
        self.assertIn(
            "My lists".lower(),
            h1.inner_text().lower(),
            msg="h1 did not have content 'My lists'",
        )

    def test_div_tag_has_a_table_with_headers_name_and_number(
        self,
    ):
        TodoList.objects.bulk_create(
            [
                TodoList(name="ZZZZZZ"),
            ]
        )
        client = Client()
        response = client.get("/todos/")
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        table = document.select("html", "body", "main", "div", "table")
        self.assertIsNotNone(
            table,
            msg="The response did not have a table tag as a direct child of the div",  # noqa: E501
        )
        self.assertIn(
            "name",
            table.inner_text().lower(),
            msg="table did not have 'Name' header in it",
        )
        self.assertIn(
            "number of items",
            table.inner_text().lower(),
            msg="table did not have 'Number of items' in it'",
        )

    def test_div_tag_has_a_table_tag_when_todos_exist_with_todolist_names(
        self,
    ):
        TodoList.objects.bulk_create(
            [
                TodoList(name="ZZZZZZ"),
                TodoList(name="YYYYYY"),
            ]
        )
        client = Client()
        response = client.get("/todos/")
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        table = document.select("html", "body", "main", "div", "table")
        self.assertIsNotNone(
            table,
            msg="The response did not have a table tag as a direct child of the div",  # noqa: E501
        )
        self.assertIn(
            "ZZZZZZ",
            table.inner_text(),
            msg="table did not have todolist name in it",
        )
        self.assertIn(
            "YYYYYY",
            table.inner_text(),
            msg="table did not have todolist name in it",
        )
