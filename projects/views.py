from rest_framework import viewsets
from .models import Project, Week, Task
from .serializers import ProjectDetailedSerializer, ProjectSerializer, WeekSerializer, TaskSerializer
from rest_framework import generics

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class WeekViewSet(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailedSerializer

    def get_object(self):
        # Override the method to fetch the project by its ID or any unique field
        project_id = self.kwargs.get('pk')  # 'pk' is the standard name for 'primary key' in Django URLs
        return Project.objects.get(id=project_id)