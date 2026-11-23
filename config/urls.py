from django.contrib import admin
from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class LoginView(TokenObtainPairView):
    # El login solo pide credenciales (usuario/contraseña); la clave API no se exige aquí.
    permission_classes = (AllowAny,)


class RefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", RefreshView.as_view(), name="token_refresh"),
    path("api/", include("api.urls")),
]
