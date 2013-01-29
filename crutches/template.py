import json
import re

from os.path import join
from config import Config

def parse_template(name, data):
    with open(join(Config.template_dir, name, name + ".html"), "r") as f:
        orig = f.read()

    # Extract template
    regex = re.compile(r"<\s*body\s*>(.*)<\s*/body\s*>",re.IGNORECASE|re.MULTILINE|re.DOTALL)
    m = regex.search(orig)
    template = m.groups()[0]
    template = re.sub(r"[\n\r]","", template)
    template = re.sub(r"([\\\"\'])", r"\\\1", template)
    orig = re.sub(regex, "<body></body>", orig)

    new_templ = orig.replace("<body>","<script>_template='{template}';_data={data};</script><body>".format(template=template, data=json.dumps(data)), 1)

    return new_templ



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
