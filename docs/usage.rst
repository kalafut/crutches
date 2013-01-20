.. _usage::

Browser Interface
#################

.. note:: All development has been done on recent versions of Chrome, with spot testing
          on other browsers.

After you've built the documentation, open the resulting .html file in your browser. Templates can
vary widely in what and how they're presenting content, but for now we'll assume standard behavior
such as that provided in the *default* template.

Queries
-------
The default behavior is to filter what is in the search box, so when you open of the page initially
all content is shown. Entering query terms will reduce the results in real time. The query is
interpreted with the following rules:

* A term is a group of characters separate by one or more spaces.
* All searches are case and order insensitive.
* Terms are always AND'd together. Entering more terms will only reduce the result set.
* A match can occur anywhere in the string (i.e. "re" is found in "present") unless...
* A term beginning with a caret (^) will only match at the beginning of a word/line
* A term is search anything the entry key, text, **Section** and **Project**.
* A term beginning with a forward slash (/) will only match **Project** names.
* A term beginning with a double forward slash (//) will only match **Section** names.

.. note:: The terms are searched for as strings, not regexes (mentioned because I've gone back and forth on this).

Example queries
^^^^^^^^^^^^^^^

=============            =======
Query                    Result set
=============            =======
python                   contains "python" in the entry text, or belongs to the python project
python string            restricts previous results to those contain "string"
ter                      matches "ter" everywhere (e.g. would match "filter")
^ter                     matches "ter" at the beginning of a word (e.g. "ternary")
/python                  elements in python project
//^re                    elements in "re" sections. "re" is so common that "^" is almost mandatory.
/perl //^re              elements of the "re" section of the Perl project
=============            =======

Project enable/disable
#####################

Keyboard commands
#################

A couple of helpful keyboard commands the interface offers:

* **ESC** will scroll to the top of the window, clear and set focus on the search box.
* **ENT** will open the first hyperlink in the result set.

