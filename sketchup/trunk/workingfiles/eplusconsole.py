#!/usr/bin/env python
# encoding: utf-8
"""
reads e.txt as the sketchup output file
save the it as e.idf
"""

import sys
import os

import makeidf


def main():
    """
    reads e.txt as the sketchup output file
    save the it as e.idf
    """
    fname = 'e.txt'
    txt = open(fname, 'r').read()
    eplustxt = makeidf.makeidf(txt) 
    open('e.idf', 'wb').write(eplustxt)


if __name__ == '__main__':
    main()

