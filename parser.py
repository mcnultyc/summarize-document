#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 21:37:14 2019

@author: Carlos McNulty
"""
import urllib.request as urllib2
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
from urllib.parse import urlparse
import urllib

def parse_default(tree, title):
    pass

def parse_cnn(tree, title):
    pass

def parse_wiki(tree, title):
    root = tree.getroot()
    parser_div = root.xpath("//div[@class='mw-parser-output']")[0]
    headers = ["h1","h2","h3","h4","h5","h6"]
    children = parser_div.getchildren()
    text = ""
    header = ""
    html = ""
    for child in children:
        if child.tag == "p":
            text += child.text_content().lstrip().rstrip()
        elif child.tag in headers:
            if len(text) > 0:
                summary = summarize(text, limit=2)
                html += "<h2>"+header+"</h2><p>"+summary+"</p>"
            text = ""
            header = child.text_content().split("[")[0]
            print(header)
    
    # TODO - add style sheet
    # TODO - format text
    html_out = E.HTML(
        E.HEAD(
            E.TITLE(title)
            ),
        E.BODY(
            E.H1(E.CLASS("heading"), title),
            lxml.html.fromstring(html)
            )
        )

    html_out.getroottree().write(file="summarized-roanoke.html", method="html")

if __name__ == "__main__":
    
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.scripts = True
    cleaner.frame = True
    cleaner.meta = True
    cleaner.comments = True
    cleaner.links = True
    cleaner.style = True    
    cleaner.kill_tags = ["cite", "sup", "img", "noscript", "label", "video"]
        
    url = "https://en.wikipedia.org/wiki/Roanoke_Colony"
    doc = urllib2.urlopen(url)
    
    tree = lxml.html.parse(doc)
    title = tree.find(".//title").text
    
    tree = cleaner.clean_html(tree)

    netloc = urlparse(url).netloc
    if netloc == "en.wikipedia.org":
        parse_wiki(tree, title)
    elif netloc == "cnn.com":
        parse_cnn(tree, title)
    else:
        parse_default(tree, title)
   