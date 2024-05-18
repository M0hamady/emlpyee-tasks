from rest_framework import serializers
from .models import Project, Week, Task

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    project_owner = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'  # Include all default fields from the Task model

    def get_title(self, obj):
        # Assuming there is a user field in the Task model that relates to the User model
        return f'{obj.title} - {obj.week.project.title}' # or any other attribute of the User model
    def get_user(self, obj):
        # Assuming there is a user field in the Task model that relates to the User model
        return obj.week.project.owner.username  # or any other attribute of the User model

    def get_project_owner(self, obj):
        return obj.week.project.owner.username  # or any other attribute of the User model


class WeekSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Week
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    weeks = WeekSerializer(many=True, read_only=True)
    current_week = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_current_week(self,obj):
        return obj.get_last_finished_or_first_unfinished_week()
    
    def get_owner(self, obj):
        return obj.title  # or any other attribute of the User model

class ProjectDetailedSerializer(serializers.ModelSerializer):
    # This field will contain all tasks related to the project
    all_tasks = serializers.SerializerMethodField()

    weeks = WeekSerializer(many=True, read_only=True)
    current_week = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_current_week(self,obj):
        return obj.get_last_finished_or_first_unfinished_week()
    
    def get_owner(self, obj):
        return obj.title  # or any other attribute of the User model
    
    def get_all_tasks(self, obj):
        """
        This method returns all tasks associated with the project.
        """
        # Retrieve all weeks related to the project
        weeks = obj.week_set.all()
        # Initialize an empty list to collect all tasks
        all_tasks_list = []
        # Iterate over each week and collect its tasks
        for week in weeks:
            tasks = week.task_set.all()
            # Serialize the tasks and add them to the all_tasks_list
            all_tasks_list.extend(TaskSerializer(tasks, many=True).data)
        return all_tasks_list