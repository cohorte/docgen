#!/usr/bin/env python

"""

Documentation generator.

Its reads all the Documentation generated html files and extract useful sections 
and builds up a new one html (and pdf) file.

:author: Bassem Debbabi

..

    Copyright 2014 isandlaTech

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Module version
__version_info__ = (0, 0, 1)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"

import json
import optparse
import sys
import os
import requests
from bs4 import BeautifulSoup

# Using Python 3
PYTHON_3 = (sys.version_info[0] == 3)

def get_page_content(url):
    r = requests.get(url)    
    html_doc = r.text
    soup = BeautifulSoup(html_doc)
    page_title = soup.find('h1', {'id':'page-title'}).text
    idx = html_doc.find('<div id="docgen-start"></div>')
    end = html_doc.find('<div id="docgen-end"></div>', idx)
    content = html_doc[idx+len('<div id="docgen-start"></div>'):end]

    # update images src
    soup = BeautifulSoup(content)
    url_parts = url.split('/')
    url_path = '/'.join(url_parts[:-1])
    for img in soup.findAll('img'):
        img['src'] = url_path + '/' + img['src']

    return "<h1>"+page_title+"</h1>\n" + soup.prettify()

def to_bytes(data, encoding="UTF-8"):
    """
    Converts the given string to an array of bytes.
    Returns the first parameter if it is already an array of bytes.

    :param data: A unicode string
    :param encoding: The encoding of data
    :return: The corresponding array of bytes
    """
    if type(data) is bytes:
        # Nothing to do
        return data

    return data.encode(encoding)

def to_str(data, encoding="UTF-8"):
        """
        Converts the given parameter to a string.
        Returns the first parameter if it is already an instance of ``str``.

        :param data: A string
        :param encoding: The encoding of data
        :return: The corresponding string
        """
        if type(data) is str:
            # Nothing to do
            return data

        return data.encode(encoding)

def main():
    p = optparse.OptionParser(
        description="Generate Cohorte website documentation's HTML and PDF files",
        prog='docgen',
        usage='docgen -o file.html'
    )
    p.add_option('--out', '-o', help="Write to OUT instead of stdout")
    options, arguments = p.parse_args()

    p1 = get_page_content('http://cohorte.github.io/docs/1.x/what-is-cohorte/index.html')
    p2 = get_page_content('http://cohorte.github.io/docs/1.x/key-concepts/index.html')
    p3 = get_page_content('http://cohorte.github.io/docs/1.x/setup/index.html')
    p4 = get_page_content('http://cohorte.github.io/docs/1.x/components/index.html')
    p5 = get_page_content('http://cohorte.github.io/docs/1.x/compositions/index.html')
    p6 = get_page_content('http://cohorte.github.io/docs/1.x/startup/index.html')
    p7 = get_page_content('http://cohorte.github.io/docs/1.x/shell/index.html')
    p8 = get_page_content('http://cohorte.github.io/docs/1.x/monitoring/index.html')
    #p8 = get_page_content('http://cohorte.github.io/docs/1.x/ide/index.html')
    
    r_final = requests.get("http://cohorte.github.io/docs/1.x/cohorte-refguide-1.x.html")
    html_doc_final = r_final.text
    
    idx = html_doc_final.find('<div id="docgen"></div>')
    tmp1 = html_doc_final[:idx]
    tmp2 = html_doc_final[idx+len('<div id="docgen"></div>'):]
    final = tmp1 + p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + tmp2
    
    if (options.out):
        file = open(options.out, 'wb')
        if PYTHON_3:
            file.write(to_byte(final))
        else:
            file.write(to_str(final))
        file.close()
    else:
        print(final)
    
if __name__ == "__main__":
    main()
