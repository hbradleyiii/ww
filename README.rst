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
``WW_File`` is a class from which all other classes representing files derive.
It provides a basic interface for consistency. It extends ``ext_pylib.file``
File class.  Currently, its only method is ``repair()`` which offers a
convinient wrapper for the ``verify()`` method with the repair flag set to
``True``.

Module: htaccess
~~~~~~~~~~~~~~~~
The ``ww.htaccess`` module contains the ``Htaccess`` class which represents a
website's htaccess file and provides an interface for creating htaccess files.

Website htaccess files are generally a collection of 'sections' that are
responsible for particular things. For instance, a WordPress website will often
have a section like:

    # BEGIN WordPress
    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.php$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.php [L]
    </IfModule>

    # END WordPress

The ww package comes with three template files representing htaccess sections.

* wordpress-htaccess.template

  This is the generic WordPress htaccess file.

* wordpress-hardened-htaccess.template

  This is a hardened WordPress htaccess file per WordPress'
  `recommendations <http://codex.wordpress.org/Hardening_WordPress>`.

* 5g-htaccess.template

   This is a generic htaccess file that adds an extra layer of security. See
   https://perishablepress.com/5g-blacklist-2013/


An ``Htaccess`` class is initialized like a normal ``WW_File`` with an
additional 'section' attribute. ``atts['section']`` is a list of 0 or more
dicts used to initialize an ``HtaccessSection`` file. This dict has the form:

    { 'name' : 'section_name', 'path' : '/path/to/section_template' }

An ``HtaccessSection`` class is merely a wrapper around an
``ext_pylib.file.Section`` class. See the ext_pylib documentation for more
information.

If the htaccess file doesn't yet exist, all sections are applied to the in
memory data at initialization. They are saved to disk by calling the ``create``
method. If the file does already exist, the existing data is loaded into
memory.

The ``verify`` method first calls the parent ``verify`` which checks existance,
permissions, and ownership. Then it checks to make sure any appropriate
sections are applied. It will also warn of sections that are applied but
contain an old or modified version of the section. If the repair flag is set to
``True`` the method attempts to correct any errors. It does not affect any data
outside the 'sections'. If the sections are malformed, it raises an error.

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
