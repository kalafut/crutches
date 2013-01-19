import os
import random
import string
from os.path import join
from textwrap import dedent

from config import Config

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
    os.mkdir(join(Config.projects_dir, r))
    with open(join(Config.projects_dir, r, "_project.yml"), "w") as f:
        boilerplate = """\
            project: {project}
            description:
            url:
            """.format(project=r)
        f.write(dedent(boilerplate))

    return r

def random_section(project, entries):
    s = random_word(5,10)
    with open(join(Config.projects_dir, project, s+".yml"), "w") as f:
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

