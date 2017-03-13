#! /usr/bin/python3

import webapp
import csv

class shortenApp(webapp.webApp):

    def initializeDicts(self):
        # primero, leo el diccionario existente, y lo importo a las listas
        try:
            self.newDB = False
            with open(self.filename) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.shortenedURLs[row['larga']] = row['corta']
                    print(row['larga'], row['corta'])
                    self.longURLs[row['corta']] = row['larga']
        except FileNotFoundError:
            pass # No existe el fichero. Los diccionarios se quedan vacíos
            print('FileNotFoundError')
            self.newDB = True
        except KeyError:
            print('Error: el diccionario está dañado. Comprueba que las cabeceras de CSV estén colocadas al principio')
            pass  # Está vacío. Se queda como está

    def updateDicts(self,longURL,shortURL):
        #shortURL = ('http://localhost:1324' + shortURL)
        self.shortenedURLs[longURL] = shortURL
        self.longURLs[shortURL] = longURL # actualizo los diccionarios

        with open(self.filename, 'a') as csvfile:    # actualizo el csv
            fieldnames = ['larga', 'corta']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if self.newDB:
                writer.writeheader()
                self.newDB = False;

            writer.writerow({'larga': longURL, 'corta': shortURL})


    def __init__(self, hostname, port, filename):

        self.shortenedURLs = {}
        self.longURLs = {} # Almaceno como clave el nombre de recurso

        self.filename = filename

        self.form = ('<form method="post">' +
            'Introduce tu URL:<br>' +
            '<input type="text" name="url">' +
            '<input type="submit" value="Acortar">' +
            '</form>') # El navegador dará los datos por POST a la misma página


        self.notFound = '<html><head><b>Error</b><br>Recurso no disponible</head></html>'

        self.emptyRequest = ('<html><head><b>Error</b><br>Has enviado una URL vacia.<br>' +
                    '<a href="http://localhost:1234">Vuelve a intentarlo</a></head></html>')

        self.initializeDicts()

        self.lastIndex = len(self.shortenedURLs) # para no machacar las ya existentes

        webapp.webApp.__init__(self, hostname, port) # método init de la clase antigua
        # tiene que ir lo último porque ya pone el servidor en marcha

    def parse(self, request):
            # De momento devolverá el método y el recurso que se piden
        request = request.decode('utf-8')
        if len(request) > 0:
            (verb, resource) = request.split()[:2]

            if verb == 'POST':  # parse también va a buscar la URL en caso de ser un POST
                newOne = request.split('url=')[1]


            else:
                newOne = None
            return (verb, resource, newOne)

        else:   # firefox envía una petición vacía, hay que tratarla para que no se caiga
            return ('POST', '/', None)
            # lo redirigimos a una página que process tratará como 404


    def process(self, parsedRequest):

        (verb, resource, newOne) = parsedRequest  # para no violar mucho la sintaxis del paquete webapp
        returnCode = str(200)   # Por defecto, sin error (200 OK)


        if verb == 'GET':
            if resource == '/':
                returnCode = '200 OK'
                responseBody= '<html>' + self.form

                if len(self.shortenedURLs) != 0:    # Imprimo la lista de las URLs ya acortadas (funciona)
                    responseBody = responseBody + '<body><b><u>Listado de las URLs que ya han sido acortadas:</u></b>'
                    for longOne in self.shortenedURLs:
                        responseBody = (responseBody + '<br>' + '<a href="' + longOne +
                                        '">' + str(longOne) + '</a>' + ' -> <a href="' + self.shortenedURLs[longOne] +
                                        '">' + str(self.shortenedURLs[longOne]) + '</a>"')
                    responseBody = responseBody + '</html>'

            else:   # si me piden una URL acortada
                resource = ('http://localhost:1234' + resource)

                if resource in self.longURLs: # si la acortada está en la lista:
                    returnCode = ('301 Moved Permanently\r\n'
                    + 'Location: ' + self.longURLs[resource])

                    responseBody = '<html><head><b>Redirecting...</b></head></html>'
                else: # Me han pedido una página que aún no he creado
                    returnCode = '404 Not Found'
                    responseBody  = self.notFound

        else: # verb == 'POST'
            if newOne == None:
                returnCode = '404 Not Found'
                responseBody = self.notFound
            elif len(newOne) == 0:
                returnCode = '404 Not Found'
                responseBody = self.emptyRequest
            else:
                if newOne[0:7] != 'http://' and newOne[0:8] != 'https://':
                    # la página está mal pasada
                    newOne = 'http://' + newOne

                if newOne in self.shortenedURLs:
                    newIndex = self.shortenedURLs[newOne] # la página ya existía. La vuelvo a servir
                else:
                    newURL = ('http://localhost:1234/' + str(self.lastIndex)) # conversión para tener la barra
                    self.lastIndex = self.lastIndex + 1

                    self.updateDicts(newOne, newURL)

                    returnCode = '200 OK';

                    responseBody = ('<html><head>Acortamiento realizado<br></head><body>' +
                    '<a href="' + self.longURLs[newURL] +'">URL larga</a><br>' +
                    '<a href="' + self.shortenedURLs[newOne] + '">URL corta</a>' + '</body></html>')






        return (returnCode, responseBody)










if __name__ == '__main__':
    app = shortenApp('localhost',1234, filename='direcciones.csv')
