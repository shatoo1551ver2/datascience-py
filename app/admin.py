# app/admin.py

from django.contrib import admin
from .models import FileUpload,Post


admin.site.register(FileUpload)
admin.site.register(Post)
