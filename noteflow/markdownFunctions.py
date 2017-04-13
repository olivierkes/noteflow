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

import markdown

def render(text):
    return markdown.markdown(text)

#==============================================================================
# Pypandoc
#==============================================================================

import pypandoc

def render(text):
    args = [
      "--standalone",
      "--smart",  # typographically correct output
      ]
    r = pypandoc.convert_text(text, "html", format="md", extra_args=args)
    return r
