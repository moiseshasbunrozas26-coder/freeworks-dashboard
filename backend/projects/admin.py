from django.contrib import admin

from .models import Client, ClientComment, Deliverable, Project


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "created_at")
    search_fields = ("name", "company", "email")
    ordering = ("name",)


class DeliverableInline(admin.TabularInline):
    model = Deliverable
    extra = 0
    fields = (
        "name",
        "due_date",
        "is_delivered",
        "delivered_at",
        "simulated_file",
    )


class ClientCommentInline(admin.TabularInline):
    model = ClientComment
    extra = 0
    fields = ("author", "content", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "client",
        "priority",
        "display_project_status",
        "display_progress",
        "due_date",
    )
    list_filter = ("status", "priority", "client")
    search_fields = (
        "name",
        "description",
        "client__name",
        "deliverables__name",
    )
    date_hierarchy = "due_date"
    inlines = (DeliverableInline, ClientCommentInline)

    @admin.display(description="Estado")
    def display_project_status(self, obj):
        return obj.display_status

    @admin.display(description="Progreso")
    def display_progress(self, obj):
        return f"{obj.progress_percentage} %"


@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "due_date",
        "is_delivered",
        "display_overdue",
    )
    list_filter = ("is_delivered", "due_date")
    search_fields = ("name", "description", "project__name")

    @admin.display(boolean=True, description="Atrasado")
    def display_overdue(self, obj):
        return obj.is_overdue


@admin.register(ClientComment)
class ClientCommentAdmin(admin.ModelAdmin):
    list_display = ("project", "author", "created_at")
    search_fields = ("project__name", "author", "content")
    list_filter = ("created_at",)