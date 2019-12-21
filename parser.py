#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 21:37:14 2019

@author: Carlos McNulty
"""

import lxml.html
from lxml.html import parse
import requests
from summarizer import summarize
import logging
from bs4 import BeautifulSoup
from lxml import etree


if __name__ == "__main__":
    

    tree = parse("roanoke.html")
    root = tree.getroot()    
    paragraphs = root.xpath("//p")
    
    for par in paragraphs:
        for child in par.iterdescendants():
            child.drop_tag()
        text = str(par.text_content())
        summary = summarize(text, limit=3)
        par.text = summary
        
    tree.write(file="roanoke-revised.html", method="html")