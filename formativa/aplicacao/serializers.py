from rest_framework import serializers
from .models import Usuario, Disciplina, ReservaAmbiente, Sala
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data['password'])  
        user.save()
        return user

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

class ReservaAmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaAmbiente
        fields = '__all__'

    def validate(self, data):
        data_inicio = data.get('data_inicio')
        data_termino = data.get('data_termino')
        sala_reservada = data.get('sala_reservada')
        periodo = data.get('periodo')
        if ReservaAmbiente.objects.filter(
            sala_reservada=sala_reservada,
            data_inicio__lte=data_termino,
            data_termino__gte=data_inicio,
            periodo=periodo
        ).exists():
            
            raise serializers.ValidationError("Não é possível realizar essa reserva, já existe uma!")

        return data


class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
            'tipo': self.user.tipo
        }
        return data
    
class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'