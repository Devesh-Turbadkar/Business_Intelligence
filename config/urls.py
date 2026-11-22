from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, dashboard_page
from products import analytics

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard_page, name="dashboard"),
    path("api/", include(router.urls)),
    path("api/analytics/summary/", analytics.summary, name="analytics-summary"),
    path("api/analytics/categories/", analytics.categories, name="analytics-categories"),
    path("api/analytics/top-rated/", analytics.top_rated, name="analytics-top-rated"),
    path("api/analytics/price-distribution/", analytics.price_distribution, name="price-distribution"),
    path("api/analytics/rating-distribution/", analytics.rating_distribution, name="rating-distribution"),
]
