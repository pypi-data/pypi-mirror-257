import syslog
from datetime import datetime


class Logger:
    logLevel=syslog.LOG_DEBUG
    def __init__(self, service_name):
        self.__service_name = service_name
        self.prefix=""

    def error(self, *args):
        if syslog.LOG_ERR <= Logger.logLevel:
            self.__logger(syslog.LOG_ERR,"error", *args)

    def warn(self, *args):
        if syslog.LOG_WARNING <= Logger.logLevel:
            self.__logger(syslog.LOG_WARNING,"warn", *args)

    def notice(self, *args):
        if syslog.LOG_NOTICE <= Logger.logLevel:
            self.__logger(syslog.LOG_NOTICE, "info", *args)

    def info(self, *args):
        if syslog.LOG_INFO <= Logger.logLevel:
            self.__logger(syslog.LOG_INFO, "info", *args)

    def debug(self, *args):
        if syslog.LOG_DEBUG <= Logger.logLevel:
            self.__logger(syslog.LOG_DEBUG,"debug", *args)

    def set_level(level):
        Logger.logLevel=level

    def __logger(self, severity, txtSev, *args):
        try:
            syslog.openlog(self.__service_name, syslog.LOG_CONS | syslog.LOG_PID | syslog.LOG_NDELAY, syslog.LOG_LOCAL1)
            msg = txtSev+" ["+self.prefix+"]"
            for a in args:
                msg = msg + " " + str(a)

            syslog.syslog(severity, msg)
            syslog.closelog()
        except Exception as e:
            print("Syslog fail ", e)

    def ___current_full_date(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
