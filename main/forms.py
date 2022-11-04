from django import forms
from django.forms import formset_factory

class EndpointForm(forms.Form):
    endpoint = forms.CharField(label='Endpoint', max_length=100)


class ConceptForm(forms.Form):
    uri = forms.CharField(label='uri', max_length=100)
    prefLabel = forms.CharField(label='prefLabel', max_length=100)
    definition = forms.CharField(label='definition', max_length=100)

ConceptFormSet = formset_factory(ConceptForm)

""" class ConceptForm(ModelForm):
    class Meta:
        model = UploadedConcept
        fields = ['uri', 'definition', 'prefLabel'] """