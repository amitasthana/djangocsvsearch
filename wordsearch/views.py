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
    lookup_url_kwarg = 's'

    def get(self,request,*args,**kwargs):
        searchword = self.kwargs['s']
        resultdict = {}
        namelist = []
        datalist = []
        with open(settings.FILES_ROOT + 'word_search.tsv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                namelist.append( row['name'])
                datalist.append( ( {'name':row['name'] } , {'frequency' : row['frequency']  }) )

        matching = [s for s in namelist if searchword in s]




        return Response(matching,status.HTTP_200_OK)
        





