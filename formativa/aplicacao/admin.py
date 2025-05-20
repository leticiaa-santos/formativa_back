from django.contrib import admin
from .models import Usuario, Disciplina, ReservaAmbiente, Sala
from django.contrib.auth.admin import UserAdmin

class UsuarioAdmin(UserAdmin):

    # Campos exibidos na listagem de usuários no admin
    list_display = ('username', 'email', 'tipo', 'ni', 'telefone', 'data_nascimento', 'data_contratacao')

    # Campos exibidos ao visualizar/editar um usuário existente no admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('tipo', 'ni', 'telefone', 'data_nascimento', 'data_contratacao')}),
    )

    # Campos exibidos ao adicionar um novo usuário no admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('tipo', 'ni', 'telefone', 'data_nascimento', 'data_contratacao')}),
    )

# Registro dos modelos
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Disciplina)
admin.site.register(ReservaAmbiente)
admin.site.register(Sala)
