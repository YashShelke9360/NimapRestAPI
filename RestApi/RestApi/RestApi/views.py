import json
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *


@login_required
def client(request, id=None):
    if request.method == "GET":
        if id is not None:
            client = Client.objects.filter(id=id).get()
            projects = []
            for client_project in ClientProjects.objects.filter(client=client):
                projects.append({
                    "id": client_project.project.id,
                    "project_name": client_project.project.project_name
                })
            return HttpResponse(json.dumps({
                "id": int(client.id),
                "client_name": str(client.client_name),
                "projects": projects,
                "created_at": str(client.created_at),
                "created_by": str(client.created_by),
            }), content_type="application/json")
        else:
            clients = []
            for client in Client.objects.all():
                clients.append({
                    "id": int(client.id),
                    "client_name": str(client.client_name),
                    "created_at": str(client.created_at),
                    "created_by": str(client.created_by),
                })
            return HttpResponse(json.dumps(clients), content_type="application/json")
    elif request.method == "POST":
        data = json.loads(request.body)
        client = Client.objects.create(client_name=data["client_name"], created_by=request.user)
        client.save()
        return HttpResponse(json.dumps({
            "id": int(client.id),
            "client_name": str(client.client_name),
            "created_at": str(client.created_at),
            "created_by": str(client.created_by),
        }), content_type="application/json")
    elif request.method == "DELETE":
        client = Client.objects.filter(id=id).get()
        client.delete()
        return HttpResponse(status=204)
    elif request.method in ["PUT", "PATCH"]:
        data = json.loads(request.body)
        client = Client.objects.filter(id=id).get()
        client.client_name = data["client_name"]
        client.save()
        return HttpResponse(json.dumps({
            "id": int(client.id),
            "client_name": str(client.client_name),
            "created_at": str(client.created_at),
            "created_by": str(client.created_by),
        }), content_type="application/json")
    else:
        return HttpResponse("405 - Method Not allowed", status=405)


@login_required
def project(request, id=None):
    if request.method == "GET":
        projects = []
        for project_user in ProjectUsers.objects.filter(user=request.user):
            projects.append({
                "id": int(project_user.project.id),
                "project_name": str(project_user.project.project_name),
                "created_at": str(project_user.project.created_at),
                "created_by": str(project_user.project.created_by)
            })
        return HttpResponse(json.dumps(projects), content_type="application/json")
    elif request.method == "POST":
        data = json.loads(request.body)
        client = Client.objects.filter(id=id).get()
        project = Project.objects.create(project_name=data["project_name"], created_by=request.user)
        project.save()
        clientProject = ClientProjects.objects.create(project=project, client=client)
        clientProject.save()
        users = []
        for user in data["users"]:
            projectUsers = ProjectUsers.objects.create(project=project, user=User.objects.filter(id=user["id"]).get())
            projectUsers.save()
            users.append({
                "id": int(projectUsers.user.id),
                "name": str(projectUsers.user.username)
            })
        return HttpResponse(json.dumps({
            "id": int(project.id),
            "project_name": str(project.project_name),
            "client": str(client.client_name),
            "users": users,
            "created_at": str(project.created_at),
            "created_by": str(project.created_by)
        }), content_type="application/json")
    else:
        return HttpResponse("405 - Method Not allowed", status=405)