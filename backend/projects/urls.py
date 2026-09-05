from rest_framework.routers import DefaultRouter

from .views import (
    ClientCommentViewSet,
    ClientViewSet,
    DeliverableViewSet,
    ProjectViewSet,
)

router = DefaultRouter()
router.register("clients", ClientViewSet, basename="client")
router.register("projects", ProjectViewSet, basename="project")
router.register("deliverables", DeliverableViewSet, basename="deliverable")
router.register("comments", ClientCommentViewSet, basename="comment")

urlpatterns = router.urls