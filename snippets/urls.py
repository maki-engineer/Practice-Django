from django.urls import path
from snippets import views
from rest_framework import routers

urlpatterns = [
  path("new/", views.snippet_new, name="snippet_new"),
  path("<int:snippet_id>/", views.snippet_detail, name="snippet_detail"),
  path("<int:snippet_id>/edit/", views.snippet_edit, name="snippet_edit"),
]

router = routers.DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)