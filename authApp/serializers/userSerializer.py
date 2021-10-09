from rest_framework                        import serializers
from authApp.models.user                   import User      # Traemos el modelo de Usuario
from authApp.models.account                import Account   # Tambien Cuentas 
from authApp.serializers.accountSerializer import AccountSerializer

class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()   # Traemos La clase Serializer de cuenta
    class Meta: # clase interna necesaria
        model = User # se define el modelo del cual vamos a traer los campos a trabajar 

        '''  Compos de Interes, tener en cuenta que se agrega un campo adicional referente a la cuenta '''
        fields = ['id', 'username', 'password', 'name', 'email', 'account'] 
    
    # Creo un Nuevo Usuario - Proceso de Deserializacion- de Json a Objecto
    def create(self, validated_data): # Recibe de la vista, la informacion en JSON previamente validada 

        ''' De esta Informacion Validada, Separamos el campo de la cuenta, para Guardarla en la variable "accountData" 
            Recordar: El método pop() elimina el elemento en el índice dado de la lista y devuelve el elemento eliminado'''
        accountData = validated_data.pop('account') 

        ''' Se Crea el objeto de tipo Usuario a partir de los datos recibidos en un diccionario,
            teniendo en cuenta que previemente fue eliminado el campo adicional para la cuenta.
            En caso de no quitar este campo de account o cuenta nos retorna error al intentar crear el objeto usuario
            porque no reconoce este campo en el modelo User'''
        userInstance = User.objects.create(**validated_data) 

        ''' Instancia del objeto de tipo cuenta, se requieren dos parametros, 
        El primero asocia el usuario creado anteriormente como llave forania a la cuenta,
        El Segundo hace referencia a los campos que se han definido en class Meta del serializador de cuenta
        Recordar que "accountData" fue la variable donde previamente Guardamos el campo de cuenta al usar el metodo POP'''
        Account.objects.create(user=userInstance, **accountData) 
        
        return userInstance 
    
    #Proceso de Serializacion - Objeto a JSON
    
    ''' Similar al toString en java, su funcion es representar la informacion 
    Emparejamiento directo entre la data que llega y la estructura del JSON que se espera '''
    def to_representation(self, obj):               # obj: cada uno de los objetos que llega de la consulta 
        user = User.objects.get(id=obj.id)          # Se obtiene el Usuario a partir del id

        print(User.objects.get(id=obj.id))
        print(Account.objects.get(user=obj.id))

        account = Account.objects.get(user=obj.id)  # Obtenemos la cuenta a partir del id de usuario
        return {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'account': {
                'id': account.id,
                'balance': account.balance,
                'lastChangeDate': account.lastChangeDate,
                'isActive': account.isActive
            }
        }

    ''' Cabe destacar que el Metodo to_representation originalmente esta automatizado para tomar los campos(filds) definidos en el meta de este serializador y convertirlos en Clave, Valor, en este caso en concreto como se quiere personalizar la forma en que se va ha pintar excluyendo algunos campos, se remplaza para lograr el objetivo '''