import logging, codecs, os
from logging import INFO, DEBUG
from __init__ import basePath, updateStatusInfo
from base import makeDir

logFilesPath = basePath + os.sep + "log" + os.sep
makeDir(logFilesPath)

logger = None


__sharedAdapter = None
__sharedLogger = None
__logFileName = ""


def getAdapter():
    return __sharedAdapter


class CustomAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra):
        logging.LoggerAdapter.__init__(self, logger, extra)
        self.logIndent = 0
        self.__onLogProc = None
        self.maxLogIndent = None
        self.__muted = False


    @property
    def muted(self):
        return self.__muted


    def mute(self):
        self.__muted = True


    def unMute(self):
        self.__muted = False


    def process(self, msg, kwargs):
        msg = '%s%s' % (self.getIndent(), msg)

        global __onLogProc
        if self.__onLogProc:
            self.__onLogProc(msg)

        return msg, kwargs


    def getIndent(self):
        result = ""
        for i in range(0, self.logIndent):result += "\t"
        return result


    def openSection(self, msg, level = logging.INFO):
        if self.__muted:return

        updateStatusInfo(msg)
        self.log(level, msg)
        self.logIndent = self.logIndent + 1


    def closeSection(self, msg="Done.", level = logging.INFO):
        if self.__muted: return

        updateStatusInfo("")
        self.logIndent = self.logIndent - 1
        if self.logIndent < 0:self.logIndent = 0
        self.log(level, msg)


    def getNumberOfLines(self):
        logFile = codecs.open(getLogFileName(), "r", "utf-8")
        result = 0
        for line in logFile:
            result = result + 1

        return result


    def getLines(self, startRowNumber, endRowNumber, newLineSequence="\n"):
        result = ""

        logFile = codecs.open(getLogFileName(), "r", "utf-8")
        rowNumber = 0
        for line in logFile:
            if rowNumber > startRowNumber and (endRowNumber == None or rowNumber <= endRowNumber):
                if newLineSequence <> "\n":
                    line = line.rstrip('\n') + newLineSequence
                result += line
            rowNumber = rowNumber + 1

        return result


def loggerNeeded():
    if not __sharedAdapter:
        createLogger("log")


def getLogFileName():
    return __logFileName


def createLoggerForModule(module, level = None):
    from __init__ import relativizePath

    logFileName = relativizePath(module).replace(os.sep, ".").replace(".py", "")

    return createLogger(logFileName, level)


def createLogger(logFileName, level = None):
    global __logFileName
    global __sharedLogger
    global __sharedAdapter
    global logger


    if not __logFileName:
        logFileName = logFilesPath + logFileName
        __sharedLogger = logging.getLogger(logFileName)
        if level:
            __sharedLogger.setLevel(level)
        else:
            __sharedLogger.setLevel(logging.DEBUG)

        logging.basicConfig(format='%(asctime)s - %(levelname)s %(message)s', datefmt="%H:%M:%S")
        __sharedAdapter = CustomAdapter(__sharedLogger, {'connid': __name__})
        logger = __sharedAdapter

        __logFileName = logFileName + ".log"
        if logFileName:
            fileHandler = logging.FileHandler(__logFileName, mode='w')
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            fileHandler.setFormatter(formatter)
            __sharedLogger.addHandler(fileHandler)

            __sharedAdapter.info("Create logger %s." % __logFileName)

    return __sharedAdapter


def mute(self):logger.mute()
def unMute(self):logger.unMute()
def getIndent(self):return logger.getIndent()
def openSection(self, msg, level=logging.INFO):logger.openSection(msg, level)
def closeSection(self, msg="Done.", level=logging.INFO):logger.closeSection(msg, level)
def getNumberOfLines(self):return logger.getNumberOfLines()
def getLines(self, startRowNumber, endRowNumber, newLineSequence="\n"):return logger.getLines(startRowNumber, endRowNumber, newLineSequence)


logger = createLogger("default")


# #############################################################################
# NO-PRODUCTION CODE
# #############################################################################
if __name__ == '__main__':

    # #############################################
    # Not proper use, custom logger direct create
    # #############################################
    logger = createLogger("log.init")
    logger.info("Logger test info")
    logger.debug("Logger test debug")
    logger.error("Logger test error")
    logger.critical("Logger test critical")
    logger.exception("Logger test exception")
    logger.warning("Logger test warning")
    logger.log(INFO, "Logger test log")

    # #############################################
    # Proper use of shared logging
    # #############################################

    import logging

    # Case A: We do not know shared logger name
    logging.info("Logger test info")
    logging.debug("Logger test debug")
    logging.error("Logger test error")
    logging.critical("Logger test critical")
    logging.exception("Logger test exception")
    logging.warning("Logger test warning")
    logging.log(INFO, "Logger test log")

    # Case B: We do know shared logger name
    logger = logging.getLogger("testapp")
    logger.info("Logger test info")
    logger.debug("Logger test debug")
    logger.error("Logger test error")
    logger.critical("Logger test critical")
    logger.exception("Logger test exception")
    logger.warning("Logger test warning")
    logger.log(INFO, "Logger test log")