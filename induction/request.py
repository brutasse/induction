__all__ = ['Request']


class Request:
    def __init__(self, raw_request):
        (self.method, self.path, self.version, self.headers,
         self.should_close, self.compression) = raw_request
        if '?' in self.path:
            self.path, qs = self.path.split('?', 1)
            # TODO parse qs
            print(qs)

        # TODO case-insensitive header access

    def __repr__(self):
        return '<Request: "{method} {path} {http_version}">'.format(
            method=self.method, path=self.path, http_version=self.http_version)

    @property
    def http_version(self):
        return 'HTTP/{0}'.format('.'.join(map(str, self.version)))
