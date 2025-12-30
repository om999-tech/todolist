import os
import django
from django.core.asgi import get_asgi_application
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware.cors import CORSMiddleware
from api.main import app as fastapi_app

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todolist.settings")
django.setup()

django_asgi_app = get_asgi_application()


#-------------CORS-----------
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#-------------Mount apps--------------
main_app = Starlette(routes=[
    Mount("/api", app=fastapi_app),   # FastAPI routes
    Mount("/", app=django_asgi_app),  # Django frontend
])
