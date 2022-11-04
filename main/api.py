from rest_framework.generics import ListAPIView

from .serializers import ConceptSerializer, UploadedConceptSerializer
from .models import Concept, UploadedConcept

class ConceptApi(ListAPIView):
    queryset = Concept.objects.all()
    serializer_class = ConceptSerializer

class PostConceptApi(ListAPIView):
    queryset = UploadedConcept.objects.all()
    serializer_class = UploadedConceptSerializer