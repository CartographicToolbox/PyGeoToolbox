# -*- coding: utf-8 -*-
__author__ = "raugustyn@post.cz"


import codecs, os, math


def setupEncoding(encoding = 'utf-8'):
    """ Setup program encoding. Using simple hack with reloading sys module.

    :param encoding: Selected encoding, if utf-8 is not appropriate.

    >>> setupEncoding()

    """
    assert isinstance(encoding, basestring)

    import sys
    reload(sys)
    sys.setdefaultencoding(encoding)


def strToFloatOrNone(str):
    if str:
        return float(str)
    else:
        return None


def sqr(value):
    """ returns square of given value.

    :param value: Value to be squared.
    :return: Square value

    >>> sqr(4)
    16
    """
    return value*value


def pathLeaf(path):
    """ Extract file name or directory name from given path.

    :param path: Full or relative path
    :return:
    >>> pathLeaf("c:/temp/test.html")
    'test.html'
    >>> pathLeaf("c:/temp/")
    'temp'
    """
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def getExtension(path):
    """ Extracts file extension of the given path.

    :param path: path or file name
    :return: extension including separator

    >>> getExtension("c:/temp/test.html")
    '.html'
    """
    (fileName, fileExtension) = os.path.splitext(path)
    return fileExtension


def changeFileExtension(fileName, newExtension):
    """

    :param fileName:
    :param newExtension:
    :return:

    >>> print changeFileExtension("c:/temp/ahoj.txt", ".sql")
    c:/temp/ahoj.sql
    >>> print changeFileExtension("c:/temp/ahoj.txt", "sql")
    c:/temp/ahoj.sql
    """
    (fileName, fileExtension) = os.path.splitext(fileName)
    if not newExtension.startswith('.'):
        newExtension = "." + newExtension
    return  fileName + newExtension


def pairItems(iterator):
    """ Returns new iterator with subsequent tupple pairs of source iterator.
    I could be used for example for converting list of vertexes in a linestring to list of edges.

    :param iterator: Iterator for join pairs
    :return: Pairs iterator

    >>> pairs = pairItems([1, 2, 3, 4, 5])
    >>> for item in pairs:print item
    (1, 2)
    (2, 3)
    (3, 4)
    (4, 5)
    """
    firstItem = None
    for item in iterator:
        if firstItem:
            yield (firstItem, item)
        firstItem = item


def safeMkDir(path):
    """ Creates directory under path if not exists. Unlike os.makedirs, first check it and don't raise error if yes.

    :param path: Path of the directory to be created
    :return: None
    >>> path = "c:/temp/testdir_1234"
    >>> safeMkDir(path)
    >>> import os
    >>> print os.path.exists(path)
    True
    >>> os.rmdir(path)
    """
    if not os.path.exists(path):
        os.makedirs(path)


def fileRead(fileName, encoding="utf-8", baseFileName=None):
    """ Reads file content using encoding specified, utf-8 as default if parameter not provided.

    :param fileName: Name of the file
    :param encoding: Encoding codec name, utf-8 as a default
    :return: File content as a string

    >>> content = fileRead(__name__ + ".py")
    >>> print content.startswith("# -*- coding: utf-8 -*-")
    True
    """
    if baseFileName:
        file = os.path.dirname(baseFileName) + os.sep + fileName

    file = codecs.open(fileName, "r", "utf-8")
    result = file.read()
    file.close()
    return result


def replaceStringBlocks(str, startId, endId, newContent):
    endPos = 0
    while True:
        startPos = str.find(startId, endPos)
        endPos = str.find(endId, startPos)
        if startPos<0 or endPos<startPos:
            break

        str = str[:startPos] + newContent + str[endPos + len(endId):]

    return str


def setParameters(template, parameters):
    """Replace values in a template string by given real values dictionary. Used mainly for SQL queries,
    enabling leave them working for copy&paste debugging.

    :param String template:Template string with identifiers to be replaced.
    :param dict parameters:Dictionary where keys are identifiers in a template which have to be replaced by values.
    :return String: Template string with replaced values.

    >>> template = "select ogc_fid from public.z_terrenrelief_l"
    >>> str = setParameters(template, { "ogc_fid": "zrdoj_id", "public" : "temp"})
    >>> print str
    select zrdoj_id from temp.z_terrenrelief_l
    """
    if parameters:
        keys = sorted(parameters.keys())
        for key in keys:
            template = template.replace(key, str(parameters[key]))

    return template


def makeDir(dirName):
    """ Creates directory dirName if not exists.

    :param String dirName: Directory to be created.

    >>> makeDir("c:/temp/testMakeDir")
    >>> os.path.exists("c:/temp/testMakeDir")
    True
    >>> os.rmdir("c:/temp/testMakeDir")
    """
    if dirName and not os.path.exists(dirName):
        os.makedirs(dirName)


def makeDirForFile(fileName):
    """ Create directory for storing file if not exists.

    :param String fileName: Name of the file for creating directory.

    >>> makeDirForFile("c:/temp/testMakeDirForFile/testfile.txt")
    >>> os.path.exists("c:/temp/testMakeDirForFile")
    True
    >>> os.rmdir("c:/temp/testMakeDirForFile")

    """
    makeDir(os.path.dirname(fileName))


