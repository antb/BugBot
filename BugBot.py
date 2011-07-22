#!/usr/bin/env python
########################################
### BugBot                           ###
### By AntB/Xenocide                 ###
### -------------------------------- ###
### Catch me on:                     ###
###                                  ###
###  irc.freenode.net (Xenocide)     ###
###    #powder ##bugbot              ###
###                                  ###
###  irc.globalgamers.net (AntB)     ###
###    #mafia #lounge                ###
########################################
import sys,socket,os,random,time,json,datetime,threading,re
from globalInfo import *

class bugbot(threading.Thread):
    """A Python bot designed to be lightweight and extendable."""
    random.seed()

    def __init__(self):
        try:
            with open('CONFIG','r') as f:
                self.config=json.load(f)
        except IOError:
            self.term(ERROR,'CONFIG not found - Have you run genconfig.py?'

        self.term(INFO,'Initalising {0}...'.format(NAME))

        self.term(INFO,' {0} = Information*'.format('{: >4}'.format(INFO)))
        self.term(INFO,' {0} = Command recieved'.format('{: >4}'.format(RCMD)))
        self.term(INFO,' {0} = Function verbose'.format('{: >4}'.format(FUNC)))
        self.term(INFO,' {0} = Subfunction verbose'.format('{: >4}'.format(SUB)))
        self.term(INFO,' {0} = Raw data to server'.format('{: >4}'.format(RSEND)))
        self.term(INFO,' {0} = Raw data from server'.format('{: >4}'.format(RRECV)))
        if TTY:
            self.term(INFO,' {1}{0} = Debugging information{2}'.format('{: >4}'.format(DBG),COL['DBG'],COL['0']))
            self.term(INFO,' {1}{0} = Error* {2}'.format('{: >4}'.format(ERROR),COL['ERR'],COL['0']))
        else:
            self.term(INFO,' {0} = Debugging information'.format('{: >4}'.format(DBG)))
            self.term(INFO,' {0} = Critical Error *'.format('{: >4}'.format(ERROR)))
            
        self.term(INFO,' * Cannot be disabled')
        self.term(INFO,'Current debug level is set to 0x{0:X}/{0:d}'.format(self.config['debug']))

        try:
            with open('USERS','r') as f:
                self.userMasks=json.load(f)
        except: self.userMasks={}

        self.term(INFO,'- Setting Variables')
        self.game={
            'name':     'Current game setup name.',
            'core':     'Current games core information..',
            'players':  'Contains a lower case list of players in the game.',
            'alive':    'Cross ref with players. Alive players are 1, dead are 0.',
            'role':     'Cross ref with players. Roles are stored here.',
            'votes':    'A nasty map contain who is voting for who.'
        }
        self.botIsAlive = True
        self.pingChannel=''
        self.buffer={'in':'','out':'','line':''}
        self.misc={'bottle':(random.random()*50)+1,'timebomb':{'wire':'','sender':''}}
        self.currentGame={'type':'','phase':0,'players':{'nick':'','role':'','alignment':''},'alive':[],'day':0}
        self.s = None
        self.nicksInChannel={}

        self.term(INFO,'- Loading command modules')

        self.cmds={'all':[]}
        self.regexp={'all':[],'cmd':{},'reg':{}}
        #Dynamic Importing
        for each in os.listdir(os.getcwd()):
            if '.py' in each and 'cmd_' in each[0:4] and '.pyc' not in each:
                each = each.split('.')[0]
                try:
                    exec('self.m{0} = __import__(\'{0}\')'.format(each))

                    exec('self.c{0} = self.m{0}.cmds(self)'.format(each))
                    exec('self.r{0} = self.m{0}.regexp(self)'.format(each))

                    each = each.split('_')[1]
                    self.cmds[each]=[]
                    self.regexp['cmd'][each]=[]
                    self.regexp['reg'][each]=[]
                    self.term(INFO,'-- {0} Module imported sucessfully'.format(each.split('_')[0].capitalize()))
                except Exception, e:
                    self.term(ERROR,'Importing {0}.py Failed. -> '.format(each,e))

        self.buildCommandList()
        self.buildRegExps()

        self.term(INFO,' {0} initalised.'.format(NAME))
        self.connect()

#######################
### TERMINAL OUTPUT ###
#######################
    def term(self,lvl,text):
        try:
            text = text.strip('\r')
            text = text.strip('\n')
        except:
            pass
        if self.config['debug']&lvl > 0 or lvl==INFO or lvl==ERROR:
            if lvl is RCMD:
                message = self.getMessage()
                if message is not None:
                    text = '{0} command called with {1} by {2}'.format(text,message,self.getFullHost())
                else:
                    text = '{0} command called by {1}'.format(text,self.getFullHost())
            elif lvl is RX:
                text = 'Regexp match for {0} {1} triggered by {2}'.format(text[0],text[1],self.getFullHost())
            elif lvl is INFO and TTY:
                text = '{1}{0}{2}'.format(text,COL['INF'],COL['0'])
            elif lvl is ERROR:
                if TTY:
                    text = '{1} ERROR: {0} {2}'.format(text,COL['ERR'],COL['0'])
                else:
                    text = 'ERROR: {0}'.format(text)
            elif lvl is RRECV and TTY:
                text = '{1}{0}{2}'.format(text,COL['REC'],COL['0'])

            if lvl is DBG and TTY:
                text='{1}{0}{2}'.format(text,COL['DBG'],COL['0'])

            if TTY:
                print '{3}{0}|{1}| {4}{2}'.format(time.strftime("%d%m%y %H:%M:%S ", time.gmtime()),'{: ^5}'.format(lvl),text.replace('\x02','').replace('\x03',''),COL['REC'],COL['0'])
            else:
                print '{0}|{1}| {2}'.format(time.strftime("%d%m%y %H:%M:%S ", time.gmtime()),'{: ^5}'.format(lvl),text.replace('\x02','').replace('\x03',''))

##################
### IRC OUTPUT ###
##################
    def quote(self,text):
        text = str(text)
        self.term(RSEND,'IRC.QUOTE-> {0}'.format(text))
        text = text.replace('\\x02','\x02').replace('\\x03','\x03').replace('\\x0f','\x0F').replace('\\x0F','\x0F')
        self.s.send('{0}\r\n'.format(text))

    def send(self, text, nick=False, channel=False):
        text+='\r\n'
        if channel is False:
            channel = self.getChannel()
        if nick is True:
            text = '\x032\x02-{0}->\x0F {1}'.format(self.getNick(),text)
        self.term(RSEND,'IRC.SEND\t-> {0}'.format(text))
        self.s.send('PRIVMSG {0} :{1}\r\n'.format(channel,text))

    def notice(self,text,target):
        self.term(RSEND,'IRC.NOTICE\t-> {0}'.format(text))
        self.s.send('NOTICE {0} :{1}\r\n'.format(target,text))

#####################
### SUB FUNCTIONS ###
#####################
    def getNick(self):
        nick = self.buffer['line'][1:].split('!')[0]
        self.term(SUB,'Nick\t\t-> {0}'.format(nick))
        return nick

    def getHost(self):
        host = self.buffer['line'].split()[0].split('@')[1]
        self.term(SUB,'Host\t-> {0}'.format(host))
        return host

    def getUser(self):
        user = self.buffer['line'].split()[0].split('!')[1].split('@')[0]
        self.term(SUB,'User\t-> {0}'.format(user))
        return user

    def getFullHost(self):
        hostmask = self.buffer['line'].split()[0][1:]
        self.term(SUB,'Hostmask\t-> {0}'.format(hostmask))
        return hostmask
        
    def getChannel(self):
        channel = self.buffer['line'].split('PRIVMSG ')[1].split(' :')[0]
        self.term(SUB,'Channel\t-> {0}'.format(channel))
        return channel

    def getMessage(self):
        try:
            message = self.buffer['line'].split(':',2)[2].split(' ',1)[1]
        except:
            message = None

        if message == '' or message == ' ':
            message = None
        self.term(SUB,'getMessage\t-> {0}'.format(message))
        return message

    def getArg(self,argument=0):
        argument+=1
        try:
            arg = self.buffer['line'].split(':',2)[2].split()[argument]
        except:
            arg = None
    
        self.term(SUB,'getArg\t-> {0}'.format(arg))
        return arg

    def saveConfig(self):
        self.term(SUB,'Saving configuration')
        try:
            with open('CONFIG','w') as f:
                json.dump(self.config,f)
        except:
            self.term(ERROR,'Unable to save config file.')

##########################
### INTERNAL FUNCTIONS ###
##########################
    def buildCommandList(self):
        for cat in self.cmds:
            if 'all' in cat: continue
            for cmd in dir(eval('self.ccmd_'+cat)):
                if '_' not in cmd[0]:
                    self.cmds[cat]+=[cmd.lower()]
                    self.cmds['all']+=[cmd.lower()]
        self.term(INFO,'- Commands Registered')
        for each in self.cmds:
            self.cmds[each].sort()
            if each is 'all': continue
            self.term(INFO,'-- {0}-> {1}'.format('{0: <6}'.format(each.upper()),str(self.cmds[each])))

    def buildRegExps(self):
        for cat in self.regexp['cmd']:
            if 'all' in cat: continue
            for rx in dir(eval('self.rcmd_'+cat)):
                try:
                    if '_' not in rx[0]:
                        self.regexp['cmd'][cat]+=[rx]
                        self.regexp['reg'][cat]+=[re.compile(eval('self.rcmd_{0}.{1}.__doc__'.format(cat,rx)))]
                except:
                    pass
        self.term(INFO,'- Regular Expressions Registered')
        for each in self.regexp['cmd']:
            if each is 'all': continue
            self.term(INFO,'-- {0}-> {1}'.format('{0: <6}'.format(each.upper()),str(self.regexp['cmd'][each])))

    def checkOwner(self):
        usermask = self.getFullHost()
        for each in range (0,9):
            usermask = usermask.replace('each','9')
        usermask = usermask.replace('999','*').replace('99','*').replace('9','*')
        if self.config['owner'] in usermask:
            self.term(FUNC,'Permission check... Granted.')
            return True
        else:
            if TTY:
                self.term(FUNC,'Permission check... \033[91mDenied\033[0m')
            else:
                self.term(FUNC,'Permission check... Denied.')
            self.send('You do not have permission to use this command.',nick=True)
            return False

    def doCTCP(self):
        ctcpReply = ''
        if 'ACTION' in self.buffer['line']:
            return None
        elif 'VERSION' in self.buffer['line'].upper():
            self.term(RCMD,'CTCP VERSION')
            ctcpReply = 'VERSION {0}'.format(VERSION)
        elif 'TIME' in self.buffer['line'].upper():
            self.term(RCMD,'CTCP TIME')
            ctcpReply = 'TIME {0}'.format(time.strftime("%y-%d-%m %H:%M:%S ", time.localtime()))
        elif 'PING' in self.buffer['line'].upper():
            self.term(RCMD,'CTCP PING')
            try:
                ctcpReply = 'PING {0}'.format(self.getArg()[:-1])
            except:
                return ''
        elif 'SOURCE' in self.buffer['line'].upper():
            self.term(RCMD,'CTCP SOURCE')
            ctcpReply = 'SOURCE '+SOURCE

        self.term(SUB,'NCTCP {0} {1}'.format(ctcpReply,self.getNick()))
        try:self.notice('\x01{0}\x01'.format(ctcpReply),self.getNick())
        except: self.term(INFO,'CTCP Reply failed.')

################
### BOT CORE ###
################
    def nsid(self):
        with open('NICKSERV','r') as f:
            nsconf = json.load(f)
        if nsconf['username'] is not '':
            self.quote('PRIVMSG NickServ :IDENTIFY {0} {1}'.format(nsconf['username'],nsconf['password']))

    def connect(self):
        self.term(INFO,'Connecting to {0} on port {1}'.format(self.config['host'],self.config['port']))
        self.s = socket.socket()
        self.s.connect((self.config['host'], self.config['port']))
        connected = False
        while not connected:
            self.buffer['in']=self.buffer['in']+str(self.s.recv(1024))
            self.buffer['out']=self.buffer['in'].split("\r\n")
            self.buffer['in']=self.buffer['out'].pop()
            for self.buffer['line'] in self.buffer['out']:
                if 'Checking Ident' in self.buffer['line']:
                    self.quote('NICK {0}'.format(self.config['nick'][0]))
                    self.currentNick = self.config['nick'][0]
                    self.quote('USER {0} {1} bla :{2}'.format(self.config['ident'], self.config['host'], self.config['realName']))
                    self.nsid()
                try:
                    irccode = int(self.buffer['line'].split()[1])

                    if irccode == 4:
                        self.term(INFO,'Connection Established.')
                    elif irccode == 433:
                        self.quote('NICK {0}'.format(self.config['nick'][1]))
                        self.currentNick = self.config['nick'][1]
                    if irccode != 372:
                        self.term(RRECV,self.buffer['line'])
                except:
                    self.term(RRECV,self.buffer['line'])
                    try:
                        if ':{0} MODE {0} :+i'.format(self.currentNick) in self.buffer['line']:
                            for channel in self.config['channels']:
                                self.quote('JOIN {0}'.format(channel))
                            connected = True
                    except: pass
        self.mainLoop()

    def mainLoop(self):
        while self.botIsAlive:
            self.buffer['in']=self.buffer['in']+str(self.s.recv(1024))
            self.buffer['out']=self.buffer['in'].split("\r\n")
            self.buffer['in']=self.buffer['out'].pop()
            for self.buffer['line'] in self.buffer['out']:
                self.term(RRECV,self.buffer['line'])
                if 'PING' in self.buffer['line'] and '\x01' not in self.buffer['line']:
                    self.quote('PONG {0}'.format(self.buffer['line'].split(' ')[1]))
                elif '\x01' in self.buffer['line'] and 'PRIVMSG' in self.buffer['line']:
                    self.doCTCP()
                elif ':\x01PING' in self.buffer['line'] and 'NOTICE' in self.buffer['line']:
                    pingReply=float(self.buffer['line'].split()[4][:-1])
                    roundTime = time.time()-pingReply
                    self.quote('PRIVMSG {0} :{1} has a ping response of {2} seconds.'.format(self.pingChannel,self.getNick(),str(round(roundTime,2))[:4]))

                if 'KICK' in self.buffer['line'] and self.currentNick in self.buffer['line'].split()[3]:
                    time.sleep(1)
                    self.quote('JOIN {0}'.format(self.buffer['line'].split()[2]))

                ####Stuff for bans - Saves last known hostmask
                try:
                    if self.buffer['line'][1:].split('!')[0] not in self.userMasks or self.buffer['line'].split()[0].split('@')[1] not in self.userMasks[self.buffer['line'][1:].split('!')[0]]:
                        self.userMasks[self.buffer['line'][1:].split('!')[0]] = self.buffer['line'].split()[0].split('@')[1]
                        with open('USERS','w') as f:
                            json.dump(self.userMasks,f)
                except:
                    pass

                for cat in self.regexp['cmd']:
                    for cmd in self.regexp['cmd'][cat]:
                        rx = re.compile(eval('self.rcmd_{0}.{1}.__doc__'.format(cat,cmd)))
                        try:
                            match = rx.search(self.buffer['line'].split(':',2)[2])
                        except:
                            match = None
                        if match is not None:
                            self.term(RX,(cat,cmd))
                            exec('self.rcmd_{0}.{1}({2})'.format(cat,cmd,match))

                for pref in self.config['prefix']:
                    try:
                        if pref in self.buffer['line'].split(':',2)[2][0]:
                            command = self.buffer['line'].split(':',2)[2].split(' ',1)[0][1:].lower()
                                    
                            if 'modreload' in command and self.checkOwner():
                                    try:
                                        module = self.getArg().lower()
                                        if module in self.cmds:
                                            exec('reload(self.mcmd_'+module+')')
                                            exec('self.c{0} = self.mcmd_{0}.cmds(self)'.format(module))
                                            self.term(INFO,'Module reloaded.')
                                            self.send('{0} has been reloaded. Use list {1} to see commands.'.format(module.capitalize(),module))
                                            for each in self.cmds:
                                                self.cmds[each]=[]
                                            self.buildCommandList()
                                            self.buildRegExps()
                                    except Exception, e:
                                        self.term(ERROR,'Unable to reload module -> {0}'.format(e))
                                    continue

                            elif 'modload' in command and self.checkOwner():
                                module = self.getArg().lower()
                                if 'mcmd_{0}'.format(module) in dir(self):
                                    self.send('Module already loaded, use modreload',nick=True)
                                    self.term(ERROR,'Module {0} already loaded'.format(module))
                                    continue
                                elif 'cmd_{0}.py'.format(module) in os.listdir(os.getcwd()):
                                    try:
                                        exec('self.mcmd_{0} = __import__(\'cmd_{0}\')'.format(module))
                                        exec('self.ccmd_{0} = self.mcmd_{0}.cmds(self)'.format(module))
                                        self.cmds[module]=[]
                                        self.term(INFO,'{0} module imported sucessfully'.format(module))
                                        self.send('{0} module has been sucessfully loaded.'.format(module),nick=True)
                                    except Exception, e:
                                        self.term(ERROR,'Importing cmd_{0}.py Failed. -> '.format(module,e))

                                    try:
                                        for each in self.cmds:
                                            self.cmds[each]=[]
                                        self.cmds[module]=[]
                                        self.buildCommandList()
                                        self.buildRegExps()
                                    except Exception, e:
                                        self.term(ERROR,'Unable to rebuild command list.')
                                    continue
                                else:
                                    self.send('cmd_{0}.py not found in {1}'.format(module,os.getcwd())

                            elif 'modunload' in command and self.checkOwner():
                                module = self.getArg().lower()
                                try:
                                    exec('del self.mcmd_{0}'.format(module))
                                    exec('del self.ccmd_{0}'.format(module))
                                    exec('del self.cmds[\'{0}\']'.format(module))
                                    self.send('{0} module removed'.format(module))
                                    self.term(INFO,'{0} module removed'.format(module))
                                    for each in self.cmds:
                                        self.cmds[each]=[]
                                    self.buildCommandList()
                                except Exception, e:
                                    self.term(ERROR,'Removing {0} module has failed.')

                            for each in self.cmds:
                                each = each.lower()
                                if 'all' in each:
                                    continue

                                if command in self.cmds[each]:
                                    self.term(RCMD,command)
                                    if each is 'owner':
                                        self.term(DBG,'Command is in owner group')
                                        if self.checkOwner() is False:
                                            self.send('You don\'t have the permission required to do that.')
                                            break
                                        else:
                                            self.term(DBG,'Executing command')
                                            try: exec('self.ccmd_{0}.{1}()'.format(each,command))
                                            except Exception, e: self.term(ERROR,'Command failed to execute  -->  self.ccmd_{0}.{1}()'.format(each,command,e))
                                            break
                                    else:
                                        self.term(DBG,'Executing command')
                                        try: exec('self.ccmd_{0}.{1}()'.format(each,command))
                                        except Exception,e: self.term(ERROR,'Command failed to execute  -->  self.ccmd_{0}.{1}()  -->  {2}'.format(each,command,e))
                                        break
                    except: pass


if __name__ == "__main__":
    bugbot().start()
