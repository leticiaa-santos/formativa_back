from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import Usuario, Disciplina, ReservaAmbiente, Sala
from .serializers import UsuarioSerializer, DisciplinaSerializer, ReservaAmbienteSerializer, LoginSerializer, SalaSerializer
from .permissions import IsGestor, IsProfessor, IsDonoOuGestor
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

# View para listar e criar usuários (acesso restrito a gestores)
class UsuarioListCreate(ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsGestor]


# View para recuperar, atualizar ou deletar um usuário específico (apenas para gestores)
class UsuarioRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsGestor]
    lookup_field = 'pk'


    def retrieve(self, request, *args, **kwargs):
        # Retorna os dados de um usuário ou mensagem de erro se não encontrado
        try:
            usuario = self.get_object()
        except Http404:
            return Response({'message': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(usuario)
        return Response({'usuario': serializer.data}, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        # Atualiza os dados de um usuário existente
        try:
            usuario = self.get_object()
        except Http404:
            return Response({'message': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(usuario, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'usuario': serializer.data}, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        # Remove um usuário do sistema
        try:
            usuario = self.get_object()
        except Http404:
            return Response({'message': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(usuario)
        return Response({'detail': f'Usuário "{usuario.username}" excluído com sucesso.'}, status=status.HTTP_200_OK)


# View para listar todas as disciplinas (todos autenticados) e criar novas (apenas gestores)
class DisciplinaListCreate(ListCreateAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsGestor()]


# View para recuperar, atualizar ou deletar uma disciplina (restrito a gestores)
class DisciplinaRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsGestor]
    lookup_field = 'pk'


    def retrieve(self, request, *args, **kwargs):
        # Retorna os dados de uma disciplina ou mensagem de erro se não encontrada
        try:
            disciplina = self.get_object()
        except Http404:
            return Response({'message': 'Disciplina não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(disciplina)
        return Response({'disciplina': serializer.data}, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        # Atualiza os dados de uma disciplina
        try:
            disciplina = self.get_object()
        except Http404:
            return Response({'message': 'Disciplina não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(disciplina, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'disciplina': serializer.data}, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        # Remove uma disciplina do sistema
        try:
            disciplina = self.get_object()
        except Http404:
            return Response({'message': 'Disciplina não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(disciplina)
        return Response({'detail': f'Disciplina "{disciplina.nome}" excluída com sucesso.'}, status=status.HTTP_200_OK)


# View que permite ao professor visualizar apenas suas próprias disciplinas
class DisciplinaProfessorList(ListAPIView):
    serializer_class = DisciplinaSerializer
    permission_classes = [IsProfessor]


    def get_queryset(self):
        # Retorna disciplinas associadas ao professor logado
        return Disciplina.objects.filter(professor=self.request.user)


# View para listar todas as reservas (todos autenticados) e criar novas (apenas gestores)
class ReservaAmbienteListCreate(ListCreateAPIView):
    queryset = ReservaAmbiente.objects.all()
    serializer_class = ReservaAmbienteSerializer


    def get_permissions(self):
        # Permite acesso GET para autenticados, e POST apenas para gestores
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsGestor()]


    def get_queryset(self):
        # Permite filtrar reservas por professor via query param (?professor=id)
        queryset = super().get_queryset()
        professor_id = self.request.query_params.get('professor', None)
        if professor_id:
            queryset = queryset.filter(professor_id=professor_id)
        return queryset


# View para recuperar, atualizar ou deletar uma reserva (restrita ao dono ou gestor)
class ReservaAmbienteRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = ReservaAmbiente.objects.all()
    serializer_class = ReservaAmbienteSerializer
    permission_classes = [IsDonoOuGestor]
    lookup_field = 'pk'


    def retrieve(self, request, *args, **kwargs):
        # Retorna dados de uma reserva ou mensagem de erro
        try:
            reserva = self.get_object()
        except Http404:
            return Response({'message': 'Reserva não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(reserva)
        return Response({'reserva': serializer.data}, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        # Atualiza uma reserva existente
        try:
            reserva = self.get_object()
        except Http404:
            return Response({'message': 'Reserva não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(reserva, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'reserva': serializer.data}, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        # Remove uma reserva do sistema
        try:
            reserva = self.get_object()
            nome_sala = reserva.sala_reservada.nome
        except Http404:
            return Response({'message': 'Reserva não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(reserva)
        return Response({'detail': f'Reserva na sala "{nome_sala}" excluída com sucesso.'}, status=status.HTTP_200_OK)


# View que permite ao professor ver apenas suas próprias reservas
class ReservaAmbienteProfessorList(ListAPIView):
    serializer_class = ReservaAmbienteSerializer
    permission_classes = [IsProfessor]


    def get_queryset(self):
        # Retorna reservas associadas ao professor logado
        return ReservaAmbiente.objects.filter(professor=self.request.user)


# View para autenticação via JWT (login do usuário)
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# View para listar todas as salas (autenticados) e criar novas (apenas gestores)
class SalaListCreate(ListCreateAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer


    def get_permissions(self):
        # Permite acesso GET para autenticados, e POST apenas para gestores
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsGestor()]


# View para recuperar, atualizar ou deletar uma sala (apenas para gestores)
class SalaRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsGestor]


    def retrieve(self, request, *args, **kwargs):
        # Retorna dados de uma sala ou mensagem de erro
        try:
            sala = self.get_object()
        except Http404:
            return Response({'message': 'Sala não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(sala)
        return Response({'sala': serializer.data}, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        # Atualiza uma sala existente
        try:
            sala = self.get_object()
        except Http404:
            return Response({'message': 'Sala não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(sala, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'sala': serializer.data}, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        # Remove uma sala do sistema
        try:
            sala = self.get_object()
        except Http404:
            return Response({'message': 'Sala não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(sala)
        return Response({'detail': f'Sala "{sala.nome}" excluída com sucesso.'}, status=status.HTTP_200_OK)