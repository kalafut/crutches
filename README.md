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
* BeautifulSoup 4




## Content Guide

Entries are a collection of one or two content elements and optional options array. If a two content blocks are provided,
the first is considered the "key" and the second the "description". These are typically shown as two columns in the output.
If a key is present, it can be used as part of the automatic URL generation.

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

