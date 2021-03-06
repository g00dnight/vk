from .session import Session


class API(object):  # Singleton
    instance = None
    instance_args = None
    instance_kwargs = None

    class __API(object):
        def __init__(self, *args, **kwargs):
            self.session = Session(*args, **kwargs)

        def __getattr__(self, method_name):
            return RequestChain(self.session, method_name)

    def __init__(self, *args, **kwargs):
        if API.instance is None:
            if not args and not kwargs:
                RuntimeError('API instance is not initialized')
            API.instance = API.__API(*args, **kwargs)
            API.instance_args = args
            API.instance_kwargs = kwargs
        elif args and API.instance_args != args or \
                kwargs and API.instance_kwargs != kwargs:
            RuntimeError('Only one API instance is available')

    def __getattr__(self, name):
        return getattr(API.instance, name)


class RequestChain(object):
    __slots__ = ('_session', '_method_name')

    def __init__(self, session, method_name):
        self._session = session
        self._method_name = method_name

    def __getattr__(self, method_name):
        return RequestChain(
            self._session,
            self._method_name + '.' + method_name
        )

    def __call__(self, **method_args):
        return self._session.make_request(self._method_name, method_args)
