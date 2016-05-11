from tornado.web import URLSpec as route

from .handlers.main import MainHandler

routes = [
    route(r"/", MainHandler, name="v1_main_handler")
]