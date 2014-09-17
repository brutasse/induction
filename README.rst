Induction
=========

A simple web framework based on asyncio. Experimental, use at your own risk.

.. image:: http://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Tesla%27s_induction_motor.jpg/320px-Tesla%27s_induction_motor.jpg
   :alt: Tesla's induction motor

Induction is the phenomenon that drives asynchronous motors. Pictured above is
`Tesla's induction motor`_.

.. _Tesla's induction motor: http://en.wikipedia.org/wiki/Induction_motor

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

    from asyncio import coroutine
    from induction import Induction
    app = Induction(__name__)

    @app.route('/slow'):
    @coroutine
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

* ``after_request(func)`` registers a function to be called after all request
  handlers. Works like ``before_request``.

* ``handle_404(request, [response])``: error handler for HTTP 404 errors.

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
