try:
    from html5lib.constants import tokenTypes
    START_TAG_CONST = tokenTypes['StartTag']
except ImportError:
    START_TAG_CONST = "StartTag"
from html5lib.sanitizer import HTMLSanitizerMixin

from .. import nodes
from . import entities
from .base import CzechtileExpander, ExpanderMap, TextNodeExpander, \
                  ListExpander, ListItemExpander

class Document(CzechtileExpander):
    def expand(self, node, format, node_map):
        if getattr(node, "wrap_document", True):
            header = u'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="cs" lang="cs">'
            footer = u'</html>'
        else:
            header = u''
            footer = u''
        return self.expand_with_content(node, format, node_map, header, footer)

class Book(CzechtileExpander):
    def expand(self, node, format, node_map):
        if getattr(node.parent, "wrap_document", True):
            header = u'<body class="book">'
            footer = u'</body>'
        else:
            header = u''
            footer = u''
        return self.expand_with_content(node, format, node_map, header, footer)

class Article(CzechtileExpander):
    def expand(self, node, format, node_map):
        if getattr(node.parent, "wrap_document", True):
            header = u'<body class="article">'
            footer = u'</body>'
        else:
            header = u''
            footer = u''
        return self.expand_with_content(node, format, node_map, header, footer)

class Sekce(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map)

class Nadpis(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u''.join([u'<h', unicode(node.level), u'>']), u''.join([u'</h', unicode(node.level), u'>']))


class Odstavec(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<p>', u'</p>')

class NeformatovanyText(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<pre>', u'</pre>')

class ZdrojovyKod(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<pre class="brush: %s">' % node.syntax_name, u'</pre>')

class Silne(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<strong>', u'</strong>')

class Zvyraznene(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<em>', u'</em>')

class Hyperlink(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u''.join([u'<a href="', unicode(node.link), u'">']), u'</a>')

class HorniIndex(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<sup>', u'</sup>')

class DolniIndex(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<sub>', u'</sub>')

class NovyRadek(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u'<br />'

class List(ListExpander):
    tag_map = {
        '-': {'tag': u'ul', 'attrs': u''},
        '1.': {'tag': u'ol', 'attrs': u' type="1"'},
        'a.': {'tag': u'ol', 'attrs': u' type="a"'},
        'i.': {'tag': u'ol', 'attrs': u' type="i"'}
    }

class ListItem(ListItemExpander):
    tag_map = {'tag': u'li', 'attrs': u''}

class Preskrtnute(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map,
          u'<strike>', u'</strike>')

class Obrazek(CzechtileExpander):

    def expand(self, node, format, node_map):
        # sanitize the picture location
        sanitizer = HTMLSanitizerMixin()
        tokens = sanitizer.sanitize_token({'type': START_TAG_CONST, \
            'name': 'img', 'data': [('src', node.source)]})['data']

        # look for the src attribute in tokens
        if len(tokens) > 0:
            for attribute, value in tokens:
                if attribute == 'src':
                    # we got it, return
                    return u'<img src="%s" />' % value

        # the src attribute wasn't sent back, it contained malicious code,
        # return the input form of the node (i.e., a macro)
        return str(node)

        # ---
        # hmm, the fail is that a node doesn't know the name of the macro
        # which created him -- this fact doesn't make reconstructing the macro
        # call very easy

class Tabulka(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<table>', u'</table>')

class TabulkaRadek(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<tr>', u'</tr>')

class TabulkaStlpec(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<td>', u'</td>')

map = ExpanderMap({
    nodes.DocumentNode: Document,
    nodes.TextNode: TextNodeExpander,

    nodes.Book: Book,
    nodes.Article: Article,
    nodes.Nadpis: Nadpis,
    nodes.Odstavec: Odstavec,
    nodes.NeformatovanyText: NeformatovanyText,
    nodes.ZdrojovyKod: ZdrojovyKod,
    nodes.Silne: Silne,
    nodes.Zvyraznene: Zvyraznene,
    nodes.HorniIndex: HorniIndex,
    nodes.DolniIndex: DolniIndex,
    nodes.TriTecky: entities.TriTecky,
    nodes.Pomlcka: entities.Pomlcka,
    nodes.Trademark: entities.Trademark,
    nodes.Copyright: entities.Copyright,
    nodes.RightsReserved: entities.RightsReserved,
    nodes.Hyperlink: Hyperlink,
    nodes.List: List,
    nodes.ListItem: ListItem,
    nodes.Uvozovky: entities.Uvozovky,
    nodes.PevnaMedzera: entities.PevnaMedzera,
    nodes.Preskrtnute: Preskrtnute,
    nodes.Obrazek: Obrazek,
    nodes.NovyRadek: NovyRadek,
    nodes.Tabulka: Tabulka,
    nodes.TabulkaRadek: TabulkaRadek,
    nodes.TabulkaStlpec: TabulkaStlpec
})
