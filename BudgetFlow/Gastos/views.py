from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.openapi import IN_HEADER, Parameter
from .models import Despesa, Receita
from .serializers import DespesaSerializer, ReceitaSerializer


class AdicionaDespesaView(APIView):
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
        request_body=DespesaSerializer,
        responses={
            201: openapi.Response(
                description="Despesa adicionada com sucesso.",
                example={"success": "Despesa criada com sucesso", "id": "despesa_id"}
            ),
            400: openapi.Response(
                description="Erro nos dados fornecidos.",
                example={"error": "Dados inválidos"}
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Adiciona uma nova despesa para o usuário autenticado.

        Este método recebe os dados da despesa no corpo da solicitação, valida-os e, se estiverem corretos,
        cria uma nova instância de despesa associada ao usuário autenticado.

        :param request: Objeto de solicitação HTTP contendo os dados da despesa.
        :type request: Request
        :return: Resposta HTTP com o status da operação e o ID da despesa criada, ou erros de validação.
        :rtype: Response
        """
        serializer = DespesaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            despesa = serializer.save()  # O usuário será adicionado no método `create` do serializer.
            return Response({
                "success": "Despesa criada com sucesso",
                "id": despesa.id
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ListaDespesasView(APIView):
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
                description="Lista de despesas.",
                schema=DespesaSerializer(many=True)
            )
        }
    )
    def get(self, request: Request) -> Response:
        """
        Lista todas as despesas do usuário autenticado.

        Este método recupera todas as despesas associadas ao usuário autenticado e retorna uma lista dessas despesas.

        :param request: Objeto de solicitação HTTP.
        :type request: Request
        :return: Resposta HTTP com a lista de despesas do usuário autenticado.
        :rtype: Response
        """
        despesas = Despesa.objects.filter(user=request.user)
        data = [{"id": despesa.id, **DespesaSerializer(despesa).data} for despesa in despesas]
        return Response(data, status=HTTP_200_OK)


class EditaDespesaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=__doc__,
        request_body=DespesaSerializer,
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
                description="Despesa editada com sucesso.",
                example={"success": "Despesa atualizada com sucesso", "id": 1}
            ),
            400: openapi.Response(
                description="Erro nos dados fornecidos.",
                example={"error": "Dados inválidos"}
            ),
        }
    )
    def put(self, request: Request, pk: int) -> Response:
        """
        Edita uma despesa específica.

        Este método recebe os dados atualizados da despesa no corpo da solicitação, valida-os e, se estiverem corretos,
        atualiza a instância da despesa especificada pelo ID (pk) associada ao usuário autenticado.

        :param request: Objeto de solicitação HTTP contendo os dados atualizados da despesa.
        :type request: Request
        :param pk: ID da despesa a ser editada.
        :type pk: int
        :return: Resposta HTTP com o status da operação e o ID da despesa atualizada, ou erros de validação.
        :rtype: Response
        """
        try:
            despesa = Despesa.objects.get(pk=pk, user=request.user)
        except Despesa.DoesNotExist:
            return Response({"error": "Despesa não encontrada"}, status=HTTP_400_BAD_REQUEST)

        serializer = DespesaSerializer(despesa, data=request.data)
        if serializer.is_valid():
            despesa = serializer.save()
            return Response({
                "success": "Despesa atualizada com sucesso",
                "id": despesa.id
            }, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class DeletaDespesaView(APIView):
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
                description="Despesa deletada com sucesso.",
                example={"success": "Despesa removida", "id": 1}
            ),
            400: openapi.Response(
                description="Erro ao tentar deletar.",
                example={"error": "Despesa não encontrada"}
            ),
        }
    )
    def delete(self, request: Request, pk: int) -> Response:
        """
        Deleta uma despesa específica.

        Este método deleta a instância da despesa especificada pelo ID (pk) associada ao usuário autenticado.

        :param request: Objeto de solicitação HTTP.
        :type request: Request
        :param pk: ID da despesa a ser deletada.
        :type pk: int
        :return: Resposta HTTP com o status da operação e o ID da despesa deletada, ou erro se a despesa não for encontrada.
        :rtype: Response
        """
        try:
            despesa = Despesa.objects.get(pk=pk, user=request.user)
            despesa_id = despesa.id
            despesa.delete()
            return Response({
                "success": "Despesa removida",
                "id": despesa_id
            }, status=HTTP_200_OK)
            
        except Despesa.DoesNotExist:
            return Response({"error": "Despesa não encontrada"}, status=HTTP_400_BAD_REQUEST)


class AdicionaReceitaView(APIView):
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
        request_body=ReceitaSerializer,
        responses={
            201: openapi.Response(
                description="Receita adicionada com sucesso.",
                example={"success": "Receita criada com sucesso", "id": "receita_id"}
            ),
            400: openapi.Response(
                description="Erro nos dados fornecidos.",
                example={"error": "Dados inválidos"}
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Adiciona uma nova receita para o usuário autenticado.

        Este método recebe os dados da receita no corpo da solicitação, valida-os e, se estiverem corretos,
        cria uma nova instância de receita associada ao usuário autenticado.

        :param request: Objeto de solicitação HTTP contendo os dados da receita.
        :type request: Request
        :return: Resposta HTTP com o status da operação e o ID da receita criada, ou erros de validação.
        :rtype: Response
        """
        serializer = ReceitaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            receita = serializer.save()  # O usuário será adicionado no método `create` do serializer.
            return Response({
                "success": "Receita criada com sucesso",
                "id": receita.id
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ListaReceitasView(APIView):
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
                description="Lista de receitas.",
                schema=ReceitaSerializer(many=True)
            )
        }
    )
    def get(self, request: Request) -> Response:
        """
        Lista todas as receitas do usuário autenticado.

        Este método recupera todas as receitas associadas ao usuário autenticado e retorna uma lista dessas receitas.

        :param request: Objeto de solicitação HTTP.
        :type request: Request
        :return: Resposta HTTP com a lista de receitas do usuário autenticado.
        :rtype: Response
        """
        receitas = Receita.objects.filter(user=request.user)
        data = [{"id": receita.id, **ReceitaSerializer(receita).data} for receita in receitas]
        return Response(data, status=HTTP_200_OK)


class EditaReceitaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=__doc__,
        request_body=ReceitaSerializer,
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
                description="Receita editada com sucesso.",
                example={"success": "Receita atualizada com sucesso", "id": 1}
            ),
            400: openapi.Response(
                description="Erro nos dados fornecidos.",
                example={"error": "Dados inválidos"}
            ),
        }
    )
    def put(self, request: Request, pk: int) -> Response:
        """
        Edita uma receita específica.

        Este método recebe os dados atualizados da receita no corpo da solicitação, valida-os e, se estiverem corretos,
        atualiza a instância da receita especificada pelo ID (pk) associada ao usuário autenticado.

        :param request: Objeto de solicitação HTTP contendo os dados atualizados da receita.
        :type request: Request
        :param pk: ID da receita a ser editada.
        :type pk: int
        :return: Resposta HTTP com o status da operação e o ID da receita atualizada, ou erros de validação.
        :rtype: Response
        """
        try:
            receita = Receita.objects.get(pk=pk, user=request.user)
        except Receita.DoesNotExist:
            return Response({"error": "Receita não encontrada"}, status=HTTP_400_BAD_REQUEST)

        serializer = ReceitaSerializer(receita, data=request.data)
        if serializer.is_valid():
            receita = serializer.save()
            return Response({
                "success": "Receita atualizada com sucesso",
                "id": receita.id
            }, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class DeletaReceitaView(APIView):
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
                description="Receita deletada com sucesso.",
                example={"success": "Receita removida", "id": 1}
            ),
            400: openapi.Response(
                description="Erro ao tentar deletar.",
                example={"error": "Receita não encontrada"}
            ),
        }
    )
    def delete(self, request: Request, pk: int) -> Response:
        """
        Deleta uma receita específica.

        Este método deleta a instância da receita especificada pelo ID (pk) associada ao usuário autenticado.

        :param request: Objeto de solicitação HTTP.
        :type request: Request
        :param pk: ID da receita a ser deletada.
        :type pk: int
        :return: Resposta HTTP com o status da operação e o ID da receita deletada, ou erro se a receita não for encontrada.
        :rtype: Response
        """
        try:
            receita = Receita.objects.get(pk=pk, user=request.user)
            receita_id = receita.id
            receita.delete()
            return Response({
                "success": "Receita removida",
                "id": receita_id
            }, status=HTTP_200_OK)
            
        except Receita.DoesNotExist:
            return Response({"error": "Receita não encontrada"}, status=HTTP_400_BAD_REQUEST)
