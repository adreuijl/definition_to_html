from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import ModelForm

# Create your models here.
class Concept(models.Model): 
    uri = models.CharField(max_length=100, blank=False)
    definition = models.CharField(max_length=100000, blank=True)
    prefLabel = models.CharField(max_length=100, blank=True)
    definitionNoHtml = models.CharField(max_length=10000, blank=True)
    definitionHtml = models.CharField(max_length=10000, blank=True)
    order = models.IntegerField(null=True)

    def _str_(self):
        return "Concept: {}".format(self.preflabel)

class UploadedConcept(models.Model): 
    uri = models.CharField(max_length=100, blank=False)
    definition = models.CharField(max_length=10000, blank=True)
    prefLabel = models.CharField(max_length=100, blank=True)
    related = models.CharField(max_length=10000, blank=True)

    def _str_(self):
        return "DefinitionToHtml: {}".format(self.subject)




""" class Match(models.Model):
    uri = models.CharField(max_length=100, blank=False)
    bevatLabel = models.CharField(max_length=100, blank=True)
    opBeginPositie = models.IntegerField(max_length=10, blank=False)
    vanLengte = models.IntegerField(max_length=10, blank=False) """

