#!/usr/bin/python
"""
A tiny pythonbased webserver used to serve a small page on my local network
and run different python commands based on the recieved GET-requests.

It tries to limit access to the subdirectories of WEBROOT and serves index.html
as the default page.

Only a few file types are handled, se mime types in code for details.
"""

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from webbrowser import open as openurl
import os 
import requests
import subprocess

PORT_NUMBER = 8000

WEBROOT='/home/pi/pyweb/www/'
CMD_TVOFF='/home/pi/script/CMD_TVOFF.py'

WEBROOT=os.path.abspath(WEBROOT)

print "Webserver root directory: " + WEBROOT


# BaseHTTPRequestHandler used by HTTPServer
class myHandler(BaseHTTPRequestHandler):

    #Handler for GET requests
    def do_GET(self):
        print "DEBUG: " + self.path
        self.suff = self.path.split('?',1)[-1]
        self.path = self.path.split('?',1)[0]

        if self.suff==self.path:
            self.suff = ''
        else:
			"""
			Let us handle and react to variables, such as ./index.html?m=foo&p=bar
			"""
            if self.suff.startswith('m&'):
                 i = self.suff[2:]
                 if i.startswith('p='):
					 print 'Media power command: [' + i[2:] + ']'
					 data = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Power>'+i[2:]+'</Power></Power_Control></Main_Zone></YAMAHA_AV>'
					 res = requests.post(url='http://192.168.1.10/YamahaRemoteControl/ctrl', data=data, headers={'Content-Type': 'text/xml'})
                 elif i.startswith('c='):
                     print 'Media channel command: [' + i[2:] + ']'
                     data = '<YAMAHA_AV cmd="PUT"><Main_Zone><Input><Input_Sel>'+i[2:]+'</Input_Sel></Input></Main_Zone></YAMAHA_AV>'
                     res = requests.post(url='http://192.168.1.10/YamahaRemoteControl/ctrl', data=data, headers={'Content-Type': 'text/xml'})
                 elif i.startswith('v='):
                     print 'Media volume command: [' + i[2:] + ']'
                     data = '<YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Lvl><Val>'+i[2:]+'</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume></Main_Zone></YAMAHA_AV>'
                     res = requests.post(url='http://192.168.1.10/YamahaRemoteControl/ctrl', data=data, headers={'Content-Type': 'text/xml'})
                 elif i=='tvoff':
                     subprocess.call(["python", CMD_TVOFF])
                 else:
                     print 'Unknown media command: [' + i + ']'
                


        if self.path.endswith('/'):
            self.path= self.path + "index.html"

        try:
            #Allowed file endings/mime types

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".htm"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open file requested and send it
				#Make sure the reuested path is inside our webroot
                self.path=os.path.abspath(os.path.join(WEBROOT, os.path.relpath(self.path.lstrip('/'))))
                if self.path.startswith(WEBROOT):
	                print "Request path: " + self.path
                    f = open(self.path) 
                    self.send_response(200)
                    self.send_header('Content-type',mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                else:
                    print "Invalid path: " + self.path
                    self.send_error(404,'File Not Found: %s' % self.path)
            return


        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

try:
    #Create a web server and set the handler function
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    server.serve_forever()

except KeyboardInterrupt:
    print 'Shutting down the web server'
    server.socket.close()
