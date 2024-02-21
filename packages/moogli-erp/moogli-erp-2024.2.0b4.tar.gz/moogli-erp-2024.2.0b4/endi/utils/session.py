"""
    Custom beaker session handling allowing to use a remember me cookie
    that allows long time connections
"""
import logging

from beaker.session import SessionObject
from pyramid_beaker import session_factory_from_settings


logger = logging.getLogger(__name__)


def get_session_factory(settings):
    """
    Wrap the beaker session factory to add longtimeout support
    """
    factory = session_factory_from_settings(settings)

    class EndiSessionObject(factory):
        """
        Our pyramid session object
        """

        _longtimeout = int(factory._options.pop("longtimeout"))

        def __init__(self, request):
            options = self._options.copy()
            if "remember_me" in list(request.cookies.keys()):
                options["timeout"] = self._longtimeout

            SessionObject.__init__(self, request.environ, **options)

            def session_callback(request, response):
                exception = getattr(request, "exception", None)
                if exception is None or self._cookie_on_exception and self.accessed():
                    self.persist()
                    headers = self.__dict__["_headers"]
                    if headers["set_cookie"] and headers["cookie_out"]:
                        response.headerlist.append(
                            ("Set-Cookie", headers["cookie_out"])
                        )

            request.add_response_callback(session_callback)

    return EndiSessionObject
