import json
import re

from os.path import join
from config import Config

def parse_template(name, data):
    with open(join(Config.template_dir, name), "r") as f:
        orig = f.read()

    # Find external Javascript and load the contents
    regex = re.compile(r"<\s*script.*?src\s*=\s*\"\s*(.*?)\s*\"\s*>.*?</script>",re.IGNORECASE|re.MULTILINE|re.DOTALL)
    orig = re.sub(regex, lambda x: "<script>{contents}</script>".format(contents=open(join(Config.asset_dir, x.groups()[0])).read()), orig)

    # Find external CSS and load the contents
    regex = re.compile("<\s*link.*?href\s*=\s*\"\s*(.*?)\s*\"\s*>",re.IGNORECASE|re.MULTILINE|re.DOTALL)
    orig = re.sub(regex, lambda x: "<style>{contents}</style>".format(contents=open(join(Config.asset_dir, x.groups()[0])).read()), orig)

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
