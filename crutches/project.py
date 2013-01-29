import cgi
import os
import re
import yaml

import template
import util

ENTRY_NAME = 0
ENTRY_DESC = 1
ENTRY_OPT  = 2

def parse_module(file, project, db):
    with open(file, "r") as input:
        module = yaml.load(input)

def load_projects(path, config = None, project_path = [], db = {"projects":[]}):
    """
    Traverse the projects tree, identify and loading matching projects.
    """

    # Check current folder
    prj_desc = load_project_desc(os.path.join(path,"_project.yml"))
    if prj_desc:
        project_path.append(prj_desc["project"])
        new_project = { "project":prj_desc["project"], "sections": [], "uid": util.next_uid(), "path": "/".join(project_path), "description": prj_desc["description"] }

        for section_file in [ os.path.join(path,name) for name in os.listdir(path) if os.path.splitext(name)[1] == ".yml" and not name == "_project.yml" ]:
            for section in load_sections(section_file):
                if not config or config.section_included(project_path, section["section"]):
                    new_project["sections"].append(section)

        # if no sections matched, don't add the project
        if len(new_project["sections"]) > 0:
            db["projects"].append(new_project)

    for name in os.listdir(path):
        next_path = os.path.join(path,name)
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
    #print("Loading " + filename)
    with open(filename, "r") as f:
        for content in yaml.load_all(f):
            content['uid'] = util.next_uid()

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

                    # TODO this is not correctly handling just a description plus options
                    if len(entry) == 1:
                        new_entry = { "description": escape(entry[0]), "uid": util.next_uid() }
                    elif len(entry) >= 2:
                        new_entry = { "term": escape(entry[0]), "description": escape(entry[1]), "uid": util.next_uid() }

                    if len(entry) > ENTRY_OPT:
                        new_entry["options"] = entry[ENTRY_OPT]
                    else:
                        new_entry["options"] = {}
                    new_entry['entry_url'] = template.prepare_entry_url(new_entry, section_url)
                    entry_array.append(new_entry)

                content["entries"] = entry_array
                sections.append(content)
    return sections

def list_projects(search = ""):
    search = search.lower()
    db = load_projects("projects")
    for project in db["projects"]:
        path, desc = project["path"], project["description"]
        if path.lower().find(search) >= 0 or desc and desc.lower().find(search) >= 0:
            print("{:<50}{:}".format(path, desc or ""))

def escape(raw):
    if raw.find("\n") != -1:
        out = "<pre>{}</pre>".format(raw)
    else:
        literal = re.compile(r"``(.+?)``", re.MULTILINE|re.DOTALL)
        em = re.compile(r"\*(.+?)\*", re.MULTILINE|re.DOTALL)
        strong = re.compile(r"\*\*(.+?)\*\*", re.MULTILINE|re.DOTALL)

        out = cgi.escape(raw)

        out = re.sub(strong, r"<strong>\1</strong>", out)
        out = re.sub(em, r"<em>\1</em>", out)
        out = re.sub(literal, r"<pre>\1</pre>", out)

    return out
