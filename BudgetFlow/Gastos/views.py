from .models import Despesa,Receita
from Gastos.serializers import DespesaSerializer,ReceitaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_HEADER

class AdicionaDespesaView(APIView):
    def post(self,request):
        serializer = DespesaSerializer(data = request.data)
        if serializer.is_valid():
            



