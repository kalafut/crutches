#!/usr/bin/env python

import argparse
from bs4 import BeautifulSoup
import json
import os
import os.path
from os.path import join
import string
import random
import re
import yaml

ASSET_DIR = "assets"
TEMPLATE_DIR = "templates"
PROJECTS_DIR = "projects"
ENTRY_NAME = 0
ENTRY_DESC = 1
ENTRY_OPT  = 2

def next_uid():
    next_uid.uid += 1
    return next_uid.uid
next_uid.uid = 0

def parse_module(file, project, db):
    with open(file, "r") as input:
        module = yaml.load(input)

def combine(sources, directory):
    combined = ""
    for s in sources:
        if "src" in s:
            with open(join(directory, s["src"]), 'r') as f:
                combined += f.read()
        else:
            combined += s["text"]

    return combined

def parse_template(name, data):
    with open(join(TEMPLATE_DIR, name), "r") as f:
        soup = BeautifulSoup(f)

    # Find included javascript, combine them, and remove original tags
    scripts = soup.find_all("script")

    combine_queue = []
    for script in scripts:
        if script.has_key("src"):
            combine_queue.append({"src": script["src"]})
        else:
            combine_queue.append({"text": script.string})
        script.extract()

    combined_js = combine(combine_queue, ASSET_DIR)

    # TODO is this really on on <head>??
    # Find included css (in <head> only), combine them, and remove original tags
    combine_queue = []
    css = soup.find_all(name=["link", "style"])
    for match in css:
        if match.name=="link" and match.has_key("href"):
            combine_queue.append({"src": match["href"]})
        else:
            combine_queue.append({"text": match.string})
        match.extract()

    combined_css = combine(combine_queue , ASSET_DIR)

    # Extract section
    body = soup.find("body").contents
    template = ""
    for x in body:
        template += str(x)

    template = re.sub(r"[\n\r]","", template)
    template = re.sub(r"([\\\"\'])", r"\\\1", template)
    templ_string = "'%s'" % template

    head = soup.find("head")
    head.append("<style>" + combined_css + "</style>")
    soup.find("body").replace_with("""
    <script>
    {js_assets}
    _template = {template};
    _data = {data};
    </script>
    """.format(
        js_assets = combined_js,
        template = templ_string,
        data = json.dumps(data)))

    return str(soup)

    with open("templates/template.html", "r") as f:
        body_tmpl = re.sub(r"[\n\r]","", f.read())

    # html = base_tmpl.format(
    #     jsbundle = package_assets(),
    #     data=json.dumps(db),
    #     template=re.sub(r"([\\\"\'])", r"\\\1", body_tmpl)
    #     )

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
    project_dir = raw_input("Project directory: ")
    section_file = raw_input("Section filename: ")
    path = join(PROJECTS_DIR, project_dir)
    if os.path.exists(join(path, section_file)):
        exit("Error: %s already exists" % section_file)

    if not os.path.exists(path):
        os.mkdir(path)

    with open(join(path, section_file), "w") as f:
        f.write(
"""section: <section_name>
url: http://example.com/{entry}
sort: fixed
entries:
    - [ sample, "Sample description" ]
""")
        print "\n" + join(path, section_file) + " created."

def load_projects(path):
    db= { 'projects': [] }

    projects = [ name for name in os.listdir(path) if os.path.isdir(join(path, name)) and os.path.exists(join(path,name,"_project.yml")) ]

    for project in projects:
        with open(join(path, project, "_project.yml")) as f:
            prj_cfg = yaml.load(f)
            prj = { 'project':prj_cfg["project"],  'sections': [], 'uid': next_uid() }
            db["projects"].append(prj)

        for infile in [ name for name in os.listdir(join(path, project)) if os.path.splitext(name)[1] == ".yml" and not name == "_project.yml" ]:
            with open(join(path, project, infile), "r") as doc:
                for content in yaml.load_all(doc):
                    content['uid'] = next_uid()

                    if "section" in content:
                        if not content["section"] in prj:
                            prj['sections'].append(content)
                        else:
                            print "Error: duplicate section"
                            exit()
                    else:
                        print "%s: missing 'section:' declaration" % section

                    if "url" in content:
                        section_url = content["url"]
                    else:
                        section_url = None

                    # convert terse entry list into dictionary and add an ID
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

    #print json.dumps(db, sort_keys = 4, indent = 2)
    return db

    #for root, dirs, files in os.walk(path):

def yamlize(txt):
    align = 0
    with open(txt,"r") as f:
        lines = f.readlines()
        yaml_lines = []
        for x in range(0, len(lines), 2):
            y = yaml.dump([lines[x].strip(), lines[x+1].strip()], width=200).strip()
            yaml_lines.append(y)
            align = max(align, y.find(", "))
        for line in yaml_lines:
            p = line.partition(", ")

            print "    - " + p[0] + p[1] + (" " * (align - len(p[0]))) + p[2]


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
    print "Generating random projects"
    stress_test(6, 15, 20)
    print "done"
    exit()


config = load_config(args.config)

db = load_projects("projects")
html = parse_template(config['template'] + ".html", db)

with open("index.html", "w") as out:
    out.write(html)

