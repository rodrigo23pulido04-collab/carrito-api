from rest_framework.routers import DefaultRouter

from .views import ComponenteViewSet, HistorialDecisionViewSet, TiempoReaccionViewSet

router = DefaultRouter()
router.register("componentes", ComponenteViewSet, basename="componente")
router.register("historial-decisiones", HistorialDecisionViewSet, basename="historial-decision")
router.register("tiempos-reaccion", TiempoReaccionViewSet, basename="tiempo-reaccion")

urlpatterns = router.urls
