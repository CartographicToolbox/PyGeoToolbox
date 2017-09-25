#  -*- coding: utf-8 -*-
__author__ = "raugustyn@post.cz"


from base import replaceStringBlocks


def replaceHTMLBlock(html, commentIdentifier, newContent):
    """ Replaces html content in block of <!-- commentIdentifier -->Old content<!-- end of commentIdentifier --> by new value.

    :param html: source html containing section(s) to be replaced
    :param commentIdentifier: identifier of section to be replaced
    :param newContent: new content of identified section
    :return: resulting html

    >>> html = "<html><body><h1>Title</h1><p><!-- content -->Here should be page content<!-- end of content --></p></body></html>"
    >>> html = replaceHTMLBlock(html, "content", "My content of page.")
    >>> print html
    <html><body><h1>Title</h1><p>My content of page.</p></body></html>
    """
    startId = ("<!-- %s -->" % commentIdentifier).upper()
    endId = ("<!-- END OF %s -->" % commentIdentifier).upper()
    while html.upper().find(startId) >= 0:
        upperCase = html.upper()
        startPos = upperCase.find(startId)

        endPos = upperCase.find(endId)
        if endPos < 0:
            import logging
            logging.error("replaceHTMLBlock endPos(%d) < 0" % (endPos))
            return html

        endCutPos = upperCase.find("-->", endPos) + 3
        if endCutPos < 3:
            return html

        if startPos>=0 and endCutPos>=0:
            html = html[:startPos] + newContent + html[endCutPos:]

    return html


def initializeJavaScriptVariable(html, variableName, value):
    startId = "var %s = " % variableName
    return replaceStringBlocks(html, startId, ";", startId + value + ";")


def replaceJavaScriptBlock(html, commentIdentifier, newContent):
    """Replaces JavScript code block in html code.

    :param html: Source html code.
    :param commentIdentifier: JavaScript comment identifier.
    :param newContent: New content of the block.
    :return: html with replaced blocks of code.
    """
    identifier = commentIdentifier.upper()
    html = replaceStringBlocks(html, "// %s" % identifier, "// END OF %s" % identifier, newContent)
    html = replaceStringBlocks(html, "/* %s */" % identifier, "/* END OF %s */" % identifier, newContent)

    return html


