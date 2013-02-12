import os
import re
import shutil

from config import Config

def create_build_dir():
    shutil.rmtree(Config.build_dir, ignore_errors = True)
    os.makedirs(Config.build_dir)

def copy_js(html=None, template_dir=None, js_dir=Config.js_dir, target_dir=Config.build_dir):
    for f in os.listdir(template_dir):
        shutil.copy(os.path.join(template_dir, f), Config.build_dir)

    # Find external Javascript copy it to the build directory
    regex = re.compile(r"<\s*script.*?src\s*=\s*\"\s*(?P<script>.*?)\s*\"\s*>.*?</script>",re.IGNORECASE|re.MULTILINE|re.DOTALL)
    for match in regex.finditer(html):
        script = match.group("script")
        templ_loc = os.path.join(template_dir, script)
        js_loc= os.path.join(js_dir, script)

        if os.path.exists(templ_loc):
            shutil.copy(templ_loc, target_dir)
        elif os.path.exists(js_loc):
            shutil.copy(js_loc, target_dir)
        else:
            exit("Error: {} not found".format(script))


def build(html, cfg):
    create_build_dir()
    template_dir = os.path.join(Config.template_dir, cfg.template)
    copy_js(html=html, template_dir=template_dir)

    with open(os.path.join(Config.build_dir, cfg.name + ".html"), "w") as out:
        out.write(html)



