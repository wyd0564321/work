import re

def app(environ, start_response):
    path = environ['PATH_INFO'].split('/')[1]
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    result = '';
    m = re.match('.*\.html$',path)

    if(m):
        try:
            for line in open(path):
                result+=line
        except FileNotFoundError as e:
            result+='404Not found'
    else:
        result+=hello(path)
    return result

def hello(path):
    return 'hello '+path
