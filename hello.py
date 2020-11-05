def application(environ,start_response):
    data = '\n'.join(environ['QUERY_STRING'].split('&'))
    data = data.encode()
    status = '200 OK'
    headers = [('Content-Type','text/plain')]
    start_response(status,headers)
    return [data]
