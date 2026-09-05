from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Client, ClientComment, Deliverable, Project


class ProjectAPITests(APITestCase):
    def setUp(self):
        today = timezone.localdate()

        self.client_record = Client.objects.create(
            name="Cliente Demo",
            company="FreeWorks",
            email="cliente@freeworks.cl",
        )

        self.project = Project.objects.create(
            name="Landing corporativa",
            description="Diseño y desarrollo del sitio web",
            client=self.client_record,
            start_date=today - timedelta(days=20),
            due_date=today - timedelta(days=2),
            status=Project.Status.IN_PROGRESS,
            priority=Project.Priority.HIGH,
        )

        self.pending_deliverable = Deliverable.objects.create(
            project=self.project,
            name="Diseño final",
            description="Entrega del diseño aprobado",
            due_date=today - timedelta(days=3),
            simulated_file="diseno-final.fig",
        )

        self.completed_deliverable = Deliverable.objects.create(
            project=self.project,
            name="Wireframes",
            description="Wireframes iniciales",
            due_date=today - timedelta(days=10),
            is_delivered=True,
            delivered_at=today - timedelta(days=11),
            simulated_file="wireframes.pdf",
        )

        ClientComment.objects.create(
            project=self.project,
            author="Cliente Demo",
            content="El diseño está avanzando correctamente.",
        )

    def test_list_projects_includes_calculated_fields(self):
        response = self.client.get(reverse("project-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        project = response.data["results"][0]
        self.assertEqual(project["progress_percentage"], 50)
        self.assertEqual(project["display_status"], "Atrasado")
        self.assertTrue(project["is_overdue"])
        self.assertEqual(len(project["deliverables"]), 2)
        self.assertEqual(len(project["comments"]), 1)

    def test_filter_projects_by_client_status_and_priority(self):
        response = self.client.get(
            reverse("project-list"),
            {
                "client": self.client_record.id,
                "status": "overdue",
                "priority": Project.Priority.HIGH,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_search_project_by_deliverable_name(self):
        response = self.client.get(
            reverse("project-list"),
            {"search": "Wireframes"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_project_statistics(self):
        response = self.client.get(reverse("project-statistics"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_projects"], 1)
        self.assertEqual(response.data["in_progress_projects"], 1)
        self.assertEqual(response.data["overdue_projects"], 1)
        self.assertEqual(response.data["average_progress"], 50)
        self.assertEqual(response.data["total_deliverables"], 2)
        self.assertEqual(response.data["delivered_deliverables"], 1)

    def test_overdue_notifications(self):
        response = self.client.get(reverse("project-notifications"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["deliverable_name"],
            "Diseño final",
        )
        self.assertGreater(
            response.data["results"][0]["days_overdue"],
            0,
        )

    def test_update_manual_progress(self):
        response = self.client.patch(
            reverse(
                "project-update-progress",
                args=[self.project.id],
            ),
            {"manual_progress": 75},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["progress_percentage"], 75)

        self.project.refresh_from_db()
        self.assertEqual(self.project.manual_progress, 75)

    def test_reject_invalid_manual_progress(self):
        response = self.client.patch(
            reverse(
                "project-update-progress",
                args=[self.project.id],
            ),
            {"manual_progress": 150},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_project_status(self):
        response = self.client.patch(
            reverse(
                "project-update-status",
                args=[self.project.id],
            ),
            {"status": Project.Status.COMPLETED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], Project.Status.COMPLETED)
        self.assertEqual(response.data["display_status"], "Finalizado")

    def test_reject_project_with_invalid_dates(self):
        today = timezone.localdate()

        response = self.client.post(
            reverse("project-list"),
            {
                "name": "Proyecto inválido",
                "description": "Prueba de validación",
                "client_id": self.client_record.id,
                "start_date": today,
                "due_date": today - timedelta(days=1),
                "status": Project.Status.PENDING,
                "priority": Project.Priority.MEDIUM,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("due_date", response.data)