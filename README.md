# Instrucciones

En la estructura de la aplicación existen dos tipos de usuario:



- Usuario normal: permite crear automoviles, editarlos y consultarlos. Sobre los datos del perfil del usuario se pueden hacer las mismas acciones. 

- Superheroe(superuser): tiene los mismos permisos del usuario normal y además permite crear marcas de vehículos.
<hr>

## Flujo de la aplicación
Al inicio de la aplicación, se visualiza un formulario de ingreso, en caso de no estar registrado, se ofrece un link para realizar el registro. Una vez realizado el registro, se redirige a la pantalla de inicio de sesión para ingresar. 

Si la autenticación es exitosa, se pasa al dashboard principal. En esta pantalla se ofrecen funcionalidades para hacer gestión de los carros del usuario. Creación, lectura y actualización. 

En la parte superior derecha, se observa un menú desplegable con las opciones sobre los datos del perfil de usuario. Dentro de este mismo menú, se ofrece un link hacia la interfaz de consumo del api. 
<hr>

## UI API
La interfaz del api es muy sencillas. Tiene dos campos. Una lista desplegable para escoger la funcionalidad(enpoint) qué se quiere visualizar. Tiene también un campo para insertar un identificador específico según la búsqueda. Por ejemplo, si se hacen busquedas por el usuario, se inserta la cédula. Si se quieren hacer busquedas por la marca, se ingresa el nombre de la marca. En caso de que no se indique nada en este campo, se despliegan los datos relacionandolos con su información. 