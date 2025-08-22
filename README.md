Proyecto creado en un entorno virtual de python usando pipenv.
Toda esta aplicacion fue creada fon FastApi.
Los paquetes que se instalaron fueron:
    sqlmodel
    pyjwt
    "passlib[bcrypt]"
    python-dotenv

La carpeta "database" solo contiene un archivo "connection.py", es la connexion a la base de datos y la creacion de nuestra session de la base de datos.

La carpeta "module" son los modulos o clases que se usan para este proyecto, como "user_module.py" el cual son los modelos para la creacion del usuarios, el otro es "note_module.py" el cual son los modulos para la creacion de las notas.

La carpeta "security" contiene dos archivos, uno es el "hash_password.py" el cual es contiene el schema que se usara para la encriptacion de la contraseña, dosfunciones las cuales es una para verificar que coincidan las contraseñas y la otra es para encriptar la contraseña del usuario.

El archivo "main.py" contiene todas nuestras rutas HTTP

La base de datos es sqlite
