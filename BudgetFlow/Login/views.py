from django.contrib.auth.models import User
from django.core.mail import send_mail
from Login.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout 
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.crypto import get_random_string
from django.core.cache import cache
from drf_yasg.openapi import Parameter, IN_HEADER
from rest_framework.authtoken.models import Token
from decouple import config


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
                    'token': 'auth_token',
                    "user_id": 'user_id',   
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
                "user_id": user.id,
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
                    'token': 'auth_token',
                    'user_id': 'user_id',
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
                "user_id": user.id,
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
                    'success': 'Usuário deslogado com sucesso',
                    'user_id': 'user_id'
                }
            ),
            401: openapi.Response(
                description="Usuário não autenticado.",
                example={
                    'error': 'Usuário não autenticado',
                    'user_id': 'user_id'
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
            user_id = request.user.id
            # Deleta o token de autenticação associado ao usuário
            request.auth.delete()
            # Remove a sessão do usuário
            logout(request)

            return Response({"success": "Usuário deslogado com sucesso", "user_id": user_id}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description=__doc__,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="E-mail do usuário cadastrado"),
            },
            required=['email'],
        ),
        responses={
            200: openapi.Response(
                description="Código de redefinição enviado com sucesso.",
                example={'success': 'Código de redefinição enviado para o e-mail fornecido.'}
            ),
            400: openapi.Response(
                description="Erro ao processar o e-mail fornecido.",
                example={'error': 'E-mail não encontrado.'}
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Lidar com requisição POST para iniciar o processo de redefinição de senha.

        Este método verifica se o e-mail fornecido está associado a um usuário registrado.
        Se o usuário for encontrado, um código de redefinição é gerado e enviado para o e-mail do usuário.

        :param request: Objeto de requisição HTTP contendo o e-mail do usuário.
        :type request: Request
        :return: Um objeto de resposta contendo uma mensagem de sucesso se o código de redefinição for enviado,
                 ou uma mensagem de erro com um código de status 400 se o e-mail não for encontrado.
        :rtype: Response
        """
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=HTTP_400_BAD_REQUEST)

        # Gerar um código de redefinição e armazená-lo no cache
        reset_code = get_random_string(length=6, allowed_chars='0123456789')
        cache.set(f"reset_code_{user.id}", reset_code, timeout=3600)

        # (Opcional) Enviar o código por email
        send_mail(
            'Redefinição de Senha',
            f'Seu código de redefinição de senha é: {reset_code}',
            'thiagocome403@gmail.com',
            [user.email],
        )

        return Response({"success": "Código de redefinição enviado com sucesso."}, status=HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description=__doc__,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="E-mail do usuário cadastrado"),
                'reset_code': openapi.Schema(type=openapi.TYPE_STRING, description="Código de redefinição enviado por e-mail"),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description="Nova senha do usuário"),
            },
            required=['email', 'reset_code', 'new_password'],
        ),
        responses={
            200: openapi.Response(
                description="Senha redefinida com sucesso.",
                example={'success': 'Senha atualizada com sucesso.'}
            ),
            400: openapi.Response(
                description="Erro na redefinição de senha.",
                example={'error': 'Código de redefinição inválido ou expirado.'}
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Lidar com requisição POST para redefinir a senha do usuário.

        Este método verifica se o código de redefinição fornecido é válido e, se for,
        atualiza a senha do usuário com a nova senha fornecida.

        :param request: Objeto de requisição HTTP contendo o e-mail do usuário, o código de redefinição e a nova senha.
        :type request: Request
        :return: Um objeto de resposta contendo uma mensagem de sucesso se a senha for redefinida com sucesso,
                 ou uma mensagem de erro com um código de status 400 se o código de redefinição for inválido ou expirado.
        :rtype: Response
        """
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=HTTP_400_BAD_REQUEST)

        reset_code = request.data.get('reset_code')
        new_password = request.data.get('new_password')

        # Verificar se o código é válido
        stored_code = cache.get(f"reset_code_{user.id}")
        if not stored_code or stored_code != reset_code:
            return Response({"error": "Código de redefinição inválido ou expirado."}, status=HTTP_400_BAD_REQUEST)

        # Atualizar a senha
        user.set_password(new_password)
        user.save()

        # Limpar o cache para o código
        cache.delete(f"reset_code_{user.id}")

        return Response({"success": "Senha redefinida com sucesso."}, status=HTTP_200_OK)
class EstaLogadoView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Verifica se o usuário está autenticado.",
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
                description="Usuário autenticado.",
                example={
                    'is_authenticated': True,
                    'user_id': 'user_id',
                    'username': 'username',
                    'email': 'email'
                }
            ),
            401: openapi.Response(
                description="Usuário não autenticado.",
                example={'is_authenticated': False}
            ),
        }
    )
    def get(self, request: Request) -> Response:
        """
        Verifica se o usuário está autenticado.

        :param request: Objeto de requisição HTTP.
        :type request: Request
        :return: Um objeto de resposta indicando se o usuário está autenticado e suas informações.
        :rtype: Response
        """
        if request.user.is_authenticated:
            user_info = {
                "is_authenticated": True,
                "user_id": request.user.id,
                "username": request.user.username,
                "email": request.user.email
            }
            return Response(user_info, status=HTTP_200_OK)
        return Response({"is_authenticated": False}, status=HTTP_401_UNAUTHORIZED)