from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from projects.models import Client, ClientComment, Deliverable, Project


class Command(BaseCommand):
    help = "Carga datos demostrativos para FreeWorks Dashboard."

    def handle(self, *args, **options):
        today = timezone.localdate()

        andes, _ = Client.objects.update_or_create(
            email="contacto@andes.cl",
            defaults={
                "name": "Constructora Andes",
                "company": "Constructora Andes SpA",
            },
        )
        turismo, _ = Client.objects.update_or_create(
            email="proyectos@turismopucon.cl",
            defaults={
                "name": "Turismo Pucón",
                "company": "Turismo Pucón Ltda.",
            },
        )
        nomade, _ = Client.objects.update_or_create(
            email="contacto@emporionomade.cl",
            defaults={
                "name": "Emporio Nómade",
                "company": "Emporio Nómade Coffee",
            },
        )

        website, _ = Project.objects.update_or_create(
            name="Rediseño sitio corporativo",
            client=andes,
            defaults={
                "description": (
                    "Renovación del sitio institucional y catálogo de servicios."
                ),
                "start_date": today - timedelta(days=25),
                "due_date": today + timedelta(days=15),
                "status": Project.Status.IN_PROGRESS,
                "priority": Project.Priority.HIGH,
                "manual_progress": None,
            },
        )

        reservations, _ = Project.objects.update_or_create(
            name="Sistema de reservas turísticas",
            client=turismo,
            defaults={
                "description": (
                    "Aplicación web para gestionar reservas y actividades."
                ),
                "start_date": today - timedelta(days=5),
                "due_date": today + timedelta(days=35),
                "status": Project.Status.PENDING,
                "priority": Project.Priority.MEDIUM,
                "manual_progress": 20,
            },
        )

        campaign, _ = Project.objects.update_or_create(
            name="Campaña digital de invierno",
            client=nomade,
            defaults={
                "description": (
                    "Diseño de piezas y estrategia digital para redes sociales."
                ),
                "start_date": today - timedelta(days=40),
                "due_date": today - timedelta(days=5),
                "status": Project.Status.COMPLETED,
                "priority": Project.Priority.LOW,
                "manual_progress": None,
            },
        )

        portal, _ = Project.objects.update_or_create(
            name="Portal de proveedores",
            client=andes,
            defaults={
                "description": (
                    "Portal para centralizar documentos y órdenes de compra."
                ),
                "start_date": today - timedelta(days=45),
                "due_date": today - timedelta(days=7),
                "status": Project.Status.IN_PROGRESS,
                "priority": Project.Priority.HIGH,
                "manual_progress": None,
            },
        )

        self.create_deliverable(
            website,
            "Wireframes",
            "Propuesta de estructura y navegación.",
            today - timedelta(days=10),
            True,
            today - timedelta(days=11),
            "wireframes-freeworks.pdf",
        )
        self.create_deliverable(
            website,
            "Diseño visual",
            "Diseño final de las pantallas principales.",
            today + timedelta(days=2),
            False,
            None,
            "diseno-visual.fig",
        )
        self.create_deliverable(
            website,
            "Versión publicada",
            "Compilación y publicación del sitio.",
            today + timedelta(days=15),
            False,
            None,
            "",
        )

        self.create_deliverable(
            reservations,
            "Levantamiento de requisitos",
            "Documento inicial de requisitos funcionales.",
            today + timedelta(days=5),
            False,
            None,
            "requisitos.docx",
        )
        self.create_deliverable(
            reservations,
            "Prototipo navegable",
            "Prototipo de las principales pantallas.",
            today + timedelta(days=18),
            False,
            None,
            "",
        )

        self.create_deliverable(
            campaign,
            "Propuesta gráfica",
            "Línea gráfica para la campaña.",
            today - timedelta(days=20),
            True,
            today - timedelta(days=21),
            "propuesta-grafica.pdf",
        )
        self.create_deliverable(
            campaign,
            "Piezas finales",
            "Entrega de publicaciones y formatos finales.",
            today - timedelta(days=6),
            True,
            today - timedelta(days=7),
            "piezas-finales.zip",
        )

        self.create_deliverable(
            portal,
            "Módulo de documentos",
            "Carga y clasificación de documentación.",
            today - timedelta(days=14),
            True,
            today - timedelta(days=15),
            "modulo-documentos.zip",
        )
        self.create_deliverable(
            portal,
            "Módulo de órdenes",
            "Gestión de órdenes de compra.",
            today - timedelta(days=8),
            False,
            None,
            "",
        )

        ClientComment.objects.get_or_create(
            project=website,
            author="María González",
            content="La propuesta visual refleja muy bien nuestra empresa.",
        )
        ClientComment.objects.get_or_create(
            project=reservations,
            author="Carlos Muñoz",
            content="Necesitamos destacar las actividades disponibles.",
        )
        ClientComment.objects.get_or_create(
            project=portal,
            author="María González",
            content="Favor priorizar el módulo de órdenes de compra.",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Datos demostrativos de FreeWorks cargados correctamente."
            )
        )

    def create_deliverable(
        self,
        project,
        name,
        description,
        due_date,
        is_delivered,
        delivered_at,
        simulated_file,
    ):
        Deliverable.objects.update_or_create(
            project=project,
            name=name,
            defaults={
                "description": description,
                "due_date": due_date,
                "is_delivered": is_delivered,
                "delivered_at": delivered_at,
                "simulated_file": simulated_file,
            },
        )