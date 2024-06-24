from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .utils import Document
from todos.models import TodoList, TodoItem


class TestTodoListDetailView(TestCase):
    def setUp(self):
        self.client = Client()
        self.todolist = TodoList.objects.create(name="ZZZZZZ")

    def test_todolist_detail_returns_200(self):
        path = reverse("todo_list_detail", args=[self.todolist.id])
        response = self.client.get(path)
        self.assertEqual(
            response.status_code,
            200,
            msg="Did not get a 200 for todolist details",
        )

    def test_todolist_detail_shows_title(self):
        path = reverse("todo_list_detail", args=[self.todolist.id])
        response = self.client.get(path)
        document = Document()
        document.feed(response.content.decode("utf-8"))
        html = document.select("html")
        self.assertIn(
            "ZZZZZZ",
            html.inner_text(),
            msg="Did not find the todolist name on the page",
        )

    def test_todolist_detail_with_a_todoitem_shows_item_task(self):
        todoitem = TodoItem.objects.create(
            task="YYYYYY", due_date=timezone.now(), list=self.todolist
        )
        path = reverse("todo_list_detail", args=[self.todolist.id])
        response = self.client.get(path)
        document = Document()
        document.feed(response.content.decode("utf-8"))
        html = document.select("html")
        self.assertIn(
            todoitem.task,
            html.inner_text(),
            msg="Did not find the todoitem task in the detail page",
        )

    def test_todolist_detail_with_a_todoitem_shows_due_date(self):
        todoitem = TodoItem.objects.create(
            task="YYYYYY", due_date=timezone.now(), list=self.todolist
        )
        path = reverse("todo_list_detail", args=[self.todolist.id])
        response = self.client.get(path)
        document = Document()
        document.feed(response.content.decode("utf-8"))
        html = document.select("html")
        self.assertIn(
            str(todoitem.due_date.year),
            html.inner_text(),
            msg="Did not find the todoitem due date in the detail page",
        )

    def test_todolist_detail_with_a_tasks_shows_task_header(self):
        TodoItem.objects.create(
            task="YYYYYY",
            due_date=timezone.now(),
            list=self.todolist,
        )
        path = reverse("todo_list_detail", args=[self.todolist.id])
        response = self.client.get(path)
        document = Document()
        document.feed(response.content.decode("utf-8"))
        html = document.select("html")
        self.assertIn(
            "task",
            html.inner_text().lower(),
            msg="Did not find the header 'Task' in the detail page",
        )

    def test_todolist_detail_with_a_todoitem_shows_due_date_header(self):
        TodoItem.objects.create(
            task="YYYYYY", due_date=timezone.now(), list=self.todolist
        )
        path = reverse("todo_list_detail", args=[self.todolist.id])
        response = self.client.get(path)
        document = Document()
        document.feed(response.content.decode("utf-8"))
        html = document.select("html")
        self.assertIn(
            "due date",
            html.inner_text().lower(),
            msg="Did not find the header 'Due date' in the detail page",
        )

    def test_todolist_list_has_link_to_todolist(self):
        path = reverse("todo_list_list")
        todolist_path = reverse("todo_list_detail", args=[self.todolist.id])
        response = self.client.get(path)
        document = Document()
        document.feed(response.content.decode("utf-8"))
        html = document.select("html")
        children = html.get_all_children("a")
        detail_link = None
        for child in children:
            if child.attrs.get("href") == todolist_path:
                detail_link = child
                break
        self.assertIsNotNone(
            detail_link,
            msg="Did not find the detail link for the todolist in the page",
        )
