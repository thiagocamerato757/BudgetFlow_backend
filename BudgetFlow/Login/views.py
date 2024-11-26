from django.contrib.auth.models import User
from Login.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as django_login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.permissions import AllowAny,IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_HEADER
from rest_framework.authtoken.models import Token

class Loginview(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Authenticate user and return an authentication token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user')
            },
            required=['username', 'password'],
        ),
        responses={
            200: openapi.Response(
                description="User authenticated successfully.",
                example={
                    'success': 'User authenticated and logged in successfully',
                    'token': 'auth_token'
                }
            ),
            400: openapi.Response(
                description="Invalid credentials.",
                example={
                    'error': 'Invalid credentials'
                }
            ),
        }
    )
    def post(self, request: Request) -> Response:  # Alterado para POST
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "success": "User authenticated and logged in successfully",
                "token": token.key,
            })
        return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Register a new user and return an authentication token.",
        request_body=UserSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully.",
                example={
                    'success': 'User created successfully',
                    'token': 'auth_token'
                }
            ),
            400: openapi.Response(
                description="Bad request due to invalid data.",
                example={
                    'username': ['This field is required.'],
                    'password': ['This field is required.']
                }
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Handle POST request to create a new user.

        This method validates the incoming request data using the `UserSerializer`.
        If the data is valid, it creates a new user with the provided username and password,
        saves the user to the database, and returns a success response.
        If the data is not valid, it returns the serializer errors with a 400 status code.

        :param request: The HTTP request object containing the data to be validated and used for user creation.
        :type request: Request
        :return: A response object containing a success message if the user is created successfully,
                 or the serializer errors with a 400 status code if the data is invalid.
        :rtype: Response
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "success": "User created successfully",
                "token": token.key,
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Log out the authenticated user by deleting their token.",
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
                description="User logged out successfully.",
                example={
                    'success': 'User logged out successfully'
                }
            ),
            401: openapi.Response(
                description="User not authenticated.",
                example={
                    'error': 'Authentication credentials were not provided.'
                }
            ),
            400: openapi.Response(
                description="Bad request.",
                example={
                    'error': 'An unexpected error occurred'
                }
            ),
        }
    )
    def delete(self, request: Request) -> Response:
        """
        Handle DELETE request to log out the user.

        This method deletes the user's authentication token, effectively logging them out.

        :param request: The HTTP request object.
        :type request: Request
        :return: A response object containing a success message if the user is logged out successfully,
                 or an error message if something goes wrong.
        :rtype: Response
        """
        try:
            request.auth.delete()  # Deleta o token do usuário autenticado
            return Response({"success": "User logged out successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)