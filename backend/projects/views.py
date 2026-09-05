from django.db.models import Q
from django.utils import timezone
from rest_framework import status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Client, ClientComment, Deliverable, Project
from .serializers import (
    ClientCommentSerializer,
    ClientSerializer,
    DeliverableSerializer,
    ProjectSerializer,
)


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.prefetch_related("projects").all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search", "").strip()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(company__icontains=search)
                | Q(email__icontains=search)
            )

        return queryset


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = (
        Project.objects.select_related("client")
        .prefetch_related("deliverables", "comments")
        .all()
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        client = params.get("client")
        project_status = params.get("status")
        priority = params.get("priority")
        search = params.get("search", "").strip()

        if client:
            queryset = queryset.filter(client_id=client)

        if project_status == "overdue":
            queryset = queryset.filter(
                due_date__lt=timezone.localdate()
            ).exclude(status=Project.Status.COMPLETED)
        elif project_status:
            queryset = queryset.filter(status=project_status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(client__name__icontains=search)
                | Q(deliverables__name__icontains=search)
                | Q(deliverables__description__icontains=search)
            ).distinct()

        return queryset

    @action(detail=True, methods=["patch"], url_path="progress")
    def update_progress(self, request, pk=None):
        project = self.get_object()

        if "manual_progress" not in request.data:
            return Response(
                {"manual_progress": "Debe indicar un valor entre 0 y 100."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            project,
            data={"manual_progress": request.data["manual_progress"]},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        project = self.get_object()

        if "status" not in request.data:
            return Response(
                {"status": "Debe indicar el nuevo estado."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            project,
            data={"status": request.data["status"]},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        projects = self.filter_queryset(self.get_queryset())
        total = projects.count()

        pending = projects.filter(status=Project.Status.PENDING).count()
        in_progress = projects.filter(status=Project.Status.IN_PROGRESS).count()
        completed = projects.filter(status=Project.Status.COMPLETED).count()
        overdue = projects.filter(
            due_date__lt=timezone.localdate()
        ).exclude(status=Project.Status.COMPLETED).count()

        progress_values = [
            project.progress_percentage for project in projects
        ]
        average_progress = (
            round(sum(progress_values) / len(progress_values))
            if progress_values
            else 0
        )

        deliverables = Deliverable.objects.filter(project__in=projects)
        total_deliverables = deliverables.count()
        delivered = deliverables.filter(is_delivered=True).count()

        return Response(
            {
                "total_projects": total,
                "pending_projects": pending,
                "in_progress_projects": in_progress,
                "completed_projects": completed,
                "overdue_projects": overdue,
                "average_progress": average_progress,
                "total_deliverables": total_deliverables,
                "delivered_deliverables": delivered,
            }
        )

    @action(detail=False, methods=["get"])
    def notifications(self, request):
        overdue_deliverables = (
            Deliverable.objects.select_related("project", "project__client")
            .filter(
                is_delivered=False,
                due_date__lt=timezone.localdate(),
            )
            .order_by("due_date")
        )

        notifications = [
            {
                "id": deliverable.id,
                "type": "overdue_delivery",
                "message": (
                    f'El entregable "{deliverable.name}" del proyecto '
                    f'"{deliverable.project.name}" está atrasado.'
                ),
                "project_id": deliverable.project_id,
                "project_name": deliverable.project.name,
                "client_name": deliverable.project.client.name,
                "deliverable_name": deliverable.name,
                "due_date": deliverable.due_date,
                "days_overdue": (
                    timezone.localdate() - deliverable.due_date
                ).days,
            }
            for deliverable in overdue_deliverables
        ]

        return Response(
            {
                "count": len(notifications),
                "results": notifications,
            }
        )


class DeliverableViewSet(ModelViewSet):
    serializer_class = DeliverableSerializer
    queryset = Deliverable.objects.select_related("project").all()

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        project = params.get("project")
        delivered = params.get("delivered")
        overdue = params.get("overdue")
        search = params.get("search", "").strip()

        if project:
            queryset = queryset.filter(project_id=project)

        if delivered in {"true", "false"}:
            queryset = queryset.filter(is_delivered=delivered == "true")

        if overdue == "true":
            queryset = queryset.filter(
                is_delivered=False,
                due_date__lt=timezone.localdate(),
            )

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(project__name__icontains=search)
            )

        return queryset


class ClientCommentViewSet(ModelViewSet):
    serializer_class = ClientCommentSerializer
    queryset = ClientComment.objects.select_related("project").all()

    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get("project")

        if project:
            queryset = queryset.filter(project_id=project)

        return queryset