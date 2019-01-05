
import time
import solve_expr
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
#HOST_NAME = '104.233.107.250'
HOST_NAME = 'localhost'
PORT_NUMBER = 9000

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/":
                self.path = "expr=3+45*21:7"
            print(self.path)
            path = urllib.parse.unquote(self.path)
            pars  = path.split("=")
            cmd = pars[0]
            expr = pars[1]
            print("espressione:" + expr)
            content =  "<!DOCTYPE html>\n"
            content += "<html><head><title>Calcolatore Espressioni matematiche passo dopo passo</title></head>\n"
            content += '<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.1.1/katex.min.css">\n'
            content += '<script src="http://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.1.1/katex.min.js"></script>\n'
            content += '<body>\n'
            content += '<div style="font-size:40px">Risolvi espressioni con Passaggi! </div>' + "<br> <br>"
            content += '<form action="http://{:}:9000"  method="get"  >\n'.format(HOST_NAME)
            content +=  'Inserisci espressione:<br>'
            content +=  '<input type="text" name="expr" value="{:}" style="margin-left:auto;  margin-right:auto; width:600px;"><br>'.format(expr)
            content +=  '<input type="submit" value="Calcola">'
            content +=  '</form>' 
            content += "<br>" + '<div">Qui trovi i tuoi passaggi</div>' + "<br>"
            try:
                steps = solve_expr.calc(expr)

                content += '<p id="katex-container"></p>'

                content += '<script>\n'
                content += "var div = document.getElementById('katex-container');\n"
                
                for s in steps:
                    content += 'div.innerHTML += katex.renderToString("={:}", {{throwOnError: false, displayMode: true}}) + "<br> <br>"\n'.format(s.replace("\\","\\\\"))
                content += '</script>\n'    
            except Exception as e:
                lines = str(e).split("\n")
                content += '<p id="katex-container">'
                content += "Errore nell'espressione:<br>"
                for line in lines:
                    content += line + "<br>"
                content += "</p>"

            content += "</body></html>"


        except Exception as e:
            print(str(e))

            content= "Errore inatteso"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode())

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
