#!/usr/bin/env python
"""
USAGE:

./bot.py nickname channel [other channels...]

Don't prepend a # to chan names
Tofbot will connect to freenode.net
"""

from irc import Bot
from jokes import Jokes
from chucknorris import ChuckNorrisFacts
from riddles import Riddles
from tofades import Tofades
from fortunes import Fortunes
import random
import sys

class Riddle(object):
    def __init__(self, riddle, answer, channel, writeback):
        self.riddle = riddle
        self.answer = answer
        self.channel = channel
        self.writeback = writeback
        self.remaining_msgs = 4
        self.writeback(self.riddle)

    def wait_answer(self, chan):
        if chan != self.channel:
            return False
        self.remaining_msgs -= 1
        if (self.remaining_msgs == 0):
            self.writeback(self.answer)
            return True
        return False

class Tofbot(Bot):

    def __init__(self, nick, name, channels, password=None):
        Bot.__init__(self, nick, name, channels, password)
        self._jokes = Jokes()
        self._chuck = ChuckNorrisFacts()
        self._tofades = Tofades()
        self._riddles = Riddles()
        self._fortunes = Fortunes()
        self.joined = False

    def dispatch(self, origin, args):
        print ("o=%s a=%s" % (origin.sender, args))
        
        commandType = args[1]
        
        if self.joined :
            
            if commandType == 'PRIVMSG':
                msg = args[0]
                chan = args[2]
                
                if chan == self.nick:
                    chan = self.channels[0]
                
                if (msg == '!help'):
                    self.msg(chan, "Commands : !blague !chuck !tofade !devinette !fortune !help")
                    self.msg(chan, "Commands ")
                if (msg == '!fortune'):
                    self.cmd_fortune(chan)
                if (msg == '!blague'):
                    self.cmd_blague(chan)
                if (msg == '!chuck'):
                    self.cmd_chuck(chan)
                if (msg == '!tofade'):
                    self.cmd_tofade(chan)
                if (msg == '!devinette' and not self.active_riddle()):
                    self.devinette = self.random_riddle(chan)
                if self.active_riddle():
                    if (self.devinette.wait_answer(chan)):
                        self.devinette = None
                if self.joined:
                    random.seed()
                    if random.randint(0, 100) > 98:
                        self.cmd_tofade(chan)
            elif commandType == 'JOIN':
                chan = args[0]
                self.cmd_tofade(chan)
                
        else :
            if (args[0] == 'End of /MOTD command.'):
                for chan in self.channels:
                    self.write(('JOIN', chan))
                self.joined = True

    def active_riddle(self):
        return (hasattr(self, 'devinette') and self.devinette is not None)

    def cmd_blague(self, chan):
        self.msg(chan, self._jokes.get())

    def cmd_fortune(self, chan):
        self.msg(chan, self._fortunes.get())

    def cmd_chuck(self, chan):
        self.msg(chan, self._chuck.get())
    
    def cmd_tofade(self, chan):
        self.msg(chan, self._tofades.get())

    def random_riddle(self, chan):
        text = self._riddles.get()
        r = Riddle (text[0], text[1], chan, lambda msg: self.msg(chan, msg))
        return r
        
if __name__ == "__main__":
	if len(sys.argv) > 2:
		chans = [ "#" + s for s in sys.argv[2:] ]
		b = Tofbot(sys.argv[1], 'Tofbot', chans)
		b.run('irc.freenode.net')
	else:
		print __doc__
