#!/usr/bin/env python

class genPlugin:
    def __init__(self):
        print "\
         ---------------------------\n\
        | BugBot Blank Plugin Maker |\n\
         ---------------------------\n\
                 | By AntB |\n\
                  ---------"

        filename = raw_input('What\'s the name of your plugin? ')
        desc = raw_input('Give a brief description of your plugin: ')

        try:
            with open('cmd_{0}.py'.format(filename),'w') as f:
                f.write('from globalInfo import *\n\nclass cmds:\n    """{0}"""\n    def __init__(self,parent):\n        self._parent = parent\n\nclass regexp:\n    def __init__(self,parent):\n        self._parent = parent'.format(desc))
        except:
            print "It failed."
            exit()

genPlugin()
