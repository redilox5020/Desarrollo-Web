from rest_framework                       import status, views
from rest_framework.response              import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authApp.serializers.userSerializer   import UserSerializer

class UserCreateView(views.APIView):
    # recibe una data en JSON, ademas de argumentos basicos del servico web y cualquier otro que requiera, como no se esta seguro de lo que pude llegar, se usan argumentos variables
    def post(self, request, *args, **kwargs):
        print(request.data)

        """ Asigno la informacion del JSON, en la instancia de userSerializer, que al final termina creando el usuario
         recordar que un serializador cuando recibe la informacion en Json lo que hace es convertirla a un objeto en el lenguaje de programacion """
        serializer = UserSerializer(data=request.data)  
        
        """ Como ya se definieron los tipos de datos de los campos en el modelo que esta conectado al serializador,
        Puedo preguntar si lo que se recibe es valido, en conclusion se valida que los tipos de datos y llaves foraneas coincidan o correspondan con lo que espera el modelo y caso de que falle lanza una excepcion """
        serializer.is_valid(raise_exception=True)
        
        """ si todo sale bien se guarda la informacion del serializador, se hace la conversion JSON - Objeto"""
        serializer.save() # este save() termina llamando al metodo create del serializador. los Guarda en BD

        """ Informacion para generar Token, traemos la data de usuario y contraseña """
        tokenData = {"username":request.data["username"],
                    "password":request.data["password"]}
        
        """ Se optiene la pareja de tokens, refresh con access a partir del usuario y contraseña,
        para luego devolver como respuesta """
        tokenSerializer = TokenObtainPairSerializer(data=tokenData) # recibe el tokenData que generamos anteriormente
        tokenSerializer.is_valid(raise_exception=True)# verifica si se crearon con exito los tokens

        """ Si todo sale bien retorno una respuesta con los tokens validados mas un status que determina que la creacion fue correcta """
        return Response(tokenSerializer.validated_data, status=status.HTTP_201_CREATED)