import json
import re


class HttpRequestBody:
    method = ''
    path = ''
    body = ''

    def __init__(self, request):
        self.request = request
        self.method, self.path = re.findall(r'(.*?) (.*?) HTTP/1.1\r\n', self.request)[0]
        data = re.findall(r'\r\n\r\n(.*)', self.request, re.S)[0]
        if data:
            self.body = json.loads(data)