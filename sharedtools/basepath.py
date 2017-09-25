#  -*- coding: utf-8 -*-
__author__ = "raugustyn@post.cz"

import os, sys

# ##########################################################################################
#
# Following sequence ensures that packages path is registered into Python environment.
# It searches in the current directory file manager.py or it's parent directories.
# If not found, then current directory assumed as basePath.
#
# ##########################################################################################

basePath = None

def setupBasePath(pathOrFile):
    global basePath

    if os.path.isfile(pathOrFile):
        basePath = os.path.dirname(pathOrFile)
    else:
        basePath = pathOrFile
    basePath = os.path.normpath(basePath)
    basePath = basePath.replace("/", os.sep)

    basePathItems = basePath.split(os.sep)
    while basePathItems and not os.path.exists(os.sep.join(basePathItems) + os.sep + "manager.py"):
        basePathItems = basePathItems[:len(basePathItems)-1]

    if basePathItems:
        basePath = os.sep.join(basePathItems)

    if not basePath in sys.path:
        sys.path.append(basePath)

setupBasePath(__file__)

def normalizePath(relativePath):
    """Path normalizer for template and configuration files.  It will create full path for the file, relativePath is addressed to
    the directory one level higher than this module.

    :param relativePath: RelativePath, addressed to the directory one level higher than this module.
    :return: Absolute path of the relativePath parameter.

    >>> print normalizePath("sharetools/")
    C:\\ms4w\\Apache\\htdocs\\Generalizace\\TB04CUZK001_CartoModel\\sharetools/
    """
    result = basePath
    if result and not basePath.endswith(os.sep):
        result += os.sep
    result += relativePath
    result = os.path.normpath(result)

    return result

def relativizePath(path):
    path = os.path.normpath(path)
    if path.startswith(basePath):
        path = path[len(basePath)+1:]

    return path
