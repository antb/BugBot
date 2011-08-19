from globalInfo import *
import threading,random,time

class cmds:
    """Enables mafia to be played."""
    def __init__(self,parent):
        self._parent = parent
        self.game={}
        self.channel='#mafia'
        self.mafchannel='##mafia_'
        self.randChars='QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
        random.seed()
        random.seed(random.random())

    def start(self):
        """Starts a game of mafia."""
        self.game['initialised'] = True
        self.game['phase']='sign'
        self._parent.send('\x02A game of mafia has begun. A minimum of 5 players are required to begin. Signups will last for 2 minutes.\x07')
        self.t = self.Timer(120,_checkSetup)


    def join(self):
        """Joins a game in the signup phase."""
        if self.game['initislised'] is False:
            self.game['players']+=[self.getNick]
            self.start()
        if self.game['phase']='sign':
            self.game['players']+=[self.getNick]
            self._parent.quote+=('MODE {0} +v {1}'.format(self.channel)
            self._parent.send('\x02{0} has joined the game. {1} players are currently signed up.'.format(self.getNick,len(self.game['players'])))

    def _checksetup(self)
        if len(self.game['players']) < 5:
            self._parent.send('Not enough players have joined for a game to start.')
            players=''
            for each in self.game['players']:
                players='{0} {1}'.format(players,each)

            self._parent.quote('MODE {0} -{1} {2}'.format(self.channel,'v'*len(self.game['players']),players)
            self._resetData()
            
        else:
            self._parent.send('\x02 -- GAME START --\x07')
            self._parent.quote('MODE +m {0}'.format(self.channel))
            self._genSetup()

    def _genSetup(self):
        playerCount = len(self.game['players'])
        mafiaCount = playercount/3
        self.game['phase']='setup'

        self._parent.send('\x02{0} players gives us {1} Mafia.\x07'.format(playerCount,len(self.game['mafia'])))                

        for each in self.game['players']:
            chance = random.randint(1,3):
            if chance = 1:
                self.game['mafia']+=[each]
            else:
                self.game['town']+=[each]
        
        if len(self.game['mafia']) > 1:
            suffix=''
            for each in range(1,random.randint(1,4):
                suffix='{0}{1}'.format(suffix,self.randChars[random.randint(0,len(self.randChars)))
                self.trueChannel = '{0}{1}'.format(self.mafChannel,suffix)
            self._parent.quote('JOIN {0}'.format(self.trueChannel))
            time.sleep(1)
            self._parent.quote('MODE +Cilstm {1}'.format(self.trueChannel))
            time.sleep(1)
            self._parent.quote('TOPIC {0} :MAFIA CHAT AREA - Only to be used at night. Talking outside of this channel is forbidden.'.format(self.trueChannel))
            for each in self.game['mafia']:
                self._parent.quote('INVITE {0} :{1}'.format(each,self.trueChannel))
        for each in self.game['mafia']
            if self.trueChannel is not False:
                self._parent.send('You are a mafia member. You buddies are waiting for you in {0}'.format(self.trueChannel),nick=each)
            else:
                self._parent.send('You\'re a man on a mission to take out as many as you can',nick=each)
            self._parent.send('To kill someone, send !kill <player>.'nick=each)
            time.sleep(1)

        for each in self.game['town']:
            self._parent.send('You are a townsperson, trying to eliminate the mafia in the village.',nick=each)
            time.sleep(1)

        self._parent.send('Alignments have been sent out. Trying for Power Roles...')

        for each in self.game['town']:
            if self.game['roles']['cop'] is False and random.randint(0,10)<4 and len(self.game['town']) > 4:
                self.game['roles']['cop']=each
                self._parent.send('A Cop has joined us...')
                self._parent.send('You are the Detective. You may use !inspect <player> to learn someones alignment.',nick=each)
                time.sleep(1)

        for each in self.game['town']:
            if self.game['roles']['vig'] is False and random.randint(0,10)<4 and len(self.game['town']) > 5 and each not in self.game['roles']['cop']:
                self.game['roles']['vig']=each
                self._parent.send('A Vigilante has joined us...')
                self._parent.send('You are the vigilante. You may kill during the night phase by sending !kill <player>.',nick=each)
                time.sleep(1)
        
        self.game['alive'] = self.game['players']
        self._parent.send('Power roles (if any) have been distributed. Everyone in game has recieved a message, and so the game will now begin.')

        self._enterNightPhase(0)

    def _enterNightPhase(self,number):
        self.send('It is now Night {0}. Night will end in 1 minute.'.number)
        self._parent.quote('MODE -m {0}'.self.trueChannel)
        self._showLivingPlayers()
        self.t = Timer(60,'self._enterDayPhase({0})'.format(number))

    def kill(self):
        player = self._parent.getNick()
        target = self._parent.getMessage()
        if player in self.game['mafia']:
            targetFound = False
            for each in self.game['alive']
                if target.lower() in each.lower():
                    self.game['mafiakill']=(player,target)
                    targetFound = True
            if targetFound is False:
                self.send('Invalid target.',nick=player)



    class Timer(threading.Thread):
        def __init__(self, seconds, callback):
            self.runTime = seconds
            threading.Thread.__init__(self)
        def run(self):
            time.sleep(self.runTime)
            exec(callback)

class regexp:
    def __init__(self,parent):
        self._parent = parent
                
