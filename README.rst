ww
##
A virtual host website deployment and management tool for Apache and WordPress
==============================================================================

.. image:: https://www.quantifiedcode.com/api/v1/project/5e43e90cc7344452b49c16c19666789f/badge.svg
    :target: https://www.quantifiedcode.com/app/project/5e43e90cc7344452b49c16c19666789f
    :alt: Code issues

----

This is a work in progress. Use at your own risk.

ww is a collection of modules packaged together to create a program that is
useful for installing and managing a number of virtualhost websites (WordPress
in particular). It helps automate the process of creating appropriate
directories with the correct permissions, creating a virtualhost file for
Apache, and installing WordPress and setting up its MySQL database. This
application solves the problem of having to manually repeat this process. It
further helps with maintenance by verifying that everything is in order and
it helps with removal by undoing everything it originally did. Finally, the
application helps with packing and unpacking entire WordPress websites to move
the site from a development server to a live server.

This software is developed for a very specific `Environment`_, but should be
easy to modify and extend to other use cases. It assumes your server OS is
Ubuntu running Apache (and for installing WordPress, PHP and MySQL). For
information on extending ww see `Package Internals`_.

To run ww, the Python modules `ext_pylib <https://www.github.com/hbradleyiii/ext_pylib>`_,
`MySQL-python <https://pypi.python.org/pypi/MySQL-python>`_ (for wordpress
installations), and `requests <https://github.com/kennethreitz/requests>`_
must be installed. Testing ww requires `pytest <http://pytest.org/>`_.


Installation and Usage
======================

Installing ww
--------------------

.. code:: bash

    $ git clone git@github.com:hbradleyiii/ww.git
    $ cd <project directory>
    $ pip install -e .

Running Tests
-------------

.. code:: bash

    $ cd <project directory>
    $ py.test

Usage
-----

.. code:: bash

    $ ww install example.com
    $ ww verify example.com
    $ ww remove example.com

Environment
===========
TODO

Package Internals
=================

Class: WW_Files
---------------
TODO

Module: htaccess
~~~~~~~~~~~~~~~~
TODO

Module: vhost
~~~~~~~~~~~~~
TODO

Module: wp_config
~~~~~~~~~~~~~~~~~
TODO

Class: Website
--------------
TODO

Class: WP_Website
-----------------
TODO

Class WebsiteDomain
-------------------
TODO
