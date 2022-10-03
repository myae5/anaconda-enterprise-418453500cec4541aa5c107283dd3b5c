"""
This file is just a simple wrapper to allow intake-server to accept
anaconda-project specific flags. This isn't needed on a local machine,
only on Anaconda Enterprise.
"""

from __future__ import absolute_import, division, unicode_literals

import sys

from functools import wraps

from intake.cli.server.server import IntakeServer, tornado


class ServerIndexHandler(tornado.web.RequestHandler):
    """Index page with all available endpoints"""
    def initialize(self, cache, catalog, auth):
        self.cache = cache
        self.catalog = catalog
        self.auth = auth

    def get(self):
        self.render("templates/index.html", sources=self.catalog)


def add_index_page_handler(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        handlers = [
            (r"/", ServerIndexHandler,
             dict(catalog=self._catalog, cache=self._cache, auth=self._auth))
        ]
        handlers.extend(f(self, *args, **kwargs))
        return handlers
    return wrapper


IntakeServer.get_handlers = add_index_page_handler(IntakeServer.get_handlers)


def transform_cmds(argv):
    """
    Allows usage with anaconda-project by remapping the argv list provided
    into arguments accepted by intake.
    """
    replacements = {'--anaconda-project-port': '--port'}
    transformed = []
    skip = False
    for arg in argv:
        if skip:
            skip = False
            continue
        if arg in replacements.keys():
            transformed.append(replacements[arg])
        elif arg in {'--anaconda-project-iframe-hosts', '--anaconda-project-host'}:
            skip = True
        elif arg.startswith('--anaconda-project'):
            continue
        else:
            transformed.append(arg)
    return transformed


def main():
    from intake.cli.server.__main__ import main as intake_entry_point
    sys.argv = transform_cmds(sys.argv)
    intake_entry_point()


if __name__ == "__main__":
    main()
