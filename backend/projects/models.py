from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Client(models.Model):
    name = models.CharField("nombre", max_length=120)
    company = models.CharField("empresa", max_length=120, blank=True)
    email = models.EmailField("correo electrónico", unique=True)
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.name


class Project(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        IN_PROGRESS = "in_progress", "En progreso"
        COMPLETED = "completed", "Finalizado"

    class Priority(models.TextChoices):
        LOW = "low", "Baja"
        MEDIUM = "medium", "Media"
        HIGH = "high", "Alta"

    name = models.CharField("nombre", max_length=150)
    description = models.TextField("descripción", blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name="cliente",
    )
    start_date = models.DateField("fecha de inicio")
    due_date = models.DateField("fecha de entrega")
    status = models.CharField(
        "estado",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    priority = models.CharField(
        "prioridad",
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    manual_progress = models.PositiveSmallIntegerField(
        "progreso manual",
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Valor entre 0 y 100. Vacío para calcularlo automáticamente.",
    )
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("última actualización", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date and self.due_date and self.due_date < self.start_date:
            raise ValidationError(
                {"due_date": "La fecha de entrega no puede ser anterior al inicio."}
            )

    @property
    def calculated_progress(self):
        deliverables = self.deliverables.all()
        total = deliverables.count()

        if total == 0:
            return 0

        delivered = deliverables.filter(is_delivered=True).count()
        return round((delivered / total) * 100)

    @property
    def progress_percentage(self):
        if self.manual_progress is not None:
            return self.manual_progress

        return self.calculated_progress

    @property
    def is_overdue(self):
        return (
            self.status != self.Status.COMPLETED
            and self.due_date < timezone.localdate()
        )

    @property
    def display_status(self):
        if self.is_overdue:
            return "Atrasado"

        return self.get_status_display()


class Deliverable(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="deliverables",
        verbose_name="proyecto",
    )
    name = models.CharField("nombre", max_length=150)
    description = models.TextField("descripción")
    due_date = models.DateField("fecha límite")
    is_delivered = models.BooleanField("entregado", default=False)
    delivered_at = models.DateField("fecha de entrega real", null=True, blank=True)
    simulated_file = models.CharField(
        "archivo simulado",
        max_length=255,
        blank=True,
        help_text="Nombre o ruta simulada del archivo.",
    )
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)

    class Meta:
        ordering = ["due_date"]
        verbose_name = "entregable"
        verbose_name_plural = "entregables"

    def __str__(self):
        return f"{self.project.name} - {self.name}"

    def clean(self):
        if self.is_delivered and not self.delivered_at:
            raise ValidationError(
                {"delivered_at": "Debe indicar la fecha de entrega real."}
            )

        if not self.is_delivered and self.delivered_at:
            raise ValidationError(
                {"delivered_at": "Un entregable pendiente no puede tener fecha real."}
            )

    @property
    def is_overdue(self):
        return not self.is_delivered and self.due_date < timezone.localdate()


class ClientComment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="proyecto",
    )
    author = models.CharField("autor", max_length=120, default="Cliente")
    content = models.TextField("comentario")
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "comentario del cliente"
        verbose_name_plural = "comentarios del cliente"

    def __str__(self):
        return f"{self.author}: {self.project.name}"