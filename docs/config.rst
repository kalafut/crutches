.. _config:

Configuration
#############

All keys are required.

.. attribute:: include

    An array of the projects and/or sections to include. If the array is empty then
    all projects and sections will be included.

.. attribute:: exclude

    An array of the projects and/or sections to exclude. If the array is empty then
    no projects or sections will be excluded.

.. attribute:: template

    Name of the template to render (without extension). The file must exist in the *templates* directory.

Project/Section naming convention
----------------------------------

Content is broken down into Projects and Sections.  A Project contains one or more sections. Every Project
and Section has a name (specified in the .yml files). To refer to project and sections, separate the two
with a double forward slash::

    Django//templates   # 'template' section within the 'Django' project

Projects may be nested. This is used to help organize the content library as well as to allow one to precisely
specify which project is being referred to. Nested projects are separated with a single forward slash::

    Python/Django//templates   # 'template' section within the 'Django' project located under the 'Python' project

Note: Sections may not be nested.

