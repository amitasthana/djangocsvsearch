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
        searcedword = self.kwargs['s']


        result = {}
        resultarray = [ ]   


        with open(settings.FILES_ROOT + 'word_search.tsv', 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                makedict = { }
                if row[2] in result:
                    result[row[2]].append( float(row[1][1:]))
                    amount = sum(result[row[6]])
                else:
                    if row[1] != 'Order Amount':
                        result[row[2]] = [ float( row[1][1:] )]                 
    

        dictlist = []   

        objet = { }

        for key, value in result.items():
            temp = [key, sum(  value) ]     
            r = lambda: random.randint(0,255)
            color = '#%02X%02X%02X' % (r(),r(),r())
            temp_dict = { "color":color, "totalamount":sum ( value) }
            objet[key] = temp_dict





        dictthis = {"searcedword" : searcedword }
        return Response(dictthis,status.HTTP_200_OK)
        





