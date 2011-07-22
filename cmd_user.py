from globalInfo import *
import time,random

class cmds:
    """User commands"""
    def __init__(self,parent):
        self._parent = parent
        random.seed()

    def list(self):
        """[Set]

        Lists all available modules and commands in the modules."""
        self._parent.term(RCMD,'List')
        level = self._parent.getArg()
        try:
            reply = 'Commands for {0}: '.format(level)
            for each in self._parent.cmds[level.lower()]:
                reply+=each.capitalize()+' '
        except:
            reply='\x02list [set]\x02 -> Available modules are: '
            for each in self._parent.cmds:
                reply+=each.capitalize()+' '
        self._parent.send(reply,nick=True)

    def coin(self):
        """<No argument>

        Flip a coin."""
        self._parent.term(RCMD,'Coin')
        coin = int(random.random()*2)
        if coin == 0:
            self._parent.send('The coin flipped \x02Tails\x02',nick=True)
        else:
            self._parent.send('The coin flipped \x02Heads\x02',nick=True)

    def shake(self):
        """<No argument>

        A shake the bottle game."""
        self._parent.term(RCMD,'Shake')
        power = (random.random()*10)+1
        self._parent.misc['bottle']-=power
        if self._parent.misc['bottle'] > 0:
            if power > 8:
                output='with a look of sheer madness in their eyes as the fizz builds up rapidly.'
            elif power > 5:
                output='playfully causing a good amount of fizz in the bottle'
            elif power > 2:
                output='very cautiously being careful not to make the bottle explode.'
            else:
                output='once and ran a mile...'
            if self._parent.misc['bottle'] < 10:
                    output+=' It looks like its ready to blow!'
            self._parent.send('\x02{0}\x02 shook the bottle {1}'.format(self._parent.getNick(),output))
        else:
            if power > 8:
                output='with an insane look in his/her eye, almost daring the bottle to explode. The bottle took that dare and promptly exploded.'
            elif power > 5:
                output='pretended to be a cocktail bar worker and did a couple of flips with the bottle, as the bottle passes their face it exploded knocking him/her unconsious.'
            elif power > 2:
                output='once or twice. As {0} put the bottle down it exploded all over him/her.'.format(self._parent.getNick())
            else:
                output='picked up the bottle, which was enough to make it explode violently in their hand.'
            self._parent.send('\x02{0}\x02 shook the bottle {0}'.format(self._parent.getNick(),output))
            time.sleep(1)
            self._parent.quote('KICK {0} {1} :Fizzy explosion (x.x)'.format(self._parent.getChannel(),self._parent.getNick()))
            self._parent.misc['bottle'] = (random.random()*50)
            self._parent.quote('INVITE {0} :{1}'.format(self._parent.getNick(),self._parent.getChannel()))

    def help(self):
        """[command]

        Provides help about any command given. <angle brackets> are mandatory arguments, [square brackets] are optional arguments"""
        self._parent.term(RCMD,'Help')
        command = self._parent.getArg()
        if command == None :
            command == 'help'
        for each in self._parent.cmds:
            if 'all' in each:
                continue
            elif command in self._parent.cmds[each]:
                docstr = eval('self._parent.'+each+'_'+command+'.__doc__').split('\n')
                self._parent.send('\x02 {0} {1}\x02 -> {3}'.format(command,docstr[0],docstr[2].replace('  ','')),nick=True)

    def ping(self):
        """[User]

        Shows [User]s CTCP PING response time in channel."""
        self._parent.term(RCMD,'Ping')
        target = self._parent.getArg()
        if '#' in str(target) and self._parent.checkOwner() is False:
            return
        if target == None:
            target = self._parent.getNick()
        self._parent.pingChannel=self._parent.getChannel()
        self._parent.quote("PRIVMSG {0} :\x01PING {1}\x01".format(target,time.time()))

    def version(self):
        """<No Arguments>

        Returns the current version information of the bot"""
        self._parent.term(RCMD,'Version')
        self._parent.send(VERSION,nick=True)

    def source(self):
        """<No Arguments>

        Returns the location of the current source for the bot"""
        self._parent.term(RCMD,'Source')
        self._parent.send(SOURCE,nick=True)

class regexp:
    def __init__(self,parent):
        self._parent = parent
