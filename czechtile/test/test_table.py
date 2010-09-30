#!/usr/bin/env python
# -*- coding: utf-8 -*-

###
#Czechtile: WikiHezkyCesky
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
###

from os import pardir, tmpfile, remove
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import logging
import re

from unittest import main
from czechtile import *

from module_test import *
#logging.basicConfig(level=logging.DEBUG)

class TestTabulkaMacro(OutputTestCase):
    def testSimplest(self):
        tree = parse('((tabulka ((radek ((stlpec text))))))', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(len(tree.children[0].children), 1)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Tabulka)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.TabulkaRadek)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].__class__, nodes.TabulkaStlpec)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].children[0].content, 'text')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<informaltable><tgroup cols="1"><tbody><row><entry>text</entry></row></tbody></tgroup></informaltable>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<table><tr><td>text</td></tr></table>', res)

if __name__ == "__main__":
    main()
