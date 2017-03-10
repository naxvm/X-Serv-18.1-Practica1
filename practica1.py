#! /usr/bin/python3

import webapp

class shortenApp(webapp.webApp):

    shortenedURLs = {}
    longURLs = {} # Almaceno como clave el nombre de recurso


    form = ('<form method="post">' +
            'Introduce tu URL:<br>' +
            '<input type="text" name="url">' +
            '<input type="submit" value="Acortar">' +
            '</form>') # El navegador dará los datos por POST a la misma página


    notFound = '<html><head><b>Error</b><br>Recurso no disponible</head></html>'

    lastIndex = 0


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
                        responseBody = (responseBody + '<br>' + longOne
                                    + ' -> ' + self.shortenedURLs[longOne])
                    responseBody = responseBody + '</html>'

            else:   # si me piden una URL acortada
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
            else:
                if newOne[0:7] != 'http://' and newOne[0:8] != 'https://':
                    # la página está mal pasada
                    newOne = 'http://' + newOne

                if newOne in self.shortenedURLs:
                    newIndex = self.shortenedURLs[newOne] # la página ya existía. La vuelvo a servir
                else:
                    newURL = ('/' + str(self.lastIndex)) # conversión para tener la barra
                    self.lastIndex = self.lastIndex + 1

                    self.shortenedURLs[newOne] = ('http://localhost:1234' + newURL)
                    self.longURLs[newURL] = newOne

                    returnCode = '200 OK';
                    responseBody = ('<html><head>Acortamiento realizado<br></head><body>' +
                    '<a href="' + self.longURLs[newURL] +'">URL larga</a><br>' +
                    '<a href="' + self.shortenedURLs[newOne] + '">URL corta</a>' + '</body></html>')






        return (returnCode, responseBody)










if __name__ == '__main__':
    app = shortenApp('localhost',1234)
