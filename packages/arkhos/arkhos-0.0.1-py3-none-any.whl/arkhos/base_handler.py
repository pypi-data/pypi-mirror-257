from collections import defaultdict
import datetime, json, time, traceback

from arkhos.http import HttpResponse, JsonResponse

# from arkhos import _global


def base_handler(event, context=""):
    start_time = time.time()

    request = Request(event)
    response = {}

    try:
        user_handler = get_user_handler()
        response = user_handler(request)
        if isinstance(response, (HttpResponse, JsonResponse)):
            response = response.serialize()
    except:
        # if False or _global.DEBUG:
        if False:
            trace = traceback.format_exc()
            response = HttpResponse(f"<pre>{trace}</pre>", status_code=500).serialize()
        else:
            response = JsonResponse(
                {"error": "500 Server Error"}, status_code=500
            ).serialize()

    finally:
        duration = time.time() - start_time
        """
        log("%s HTTP %s request" %(_global.APP_NAME, request["method"]),
            status_code=response.status_code, # bigtodo: user set status_code
             type=request["method"]) # todo: headers
        log_flush()
        """

    return response


def get_user_handler():
    """This returns the user's handler"""
    from main import arkhos_handler

    return arkhos_handler


class Request:
    """Represents a request"""

    def __init__(self, lambda_event):
        self.method = lambda_event.get("method")
        self.headers = lambda_event.get("headers", {})
        self.GET = lambda_event.get("GET", {})
        self.POST = lambda_event.get("POST", {})
        self.parsed_json = False

        # todo
        self.path = lambda_event.get("path")  # todo: cron

    @property
    def json(self):
        """Parse the request body. This will throw an error if request.body
        isn't valid json"""
        self.parsed_json = self.parsed_json or json.loads(self.POST)
        return self.parsed_json
