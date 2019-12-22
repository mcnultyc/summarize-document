#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 21:37:14 2019

@author: Carlos McNulty
"""

import lxml.html
from lxml.html import parse
from lxml.html import document_fromstring
import requests
from summarizer import summarize
import logging
from bs4 import BeautifulSoup
from lxml import etree
from lxml.html.clean import Cleaner
from lxml.html import builder as E


if __name__ == "__main__":
    
    cleaner = Cleaner()
    # Remove tags without meaningful text
    cleaner.javascript = True
    cleaner.scripts = True
    cleaner.frame = True
    cleaner.meta = True
    cleaner.comments = True
    cleaner.links = True
    cleaner.style = True    
    cleaner.kill_tags = ["a", "h1", "h2", "h3", "h4", "cite"]
    # Create tree from html source
    orig_tree = parse("cnn.html")
    # Clean tree of unnecessary tags
    tree = cleaner.clean_html(orig_tree)
    root = tree.getroot()
    # Get all text from the html
    elems = root.xpath("//text()")
    text = " ".join(elems)
    summary = summarize(text)
    
    title = orig_tree.find(".//title").text_content()
    # Create html document with summary
    html = E.HTML(
        E.HEAD(
            E.TITLE(title)
            ),
        E.BODY(
            E.H1(E.CLASS("heading"), title),
            E.P(summary, style="font-size: 200%")
            )
        )

    html.getroottree().write(file="summarized.html", method="html")
   