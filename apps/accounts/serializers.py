from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    nome_completo = serializers.ReadOnlyField()
    iniciais = serializers.ReadOnlyField()
    setor_nome = serializers.SerializerMethodField()
    setor_codigo = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'nome_completo', 'iniciais', 'perfil', 'cargo', 'telefone',
            'setor', 'setor_nome', 'setor_codigo', 'ativo'
        ]
        read_only_fields = ['id', 'nome_completo', 'iniciais']

    def get_setor_nome(self, obj):
        return obj.setor.nome if obj.setor else None

    def get_setor_codigo(self, obj):
        return obj.setor.codigo if obj.setor else None


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['perfil'] = user.perfil
        token['nome'] = user.nome_completo
        token['setor'] = user.setor.codigo if user.setor else None
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['usuario'] = UsuarioSerializer(self.user).data
        return data
