
import requests
import json
import pandas as pd
import lightrdf
import openpyxl
import re
import ast

from main.models import Concept, UploadedConcept
from pandas import json_normalize
from flatten_json import flatten
from pandas import DataFrame, concat
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from django.shortcuts import render
from rdflib import Graph, URIRef, Literal
from django.db.models.functions import Length
from django.http import HttpResponseRedirect
from .forms import EndpointForm, ConceptForm
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from main.serializers import UploadedConceptSerializer
from rdflib.namespace import SKOS, RDF
from pathlib import Path 

endpoint = "http://localhost:8083/tbl/graphql/begrippenkader_algemeen_politiewerk"

query = """ query {
    concepts {
        uri,
        prefLabel{string},
        definition {string}
    }
}"""


@api_view(['GET', 'POST', 'DELETE'])
def uploadedconcept_add(request):
    
    if request.method == 'GET':
        uploadedConcept = UploadedConcept.objects.all()
        uri = request.query_params.get('uri', None)
        print(uri)
        
        if uri is not None:
            uploadedConcept = uploadedConcept.filter(uri= uri)
        
        UploadedConcept_serializer = UploadedConceptSerializer(uploadedConcept, many=True)
        return JsonResponse(UploadedConcept_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        UploadedConcept_data = JSONParser().parse(request)
        UploadedConcept_serializer = UploadedConceptSerializer(data=UploadedConcept_data)

        if UploadedConcept_serializer.is_valid():
            UploadedConcept_serializer.save()
            makeNewDefinition(request)
            return JsonResponse(UploadedConcept_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(UploadedConcept_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = UploadedConcept.objects.all().delete()
        return JsonResponse({'message': '{} Concepts were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
def count_space(Test_string):
    return Test_string.count(" ")

def makeNewDefinition(request):
    '''
    all_concepts = Concept.objects.all().order_by(Length('prefLabel').asc())
    uploaded_concepts = UploadedConcept.objects.all().order_by(Length('prefLabel').asc())
    
    dataframe_all = pd.DataFrame(columns = ['uri'])
    for i in all_concepts:
        flat = flatten_json(i)
        df_data = json_normalize(flat)
        df = pd.DataFrame(df_data) 
        dataframe_all = pd.concat([dataframe_all, df], ignore_index = True)
    '''
    #df = df.dropna()
    table = Concept.objects.all().order_by('-order')
    for row1 in table:
        #preflabel = ast.literal_eval(row1.prefLabel)
        preflabel = row1.prefLabel
        teVindenLabel = ""
        try:
            #preflabel_first=preflabel[0]
            #print(preflabel[0]['string'].lower())
            #teVindenLabel = preflabel[0]['string'].lower()
            teVindenLabel = preflabel
        except:
            pass
        
          
        uri_TeVindenLabel = row1.uri
 
        for row2 in UploadedConcept.objects.all():
            definition_first = row2.definition
            #print(definition_first)
            if(uri_TeVindenLabel == row2.uri):
                x=1
            else:
                try:
                    if (isinstance(teVindenLabel, str) and isinstance(definition_first, str) ):
                        positie = definition_first.lower().find(teVindenLabel.lower())
                        if(positie != -1):
                            uri = row2.uri
                            definitie = definition_first

                            match = {'uri_TeVindenLabel': uri_TeVindenLabel, 'teVindenLabel': teVindenLabel , 'uri': uri ,'positie':positie, 'definitie': definitie }
                            #print(match)
                            gevonden_concept = UploadedConcept.objects.get(uri = match['uri'])
                            if gevonden_concept :
                                try:
                                    definition = gevonden_concept.definition
                                   
                                   # definition = definition.lower()
                                    #definition = definition.replace((' '+match['teVindenLabel'].lower() + ' ') , ' <a href=\"' +match['uri_TeVindenLabel'].lower() + '\" target=\"_blank\" rel=\"noopener\">' + match['teVindenLabel'] + '</a> ')
                                   # definition = definition.replace((' '+match['teVindenLabel'].lower() + '.') , ' <a href=\"' +match['uri_TeVindenLabel'].lower() + '\" target=\"_blank\" rel=\"noopener\">' + match['teVindenLabel']  + '</a>.')
                                    #definition = definition.replace((' '+match['teVindenLabel'].lower() + ',') , ' <a href=\"' +match['uri_TeVindenLabel'].lower() + '\" target=\"_blank\" rel=\"noopener\">' + match['teVindenLabel']  + '</a>,')

                            
                                    hello =  "\s" + match['teVindenLabel']+ "\s" 
                                    hello2 = "\s" + match['teVindenLabel']+ "[.]" 
                                    hello3 = "\s" + match['teVindenLabel']+ "[,]" 
                                    print ('hello =' + hello)
                                    bye =  (' <a href=\"' +match['uri_TeVindenLabel'].lower() + '\" target=\"_blank\" rel=\"noopener\">' + match['teVindenLabel'] + '</a> ')
                                    bye2 =  (' <a href=\"' +match['uri_TeVindenLabel'].lower() + '\" target=\"_blank\" rel=\"noopener\">' + match['teVindenLabel'] + '</a>. ')
                                    bye3 =  (' <a href=\"' +match['uri_TeVindenLabel'].lower() + '\" target=\"_blank\" rel=\"noopener\">' + match['teVindenLabel'] + '</a>, ')
                                    print ('bye =' + bye)
                                    
                                    definition2 = re.sub(hello, bye, definition,flags=re.IGNORECASE )
                                    definition3 = re.sub(hello2, bye2, definition2,flags=re.IGNORECASE )
                                    definition4 = re.sub(hello3, bye3, definition3,flags=re.IGNORECASE )
                                      

                                    gevonden_concept.definition = definition4 
                                    gevonden_concept.save(update_fields=['definition'])
                                except: 
                                    print("een fout bij het maken van de niewe definitie")

                except  Exception as e:
                    print(e)

    return render(request, 'concepts/home.html') 


""" 
def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out """


#deze functie neemt een string waar vermoedelijk html in zit, test deze op html en als die er in zit haalt hij de text eruit
def remove_html(y):
    out = ""
    try:
        if bool(BeautifulSoup(y, "html.parser").find()) :
                out = BeautifulSoup(y, "html.parser").get_text()
        else:
            out = y 
    except:
        print ("fout bij html")
    return out

#deze functie neemt een string en test of er html in zit, als dat er niet in zit voegt hij de div tags toe.
def make_html(y):
    out = ""
    try:
        if bool(BeautifulSoup(y, "html.parser").find()) :
            out = y
        else:
            out = '<div lang="nl">' + y + '</div>'
    except:
        print("fout by html maken")
    return out
 


def getConcepts ():
    #all_concepts = {}
    response = requests.post(endpoint, json={'query': query})
    json_data = json.loads(response.text)
    concepts = json_data['data']['concepts']
    
    #dataframe_all = pd.DataFrame(columns = ['uri'])

    Concept.objects.all().delete()
    for i in concepts:
        print(i)
        definitionNoHtml = ""
        definitionHtml = ""
        try: 
            definition = i['definition'][0]['string']
            definitionNoHtml = remove_html(definition)
            definitionHtml = make_html(definition)
        except: 
            print ("geen def aanwezig")
        
        order = 0
        preflabel = ""
        try:
            preflabel = i['prefLabel'][0]['string']
            order = count_space(preflabel)
        except: 
            print("geen label")
       
        concept_data = Concept(
            uri = i['uri'],
            #prefLabel = i['prefLabel'],
            prefLabel = preflabel,
            definition = i['definition'],
            definitionNoHtml = definitionNoHtml,
            definitionHtml = definitionHtml,
            order = order
        )

        concept_data.save()
        #Concept.objects.all().order_by(Length('prefLabel').asc())


     #   flat = flatten_json(i)
    #    df_data = json_normalize(flat)
    #    df = pd.DataFrame(df_data)    
     #   dataframe_all = pd.concat([dataframe_all, df], ignore_index = True)

    #makeNewDefinition(dataframe_all)
    return
    #return render(request, 'concepts/concept.html', {"all_concepts": all_concepts})

def showConcepts (request):
    all_concepts = {}
    all_concepts = UploadedConcept.objects.all().order_by('prefLabel')
    print(all_concepts)        
    form = EndpointForm(request.POST)
    #definition = form.data['definition']
    
    #getConcepts()
    if form.is_valid():
        pass
    else:
        form = EndpointForm()

    return render(request, 'concepts/concept.html', {"all_concepts": all_concepts})


def upload (request):
    if "GET" == request.method:
        return render(request, 'concepts/upload.html', {})
    else:
        ttl_file = request.FILES["file"]
        graph = Graph()
        graph.parse(ttl_file, format='ttl')
        turtle_data = list()
        for stmt in graph: 
            row_data = stmt
            turtle_data.append(row_data)
        file_to_database (turtle_data)
        return render(request, 'concepts/upload.html')


def file_to_database (ttllist):
    UploadedConcept.objects.all().delete()
    for row in ttllist:
        for triple in row:
            if triple == URIRef('http://www.w3.org/2004/02/skos/core#definition'):
                try:
                    UploadedConcept.objects.get(uri = row[0])
                except UploadedConcept.DoesNotExist:
                    uri = row[0]
                    definition = make_html(row[2])
                    concept_data = UploadedConcept(
                    uri = uri,
                    definition = definition
                    )
                    concept_data.save()  
                else :
                    try:
                        UploadedConcept.objects.get(definition = row[2])
                    except :

                        definition = make_html(row[2])
                        concept_data = UploadedConcept.objects.get(uri = row[0])
                        concept_data.definition = definition
                        concept_data.save(update_fields=['definition'])
                    else:
                        #definitie is gelijk, dus doe niks of update de rij met dezelfde gegevens
                        definition = make_html(row[2])
                        concept_data = UploadedConcept.objects.get(uri = row[0])
                        concept_data.definition = definition
                        concept_data.save(update_fields=['definition'])

            else:
                if triple == URIRef('http://www.w3.org/2004/02/skos/core#prefLabel'):
                    try:
                        UploadedConcept.objects.get(uri= row[0])
                    except UploadedConcept.DoesNotExist:
                        uri = row[0]
                        label = row[2]
                        concept_data = UploadedConcept(
                        uri = uri,
                        prefLabel = label
                        )
                        concept_data.save()
                    else :
                        label = row[2]
                        concept_data = UploadedConcept.objects.get(uri = row[0])
                        concept_data.prefLabel = label
                        concept_data.save(update_fields=['prefLabel'])

    return 



def set_endpoint(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
       
        form = EndpointForm(request.POST)
        global endpoint 
        endpoint = form.data['endpoint']
        getConcepts()
        if form.is_valid():
            
            pass

    else:
        form = EndpointForm()

    return render(request, 'concepts/endpoint.html', {'form': form})


def display_editable_definition(request):
    all_concepts = UploadedConcept.objects.all().order_by('prefLabel')
    if request.method == 'POST':
        form = ConceptForm(request.POST)
        # create a form instance and populate it with data from the request:
        print('Form data def: ' + form.data['definition'])
        #print('Form data : ' +  form.data['prefLabel'])
        test = form.data['uri']
        
        definition =form.data['definition']

        gevonden_concept = UploadedConcept.objects.get(uri = test)                
        gevonden_concept.definition = definition 
        gevonden_concept.save(update_fields=['definition'])
        
        
        
        if form.is_valid():
            pass
    else:
        form = all_concepts
    form = all_concepts
    return render(request, 'concepts/concept.html', {'form': form})




def home(request):
    return render(request, 'concepts/home.html') 



def export_to_ttl(request):
    data = UploadedConcept.objects.all()
    form = UploadedConcept.objects.all().order_by('prefLabel')
    g = Graph()
    for row in data:

        g.add( (URIRef(row.uri), SKOS.definition, Literal(row.definition,  datatype=RDF.HTML)) )
    
    g.serialize(destination=str(Path.home() / "Downloads" / "export.ttl"), format='ttl')

    return render(request, 'concepts/concept.html', {'form': form})