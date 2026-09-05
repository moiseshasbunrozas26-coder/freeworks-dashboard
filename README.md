# FreeWorks Dashboard

Aplicación web para la gestión de proyectos freelance, clientes, entregables y comentarios. Incluye un dashboard visual con estadísticas, filtros, búsqueda, alertas y seguimiento del avance de cada proyecto.

## Autor

**Alex Hasbún Rozas**

Proyecto desarrollado como evaluación académica utilizando Django REST Framework, Angular y Docker.

## Funcionalidades

- Gestión de proyectos.
- Creación y edición de proyectos.
- Eliminación de proyectos con confirmación.
- Registro de clientes.
- Registro de entregables.
- Registro de comentarios de clientes.
- Seguimiento manual del progreso.
- Cálculo automático del avance según entregables completados.
- Cambio manual del estado de cada proyecto.
- Detección de proyectos y entregables atrasados.
- Estadísticas generales del portafolio.
- Notificaciones de entregas vencidas.
- Búsqueda por proyecto o entregable.
- Filtros por cliente, estado y prioridad.
- Diseño profesional y responsive.
- API REST paginada.
- Datos demostrativos.
- Pruebas automatizadas.
- Ejecución local o mediante Docker Compose.

## Tecnologías

### Backend

- Python 3.12
- Django 5.2
- Django REST Framework
- django-cors-headers
- Gunicorn
- SQLite

### Frontend

- Angular 21
- TypeScript
- SCSS
- Reactive Forms
- RxJS
- Nginx

### Infraestructura

- Git y GitHub
- Docker
- Docker Compose

## Arquitectura

```text
freeworks-dashboard/
├── backend/
│   ├── config/
│   ├── projects/
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   └── app/
│   │       ├── core/
│   │       ├── features/
│   │       └── shared/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md