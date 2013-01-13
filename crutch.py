#!/usr/bin/env python
#
# Copyright (c) 2013 Jim Kalafut
#
# Released under the MIT license
# https://raw.github.com/kalafut/crutches/master/LICENSE
#

import argparse
import json
import os
import os.path
import random
import re
import string
import sys
import yaml

from os.path import join
from textwrap import dedent

ASSET_DIR = "assets"
TEMPLATE_DIR = "templates"
PROJECTS_DIR = "projects"
ENTRY_NAME = 0
ENTRY_DESC = 1
ENTRY_OPT  = 2

# Python 3 compatibility shim
if sys.hexversion > 0x03000000:
    get_input = input
else:
    get_input = raw_input

def next_uid():
    next_uid.uid += 1
    return next_uid.uid
next_uid.uid = 0

def parse_module(file, project, db):
    with open(file, "r") as input:
        module = yaml.load(input)

def combine_files(files, directory):
    combined = ""
    for f in files:
        with open(join(directory, f), 'r') as f:
            combined += f.read()
    return combined

def replace_tag(match):
    fn = match.groups()[0]
    with open(join(ASSET_DIR, fn), 'r') as f:
        contents = f.read()
    return "<script>{contents}</script>".format(contents=contents)

def parse_template(name, data):
    with open(join(TEMPLATE_DIR, name), "r") as f:
        orig = f.read()

    # Find external Javascript and load the contents
    regex = re.compile(r"<\s*script.*?src\s*=\s*\"\s*(.*?)\s*\"\s*>.*?</script>",re.IGNORECASE|re.MULTILINE|re.DOTALL)
    orig = re.sub(regex, lambda x: "<script>{contents}</script>".format(contents=open(join(ASSET_DIR, x.groups()[0])).read()), orig)

    # Find external CSS and load the contents
    regex = re.compile("<\s*link.*?href\s*=\s*\"\s*(.*?)\s*\"\s*>",re.IGNORECASE|re.MULTILINE|re.DOTALL)
    orig = re.sub(regex, lambda x: "<style>{contents}</style>".format(contents=open(join(ASSET_DIR, x.groups()[0])).read()), orig)

    # Extract template
    regex = re.compile(r"<\s*body\s*>(.*)<\s*/body\s*>",re.IGNORECASE|re.MULTILINE|re.DOTALL)
    m = regex.search(orig)
    template = m.groups()[0]
    template = re.sub(r"[\n\r]","", template)
    template = re.sub(r"([\\\"\'])", r"\\\1", template)
    orig = re.sub(regex, "<body></body>", orig)

    new_templ = orig.replace("<body>","<script>_template='{template}';_data={data};</script><body>".format(template=template, data=json.dumps(data)), 1)

    return new_templ

def mini_markdown(raw):
    em = re.compile(r"([_*])(.+?)\1", re.MULTILINE|re.DOTALL)
    strong = re.compile(r"(__|\*\*)(.+?)\1", re.MULTILINE|re.DOTALL)
    code = re.compile(r"`(.+?)`", re.MULTILINE|re.DOTALL)

    strong_sub = re.sub(strong, r"<strong>\2</strong>", raw)
    em_sub = re.sub(em, r"<em>\2</em>", strong_sub)
    code_sub = re.sub(code, r"<code>\1</code>", em_sub)

    return code_sub

def load_config(config):
    with open("config.yml","r") as f:
        config_file = yaml.load(f)

    return config_file[config]


def prepare_entry_url(entry, section_url):
    if "url" in entry["options"]:
        url = entry["options"]["url"]
    elif section_url:
        url = section_url
    else:
        url = None

    if url and "term" in entry:
        url = url.format(entry = entry["term"].partition(" ")[0], entry_lc = entry["term"].partition(" ")[0].lower())

    return url

def generate():
    project_dir = get_input("Project: ")
    section_file = get_input("Section: ")
    path = join(PROJECTS_DIR, project_dir)
    if os.path.exists(join(path, section_file)):
        exit("Error: %s already exists" % section_file)

    if not os.path.exists(path):
        os.mkdir(path)
        with open(join(path, "_project.yml"), "w") as f:
            boilerplate = """\
                project: {project}
                description:
                url:
                """.format(project=project_dir)
            f.write(dedent(boilerplate))

    with open(join(path, section_file + ".yml"), "w") as f:
        boilerplate = """\
            section: {section}
            url: http://example.com/{{entry}}
            sort: fixed
            entries:
                - [ sample, "Sample description" ]
            """.format(section=section_file)
        f.write(dedent(boilerplate))

        print("\n" + join(path, section_file) + " created.")

def sectionIncluded(path, section, config):
    # Make a fully qualified section name
    fq_section = "/".join(path) + "//" + section

    matched = False

    if config["include"]:
        for include in config["include"]:
            # TODO  Compile these things once!
            if re.search(re.compile(include), fq_section):
                matched = True
                break;
    else:
        # No include implies everything matches
        matched = True

    if matched and config["exclude"]:
        for exclude in config["exclude"]:
            # TODO  Compile these things once!
            if re.search(re.compile(exclude), fq_section):
                matched = False
                break;

    return matched

