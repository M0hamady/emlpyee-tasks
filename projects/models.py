from django.db import models
from clients.models import User
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_created_with_tasks =models.BooleanField(default=True)
    # Add more fields as needed
    
    
    
    
    def save(self, *args, **kwargs):
        # Call the original save method to ensure the project is saved
        super(Project, self).save(*args, **kwargs)
        # After saving, check if the project should be created with tasks
        if self.is_created_with_tasks and not self.week_set.exists():
            self.create_weeks_with_tasks()

            
    def get_last_finished_or_first_unfinished_week(self):
        """
        This method returns the last 'Week' instance associated with this project
        that has at least one finished task. If no such week exists, it returns the
        first 'Week' instance that has unfinished tasks.
        """
        # Get all weeks associated with this project
        weeks = self.week_set.all()
        # First, try to find the last finished week
        for week in weeks.order_by('-number'):
            if week.task_set.filter(is_finished=True).exists():
                return week.number
        # If no finished week, find the first week with unfinished tasks
        for week in weeks.order_by('number'):
            if week.task_set.filter(is_finished=False).exists():
                return week.number
        return 1 
    def create_weeks_with_tasks(self):
        """
        This method creates 10 weeks for the project, each with a predefined list of tasks.
        """
        tasks_for_weeks = {
            1: ['شراء ابواب الغرف', 'شراء السيراميك','3D تصميم','اختيار الالوان والدهانات النهائية','رفع مقاسات الالومنيوم'],
            2: ['task 1', 'task 2'],
            3: ['task 1', 'task 2'],
            4: ['task 1', 'task 2'],
            5: ['task 1', 'task 2'],
            6: ['task 1', 'task 2'],
            7: ['task 1', 'task 2'],
            8: ['task 1', 'task 2'],
            9: ['task 1', 'task 2'],
            10: ['task 1', 'task 2'],
            # ... add lists for weeks 3 to 10 ...
        }
        
        for week_number in range(1, 11):  # Create 10 weeks
            week = Week.objects.create(project=self, number=week_number)
            # Create tasks for the week
            for task_name in tasks_for_weeks.get(week_number, []):
                Task.objects.create(title=task_name, week=week)


class Week(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    number = models.PositiveIntegerField(default=1)
    # Add more fields as needed
    def __str__(self) :
        return f'{self.number}'
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    week = models.ForeignKey('Week', on_delete=models.SET_NULL, null=True)
    is_finished = models.BooleanField(default=False)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks')
    date_finished = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_finished and not self.date_finished:
            self.date_finished = timezone.now()
        self.date_updated = timezone.now()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    # Add more fields as needed