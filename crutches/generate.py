import os
import sys
from textwrap import dedent

from config import Config

# Python 3 compatibility shim
if sys.hexversion > 0x03000000:
    get_input = input
else:
    get_input = raw_input

def generate():
    project_dir = get_input("Project: ")
    section_file = get_input("Section: ")
    path = os.path.join(Config.projects_dir, project_dir)
    if os.path.exists(os.path.join(path, section_file)):
        exit("Error: %s already exists" % section_file)

    if not os.path.exists(path):
        os.mkdir(path)
        with open(os.path.join(path, "_project.yml"), "w") as f:
            boilerplate = """\
                project: {project}
                description:
                url:
                """.format(project=project_dir)
            f.write(dedent(boilerplate))

    with open(os.path.join(path, section_file + ".yml"), "w") as f:
        boilerplate = """\
            section: {section}
            url: http://example.com/{{entry}}
            sort: fixed
            entries:
                - [ sample, "Sample description" ]
            """.format(section=section_file)
        f.write(dedent(boilerplate))

        print("\n" + os.path.join(path, section_file) + " created.")


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

