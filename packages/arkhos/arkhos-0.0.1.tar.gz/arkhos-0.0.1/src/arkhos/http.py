import datetime
import decimal
import json
import uuid

from arkhos.utils import DjangoJSONEncoder
from arkhos.templates import render_template


class HttpResponseBase(object):
    def __init__(self, content, status_code=200, headers=None):
        self.content = content

        self.headers = {}
        if headers:
            self.headers = headers

        if "content-type" not in self.headers:
            self.headers["content-type"] = "text/html"

        if status_code is not None:
            try:
                self.status_code = int(status_code)
            except (ValueError, TypeError):
                raise TypeError("HTTP status code must be an integer.")

            if not 100 <= self.status_code <= 599:
                raise ValueError("HTTP status code must be an integer from 100 to 599.")

    def serialize(self):
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format
        # big todo: we're off lambda

        response = {
            "status_code": self.status_code,
            "body": self.content,
            "headers": self.headers,
        }
        return response

    def __repr__(self):
        return f"<{self.__class__.__name__} status_code={self.status_code} {self.headers['content-type']}>"


class HttpResponse(HttpResponseBase):
    def __init__(self, content, **kwargs):
        if not isinstance(content, str):
            try:
                self.content = str(content)
            except (ValueError, TypeError):
                raise TypeError(
                    "HttpResponse content %s could not be converted to a string"
                    % (type(content),)
                )
        # Big todo jinja escape
        super(HttpResponse, self).__init__(content, **kwargs)


class JsonResponse(HttpResponseBase):
    # https://docs.djangoproject.com/en/2.2/_modules/django/http/response/#HttpResponse

    def __init__(
        self,
        data,
        headers = None,
        encoder = DjangoJSONEncoder,
        json_dumps_params = None,
        **kwargs,
    ):
        self.headers = {}
        if headers:
            self.headers = headers

        if json_dumps_params is None:
            json_dumps_params = {}

        if "content-type" not in self.headers:
            self.headers["content-type"] = "application/json"

        content = json.dumps(data, cls=encoder, **json_dumps_params)
        super(JsonResponse, self).__init__(content=content, **kwargs)

def render(template_path, context, status_code=200, headers=None):
    """
        Return an HttpResponse from a template and context eg.
        arkhos.render(
          "path/to/template.html",
          {"key": "value", ...},
          status_code = 200,
          headers = {...}
        )
    """
    return 0
