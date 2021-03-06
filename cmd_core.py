from globalInfo import *

class cmds:
    """This module does nothing. The commands in this module are hardcocded into
        the bot."""

    def __init__(self,parent):
        self._parent = parent

    def modreload(self):
        """<module>

        Reloads a module."""
        pass # This command is coded into the main script.

    def modload(self):
        """<module>

        Loads a module. module name must take the form of cmd_<name>.py"""
        pass # This command is coded into the main script.

    def modunload(self):
        """<module>

        Unloads a module from the bot."""
        pass # This command is coded into the main script.

    def makeowner(self):
        if self._parent.getArg() in self._parent.config['owner'] and self._parent.config['isOwnerSet'] is 0:
            try:
                ownermask = self._parent.getHost()
                for each in range(0,9):
                    ownermask.replace('each','9')
                ownermask = ownermask.replace('999','*').replace('99','*').replace('9','*')
                ownermask = self._parent.getUser()+'@'+ownermask
            except Exception,e: 
                self._parent.term(ERROR,'Hostmask gen -> {0}'.format(e))
            try:
                self._parent.config['owner'] = ownermask
                self._parent.config['isOwnerSet'] = 1
                self._parent.saveConfig()
                self._parent.send('Owner registered as {0}'.format(ownermask))
            except Exception,e:
                self._parent.term(ERROR,'config gen -> {0}'.format(e))

class regexp:
    def __init__(self,parent):
        self._parent = parent

    def greeter(self,match):
        r"^(hello|hi|sup|hey|o?[bh]ai|wa+[sz]+(a+|u+)p?|Bye*|cya*|later[sz]?)[,. ]+(stewi?e?[griffin]?|bot|all|there)[.!]?"
        print match
        self._parent.send('Hi, {0}'.format(self._parent.getNick()))
