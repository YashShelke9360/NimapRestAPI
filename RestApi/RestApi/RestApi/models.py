from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ClientProjects(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectUsers(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)





