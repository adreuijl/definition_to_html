from django.urls import path
from . import views
from .api import ConceptApi, PostConceptApi
app_name = "main"
urlpatterns = [
    path('api/postdefinition', views.uploadedconcept_add),
    path('conceptsapi/', ConceptApi.as_view()),
    path('concepts/', views.display_editable_definition, name = "concepts"),
    path('', views.home, name = "home"),
    path('maakmatch', views.makeNewDefinition, name = "maakmatch"),
    path('upload', views.upload, name = "upload"),
    path('endpoint', views.set_endpoint, name = "endpoint"),
    path('export', views.export_to_ttl, name = "export"),
    
]