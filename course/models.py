from django.conf import settings
from account.models import User
from django.db import models
from uuid import uuid4
import os


class File(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    owner = models.ForeignKey(User, related_name="files", on_delete=models.CASCADE, null=True, blank=True)
    solution = models.ForeignKey("Solution", related_name="attached_files", on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT, "files"))

    def __str__(self):
        return f"{self.owner.email}"
    
    class Meta:
        verbose_name = 'файл'
        verbose_name_plural = 'файлы'

class Link(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    owner = models.ForeignKey(User, related_name="links", on_delete=models.CASCADE, null=True, blank=True)
    solution = models.ForeignKey("Solution", related_name="attached_links", on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=256, blank=True)
    
    def __str__(self):
        return f"{self.owner.email}"
    
    class Meta:
        verbose_name = 'ссылка'
        verbose_name_plural = 'ссылки'

class Solution(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    owner = models.ForeignKey(User, related_name="solutions", on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey("Task", related_name="solutions", on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    grade = models.IntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.owner.email}"
    
    class Meta:
        verbose_name = 'решение'
        verbose_name_plural = 'решения'

class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    course = models.ForeignKey("Course", related_name="tasks", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=32)
    description = models.TextField(default="", max_length=4096)
    higher_grade = models.IntegerField(default=5)
    closing_at = models.DateTimeField(default=None, null=True, blank=True)
    accept_after_closing = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.uuid} {self.name}"
    
    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'

class Course(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    name = models.CharField(max_length=32)
    description = models.TextField(default="", max_length=4096)
    owners = models.ManyToManyField(User, related_name="owner_of_courses", blank=True)
    teachers = models.ManyToManyField(User, related_name="teacher_of_courses", blank=True)
    students = models.ManyToManyField(User, related_name="student_of_courses", blank=True)
    observers = models.ManyToManyField(User, related_name="observer_of_courses", blank=True)
    user_query = models.ManyToManyField(User, related_name="in_user_query_of_courses", blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.uuid} {self.name}"
    
    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'