def saveStrToFile(str, fileName, encoding = "utf-8"):
    """ Saves given string str into file fileName using encoding parameter.

    :param String str: String to be saved.
    :param String fileName: Name of the created file.
    :param String encoding: Character encoding, utf-8 as defatult.

    >>> saveStrToFile("Ahoj", "c:/temp/testSaveToStr.txt")
    >>> import os
    >>> os.path.exists("c:/temp/testSaveToStr.txt")
    True
    >>> # Cleaning after test
    >>> os.remove("c:/temp/testSaveToStr.txt")
    """
    makeDirForFile(fileName)
    outputFile = codecs.open(fileName, "w", encoding)
    outputFile.write(str)
    outputFile.close()


def saveJSONtoJavaScript(obj, identifier, javaScriptFileName):
    """ Saves obj to the JavaScript file as a identifier variable.

    :param obj: Object to be saved.
    :param identifier: JavaScript reference variable name.
    :param javaScriptFileName: JavaScript file name.

    >>> obj = { "value" : 3 }
    >>> saveJSONtoJavaScript(obj, "testValue", "c:/temp/test.js")
    >>> print open("c:/temp/test.js", "r").read()
    testValue = {
        "value": 3
    }
    >>> os.remove("c:/temp/test.js")

    """
    from json import dumps

    jsonString = "%s = %s" % (identifier, dumps(obj, indent=4, ensure_ascii=False).encode('utf-8'))
    saveStrToFile(jsonString, javaScriptFileName)


def getMessageIfFalse(condition, msg):
    """If condition is False, then returns msg, otherwise returns empty string.

    :param condition: Condition paramater.
    :param msg: Message returned if condition is False.
    :return: msg or empty string.


    >>> getMessageIfFalse(False, "Condition is set to False.")
    'Condition is set to False.'

    """
    if condition:
        return ""
    else:
        return msg


def getTrueFalseMessage(condition, trueMessage, falseMessage):
    """Returns trueMessage if condition is True, otherwise returns falseMessage.

    :param condition: Condition parameter.
    :param trueMessage: True case string message.
    :param falseMessage: False case string message.
    :return: Appropriate message string.

    >>> getTrueFalseMessage(True, "Condition is True", "Condition is False")
    'Condition is True'

    """
    if condition:
        return trueMessage
    else:
        return falseMessage


def formatValueIfNotEmpty(template, value):
    """Formats value if template is given, if not, the just convert it into string. Returns empty string if value is None.

    :param template: String formating template.
    :param value: Value to be formated.
    :return: Formated value.

    >>> formatValueIfNotEmpty("%3.1f", 8.54684)
    '8.5'

    >>> formatValueIfNotEmpty("%f3.1", None)
    ''

    """
    if value:
        if template.find('%') >= 0:
            return template % value
        else:
            return template
    else:
        return ""


def searchForFileAtPath(deepestPath, fileName):
    """

    :param deepestPath: Path to start search at.
    :param fileName:  File name to be searched for.
    :return: Tupple (Found, FullFileName)

    """
    deepestPath = os.path.normpath(deepestPath)
    pathItems = deepestPath.split(os.sep)
    pathLen = len(pathItems)
    while pathLen > 1:
        fullFileName = os.sep.join(pathItems[:pathLen]) + os.sep + fileName
        if os.path.exists(fullFileName):
            return (True, fullFileName)

        pathLen = pathLen - 1

    return (False, deepestPath + os.sep + fileName)


def listToSqlStr(value):
    """Converts list items into SQL list sequence.

    >> a = [4, 5, "Ahoj"]
    >> listToSqlStr(a)
    (4, 5, 'Ahoj')
    """
    return str(value).replace("[", "(").replace("]", ")").replace('"', "'")


def getTableHTML(rows):
    if rows:
        result = "<table>"
        for row in rows:
            result += "<tr>"
            for item in row:
                result += "<td>%s</td>" % item
            result += "</tr>"
        result += "<table>"
        return result
    else:
        return ""


def dump(shape):
    if hasattr(shape, "geoms") and len(shape.geoms) == 1:
        return shape.geoms[0]
    else:
        return shape


def createContainer(values):
    class Container:
        pass

    result = Container()
    for key, value in values.iteritems():
        setattr(result, key, value)

    return result


def sign(a):
    return (a > 0) - (a < 0)


def maxWithNone(a, b):
    if a == None:
        return b
    elif b == None:
        return a
    else:
        return max(a, b)


class __DummySelfExplainingClass:
    pass


SelfExplainingClass = __DummySelfExplainingClass


def angleToStr(angle):
    return str(180*angle/math.pi)


def normalizeAngle(angle, maxValue = math.pi):
    while angle < 0:
        angle += maxValue

    while angle > maxValue:
        angle -= maxValue

    return angle


def copyAttributes(source, target, attributes):
    for attribute in attributes:
        if hasattr(source, attribute):
            setattr(target, attribute, getattr(source, attribute))


def copyAttributesToItems(source, items, attributes):
    for item in items:
        copyAttributes(source, item, attributes)


def extendListNoDuplicates(listToBeExtended, newItems):
    for item in newItems:
        if not item in listToBeExtended:
            listToBeExtended.append(item)


def safeRemoveItemsFromList(listWithItems, itemsToBeRemoved):
    if itemsToBeRemoved:
        for item in itemsToBeRemoved:
            if item in listWithItems:
                listWithItems.remove(item)


class WellKnownClass:
    def __init__(self, name, description = ""):
        self.name = name
        self.description = description