from globalInfo import *
import time,imp

class cmds:
    """Owner commands"""
    def __init__(self,parent):
        self._parent = parent

    def quit(self):
        """[Message]

        Quit the bot with [Message]"""
        message = self._parent.getMessage()
        if message is not None:
            self._parent.quote('QUIT :{0}'.format(message))
        else:
            self._parent.quote('QUIT :{0} by AntB has exited.'.format(NAME))
        time.sleep(2)
        self._parent.botIsAlive = False
        self._parent.term(INFO,'{0} is no longer active.'.format(NAME))

    def quote(self):
        """<IRC RAW Command>

        Pass a command directly to the server"""
        self._parent.quote(self._parent.getMessage().replace('\\x01','\x01').replace('\\x02','\x02'))

    def reportlevel(self):
        """[No Argument|num|'levels']

        No argument displays the current level and which options are enabled. Entering a number sets that debug level. 'levels' displays the available level codes"""
        level = self._parent.getArg()

        if level is None:
            enabledLevels = ''
            if self._parent.config['debug']&RCMD:
                enabledLevels+='RCMD '
            if self._parent.config['debug']&FUNC:
                enabledLevels+='FUNC '
            if self._parent.config['debug']&SUB:
                enabledLevels+='SUB ' 
            if self._parent.config['debug']&RSEND:
                enabledLevels+='RSEND '
            if self._parent.config['debug']&RRECV:
                enabledLevels+='RRECV '
            if self._parent.config['debug']&DBG:
                enabledLevels+='DBG '
            self._parent.send('Current debug level is 0x{0:X}. - Enabled levels: {1}'.format(self._parent.config['debug'],enabledLevels),nick=True)
            return None

        try:
            if level.lower() == 'show':
                self._parent.send("\x020x01\x02 RCMD -- \x020x02\x02 FUNC -- \x020x04\x02 SUB -- \x020x08\x02 RSEND --\x020x10\x02 RRECV -- \x020x20\x02 -- DBG",nick=True)
                return None
        except Exception, e:
            self._parent.term(ERROR,e)

        try: level = int(level)
        except:
            try: level = int(level,16)
            except Exception,e: 
                self._parent._term(DBG,e)

        try:
            oldLevel = self._parent.config['debug']
            self._parent.config['debug']=level
            self._parent.saveConfig()
            self._parent.send('Debug level changed from 0x{0:X} to 0x{1:X}.'.format(oldLevel,level),nick=True)
            self._parent.term(INFO,'Debug level set to 0x{0:X}|{0:d}'.format(level))
        except Exception,e:
            self._parent.term(ERROR,e)

    def bottle(self):
        """[float]

        Sets the bottle life."""
        newValue = self._parent.getArg()
        if newValue is not None:
            self._parent.misc['bottle']=float(newValue)
        else:
            self._parent.send(str(self._parent.misc['bottle']),nick=True)

    def nick(self):
        """<nick> [AlternateNick]

        Changes the bots nick to <nick> with [AlternateNicks] as alternates"""
        newNick = self._parent.getArg()
        altNick = self._parent.getArg(1)
        if newNick is not None:
            self._parent.quote('NICK :{0}'.format(newNick))
            self._parent.config['nick'][0] = newNick
        else:
            self._parent.send(self.nick.__doc__,nick=True)
            self._parent.term(FUNC,'Owner Nick -> No nick specified')

        if altNick is not None:
            self._parent.config['nick'][1]=altNick
        self._parent.saveConfig()

    def prefix(self):
        """<prefix[s]>

        Sets a new prefix for {0} to use. Multiple prefixes should be seperated by a space."""
        newPrefixes = self._parent.getMessage()
        if newPrefixes is None:
            self._parent.term(DBG,self._parent.config['prefix'])
            self._parent.send(self._parent.config['prefix'],nick=True)
            return False
        else:
            self._parent.config['prefix'] = []
            for each in newPrefixes.split(' '):
                self.parent.config['prefix']+=[each]
            self._parent.send('Prefixes updated -> {0}'.format(str(self._parent.config['prefix'])),nick=True)
            self._parent.saveConfig()
    
    def join(self):
        """<channel>

        Joins the specified channel"""
        channels = self._parent.getMessage().split(' ')
        if channels is None:
            self._parent.send('Please Specify channel[s]')
            return 0
        for each in channels:
            self._parent.quote('JOIN :{0}'.format(each))
            self._parent.config['channels']+=[each]
        self._parent.saveConfig()

    def part(self):
        """[channel]

        Parts the specified channel, or the current channel if none specified."""
        channel = self._parent.getMessage().split(' ')
        if channel is None:
            channel = self._parent.buffer['line'].split(' ',3)[2]
        else:
            for each in channel:
                if '#' not in each:
                    pass
                else:
                    self._parent.quote('PART {0} :Commanded by {1}'.format(each,self._parent.getNick()))
                    self._parent.config['channels'].pop(self._parent.config['channels'].index(each))
        self._parent.saveConfig()
