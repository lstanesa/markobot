class BotException(Exception):
    def __init__(self, msg):
        self.msg = msg

    @property
    def message(self):
        return self.msg

class ConfigException(BotException):
    def __init__(self, msg):
        super().__init__(msg)

    @property 
    def message(self):
        return 'There was an error in the configuration: %s' % self.msg

class CommandException(BotException):
    def __init__(self, msg, cmd):
        super().__init__(msg)
        self.cmd = cmd

    @property
    def message(self):
        return "Error on command %s: %s" % (self.msg, self.cmd)
