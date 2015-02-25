.. _library:

=======================================
 Using Total Open Station as a library
=======================================

All the functionality implemented in Total Open Station can be used
independently, with the exception of the user interfaces.

In other words, the classes for reading specific formats and those for writing
well-known formats are entirely usable on their own.

This is a feature.

Example: a web app for converting total station data
====================================================

If you want to see how to write a web app to convert total station
data in 50 lines of Python code, check out `TOPS in the Cloud
<https://bitbucket.org/steko/tops-cloud/overview>`_. It is made with
`Flask <http://flask.pocoo.org/>`_ and shows how to use Total Open
Station as a programming library.

We think it's important to be able to use TOPS in this way as in any
other way (GUI, command-line), and this is one of the reasons why
there is no stable release yet: the TOPS API is still unstable.
