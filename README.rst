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
