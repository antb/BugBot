from globalInfo import *
import re

class cmds:
    """Operator commands"""
    def __init__(self,parent):
        self._parent = parent

    def voice(self,channel=None,users=None):
        """<User[s]>

        Gives voice to a user (+v)"""
        if users is None:
            users = self._parent.getMessage()
            count = len(self._parent.getMessage().split())
        else:
            count = len(self._parent.getMessage().split())

        if channel is None:
            channel = self._parent.getChannel()

        self._parent.quote('MODE {0} +{1} {2}'.format(channel,'v'*count,users))

    def op(self,channel=None,users=None):
        """<User[s]>

        Gives op to a user (+o)"""
        if users is None:
            users = self._parent.getMessage()
            count = len(self._parent.getMessage().split())
        else:
            count = len(self._parent.getMessage().split())

        if channel is None:
            channel = self._parent.getChannel()

        self._parent.quote('MODE {0} +{1} {2}'.format(channel,'o'*count,users))

    def devoice(self,channel=None,users=None):
        """<User[s]>

        Removes voice from users (-v)"""
        if users is None:
            users = self._parent.getMessage()
            count = len(self._parent.getMessage().split())
        else:
            count = len(self._parent.getMessage().split())

        if channel is None:
            channel = self._parent.getChannel()

        self._parent.quote('MODE {0} -{1} {2}'.format(channel,'v'*count,users))

    def deop(self,channel=None,users=None):
        """<User[s]>

        Removes ops from a user (-o)"""
        if users is None:
            users = self._parent.getMessage()
            count = len(self._parent.getMessage().split())
        else:
            count = len(self._parent.getMessage().split())

        if channel is None:
            channel = self._parent.getChannel()

        self._parent.quote('MODE {0} -{1} {2}'.format(channel,'o'*count,users))

    def ban(self):
        """<user> ['kick'] [ip/host]

        Bans <user> using [ip/host] and kicks if specified"""
        args = self._parent.getMessage().split()
        user = self._parent.userMasks[args[0]]
        kick = 'kick' in args
        bantype = 'ip'

        if   'user' in args: bantype = 'user'
        elif 'ip' in args: bantype = 'ip'
        elif 'host' in args: bantype = 'host'

        if bantype is 'ip':
            bm = self._ip(user)
        elif bantype is 'host':
            bm = self._host(user)

        self._parent.quote('MODE {0} +b {1}'.format(self._parent.getChannel(),bm))

    def _ip(self,user,d=True):
        """SUBROUTINE - Get IP mask from hostmask for bans"""
        ipmask = re.compile(r'[0-9]{1,3}[.-][0-9]{1,3}[.-][0-9]{1,3}[.-][0-9]')
        result = ipmask.search(user)
        try:
            bm = result.group(0)
            bm = '*!*@*{0}*'.format(bm)
            return bm
        except:
            if d: return self._host(user,d=False)

    def _host(user,d=True):
        """SUBROUTINE - Get host from hostmask for bans"""
        user = user.split('@')[1]
        for each in range(0,10):
            user = user.replace(each,'?')
        alpha = []
        alpha +='qwertyuiopasdfghjklzxcvbnm' #import laziness :D
        for each in alpha:
            if alpha in user:
                return '*!*@*'+user
        if d: return self._ip(user,d=False)

