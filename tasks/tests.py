from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task
from .serializers import TaskSerializer
from django.http import HttpResponse

User = get_user_model()


class TaskModelTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.task = Task.objects.create(
            user=self.user,
            title="Sample Task",
            description="Test description"
        )

    def test_task_str(self):
        """__str__ should return the task title"""
        self.assertEqual(str(self.task), "Sample Task")

    def test_task_default_completed_false(self):
        """New tasks should default to not completed"""
        self.assertFalse(self.task.completed)

    def test_task_ordering(self):
        """Tasks should be ordered by title"""
        Task.objects.create(user=self.user, title="A Task", description="desc")
        tasks = Task.objects.all()
        self.assertEqual(tasks[0].title, "A Task")  # Ordered alphabetically


class TaskSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="serializer", password="testpass123")
        self.task = Task.objects.create(
            user=self.user, title="Serializer Task", description="desc"
        )

    def test_serializer_data(self):
        serializer = TaskSerializer(self.task)
        data = serializer.data
        self.assertEqual(data["title"], "Serializer Task")
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)


class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="testpass123")
        self.client = APIClient()
        self.client.login(username="apiuser", password="testpass123")

        self.task = Task.objects.create(
            user=self.user, title="API Task", description="API description"
        )

    def test_list_tasks(self):
        url = reverse("tasks:tasks-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        url = reverse("tasks:tasks-list")
        payload = {"user": self.user.id, "title": "New Task", "description": "Some text"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_retrieve_task(self):
        url = reverse("tasks:tasks-detail", args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "API Task")

    def test_update_task(self):
        url = reverse("tasks:tasks-detail", args=[self.task.id])
        payload = {"user": self.user.id, "title": "Updated Title", "description": "Updated desc"}
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Title")

    def test_delete_task(self):
        url = reverse("tasks:tasks-detail", args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class TaskCustomViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="custom", password="testpass123")
        self.client = APIClient()
        self.client.login(username="custom", password="testpass123")

        self.task1 = Task.objects.create(user=self.user, title="T1", description="d1", completed=True)
        self.task2 = Task.objects.create(user=self.user, title="T2", description="d2", completed=False)

    def test_my_tasks(self):
        url = reverse("tasks:my-tasks")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_task_detail(self):
        url = reverse("tasks:task-detail", args=[self.task1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "T1")

    def test_task_detail_not_found(self):
        url = reverse("tasks:task-detail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_completed_tasks(self):
        url = reverse("tasks:compleated")
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]["completed"])

    def test_incompleted_tasks(self):
        url = reverse("tasks:incompleated")
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertFalse(response.data[0]["completed"])


class ExportViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="exporter", password="testpass123")
        self.client = APIClient()
        self.client.login(username="exporter", password="testpass123")

        Task.objects.create(user=self.user, title="Done", description="desc", completed=True)
        Task.objects.create(user=self.user, title="Not Done", description="desc", completed=False)

    def test_export_csv(self):
        url = reverse("tasks:save-as-csv")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment; filename=", response["Content-Disposition"])

    def test_export_xls(self):
        url = reverse("tasks:save-as-xls")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/ms-excel")
        self.assertIn("attachment; filename=", response["Content-Disposition"])
