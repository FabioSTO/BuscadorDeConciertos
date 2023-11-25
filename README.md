## Cómo ejecutar en Docker

+ Antes de nada, asegurarse de tener instalado Docker y su extensión, así como Dev Containers:
![Ejemplo configuración](/app/static/BuscadorConciertos/img/extDocker.png)
![Ejemplo configuración](/app/static/BuscadorConciertos/img/extCont.png)

+ Ejecutar el comando Rebuild de Dev Containers para crear la imagen a partir del DockerFile. Cambiará la apariencia y se mostrará el container en la esquina inferior izquierda.
![Ejemplo configuración](/app/static/BuscadorConciertos/img/rebuilds.png)
![Ejemplo configuración](/app/static/BuscadorConciertos/img/container.png)

+ Ejecutar el comando 'python manage.py runserver 0.0.0.0:8000' para correr la aplicación. Es posible tener que realizar 'python manage.py makemigrations' y 'python manage.py migrate'.
![Ejemplo configuración](/app/static/BuscadorConciertos/img/comando.png)

+ Acceder a la aplicación escribiendo la ruta 'http://localhost:8000/'. ¡Dependiendo del buscador usado existe la posibilidad de que haya sido guardada en caché propia  ciertos archivos estáticos de versiones anteriores de la aplicación! Por lo que se recomienda el uso de modo incógnito o la limpieza de la caché del buscador.
![Ejemplo configuración](/app/static/BuscadorConciertos/img/ruta.png)

## Instrucciones para el LOGGING con SPOTIFY:

+ Una vez dentro de la app, para loguearse se pulsará en el icono de Spotify de la esquina superior-derecha:
![Instrucciones para logging](/app/static/BuscadorConciertos/img/Log_sel.png)

+ Se escogerá la opción de Logging mediante Google y se introducirán las credenciales (CORREO: usuariopruebasspotiapi@gmail.com y CONTRASEÑA: Spoti_Pru3b4s.). El siguiente paso sería pulsar en "autorizar" a la aplicación a leer tus datos de Spotify (este paso puede que se salte directamente ya que hemos autorizado previamente con esta cuenta durante las pruebas en el desarrollo):
![Instrucciones para logging](/app/static/BuscadorConciertos/img/Goog_sel.png)


## Riesgos en versión actual:

### Debido al funcionamiento del API de TicketMaster, las IDs de eventos y las de los artistas comparten base de datos (de TicketMaster) como AttractionIds: 

+ En nuestro caso, a la hora de obtener el ID de artista, solventamos este percance obteniendo el primer resultado ordenando por "relevancia" al llamar a la API con el nombre de artista. Esto funciona en el 95% de los casos (aproximadamente según nuestras pruebas). Pero sí que es verdad que en ciertos casos, puede obtener un evento y dar un resultado no deseado.

    * Un ejemplo es Badd Bunny, que debido a que no hace conciertos actualmente, aparece como resultado más relevante un tributo (evento).


### Debido a que los datos que proporciona la API de TicketMaster varían mucho según los artistas, recomendamos ciertas configuraciones para obtener suficientes eventos y así comprobar el correcto funcionamiento de la aplicación:

+ Emplear en la medida de lo posible la base de datos que ya proporcionamos nosotros.

+ Seleccionar como país de búsqueda Estados Unidos (mayor número de conciertos).

+ Seleccionar como ubicación una ciudad estadounidense.

+ No seleccionar un rango de fechas muy cerrado, puede que no se celebren demasiados eventos, ni un presupuesto muy bajo.

![Ejemplo configuración](/app/static/BuscadorConciertos/img/ej.png)
	 

### Riesgos con los tests:

+ El test que comprueba la llamada a la API de Google Maps para obtener la distancia entre dos puntos es posible que falle. Esto es debido a que calcula la ruta en tiempo real y por lo tanto dependiendo del estado de las carreteras puede variar la distancia.

+ Lo anterior es tambien posible que suceda con los eventos de Ticketmaster, ya que si se diera el caso de que justo los eventos testeados desaparecen de la web de Ticketmaster, el test fallaría.

+ Para los tests de Spotify hemos decidido realizarlos de forma 'simulada' para evitar problemas con el ACCESS_TOKEN, ya que no es permanente y por lo tanto deja de ser usable pasado un tiempo.


## Notas adicionales

+ El código empleado para map.js se ha modificado del existente en el blog https://lemonharpy.wordpress.com/2011/12/15/working-around-8-waypoint-limit-in-google-maps-directions-api/
