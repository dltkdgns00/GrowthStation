import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import importlib
import json
import glob
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape
from cgi import FieldStorage, parse_header, parse_multipart
import subprocess

def errlog(a):
    sys.stderr.write(a+"\n")

def call_function(function_name, function_data):
    files = glob.glob("./func*_*.py")[::-1]
    
    for file in files:
        base_name = os.path.basename(file)
        module_name = base_name.split('.')[0]

        # Import the module
        module = importlib.import_module(module_name)
        # Reload to get the latest version
        module = importlib.reload(module)

        # Check if the module has the desired function
        function_scv_name = "func_"+function_name
        if not hasattr(module, function_scv_name): continue

        try:
            function = getattr(module, function_scv_name)
            return function(function_data)
        except AttributeError as e:
            errlog(f"[{base_name}]Caught an attribute error: {e}")
            pass
    # If the function is not found in any of the modules, return None
    return {"data":f"[{function_name}] not defined", "status":"fail"}

def application(environ, start_response):

    if environ['REQUEST_METHOD'].upper() == 'POST':
        content_type = environ.get('CONTENT_TYPE')

        data = {}
        if content_type.startswith('multipart/form-data'):
            form = FieldStorage(fp=environ['wsgi.input'], environ=environ)
            for field in form.keys():
                #errlog(field)
                data[field] = form[field].value
        else:
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0

            request_body = environ['wsgi.input'].read(request_body_size)
            form = parse_qs(request_body)
            for field in form.keys():
                data[field.decode("utf-8")] = form[field][0].decode("utf-8")
    else: # GET
        form = parse_qs(environ['QUERY_STRING'])
        data = {}
        for field in form.keys():
            data[field] = form[field][0]

    #check func
    func = data.get('func', '')
    errlog("func[{}] type: {}".format(func, type(func)) )

    os.chdir(os.path.dirname(__file__))
    if func == "websocket":
        subprocess.Popen( ["sudo", "-u", "pi", "bin/wssctl.sh", data['action']] )
        response = {"data":f"{func}: {data['action']} @ {str(os.getcwd())}", 
                    "status":"success"}

    elif func != '':
        #data.pop("func")
        response = call_function(func, data)

    else:
        response = {"data":"Growth Station!\n"
                    , "status":"success"}

    output = bytes(json.dumps(response), "utf-8")
    response_len = str(len(output))
    """
    if (len(output) > 200):
        errlog(f"RESPONSE: {func} length [{response_len}]...")
    else:
        errlog(f"RESPONSE: {response}")
    """
     
    status = '200 OK'
    response_headers = [('Content-type', 'application/json'),
                        ('Content-Length', response_len)]
    start_response(status, response_headers)
    return [output]

if __name__ == "__main__":
    httpd = make_server('localhost', 8051, application)
    httpd.serve_forever()
