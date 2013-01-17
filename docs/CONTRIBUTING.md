## Project organization

Good project organization is important both for people wanting to create
or maintain material, and for those wanting to consume it. Developing a
taxonomy for just about anything is difficult. Any structure will be a poor
fit for some items, and people will have strong opinions on how to arrange
things.

A **Project** is defined a folder that has the file `_project.yml` in it. To be
useful that same folder will contain one or more section files (also YAML). The
name of the folder is not significant for the generated output, but it is
important for the maintainability of the Crutches project.

TBD: whether directories can be allowed to not have a `_project.yml` file in it.


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

