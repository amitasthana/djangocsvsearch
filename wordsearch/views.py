from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
import csv
from pprint import pprint
import difflib
import re
from nltk import FreqDist

# Create your views here.

class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = ((AllowAny,))

    def post(self, request, *args, **kwargs):

        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        
        token = Token.objects.get(key=response.data['token'])
        
        uid=token.user_id
        print('user id is ',uid)
     
        return Response({ 
                    'token': token.key, 
                    'id': token.user_id,
                })



class WordSearch(APIView):
    """docstring for WordSearch"""
    permission_classes = ((AllowAny,))
    objectify = True
    
    def get(self,request,*args,**kwargs):
        word = request.GET['word']    
        searchword = word
        resultdict = {}
        namelist = []
        datalist = []
        text1 = []

        #reading the file and taking it in the array
        with open(settings.FILES_ROOT + 'word_search.tsv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                datalist.append( ( {'name':row['name'] , 'frequency' : int(  row['frequency'] ) }) )

        
        #creating a sorted list as per the frequency        
        newlist = sorted(datalist, key=lambda k: k['frequency'], reverse=True) 
        
        #just taking the sorted list which sorted by frequency in namelist
        for f in newlist:
            namelist.append(f['name'])


        #Doing the searching of the word in the list which is sorted by frequency    
        matching = [s for s in namelist if searchword in s]

        #in the mathing now finding the elements which start with the search word
        result_startwith = list(  filter(lambda x: x.startswith(searchword), matching))
        sortlist = sorted ( result_startwith)        
        
        #creating a array which excludes all the elements which starts with the search word
        l3 = set(  matching ) - set(  list(result_startwith ) )
        

        #creating a new list first part is the list which is sorted by the starting of the search word
        #Taking only 25 elemets form the new list            
        mergedlist = (  sortlist + list(l3) )[:25]    
            
        #sending in response the first 25 results
        return Response(mergedlist,status.HTTP_200_OK)
        





