from django.contrib import admin

# Register your models here.
from .models import Concept, UploadedConcept

admin.site.register(Concept)
admin.site.register(UploadedConcept)