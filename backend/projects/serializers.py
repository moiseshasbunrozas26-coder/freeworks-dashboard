from rest_framework import serializers

from .models import Client, ClientComment, Deliverable, Project


class ClientSerializer(serializers.ModelSerializer):
    project_count = serializers.IntegerField(
        source="projects.count",
        read_only=True,
    )

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "company",
            "email",
            "project_count",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "El nombre debe contener al menos 2 caracteres."
            )

        return value


class DeliverableSerializer(serializers.ModelSerializer):
    is_overdue = serializers.BooleanField(read_only=True)
    project_name = serializers.CharField(
        source="project.name",
        read_only=True,
    )

    class Meta:
        model = Deliverable
        fields = (
            "id",
            "project",
            "project_name",
            "name",
            "description",
            "due_date",
            "is_delivered",
            "delivered_at",
            "simulated_file",
            "is_overdue",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "is_overdue", "project_name")

    def validate(self, attrs):
        instance = getattr(self, "instance", None)

        is_delivered = attrs.get(
            "is_delivered",
            getattr(instance, "is_delivered", False),
        )
        delivered_at = attrs.get(
            "delivered_at",
            getattr(instance, "delivered_at", None),
        )

        if is_delivered and not delivered_at:
            raise serializers.ValidationError(
                {
                    "delivered_at": (
                        "Debe indicar la fecha cuando el entregable está completado."
                    )
                }
            )

        if not is_delivered and delivered_at:
            raise serializers.ValidationError(
                {
                    "delivered_at": (
                        "Un entregable pendiente no puede tener fecha de entrega."
                    )
                }
            )

        return attrs


class ClientCommentSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(
        source="project.name",
        read_only=True,
    )

    class Meta:
        model = ClientComment
        fields = (
            "id",
            "project",
            "project_name",
            "author",
            "content",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "project_name")

    def validate_content(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "El comentario debe contener al menos 3 caracteres."
            )

        return value


class ProjectSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        source="client",
        queryset=Client.objects.all(),
        write_only=True,
    )
    deliverables = DeliverableSerializer(many=True, read_only=True)
    comments = ClientCommentSerializer(many=True, read_only=True)
    status_label = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    priority_label = serializers.CharField(
        source="get_priority_display",
        read_only=True,
    )
    calculated_progress = serializers.IntegerField(read_only=True)
    progress_percentage = serializers.IntegerField(read_only=True)
    display_status = serializers.CharField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "client",
            "client_id",
            "start_date",
            "due_date",
            "status",
            "status_label",
            "priority",
            "priority_label",
            "manual_progress",
            "calculated_progress",
            "progress_percentage",
            "display_status",
            "is_overdue",
            "deliverables",
            "comments",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "calculated_progress",
            "progress_percentage",
            "display_status",
            "is_overdue",
        )

    def validate(self, attrs):
        instance = getattr(self, "instance", None)

        start_date = attrs.get(
            "start_date",
            getattr(instance, "start_date", None),
        )
        due_date = attrs.get(
            "due_date",
            getattr(instance, "due_date", None),
        )

        if start_date and due_date and due_date < start_date:
            raise serializers.ValidationError(
                {
                    "due_date": (
                        "La fecha de entrega no puede ser anterior al inicio."
                    )
                }
            )

        return attrs