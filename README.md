# aplicacion_gjango-cancelo_fernandez_senande

## Trabajo semanal aproximado:



|         |   Fabio   |    Fran   |  Miguel   |
|---------|-----------|-----------|-----------|
| Semana 1| 12 horas  |  8 horas  |  7 horas  |
| Semana 2| 16 horas  |  4 horas  | 13 horas  |
| Semana 3| 4 horas   | 12 horas  |  4 horas  |
| Semana 4| 4 horas   |  3 horas  |  3 horas  |
| Semana 5| 4 horas   |           |  3 horas  |
| Semana 6| 20 horas  |           |  12 horas |
| Semana 7| 50 horas  |           |  32 horas |

**__Semana 1 es la semana del 24/04/2023__*


## Como ejecutar en Docker

+ Antes de nada, asegurarse de tener instalado Docker y su extensión, así como Dev Containers:
![Ejemplo configuración](/app/static/BuscadorConciertos/img/extDocker.png)
![Ejemplo configuración](/app/static/BuscadorConciertos/img/extCont.png)

+ Ejecutar el comando Rebuild de Dev Containers para crear la imagen a partir del DockerFile. Cambiará la apariencia y se mostrará el container en la esquina inferior izquierda.
![Ejemplo configuración](/app/static/BuscadorConciertos/img/rebuilds.png)
![Ejemplo configuración](/app/static/BuscadorConciertos/img/container.png)

+ Ejecutar el comando 'python manage.py runserver 0.0.0.0:8000' para correr la aplicación. Es posible tener que realizar 'python manage.py makemigrations' y 'python manage.py migrate'.
![Ejemplo configuración](/app/static/BuscadorConciertos/img/comando.png)

+ Acceder a la aplicación escribiendo la ruta 'http://localhost:8000/'.
![Ejemplo configuración](/app/static/BuscadorConciertos/img/ruta.png)


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
	 


