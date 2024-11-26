from django.contrib.auth.models import User
from Login.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout 
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_HEADER
from rest_framework.authtoken.models import Token


class LoginView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description=__doc__,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nome de usuário'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuário')
            },
            required=['username', 'password'],
        ),
        responses={
            200: openapi.Response(
                description="Usuário autenticado e logado com sucesso.",
                example={
                    'success': 'Usuário autenticado e logado com sucesso',
                    'token': 'auth_token'
                }
            ),
            400: openapi.Response(
                description="Credenciais inválidas.",
                example={
                    'error': 'Credenciais inválidas'
                }
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Lidar com requisição POST para autenticar e logar o usuário.

        Este método autentica o usuário com o nome de usuário e senha fornecidos,
        e loga o usuário se as credenciais forem válidas. Se a autenticação for bem-sucedida,
        um token de autenticação é retornado.

        :param request: Objeto de requisição HTTP contendo o nome de usuário e senha.
        :type request: Request
        :return: Um objeto de resposta contendo uma mensagem de sucesso e um token de autenticação se o usuário for autenticado e logado com sucesso,
                 ou uma mensagem de erro com um código de status 400 se as credenciais forem inválidas.
        :rtype: Response
        """
        
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            # Cria ou recupera o token do usuário
            token, created = Token.objects.get_or_create(user=user)
            # Cria a sessão do usuário
            login(request, user)

            return Response({
                "success": "Usuário autenticado e logado com sucesso",
                "token": token.key,
            })
        return Response({"error": "Credenciais inválidas"}, status=HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description=__doc__,
        request_body=UserSerializer,
        responses={
            201: openapi.Response(
                description="Usuário registrado com sucesso.",
                example={
                    'success': 'Usuário criado com sucesso',
                    'token': 'auth_token'
                }
            ),
            400: openapi.Response(
                description="Requisição inválida devido a dados incorretos.",
                example={
                    'username': ['Este campo é obrigatório.'],
                    'password': ['Este campo é obrigatório.']
                }
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Lidar com requisição POST para criar um novo usuário.

        Este método valida os dados da requisição usando o UserSerializer.
        Se os dados forem válidos, cria um novo usuário com o nome de usuário e senha fornecidos,
        salva o usuário no banco de dados e retorna uma resposta de sucesso.
        Se os dados não forem válidos, retorna os erros do serializer com um código de status 400.

        :param request: Objeto de requisição HTTP contendo os dados a serem validados e usados para criação do usuário.
        :type request: Request
        :return: Um objeto de resposta contendo uma mensagem de sucesso se o usuário for criado com sucesso,
                 ou os erros do serializer com um código de status 400 se os dados forem inválidos.
        :rtype: Response
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data.get('email')
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            # Cria um token para o novo usuário
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "success": "Usuário criado com sucesso",
                "token": token.key,
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=__doc__,
        manual_parameters=[
            Parameter(
                name="Authorization",
                in_=IN_HEADER,
                description="Token de autenticação no formato 'Token <seu_token>'",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Usuário deslogado com sucesso.",
                example={
                    'success': 'Usuário deslogado com sucesso'
                }
            ),
            401: openapi.Response(
                description="Usuário não autenticado.",
                example={
                    'error': 'Usuário não autenticado'
                }
            ),
        }
    )
    def delete(self, request: Request) -> Response:
        """
        Lidar com requisição DELETE para deslogar o usuário.

        Este método deleta o token de autenticação do usuário, efetivamente deslogando-o.

        :param request: Objeto de requisição HTTP.
        :type request: Request
        :return: Um objeto de resposta contendo uma mensagem de sucesso se o usuário for deslogado com sucesso,
                 ou uma mensagem de erro se algo der errado.
        :rtype: Response
        """
        try:
            # Deleta o token de autenticação associado ao usuário
            request.auth.delete()
            # Remove a sessão do usuário
            logout(request)

            return Response({"success": "Usuário deslogado com sucesso"})
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
