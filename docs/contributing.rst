.. _contributing:

Unicode
#######

The toolchain supports Unicode, so you are able to include "special" characters
as needed. But be on the lookout for inadvertant subtitions that may get introduced
if you're importing content from elsewhere. For example, the replacement of quotes
(e.g. \` -> ‘), often done to enhance the appearance of a website, can cause annoying
hiccups when later copying-and-pasting from a cheat sheet into code. In general, I'd
recommend keeping sections free of such characters unless there is a good reason not to.

There is tool support to help you. (not yet!) TODO: flagged non-standard(?) characters.

(Talk about editors/YAML/UTF-8?)

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

