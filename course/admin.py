from django.contrib import admin
from .models import Course, Task, Solution, File, Link

class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Course, CourseAdmin)
admin.site.register(Task)
admin.site.register(Solution)
admin.site.register(File)
admin.site.register(Link)