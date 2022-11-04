from rest_framework import serializers
from .models import Concept, UploadedConcept

class ConceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concept
        fields = '__all__'

class UploadedConceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedConcept
        fields = '__all__'

