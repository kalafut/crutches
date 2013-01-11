# Crutches

## Goals

* Create useful developer reference material and make it available under a permissive license.
* Develop conventions that allow people to easily contribute to the library.
* Provide a tool to combine select material into a searchable, single-file reference document.

## Status

* Base functionality is coming along reasonably well. I would like to get some nicer sample templates done as well as provide more sample material.
* Lots of back and forth on some of the finer points of the YAML schema. I'd like to wrap this up ASAP and tweak later.

# Installation

## Prerequisites

* PyYaml

## Configuration

* YAML references (& and \*)  will be flatted in include/exclude sections to simplify files groups.
* Include spec:  ^Python/shutil

## Content Guide

Entries are a collection of one or two content elements and optional options array. If a two content blocks are provided,
the first is considered the "key" and the second the "description". These are typically shown as two columns in the output.
If a key is present, it can be used as part of the automatic URL generation.

Project/section division.
How to handle packages, such as the bazillion in PyPy?  Are they projects?  (Probably)
How to handle http://www.cpan.org/modules/01modules.index.html?

Sample file types (from Ack):

* actionscript
* ada
* asm
* batch
* binary
* cc
* cfmx
* clojure
* cpp
* csharp
* css
* delphi
* elisp
* erlang
* fortran
* go
* groovy
* haskell
* hh
* html
* java
* js
* jsp
* lisp
* lua
* make
* mason
* objc
* objcpp
* ocaml
* parrot
* perl
* php
* plone
* python
* rake
* ruby
* scala
* scheme
* shell
* smalltalk
* sql
* tcl
* tex
* text
* tt
* vb
* verilog
* vhdl
* vim
* xml
* yaml

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

<pre>
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
</pre>

### URLs


### Options

* URL
* Escape HTML
* no markdown

* A single content string
## Template Guide

### Processing

Crutch uses Handlebars templates to generate the aggregate output. The parsing of the template goes roughly like:

1. Load the template file specified by the configuration.
2. Search for references to external Javascript and stylesheets.
3. Load scripts and stylesheets from the Assets directory. (Compilation will fail if they're not found.)
4. Create an single HTML file that contains all .js and .css assets, reference card data assigned to a variable, the template assigned to a variable.
5. When the file is loaded, the template is processed using the reference cards data as a context.

#### Context
#### API
filter()


# Future

This application has most of the feature that I need, but there are few that I'm considering adding. As more people use the
tool I'm sure this list will grow.

* Per section/item versions. It would be good if one could see only the reference material for a given version range.

