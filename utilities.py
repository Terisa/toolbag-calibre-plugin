# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__docformat__ = 'restructuredtext en'

import sys
is_py3 = sys.version_info[0] == 3
if is_py3:
    myunichr = chr
else:
    myunichr = unichr  # noqa

def unescape(text):
    import re
    if is_py3:
        from html.entities import name2codepoint
    else:
        from htmlentitydefs import name2codepoint
    """Removes HTML or XML character references
      and entities from a text string.
    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    from Fredrik Lundh
    2008-01-03: input only unicode characters string.
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == '&#':
            # character reference
            try:
                if text[:3] == '&#x':
                    return myunichr(int(text[3:-1], 16))
                else:
                    return myunichr(int(text[2:-1]))
            except ValueError:
                print('Value Error')
                pass
        else:
            # named entity
            # reescape the reserved characters.
            try:
                if text[1:-1] == 'amp':
                    text = '&amp;amp;'
                elif text[1:-1] == 'gt':
                    text = '&amp;gt;'
                elif text[1:-1] == 'lt':
                    text = '&amp;lt;'
                else:
                    text = myunichr(name2codepoint[text[1:-1]])
            except KeyError:
                print('KeyError')
                pass
        return text  # leave as is
    return re.sub(r"""&#?\w+;""", fixup, text)
