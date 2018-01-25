#!/usr/bin/env python
#--!-- coding: utf8 --!--

#==============================================================================
# Mistune
#==============================================================================

#import mistune
#
#markdown = mistune.Markdown()
#
#def render(text):
#    return markdown(text)
#

#==============================================================================
# Python-Markdown
#==============================================================================

#import markdown

#def render(text):
    #return markdown.markdown(text)

#==============================================================================
# Pypandoc
#==============================================================================

import pypandoc
import re
from noteflow import functions as F

def render(text):
    args = [
        "--standalone",
        # "--smart",  # typographically correct output
        # "--css=ressources/killercup-pandoc.css",
        # "--css=file://{}".format(F.appPath("ressources/killercup-pandoc.css")),
        # "--css=file://{}".format(F.appPath("ressources/github-pandoc.css")),
        "--css=file://{}".format(F.appPath("ressources/custom-pandoc.css")),
        ]

    text = F.fixLocalLinks(text)

    r = pypandoc.convert_text(text, "html+smart", format="md", extra_args=args)

    # FIXME: add custom rules
    r = re.sub("°(.*?)°", '<span style="background:#FF0;">\\1</span>', r)

    return r
