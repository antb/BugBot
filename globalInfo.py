#All this gets imported into the various files
import sys

TTY     = False
if 'linux' in sys.platform or 'BSD' in sys.platform: TTY = True

NAME    = 'BugBot'
VERSION = 'ALPHA - Python {0}.{1}.{2}'.format(sys.version_info[0],sys.version_info[1],sys.version_info[2])
SOURCE  = 'https://github.com/antb/BugBot'

COL = {}
COL['DBG'] = '\033[1m\033[94m'
COL['ERR'] = '\033[41m'
COL['INF'] = '\033[1m'
COL['REC'] = '\033[2m'
COL['0']   = '\033[0m'

INFO   = 0x000
RCMD   = 0x001
RX     = 0x002
FUNC   = 0x004
SUB    = 0x008
RSEND  = 0x010
RRECV  = 0x020
DBG    = 0x040
ERROR  = 0x100
