from django.shortcuts import redirect
from django.urls import path

# from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views.cart import CartViewSet
from .views.product import ProductViewSet
from .views.user import CustomUserViewSet

# router = DefaultRouter()
# router.register(r'', ManagerViewSet, basename='manager')

urlpatterns = [
    path("users/", CustomUserViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "users/<int:pk>/",
        CustomUserViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
                "put": "update",
                "patch": "partial_update",
            }
        ),
    ),
    # path('users/me/', ManagerViewSet.as_view({'get': 'me'})),
    path("accounts/login/", TokenObtainPairView.as_view(), name="login"),
    path("accounts/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("products/", ProductViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "products/<int:pk>",
        ProductViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
                "put": "update",
                "patch": "partial_update",
            }
        ),
    ),
    path("cart/", CartViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "cart/<int:product_id>",
        CartViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "patch": "partial_update"}
        ),
    ),
    # path('', include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", lambda request: redirect("swagger-ui")),
    path(
        route="v1/docs/",
        view=SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
