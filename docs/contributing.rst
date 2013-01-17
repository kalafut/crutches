.. _contributing:

Licensing
#########
The Crutches content is provided under the Creative Common Attribution-ShareAlike 3.0
Unported license. This ensures that the content can be broadly used and shared.

**Important**: if you are creating content and contributing it to the Cruthes repository,
you are agreeing for it to be provided under this license.

I think most people writing content will probably have little issue with this requirement
(and if you do, don't contribute). The trickier bit is trying to make sure that copied
and derived content from elsewhere is acceptable and properly attributed. First, all
content should be attributed whenever possible. This is just good etiquette. But in many
cases, attribution is **required**. You must review the copyright and/or licensing of
text before bringing it in, and often you will need to add or update the ``attribution``
tag.

Some content cannot be imported. If material bears a copyright with no additional licensing
expressly given, you can't assume you can import it. You may contact the author to seek
permission, but be sure to explain the CC license that you're seeking. The more difficult
to.....  ref GFDL.




Project organization
####################

Good project organization is important both for people wanting to create
or maintain material, and for those wanting to consume it. Developing a
taxonomy for just about anything is difficult. Any structure will be a poor
fit for some items, and people will have strong opinions on how to arrange
things.

A **Project** is defined a folder that has the file ``_project.yml`` in it. To be
useful that same folder will contain one or more section files (also YAML). The
name of the folder is not significant for the generated output, but it is
important for the maintainability of the Crutches project.

TBD: whether directories can be allowed to not have a ``_project.yml`` file in it.::


    projects
        JavaScript
            _project.yml
            jQuery
                _project.yml
                selectors.yml
                traversing.yml
                jQueryUI
                    _project.yml
                    interactions.yml
                    widgets.yml
                    effects.yml
            Array.yml
            String.yml
        Python
            _project.yml
            Django
                _project.yml
                db.models.yml
            re.yml
            shutil.yml
        tools
            _project.yml
            Emacs
                _project.yml
            VIM
                _project.yml

