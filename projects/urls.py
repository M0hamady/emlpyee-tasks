from django.urls import include, path
from rest_framework import routers
from .views import ProjectDetailView, TaskViewSet, ProjectViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    # Other URL patterns
    path('api/projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('api/', include(router.urls)),

]