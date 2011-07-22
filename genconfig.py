#!/usr/bin/env python
import json,random,sys

class config:
    def __init__(self):
        random.seed()
        self.alpha = []
        self.alpha += 'abcdefghijklmnopqrstuvwxyz0123456789.#_-' #Laziness()
        if 'linux' in sys.platform:
            b = '\033[1m'
            n = '\033[0m'
        else:
            b = n = ''


        print '{0}\
         ----------------------\n\
        | BugBot Configuration |\n\
         ----------------------\n\
        | By AntB              |\n\
         ----------------------'.format(b)

        print 'This small script will configure BugBot in next to no time.'
        print 'If you make an error, just type \'menu\' into a prompt and it\'ll take'
        print 'you to a menu of all the possible options.\nThe error checking in this'
        print 'script is only very basic, so if it you can\'t connect double check'
        print 'your settings.\n'
        self.conf_user()

    def conf_user(self):
        print 'First off is your bots Ident information, which shows up in a whois.'
        self.ident = raw_input('What is your bots username? (default: BugBot){0}'.format(n))
        self.chkresponse(self.ident,'self.conf_user()')
        if self.ident is '': self.ident = 'BugBot'
        self.conf_rname()

    def conf_rname(self):
        self.realname = raw_input('{0}What\'s your bots \'Real\' Name? (default: BugBot) {1}'.format(b,n))
        self.chkresponse(self.realname,'self.conf_rname()')
        if self.realname is '': self.realname = 'BugBot'
        self.conf_server()

    def conf_server(self):
        print '{0}Now I need to know how to connect to the server of your choice.'.format(b)
        self.server = raw_input('Server address? {0}'.format(n))
        self.chkresponse(self.server,'self.conf_server()')
        if self.server is '': self.conf_server()
        self.conf_port()

    def conf_port(self):
        self.port = raw_input('{0}Port number? (default: 6667) {1}'.format(b,n))
        self.chkresponse(self.port,'self.conf_port()')
        if self.port is '': self.port = 6667
        try: self.port = int(self.port)
        except: self.conf_port()
        self.conf_nick()    

    def conf_nick(self):
        print '{0}Please enter two nicknames for your bot to use. (defaults are random nicks)'.format(b)
        self.nick1 = raw_input('Nick 1 -> {0}'.format(n))
        self.chkresponse(self.nick1,'self.conf_nick()')
        self.nick2 = raw_input('{0}Nick 2 -> {1}'.format(b,n))
        self.chkresponse(self.nick2,'self.conf_nick()')
        if self.nick1 is '':
            x=0
            while x < 8:
                self.nick1=self.nick1+self.alpha[random.randint(0,len(self.alpha)-15)]
                x+=1
        if self.nick2 is '':
            x=0
            while x < 8:
                self.nick2=self.nick2+self.alpha[random.randint(0,len(self.alpha)-15)]
                x+=1
        self.conf_nickserv()

    def conf_nickserv(self):
        nsid = raw_input('{0}Please enter your bots Nickserv username -> {1}'.format(b,n))
        self.chkresponse(nsid,'self.conf_nickserv()')        
        nspw = raw_input('{0}Please enter your bots Nickserv password (will be shown) -> {1}'.format(b,n))
        self.chkresponse(nspw,'self.conf_nickserv()')
        with open('NICKSERV','w') as f:
            data = {}
            data['username'] = nsid
            data['password'] = nspw
            json.dump(data,f)
        self.conf_channels()

    def conf_channels(self):
        print '{1}Specify some channels you\'d like {0} to join when its identified. Seperate each channel with a space.'.format(self.nick1,b)
        self.channels = raw_input('-> {0}'.format(n))
        self.channels = self.channels.split(' ')
        for each in self.channels:
            self.chkresponse(each,'self.conf_channels()')
        self.conf_prefix()

    def conf_prefix(self):
        self.prefixes = raw_input('{0}Enter the prefixes for your bot to respond to -> {1}'.format(b,n)
        self.prefixes = self.prefixes.split()
        self.generate()

    def doMenu(self):
        print "{0}--MENU--"
        print "1 - Username"
        print "2 - Realname"
        print "3 - Server"
        print "4 - Port"
        print "5 - Nicks"
        print "6 - Nickserv"
        print "7 - Channels"
        print "8 - Prefixes"
        self.doMenuChoice()

    def doMenuChoice(self):
        num = raw_input('[1-8]-> {0}'.format(n))
        try: num = int(num)
        except: self.doMenuChoice()
        if num is 1:
            self.conf_user()
        elif num is 2:
            self.conf_rname()
        elif num is 3:
            self.conf_server()
        elif num is 4:
            self.conf_port()
        elif num is 5:
            self.conf_nick()
        elif num is 6:
            self.conf_nickserv()
        elif num is 7:
            self.conf_channels()
        else:
            self.doMenuChoice()

    def generate(self):
        data = {}
        data['ident'] = self.ident
        data['realName'] = self.realname
        data['host'] = self.server
        data['port'] = self.port
        data['channels'] = self.channels
        data['nick'] = []
        data['nick']+=[self.nick1]
        data['nick']+=[self.nick2]
        data['prefix'] = self.prefixes
        data['debug'] = 1
        data['owner'] = ''
        data['isOwnerSet'] = 0
        x = 0
        while x < 15:
            data['owner']+=self.alpha[random.randint(0,len(self.alpha)-1)]
            x+=1

        with open('CONFIG','w') as f:
            json.dump(data,f)
            json.dumps(data)

        print '{0}Config file generated.'.format(b)
        print 'You will be identified as the owner using a hostmask. This means ANY'
        print 'change in your hostmask which isn\'t numerical will mean you won\'t'
        print 'be reconised.'
        print 'In order for this to work, you must send the command below:'
        print 'makeOwner {0}'.format(data['owner'])
        print 'When this command is recieved it will write your hostmask to the owner.{0}'.format(n)
        exit()
            
    def chkresponse(self,x,cmd):
        if 'menu' in x:
            self.doMenu()
        for each in x:
            if each.lower() not in self.alpha:
                print '\nInvalid response.\n'
                print 
                exec(cmd)

config()

