from django.conf                        import settings

""" Los generics son esas clases genericas, que cada una incorpora funcionalidades directas para las operaciones del crud"""
# con generics heredamos clases que incorporan las funciones necesarias para el crud
from rest_framework                     import generics, status 
from rest_framework.response            import Response
from rest_framework_simplejwt.backends  import TokenBackend
from rest_framework.permissions         import IsAuthenticated # Para verificar los permisos del usuario
from authApp.models.user                import User
from authApp.serializers.userSerializer import UserSerializer

""" RetriveAPIView Obtiene un Objeto y su ID
    Vista concreta para recuperar una instancia de modelo
 """
class UserDetailView(generics.RetrieveAPIView):
    queryset           = User.objects.all() # Se traen todos los elementos de la tabla
    serializer_class   = UserSerializer     # Se Define la clase que se va a usar para la serializacion en un Atributo heredado
    permission_classes = (IsAuthenticated,) # Tipos de Permisos a manejar. El unico permiso que se asigna es que este autenticado
    
    # se usa get para visualizar el usuario simplemente colocando su id en la url
    def get(self, request, *args, **kwargs):
        
        """ Recupero el token que incluye la peticion. 
            de la peticion que llega vamos a sus metadatos para traer lo que se guarda 'HTTP_AUTHORIZATION'
            que no es mas que un token de acceso, para luego verificar que coincide con el usuario que se quiere consultar
            """
        # Se Imprime el token completo "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...."
        print(request.META.get('HTTP_AUTHORIZATION'))               

        # Se recupera desde la posicion 7 hasta el final, porque se anteponen los caracteres "Bearer ", 
        # Se extrae el token tal cual lo colocan en el servicio web
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]   

        """ con TokenBackend se va ha hacer la verificacion del token extraido anteriormente,
            basicamente lo que hace es la decodificacion a partir del algoritmo configurado en lo ajustes del proyecto """
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM']) # Asigna el algoritmo definido en los ajustes
       
        """ Ademas cabe destacar en que el proceso de codificacion del token se guarda varia informacion 
            que incluye el usuario para el que se genero este token, por tanto esta informacion adicional 
            se almacena en en la Variable 'valid_data' luego del proceso de decodificacion y verficacion"""
        valid_data   = tokenBackend.decode(token,verify=False)  # es aqui donde se decodifica y luego verifica si el tokens se genero con el algoritmo seleccionado

        """ por tanto ahora puedo comparar el id del usuario para el que se genero el token, 
            con el id que se ingresa en el url de la vista Datalle, 
            esta validacion se realiza para que el usuario logeado no pueda acceder a la informacion de otros usuarios dentro del sistema,
            unicamente puede acceder a su informacion"""
        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':'Acceso no autorizado'} # en caso de intentar consultar la informacion de otro usuario diferente
            
            """ se retorna el mensaje de respuesta junto con un status que hace alusion a que no esta autorizado """
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        ''' En caso de pasar todos la validaciones. entre esas que el usuario para el que se genero el token coincide con el que se quiere    consultar. se retorna haciendo el llamado a la clase padre para usar el metodo get el cual va a traer un unico registro '''
        return super().get(request, *args, **kwargs)