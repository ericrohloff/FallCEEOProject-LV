
import js
from js import navigator
from pyodide.ffi import to_js, create_proxy
import time
import asyncio
from pyscript import Element


# Utility function for converting py dicts to JS objects


def j(obj):
    return to_js(obj, dict_converter=js.Object.fromEntries)


modifier = ''
ModLUT = {'Shift': 'Shift', 'Control': 'Control',
          'Meta': 'Command', 'Alt': 'Option'}
KeyLUT = {'Enter': '\r\n', 'Backspace': '', 'ArrowUp': '\x1B[A', 'ArrowDown': '\x1B[B',
          'ArrowRight': '\x1B[C', 'ArrowLeft': '\x1B[D', 'Tab': '\t', 'Backspace': '\b'}

test = 'import machine\r\nmachine.Pin(5).value\r\n'
pSize = 10


pSize = 6


def keyDOWN(e):
    global modifier
    payload = e.key
    if (e.keyCode == 9):
        e.preventDefault()
    if payload in ModLUT:
        modifier = ModLUT[payload]


def keyUP(e):
    global modifier
    data = e.key
    payload = ''
    if data in ModLUT:
        modifier = ''  # lifted up the key
    elif data in KeyLUT:
        payload = KeyLUT[data]
    else:
        if modifier in ['Command', 'Control']:
            ctrl = ord(data)-96
            payload = chr(ctrl if ctrl > 0 else ctrl + 32)
        else:
            payload = data
    s.write(payload)


def REPL_Read():
    myREPL = js.document.querySelectorAll('py-repl .cm-line')
    output = [str(text.textContent)+"\r\n" for text in myREPL]
    return ''.join(output)


async def connect():
    js.console.log('connecting')
    await s.ask()
    asyncio.create_task(s.startReading())
    s.CtrlC()


class serialCntrl():
    def __init__(self, ref):
        self.connected = False
        self.buffer = ''
        self.consoleText = ''
        self.lastline = ''
        self.line_buffer = ''
        self.waiting = 0
        self.cursor = 0
        self.done = False
        self.ref = ref
        if not hasattr(navigator, 'serial'):
            warning = "Use Chrome"
            print(warning)
            raise NotImplementedError(warning)

    def VT100(self, text):
        # dt = [ord(text[i]) for i in range(len(text))]
        skip = 0
        for i, char in enumerate(text):
            if skip > 0:
                skip -= 1
                continue
            value = ord(char)
            # lower/uppercase letters and symbols
            if (value in [9, 10, 13]) | (32 <= value <= 126):
                self.buffer += char
                if value == 10:
                    self.lastline = self.line_buffer
                    self.line_buffer = ''
                else:
                    self.line_buffer += char
                # they are using arrow keys to move back/forward
                if self.cursor < len(self.consoleText):
                    self.consoleText = self.consoleText[:self.cursor] + \
                        char + self.consoleText[self.cursor+1:]
                else:
                    self.consoleText += char
                self.cursor += 1

            elif (value == 8):  # \b - backspace
                self.cursor -= 1
            elif (value in [0,]):  # Do nothing with these
                pass
            elif (value == 27):  # escape sequence
                skip = 2
                cmd = ord(text[i+2])
                if cmd == 75:  # delete to the end
                    self.consoleText = self.consoleText[:self.cursor]
                else:
                    print('did not recognize ESC: %d' % cmd)
            else:
                print('did not recognize: %d' % value)
        return self.consoleText

    def cprint(self, text):
        consoleText = self.VT100(text)
        Element(self.ref).element.innerText = consoleText

    async def ask(self):
        self.port = await navigator.serial.requestPort()
        await self.port.open(j({"baudRate": 115200}))
        # self.cprint('Opened Port'+str(self.port))
        self.connected = True
        # Set up encoder to write to port
        self.encoder = js.TextEncoderStream.new()
        outputDone = self.encoder.readable.pipeTo(self.port.writable)
        # Set up listening for incoming bytes
        self.decoder = js.TextDecoderStream.new()
        inputDone = self.port.readable.pipeTo(self.decoder.writable)
        self.reader = self.decoder.readable.getReader()

    async def startReading(self):
        while not self.done:
            response = await self.reader.read()
            value, end = response.value, response.done
            js.console.log("Read %d: %s" % (len(value), value.encode()))
            self.cprint(value)
            if end:
                js.console.log('Response was DONE')
                break
        self.reader.releaseLock()
        js.console.log("done")

    def write(self, data):
        '''Write to the serial port'''
        if data != '':
            outputWriter = self.encoder.writable.getWriter()
            outputWriter.write(data)
            outputWriter.releaseLock()
            js.console.log(f"Wrote: {data.encode()}")

    def send(self, data):
        if self.connected:
            size = len(self.buffer)
            self.write(data + '\r\n')
            # await asyncio.create_task(self.wait_reply(size + len(data)))
        else:
            print('no connection')

    async def wait_reply(self, size):
        count = 0
        while (size > len(self.buffer)):
            await asyncio.sleep(0.1)
            if count > 10:
                print('waited forever')
                print(self.buffer)
                break

    def CtrlC(self):
        self.send('\x03')

    def upload(self, value):
        if self.connected:
            value = value.replace('\n', '\r\n')
            self.write('\x05' + value + '\x04')
        else:
            print('no connection')

    def file_save(self, file, text):
        code = '''import os,gc\nos.remove("%s")\ngc.collect()\nwith open("%s","wb") as bfile:\n''' % (
            file, file)
        for i in range(0, len(text), pSize):
            row = str(text[i:i+pSize])
            nums = [int(ord(c)) for c in row]
            code += 'f = bfile.write(bytes(' + str(nums) + '))\n'
        code += '\n\n\n'
        for line in code.split('\n'):
            # print(line)
            self.send(line)

    def file_read(self, file):
        self.send('f = open("%s","r")' % file)
        self.send('f.read()')
        self.send('f.close()')
        self.data = self.buffer
        '''try:
            reply = self.data.split('>>> f.read()')[-1].split('\r\n>>> f.close()')[0]
            reply = reply.strip().replace('\\r\\n','\r\n').replace("'",'').encode()
        except:
            reply = None
        return reply'''
        return self.data

# https://github.com/ntoll/microfs/blob/master/microfs.py for Mu way
    def fileio_save(self, ufilename, filename):
        if not os.path.isfile(filename):
            raise IOError("No such file.")
        with open(filename, "rb") as local:
            content = local.read()
        filename = os.path.basename(filename)  # get just the name
        self.send("fd = open('{}', 'wb')".format(ufilename))
        while content:
            line = content[:64]
            self.send("fd.write(" + repr(line) + ")")
            content = content[64:]
        self.send("fd.close()")


s = None


def SerialConsole(ref):
    global s
    s = serialCntrl(ref)
    typing = js.document.querySelector('#' + ref)
    typing.addEventListener('keydown', create_proxy(keyDOWN))
    typing.addEventListener('keyup', create_proxy(keyUP))
