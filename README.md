# Crutch

## Goals

* Create/collect useful developer reference material and make it available under a permissive license.
* Develop conventions that allow people to easily contribute to the library.
* Provide a tool to combine select material into a searchable, single-file reference document.

## Status

* Base functionality is coming along reasonably well. I would like to get some nicer sample templates done as well as provide more sample material.
* Lots of back and forth on some of the finer points of the YAML schema. I'd like to wrap this up ASAP and tweak later.

# Installation

## Prerequisites

* PyYaml

## Configuration

* YAML references (&/\*) to will be flatted in include/exclude sections to simplify files groups.
* Include spec:  ^Python#shutil

## Content Guide

Entries are a collection of one or two content elements and optional options array. If a two content blocks are provided,
the first is considered the "key" and the second the "description". These are typically shown as two columns in the output.
If a key is present, it can be used as part of the automatic URL generation.

Project/section division.
How to handle packages, such as the bazillion in PyPy?  Are they projects?  (Probably)
How to handle http://www.cpan.org/modules/01modules.index.html?

Sample file types (from Ack):
    --[no]actionscript .as .mxml
    --[no]ada          .ada .adb .ads
    --[no]asm          .asm .s
    --[no]batch        .bat .cmd
    --[no]binary       Binary files, as defined by Perl's -B op (default: off)
    --[no]cc           .c .h .xs
    --[no]cfmx         .cfc .cfm .cfml
    --[no]clojure      .clj
    --[no]cpp          .cpp .cc .cxx .m .hpp .hh .h .hxx
    --[no]csharp       .cs
    --[no]css          .css
    --[no]delphi       .pas .int .dfm .nfm .dof .dpk .dproj .groupproj .bdsgroup .bdsproj
    --[no]elisp        .el
    --[no]erlang       .erl .hrl
    --[no]fortran      .f .f77 .f90 .f95 .f03 .for .ftn .fpp
    --[no]go           .go
    --[no]groovy       .groovy .gtmpl .gpp .grunit
    --[no]haskell      .hs .lhs
    --[no]hh           .h
    --[no]html         .htm .html .shtml .xhtml
    --[no]java         .java .properties
    --[no]js           .js
    --[no]jsp          .jsp .jspx .jhtm .jhtml
    --[no]lisp         .lisp .lsp
    --[no]lua          .lua
    --[no]make         Makefiles (including *.mk and *.mak)
    --[no]mason        .mas .mhtml .mpl .mtxt
    --[no]objc         .m .h
    --[no]objcpp       .mm .h
    --[no]ocaml        .ml .mli
    --[no]parrot       .pir .pasm .pmc .ops .pod .pg .tg
    --[no]perl         .pl .pm .pm6 .pod .t
    --[no]php          .php .phpt .php3 .php4 .php5 .phtml
    --[no]plone        .pt .cpt .metadata .cpy .py
    --[no]python       .py
    --[no]rake         Rakefiles
    --[no]ruby         .rb .rhtml .rjs .rxml .erb .rake .spec
    --[no]scala        .scala
    --[no]scheme       .scm .ss
    --[no]shell        .sh .bash .csh .tcsh .ksh .zsh
    --[no]skipped      Files, but not directories, normally skipped by ack (default: off)
    --[no]smalltalk    .st
    --[no]sql          .sql .ctl
    --[no]tcl          .tcl .itcl .itk
    --[no]tex          .tex .cls .sty
    --[no]text         Text files, as defined by Perl's -T op (default: off)
    --[no]tt           .tt .tt2 .ttml
    --[no]vb           .bas .cls .frm .ctl .vb .resx
    --[no]verilog      .v .vh .sv
    --[no]vhdl         .vhd .vhdl
    --[no]vim          .vim
    --[no]xml          .xml .dtd .xsl .xslt .ent
    --[no]yaml         .yaml .yml



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

