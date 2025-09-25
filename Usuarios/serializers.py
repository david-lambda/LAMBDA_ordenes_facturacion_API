
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'correo', 'nombres', 'apellidos', 'password', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_admin': {'write_only': True}
        }
        
    def __init__(self, *args, **kwargs):
        super(UsuarioSerializer, self).__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['password'].required = False 

    def create(self, validated_data):
        is_admin = validated_data.pop('is_admin', False)
        
        if is_admin:
            user = Usuario.objects.create_superuser(
                correo=validated_data['correo'],
                nombres=validated_data['nombres'],
                apellidos=validated_data['apellidos'],
                password=validated_data['password'],
            )
        else:
            user = Usuario.objects.create_user(
                correo=validated_data['correo'],
                nombres=validated_data['nombres'],
                apellidos=validated_data['apellidos'],
                password=validated_data['password'],
            )
        return user

    def update(self, instance, validated_data):
        instance.correo = validated_data.get('correo', instance.correo)
        instance.nombres = validated_data.get('nombres', instance.nombres)
        instance.apellidos = validated_data.get('apellidos', instance.apellidos)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class UsuarioLoginSerializer(serializers.Serializer):
    correo = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=100, required=False)

    def validate(self, data):
        correo = data.get('correo', None)
        password = data.get('password', None)

        if not correo  or not password:
            raise serializers.ValidationError({"error": "Debe proporcionar un correo electrónico y una contraseña."})
        
        try:
            user = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"error": "No se encontró un usuario con este correo electrónico."})

        if not user.check_password(password):
            raise serializers.ValidationError({"error": "La contraseña proporcionada es incorrecta."})

        if not user.is_active:
            raise serializers.ValidationError({"error": "Su cuenta está inactiva, contacte al administrador."})

        data['usuario'] = user
        return data