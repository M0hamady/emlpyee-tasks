from django.contrib import admin
from .models import Project, Week, Task

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class WeekInline(admin.StackedInline):
    model = Week
    extra = 1
    inlines = [TaskInline]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    inlines = [WeekInline]

@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ('project', 'number')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'week')
    list_filter = ('week__project',)
    search_fields = ('title', 'description', 'week__project__title')

admin.site.site_header = 'Project Administration'
admin.site.site_title = 'Project Admin'