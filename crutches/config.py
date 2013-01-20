import re
import yaml

import util

class Config:
    asset_dir = "assets"
    template_dir = "templates"
    projects_dir = "projects"
    build_dir = "build"
    js_dir = "js"

    def __init__(self, user_cfg):
       self.load_config(user_cfg)

    def load_config(self, config):
        with open("config.yml","r") as f:
            try:
                cfg = yaml.load(f)[config]
                self.template = cfg["template"]
                self.include = cfg.get("include", [])
                self.exclude = cfg.get("exclude", [])
            except KeyError as e:
                exit("Error: required key {} missing in configuration.".format(e))


    def section_included(self, path, section):
        # Make a fully qualified section name
        fq_section = "/" + "/".join(path) + "//" + section

        matched = False

        if self.include:
            for include in util.flatten(self.include):
                # TODO  Compile these things once!
                if re.search(re.compile(include), fq_section):
                    matched = True
                    break;
        else:
            # No include implies everything matches
            matched = True

        if matched and self.exclude:
            for exclude in self.exclude:
                # TODO  Compile these things once!
                if re.search(re.compile(exclude), fq_section):
                    matched = False
                    break;

        return matched
