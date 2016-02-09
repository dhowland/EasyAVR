# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2013-2016 David Howland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This file defines a window that allows input of password generator
parameters.
"""

from __future__ import print_function

import sys
import copy
import struct
import random

try:
    from Tkinter import *
    from ttk import *
    import tkSimpleDialog as simpledialog
    import tkMessageBox as messagebox
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import simpledialog
    from tkinter import messagebox


NUM_PASSWORDS = 4
MAX_SECRET_LEN = 40
MIN_PASSWORD_LEN = 4
MAX_PASSWORD_LEN = 40
DEFAULT_PASSWORD_LEN = 20

struct_format = '40sBBBBBB'

py3k = (sys.version_info.major == 3)

class Password(object):

    def __init__(self, data=None):
        self.data = PGData(data)
    
    def popup(self, root, limit):
        new_win = PGWindow(root, "Password Generator", self.data, limit)
        if new_win.result:
            self.data = new_win.result

    def getstruct(self):
        return self.data.export()

    def getstring(self):
        return b''.join([struct.pack(struct_format, *tup) for tup in self.data.export()])


class PGData(object):
    
    def __init__(self, data=None):
        self.create()
        if data is not None:
            self.initialize(data)

    def create(self):
        self.secrets = [''] * NUM_PASSWORDS
        self.lengths = [DEFAULT_PASSWORD_LEN] * NUM_PASSWORDS
        chardict = {'lowers': True, 'uppers': True, 'numbers': True, 'symbols': True}
        self.charsets = [chardict.copy() for i in range(NUM_PASSWORDS)]

    def initialize(self, data):
        if len(data) != NUM_PASSWORDS:
            raise ValueError('Initialization data must be of length %d' % NUM_PASSWORDS)
        for i,tup in enumerate(data):
            if not isinstance(tup, tuple):
                raise TypeError('Initialization data must contain tuples')
            if len(tup) != 7:
                raise ValueError('Initialization data must contain tuples of length 7')
            if len(tup[0]) != tup[1]:
                raise ValueError('Inconsistency in length of secret string')
            if py3k:
                if not isinstance(tup[0], str):
                    self.secrets[i] = tup[0].decode(encoding="utf-8")
            else:
                self.secrets[i] = tup[0]
            self.charsets[i]['lowers'] = bool(tup[2])
            self.charsets[i]['uppers'] = bool(tup[3])
            self.charsets[i]['numbers'] = bool(tup[4])
            self.charsets[i]['symbols'] = bool(tup[5])
            self.lengths[i] = str(tup[6])

    def export(self):
        output = []
        for i in range(NUM_PASSWORDS):
            if py3k:
                secretstr = bytes(self.secrets[i], encoding="utf-8")
            else:
                secretstr = self.secrets[i]
            tup = (
                secretstr,
                len(self.secrets[i]),
                int(self.charsets[i]['lowers']),
                int(self.charsets[i]['uppers']),
                int(self.charsets[i]['numbers']),
                int(self.charsets[i]['symbols']),
                int(self.lengths[i])
            )
            output.append(tup)
        return output


class PGWindow(simpledialog.Dialog):

    def __init__(self, root, title, data, max_length=MAX_PASSWORD_LEN):
        if not isinstance(data, PGData):
            raise TypeError('PGWindow requires a PGData object')
        self.indata = data
        self.max_length = max_length
        simpledialog.Dialog.__init__(self, root, title)

    def body(self, master):
        self.resizable(0, 0)
        self.secrets = []
        self.lengths = []
        self.charsets = []
        self.testinputs = []
        self.testoutputs = []
        for i in range(NUM_PASSWORDS):
            Label(master, text="PW Gen #%d" % (i+1)).pack(fill=X)
            f = self.oneframe(master)
            f.pack(fill=X)
            Separator(master, orient=HORIZONTAL).pack(fill=X, pady=4)
        self.filldata()

    def oneframe(self, master):
        container = Frame(master)
        top_frame = Frame(container)
        Label(top_frame, text="Secret string: ").pack(side=LEFT, pady=2)
        secret = StringVar()
        e = Entry(top_frame, width=45, textvariable=secret, show='*')
        e.pack(fill=X, expand=True, side=LEFT, pady=2)
        self.secrets.append(secret)
        hidesecret = StringVar()
        hidesecret.set('True')
        cmd = self.hideaction(e, hidesecret)
        Checkbutton(top_frame, text='*', variable=hidesecret, onvalue='True',
                    offvalue='False', command=cmd).pack(side=LEFT, pady=2)
        Frame(top_frame, width=5).pack(side=LEFT, pady=2)
        cmd = self.randaction(secret)
        Button(top_frame, text="Randomize", command=cmd).pack(side=LEFT, pady=2)
        top_frame.pack(fill=X)
        middle_frame = Frame(container)
        Label(middle_frame, text="Password length: ").pack(side=LEFT, pady=2)
        outlen = StringVar()
        Entry(middle_frame, width=3, textvariable=outlen).pack(side=LEFT, pady=2)
        self.lengths.append(outlen)
        Label(middle_frame, text="    ").pack(side=LEFT, pady=2)
        vars = {}
        for charset in ('lowers', 'uppers', 'numbers', 'symbols'):
            usecharset = StringVar()
            Checkbutton(middle_frame, text='Use %s  '%charset, variable=usecharset,
                        onvalue='True', offvalue='False').pack(side=LEFT, pady=2)
            usecharset.set('True')
            vars[charset] = usecharset
        self.charsets.append(vars)
        middle_frame.pack(fill=X)
        bottom_frame = Frame(container)
        Label(bottom_frame, text="Test input: ").pack(side=LEFT, pady=2)
        testinput = StringVar()
        Entry(bottom_frame, width=16, textvariable=testinput, show='*').pack(side=LEFT, pady=2)
        self.testinputs.append(testinput)
        Label(bottom_frame, text="  Test output: ").pack(side=LEFT, pady=2)
        testoutput = StringVar()
        Entry(bottom_frame, width=45, textvariable=testoutput, state='readonly').pack(fill=X, expand=True, side=LEFT, pady=2)
        self.testoutputs.append(testoutput)
        bottom_frame.pack(fill=X)
        # trace all the inputs so they can be used for updating the test output
        closure = self.testaction(testinput, testoutput, secret, outlen, vars)
        testinput.trace('w', closure)
        testoutput.trace('w', closure)
        secret.trace('w', closure)
        outlen.trace('w', closure)
        for var in vars.values():
            var.trace('w', closure)
        return container

    def filldata(self):
        for i in range(NUM_PASSWORDS):
            self.secrets[i].set(self.indata.secrets[i])
            self.lengths[i].set(self.indata.lengths[i])
            for k in self.charsets[i]:
                self.charsets[i][k].set(repr(self.indata.charsets[i][k]))

    def hideaction(self, entry, hidevar):
        def onevent():
            if (hidevar.get() == 'True'):
                entry['show'] = '*'
            else:
                entry['show'] = ''
        return onevent

    def randaction(self, secret):
        def onevent():
            s = ''.join([chr(random.randint(32,126)) for i in range(MAX_SECRET_LEN)])
            secret.set(s)
        return onevent
    
    def testaction(self, invar, outvar, secretvar, outlen, sets):
        def onevent(*args):
            s = ''
            secret = secretvar.get()
            password = invar.get()
            if (len(secret) > 0) and (len(password) > 0):
                try:
                    length = int(outlen.get())
                except:
                    length = 0
                if (length >= MIN_PASSWORD_LEN) and ((length <= self.max_length) or (self.max_length == 0)):
                    use_lowers = (sets['lowers'].get() == 'True')
                    use_uppers = (sets['uppers'].get() == 'True')
                    use_numbers = (sets['numbers'].get() == 'True')
                    use_symbols = (sets['symbols'].get() == 'True')
                    if (use_lowers or use_uppers or use_numbers or use_symbols):
                        s = scramble(secret, password, length, use_lowers, use_uppers, use_numbers, use_symbols)
            outvar.set(s)
        return onevent

    def validate(self):
        errormsg = []
        for i in range(NUM_PASSWORDS):
            # secret is len 4..MAX_SECRET_LEN
            if len(self.secrets[i].get()) > 0:
                if self.max_length == 0:
                    errormsg.append('PW Gen #%d: the current keyboard does not support PW Gen, the secret must remain empty' % ((i+1),))
                elif ((len(self.secrets[i].get()) < MIN_PASSWORD_LEN) or 
                      (len(self.secrets[i].get()) > MAX_SECRET_LEN)):
                    errormsg.append('PW Gen #%d: length of secret string must be between %d and %d' % ((i+1), MIN_PASSWORD_LEN, MAX_SECRET_LEN))
            # output is len MIN_PASSWORD_LEN..MAX_PASSWORD_LEN
            try:
                length = int(self.lengths[i].get())
            except ValueError:
                errormsg.append('PW Gen #%d: password length must be an integer' % ((i+1),))
                length = 0
            if (self.max_length > 0) and ((length < MIN_PASSWORD_LEN) or (length > self.max_length)):
                errormsg.append('PW Gen #%d: password length must be between %d and %d' % ((i+1), MIN_PASSWORD_LEN, self.max_length))
            # at least one charset is selected
            if not any([(x.get()=='True') for x in self.charsets[i].values()]):
                errormsg.append('PW Gen #%d: at least one character set must be selected' % ((i+1),))
        if errormsg:
            messagebox.showerror(title="Validation error",
                                 message=('\n'.join(errormsg)),
                                 parent=self.parent)
            return False
        return True

    def apply(self):
        self.result = copy.deepcopy(self.indata)
        for i in range(NUM_PASSWORDS):
            self.result.secrets[i] = self.secrets[i].get()
            self.result.lengths[i] = self.lengths[i].get()
            for k in self.charsets[i]:
                self.result.charsets[i][k] = (self.charsets[i][k].get() == 'True')


lowers = "abcdefghijklmnopqrstuvwxyz"
lowers_len = len(lowers)
lowers_end = lowers_len
uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
uppers_len = len(uppers)
uppers_end = lowers_end + uppers_len
numbers = "0123456789"
numbers_len = len(numbers)
numbers_end = uppers_end + numbers_len
symbols = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
symbols_len = len(symbols)
symbols_end = numbers_end + symbols_len

stringdata = lowers + uppers + numbers + symbols

sources = (None, lowers, uppers, numbers, symbols, stringdata)
source_lens = (0, lowers_len, uppers_len, numbers_len, symbols_len, len(stringdata))

def scramble(secret, password, length, use_lowers=True, use_uppers=True, use_numbers=True, use_symbols=False):
    uses = (False, use_lowers, use_uppers, use_numbers, use_symbols, True)
    output = [' '] * length
    state = 0
    source = 0
    # initialize the state using the secret
    for c in secret:
        state = (state + ord(c)) & 0xFF
    # initialize the starting position using the password
    pos = state
    for c in password:
        pos = (pos + ord(c)) & 0xFF
    pos = pos % length
    for i in range(length):
        pi = i % len(password)
        si = i % len(secret)
        # update the state for the next round
        state = (state + ord(password[pi])) & 0xFF
        if (state & 0x80) == 0x80:
            state = ((state << 1) + 1) & 0xFF
        else:
            state = (state << 1) & 0xFF
        state = (state ^ ord(secret[si])) & 0xFF
        # get next source
        while True:
            source = 5 if source >= 5 else (source + 1)
            if uses[source]:
                break
        # get the character for the current state
        if source < 5:
            char = sources[source][(state % source_lens[source])]
        else:
            wrap = 0
            if use_lowers: wrap += lowers_len
            if use_uppers: wrap += uppers_len
            if use_numbers: wrap += numbers_len
            if use_symbols: wrap += symbols_len
            index = (state % wrap)
            if (not use_lowers):
                index += lowers_len
            if (not use_uppers) and (index >= lowers_end):
                index += uppers_len
            if (not use_numbers) and (index >= uppers_end):
                index += numbers_len
            char = stringdata[index]
        # update output
        output[pos] = char
        pos = (pos + 1) % length
    return ''.join(output)


if __name__ == '__main__':
    print("Password must be run from the main GUI.")