def validate_section(section):
    pass

def load_projects(path, config, project_path = [], db = {"projects":[]}):
    """
    Traverse the projects tree, identify and loading matching projects.
    """

    # Check current folder
    prj_desc = load_project_desc(join(path,"_project.yml"))
    if prj_desc:
        new_project = { "project":prj_desc["project"], "sections": [], "uid": next_uid() }
        db["projects"].append(new_project)

        project_path.append(prj_desc["project"])
        for section_file in [ join(path,name) for name in os.listdir(path) if os.path.splitext(name)[1] == ".yml" and not name == "_project.yml" ]:
            for section in load_sections(section_file):
                if sectionIncluded(project_path, section["section"], config):
                    new_project["sections"].append(section)

    for name in os.listdir(path):
        next_path = join(path,name)
        if os.path.isdir(next_path):
            load_projects(next_path, config, project_path, db)

    if prj_desc:
        project_path.pop()

    return db

def load_project_desc(filename):
    content = None

    if os.path.exists(filename):
        with open(filename, "r") as f:
            content = yaml.load(f)

    return content

def load_sections(filename):
    """
    Load a section .yml file. This will usually result in one section structure,
    but YAML will permit multiple document in file. Therefore an array of documents
    will always be returned.
    """
    sections = []
    print("Loading " + filename)
    with open(filename, "r") as f:
        for content in yaml.load_all(f):
            content['uid'] = next_uid()

            """
            if "section" not in content:
                exit("%s: missing 'section:' declaration" % infile)

            if content["section"] in prj:
                exit("Error: duplicate section: %s" % infile)
"""

            if True: #sections_matches(prj["project"], content, config):
                # entries
                section_url = content.get("url")

                entry_array = []
                for entry in content['entries']:
                    if len(entry) > 3 or (len(entry) == 3 and not type(entry[2]) == dict):
                        exit("Invalid entry declaration in %s/%s: " % (project, content["section"])  + repr(entry))

                    #TODO this is not correctly handling just a description plus options
                    if len(entry) == 1:
                        new_entry = { "description": entry[0], "uid": next_uid() }
                    elif len(entry) >= 2:
                        new_entry = { "term": entry[0], "description": entry[1], "uid": next_uid() }

                    if len(entry) > ENTRY_OPT:
                        new_entry["options"] = entry[ENTRY_OPT]
                    else:
                        new_entry["options"] = {}
                    new_entry['entry_url'] = prepare_entry_url(new_entry, section_url)
                    entry_array.append(new_entry)

                content["entries"] = entry_array
                sections.append(content)
    return sections

def yamlize(txt):
    align = 0
    with open(txt,"r") as f:
        yaml_lines = []
        line1 = line2 = None
        for x in f:
            if not line1:
                if x.strip() != "":
                    line1 = x
            elif not line2:
                line2 = x
            else:
                y = yaml.dump([line1.strip(), line2.strip()], width=200).strip()
                align = max(align, y.find(", "))
                yaml_lines.append(y)
                line1 = line2 = None

        for line in yaml_lines:
            p = line.partition(", ")

            print("    - " + p[0] + p[1] + (" " * (align - len(p[0]))) + p[2])


#
# Stress test code
#
def random_word(min_len, max_len):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(random.randint(min_len,max_len)))

def random_sentence(min_len, max_len):
    s = ""
    for x in range(random.randint(min_len,max_len)):
        s += random_word(4,10) + " "
    s += "."
    return s

def random_project():
    r = random_word(5,10)
    os.mkdir(join(PROJECTS_DIR, r))
    return r

def random_section(project, entries):
    s = random_word(5,10)
    with open(join(PROJECTS_DIR, project, s+".yml"), "w") as f:
        f.write("""section: %s
url: http://example.cm/{entry}
sort: fixed
entries:\n""" % (s))
        for x in range(entries):
            f.write('    - [ "%s", "%s" ]\n' % (random_word(4,10), random_sentence(5,20)))

def stress_test(projects, sections, entries):
    for i in range(projects):
        p = random_project()
        for j in range(sections):
            random_section(p, entries)


def main():
    parser = argparse.ArgumentParser(description='Generate parse project files into a single-file reference.')
    parser.add_argument('-c', '--config', dest='config', action='store', default='main', help='Select a configuration from config.yml [default: main]')
    parser.add_argument('-g', '--generate', dest='generate', action='store_true', help='Generate a boilerplate project/section')
    parser.add_argument('-y', '--yamlize', dest='yamlize', action='store', metavar='FILE', help='Create an entries section from FILE')
    parser.add_argument('--stress', dest='stress', action='store_true', help='Stress test')
    args = parser.parse_args()

    if args.generate:
        generate()
        exit();

    if args.yamlize:
        yamlize(args.yamlize)
        exit();
    elif args.stress:
        print("Generating random projects")
        stress_test(6, 15, 20)
        print("done")
        exit()

    config = load_config(args.config)

    db = load_projects("projects", config)
    html = parse_template(config['template'] + ".html", db)

    with open("index.html", "w") as out:
        out.write(html)
        print ("index.html compiled ({size} bytes)".format(size=len(html)))


if __name__ == "__main__":
    main()
