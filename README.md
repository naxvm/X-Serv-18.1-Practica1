# X-Serv-18.1-Practica1
PRÁCTICA TERMINADA

Práctica 1 (Ejercicio 18.1): Web acortadora de URLs

## Funcionamiento
El fichero ejecutable creará un objeto de la clase webapp.webApp, cuyos parámetros serán máquina y puerto donde arrancará el servidor, y nombre del fichero CSV donde están almacenadas/se almacenarán las URLs acortadas. Los campos ya existentes se volcarán por pantalla al arrancar el servidor, y en caso de no existir dicho fichero, se creará, actualizándose cada vez que llegue una nueva petición. 

## Enunciado

Esta práctica tendrá como objetivo la creación de una aplicación web simple para acortar URLs. La aplicación funcionará únicamente con datos en memoria: se supone que cada vez que la aplicación muera y vuelva a ser lanzada, habrá perdido todo su estado anterior. La aplicación tendrá que realizarse según un esquema de clases similar al explicado en clase.

El funcionamiento de la aplicación será el siguiente:

<ul>
<li> Recurso <em>/</em>, invocado mediante GET. Devolverá una página HTML con un formulario. En ese formulario se podrá escribir una url, que se enviará al servidor mediante POST. Además, esa misma página incluirá un listado de todas las URLs reales y acortadas que maneja la aplicación en este momento.

<li> Recurso <em>/</em>, invocado mediante POST. Si el comando POST incluye una <b>qs</b> (query string) que corresponda con una url enviada desde el formulario, se devolverá una página HTML con la url original y la url acortada (ambas como enlaces pinchables), y se apuntará la correspondencia (ver más abajo).

Si el POST no trae una <b>qs</b> que se haya podido generar en el formulario, devolverá una página HTML con un mensaje de error.

Si la URL especificada en el formulario comienza por <em>http://</em> o <em>https://</em>, se considerará que ésa es la URL a acortar. Si no es así, se le añadirá <em>http://</em> por delante, y se considerará que esa es la url a acortar. Por ejemplo, si en el formulario se escribe <em>http://gsyc.es</em>, la url a acortar será <em>http://gsyc.es</em>. Si se escribe <em>gsyc.es</em>, la URL a acortar será <em>http://gsyc.es</em>.

Para determinar la URL acortada, utilizará un número entero secuencial, comenzando por 0, para cada nueva petición de acortamiento de una URL que se reciba. Si se recibe una petición para una URL ya acortada, se devolverá la URL acortada que se devolvió en su momento.

Así, por ejemplo, si se quiere acortar

<i>http://docencia.etsit.urjc.es</i>

y la aplicación está en el puerto 1234 de la máquina <em>localhost</em>, se invocará (mediante POST) la URL

<i>http://localhost:1234/</i>

y en el cuerpo de esa petición HTTP irá la <b>qs</b>

<i>url=http://docencia.etsit.urjc.es</i>

si el campo donde el usuario puede escribir en el formulario tiene el nombre <em>URL</em>. Normalmente, esta invocación POST se realizará rellenando el formulario que ofrece la aplicación.

Como respuesta, la aplicación devolverá (en el cuerpo de la respuesta HTTP) la URL acortada, por ejemplo

<i>http://localhost:1234/3</i>

Si a continuación se trata de acortar la URL

<i>http://docencia.etsit.urjc.es/moodle/course/view.php?id=25</i>

mediante un procedimiento similar, se recibirá como respuesta la URL acortada

<i>http://localhost:1234/4</i>

Si se vuelve a intentar acortar la URL

<i>http://docencia.etsit.urjc.es</i>

como ya ha sido acortada previamente, se devolverá la misma URL corta:

<i>http://localhost:1234/3</i>

<li> Recursos correspondientes a URLs acortadas. Estos serán números con el prefijo <em>/</em>. Cuando la aplicación reciba un GET sobre uno de estos recursos, si el número corresponde a una URL acortada, devolverá un HTTP REDIRECT a la URL real. Si no la tiene, devolverá HTTP ERROR <em>Recurso no disponible</em>.

Por ejemplo, si se recibe 

<i>http://localhost:1234/3</i>

la aplicación devolverá un HTTP REDIRECT a la URL

<i>http://docencia.etsit.urjc.es</i>

</ul>

## Comentarios de implementación

Se recomienda utilizar la clase <b>webApp</b> del fichero webapp.py, heredando de la misma. La funcionalidad de esta práctica debería implementarse en el fichero <b>practica1.py</b>.

Se recomienda utilizar dos diccionarios para almacenar las URLs reales y los números de las URLs acortadas. En uno de ellos, la clave de búsqueda será la URL real, y se utilizará para saber si una URL real ya está acortada, y en su caso saber cuál es el número de la URL corta correspondiente.

En el otro diccionario la clave de búsqueda será el número de la URL acortada, y se utilizará para localizar las URLs reales dadas las cortas. De todas formas, son posibles (e incluso más eficientes) otras estructuras de datos.

Se recomienda realizar la aplicación en varios pasos:

<ol>
<li> Comenzar por reconocer <em>GET /</em>, y devolver el formulario correspondiente.
<li> Reconocer <em>POST /</em>, y devolver la página HTML correspondiente (con la URL real y la acortada).
<li> Reconocer <em>GET /num</em> (para cualquier número num), y realizar la redirección correspondiente.
<li> Manejar las condiciones de error y realizar el resto de la funcionalidad.
</ol>


## Entrega


Has de tener un repositorio llamado X-Serv-18.1-Practica1 en tu cuenta en GitHub
que incluya el fichero de nombre 'practica1.py' que contenga las
instrucciones en Python para solucionar el ejercicio.

Se proporciona un script, check.py, para comprobar la entrega correcta
del ejercicio. El script de comprobación se ha de ejecutar desde terminal
pasándole como parámetro tu nombre de usuario en GitHub. Así, un ejemplo de
ejecución sería:

$ python check.py gregoriorobles
