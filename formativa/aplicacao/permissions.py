from rest_framework.permissions import BasePermission

class IsGestor(BasePermission):
    message = "Apenas gestores têm permissão para realizar esta ação."
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'G' # Permite acesso apenas a usuários autenticados com tipo 'G' (gestor)
    
class IsProfessor(BasePermission):
    message = "Apenas professores têm permissão para realizar esta ação."
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'P' # Permite acesso apenas a usuários autenticados com tipo 'P' (professor)
    
class IsDonoOuGestor(BasePermission):
    def has_object_permission(self, request, view, obj): # Permite o acesso se o usuário for gestor ou o dono (professor que pertence o objeto)
        if request.user.tipo == 'G':
            return True
        return obj.professor == request.user