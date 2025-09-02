from todos.views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'todo', TodoViewSet)


urlpatterns = router.urls
