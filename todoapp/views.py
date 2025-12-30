import requests
import json
from django.shortcuts import render, redirect

API_URL = "http://localhost:4000/"

def task_list(request):
    resp = requests.get(f"{API_URL}api/tasks")
    resp_data = resp.json()
    tasks=resp_data.get("data", {})
    print('tasks...',tasks)

    return render(request, "task_list.html", {"tasks": tasks})

def apidocumnets(request):
	return render(request,'apidocuments.html')
