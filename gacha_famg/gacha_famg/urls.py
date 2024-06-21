from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-bZ5Myf3Z/', admin.site.urls),
    path('', include("finance.urls")),
]
