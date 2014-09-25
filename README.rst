Induction
=========

.. image:: https://travis-ci.org/brutasse/induction.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/brutasse/induction

A simple web framework based on asyncio.

.. image:: https://raw.githubusercontent.com/brutasse/induction/master/tesla.jpg
   :alt: Tesla's induction motor

Induction is the phenomenon that drives asynchronous motors. Pictured above is
`Tesla's induction motor`_.

.. _Tesla's induction motor: http://en.wikipedia.org/wiki/Induction_motor

Installation
------------

::

    pip install induction

Usage examples
--------------

If you know `express`_ and/or `Flask`_, you'll feel right at home.

.. _express: http://expressjs.com/
.. _Flask: http://flask.pocoo.org/

Synchronous route
`````````````````

.. code-block:: python

    from induction import Induction
    app = Induction(__name__)

    @app.route('/')
    def index(request):
        return app.render_template('index.html')

Async route
```````````

.. code-block:: python

    import asyncio
    from induction import Induction
    app = Induction(__name__)

    @app.route('/slow'):
    @asyncio.coroutine
    def slow(request, response):
        yield from asyncio.sleep(10)
        response.write('Hello, world!')

Handlers
--------

Handlers are decorated with ``@app.route(url_pattern)``. Routes are managed by
the `Routes`_ library.

.. _Routes: https://routes.readthedocs.org/en/latest/

Handlers have several way to send data back to the client:

* *returning*: synchronous routes can return data directly. The return values
  are passed to the response object. Supported return values are:

  - A string or bytes object, which becomes the body of the response. A
    default status of ``200 OK`` and mimetype of ``text/html`` are added.

  - A tuple of ``(response, headers, status)``, in any order and with at least
    one item provided. ``headers`` can be a list or a dictionnary.

* *writing*: handlers can be defined to accept two arguments, ``request`` and
  ``response``. They can then directly write data to the response.

``Induction`` objects
---------------------

The ``Induction`` constructor accepts the following arguments:

* ``name``: the name for your app.

And the following keyword arguments:

* ``template_folder``: path to the folder from which to load templates.
  Defaults to ``'templates'`` relatively to the current working directory.

The following methods are available on ``Induction`` instances:

* ``route(path, **conditions)``: registers a route. Meant to be used as a
  decorator::

      @app.route('/')
      def foo(request):
          return jsonify({})

* ``before_request(func)``: registers a function to be called before all
  request handlers. E.g.::

      @app.before_request
      def set_some_header(request, response):
          request.uuid = str(uuid.uuid4())
          response.add_header('X-Request-ID', request.uuid)

  ``before_request`` functions are called in the order they've been declared.

  When a ``before_request`` function returns something else than ``None``, all
  request processing is stopped and the returned data is passed to the
  response.

* ``after_request(func)`` registers a function to be called after all request
  handlers. Works like ``before_request``.

* ``handle_404(request, [response])``: error handler for HTTP 404 errors.

* ``error_handler(exc_type)``: registers a function to be called when a
  request handler raises an exception of type ``exc_type``. Exception handlers
  take the request, the response and the exception object as argument::

      @app.error_handler(ValueError):
      def handle_value_error(request, response, exception):
          response.add_header("X-Exception", str(exception))

  Note that the response may have been partially sent to the client already.
  Depending on what your application does, it might not be safe to set headers
  or even send data to the response.

  Setting ``exc_type`` to ``None`` lets you register a catch-all error handler
  that will process all unhandled exceptions::

      @app.error_handler(None):
      def handle_exception(request, response, exception):
          # Send exception to Sentry
          client = raven.Client()
          client.captureException()

* ``render_template(template_name_or_list, **context)``: loads the first
  matching template from ``template_name_or_list`` and renders it using the
  given context.

Response objects
----------------

The following attributes and methods are available on ``Response`` objects:

* ``status``, ``status_line``: the HTTP status code and line for this
  response.

* ``write(chunk, close=False, unchunked=False)``: writes a chunk of data to
  the reponse.

  If ``chunk`` is a string, it'll be encoded to bytes.

  If ``close`` is ``True``, ``write_eof()`` is called on the response.

  If ``unchunked`` is ``True`` a ``Content-Length`` header is added and the
  response will be closed once the chunk is written.

* ``redirect(location, status=302)``: redirects to ``location`` using the
  given status code.

Releases
--------

* **0.2** (2014-09-25)

  * 404 error returns HTML by default.

  * Ability to set a catch-all error handler, e.g. for Sentry handling.

* **0.1** (2014-09-19)

  * Initial release.
