.. _templates:

##############
Template Guide
##############

Templates allow complete flexibility in how content is presents and even acted upon. The ``crutch`` parser will provide the template
with virtually all of the input data (after being massaged and filter based on configuration), and it's up to the template logic to
display it. This arrangement makes it easy to customized the output to your liking, or come up with an entirely different scheme altogether.

It is important to first understand the steps taken to parse and prepare the template:

1. The template file specified by the configuration is loaded.
2. References to external JavaScript and stylesheets are located
3. Scripts and stylesheets from the ``assets`` directory (and below) are loaded. Compilation will fail if they're not found.
4. External script and stylesheet tags are replaced with the actual file contents.
5. Everything within the templates ``<body>`` tag is *moved* into a JavaScript variable.
6. All reference content is placed in a JavaScript.
7. The Crutch.render() function is called, which should populate the template with ref card data, and target the result back in the `<body` section.

As you can see, the rendering takes place in JavaScript, in the client. (See xxxx for why). The means that we need a JavaScript templating library for this approach to work. Fortunately there are many to choose from.

API
####

The ``crutch`` parser will generate a single HTML file the includes the template and content. Your template will also include ``crutch.js``, which provides functions that are used by most templates. In this section we'll describe the data and functions that your template has access to and/or must provide.


Crutch object
-------------


.. attribute:: projects

    An array of :ref:`project`. This will contain all of the projects matching the user's
    configuration, in the order that they specified (or alphabetically if unspecified).

.. _project:

Project objects
---------------
.. attribute:: name

    The project name.

.. attribute:: entries

    An array of all :ref:`entry`.

.. attribute:: uid

    An unique ID for this project element. This ID should be assigned to ``data-uid`` for the project name
    markup in order for filtering to work properly.

.. _entry:

Entry objects
--------------


.. attribute:: key

    The element to be described, such as an API keyword, command, etc. This is usually the left
    column of a reference table. This term should be hyperlinked in the output if there is a URL
    associated with the entry.


.. attribute:: description

    The text to describe **key**. This is usually the right column of a reference table.


.. note:: The **key** element is optional, but the **description** is not. Template should test for the presence of
   **key** and render accordingly (usually by consolidating to a single column those rows that have no **key**.
