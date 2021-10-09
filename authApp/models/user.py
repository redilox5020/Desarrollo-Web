from django.db import models # clase abstracta que nos proporciona herramientas para los modelos
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# genera contraseña encriptada a partir del password original que se envia al hashers como una palabra clave
from django.contrib.auth.hashers import make_password 

# Ayuda a gestionar el modelo, Equivalente a los Daos, se tienen algunas operaciones que funcionan sobre el modelo
class UserManager(BaseUserManager):

  # Funcion para hacer un insert
  def create_user(self, username, password=None):
    """Creates and saves a user with the given username and password.
    """
    if not username:
      raise ValueError('Los usuarios deben tener un nombre de usuario.')

    """
    Creo el Usuario que sera igual al self.model, este model hereda de la clase padre,
    por tanto la instruccion, sera crear un modelo de ese usuario base, donde el username requerido
    va a ser igual al parametro que recibimos en la funcion 
    """
    user = self.model(username=username)
    user.set_password(password)

    # asignamos el parametro using que hace referencia a cual bd vamos a usar, 
    # en este caso utilizamos la bd por defecto es decir la que configuramos en el settings
    user.save(using=self._db)
    return user

  def create_superuser(self, username, password):
    """
    Creates and saves a superuser with the given username and password.
    """
    user = self.create_user(
      username=username,
      password=password,
    )
    # para hacerlo admin se hereda el atributo is_admin que por defecto es falso
    user.is_admin = True
    user.save(using=self._db)
    return user

class User(AbstractBaseUser, PermissionsMixin):
  id       = models.BigAutoField(primary_key=True) # forma de generar id seguros como de 64 caracteres
  username = models.CharField('Username', max_length = 15, unique=True)
  password = models.CharField('Password', max_length = 256)
  name     = models.CharField('Name', max_length = 30)
  email    = models.EmailField('Email', max_length = 100)
 
  def save(self, **kwargs):
    # texto aleatorio que ayuda a cifrar, basado en este texto hacemos un cifrado de la contraseña original - Palabra Clave
    some_salt = 'mMUj0DrIK6vgtdIYepkIxN' 

    # la funcion make_password recibe el password original y la palabra clave, 
    # basado en estos parametros implementa una operacion de hashing para cifrar la contraseña
    self.password = make_password(self.password, some_salt)
    super().save(**kwargs)

  def __str__(self) -> str: # metodo para Representar objectos en String
      return f"""Usuario[
            id : {self.id}
            Apodo : {self.username}
            Nombre : {self.name}
            Email: {self.email}
      ]"""

  objects = UserManager() # instancia de la clase userManager definida arriba
  USERNAME_FIELD = 'username' #Campo de login que el usuario va especificar
