# ------------- serial code -----------------
import sys
import asyncio
from pyodide.ffi import to_js
import js

# Utility function for converting py dicts to JS objects


def j(obj):
    return to_js(obj, dict_converter=js.Object.fromEntries)


class SerialManager():
    def __init__(self):
        self.response = ''
        self.written = ''
        self.reply = ''
        self.connected = False

    async def askForSerial(self):
        if not hasattr(js.navigator, 'serial'):
            warning = "Use Chrome please"
            print(warning)
            raise NotImplementedError(warning)
        self.port = await js.navigator.serial.requestPort()
        await self.port.open(j({"baudRate": 115200, 'BufferSize': 5000}))
        print('Opened Port'+str(self.port))
        # Set up encoder to write to port
        self.encoder = js.TextEncoderStream.new()
        outputDone = self.encoder.readable.pipeTo(self.port.writable)

        # Set up listening for incoming bytes
        self.decoder = js.TextDecoderStream.new()
        inputDone = self.port.readable.pipeTo(self.decoder.writable)
        self.reader = self.decoder.readable.getReader()
        self.connected = True
        # await self.listenAndEcho()

    async def Write(self, data):
        outputWriter = self.encoder.writable.getWriter()
        self.written = data + '\r\n'
        outputWriter.write(self.written)
        outputWriter.releaseLock()
        js.console.log("Wrote to stream: " + data + '\r\n')

    async def listenAndEcho(self):
        '''Loop forever, echoing values received on the serial port to the JS console'''
        receivedValues = []
        while (True):
            response = await self.reader.read()
            value, done = response.value, response.done
            if ('\r' in value or '\n' in value):
                # Output whole line and clear buffer when a newline is received
                print(f"Received from Serial: {''.join(receivedValues)}")
                receivedValues = []
            elif (value):
                # Output individual characters as they come in
                print(f"Received Char: {value}")
                receivedValues.append(value)

    async def ReadChar(self):
        response = await self.reader.read()
        self.reply, done = response.value, response.done
        js.console.log('Read from stream: ' + self.reply)
        print(self.reply, end='')
        sys.stdout.flush()
        if done:
            self.reader.releaseLock()
            js.console.log("done")

    async def writeToSerial(self, data):
        outputWriter = self.encoder.writable.getWriter()
        outputWriter.write(data + '\r\n')
        outputWriter.releaseLock()
        js.console.log("Wrote to stream: " + data + '\r\n')

    async def ReadResponse(self):
        self.response = ''
        while not ('>>>' in self.response):
            left, reply = await self.ReadLine()
            self.response += reply + left
        return self.response

    async def ReadLine(self, reply=''):
        while not '\n' in reply:
            response = await self.reader.read()
            value, done = response.value, response.done
            js.console.log('Read from stream: ' + value)
            reply += value
            left = ''
            if done:
                self.reader.releaseLock()
                js.console.log("done")
        return left, reply


class serialPort():
    def __init__(self, baud=115200):
        self.sm = SerialManager()

    def ask(self):
        loop = asyncio.get_running_loop()
        loop.run_until_complete(self.sm.askForSerial())

    def write(self, text):
        loop = asyncio.get_running_loop()
        loop.run_until_complete(self.sm.Write(text))

    def read(self):
        loop = asyncio.get_running_loop()
        loop.run_until_complete(self.sm.ReadChar())
        return self.sm.response

    def readline(self):
        loop = asyncio.get_running_loop()
        reply = ''
        while not ('\n' in reply):
            loop.run_until_complete(self.sm.ReadChar())
            reply += self.sm.reply
        return self.sm.reply

    def CtrlC(self):
        print('ctrlC')
        value = '\x03\r\n'
        self.write(value)
        print(self.read())

    def test(self):
        print('testing')
        value = 'help("modules")\r\n'
        self.write(value)
        print(self.readline())


async def sendValueFromInputBox(sm: SerialManager):
    textInput = js.document.getElementById("text")
    value = textInput.value
    textInput.value = ''
    await sm.writeToSerial(value)
    print(await sm.ReadResponse())


async def readPort(sm: SerialManager):
    print(await sm.ReadResponse())


async def uploadCode(sm: SerialManager):
    code = js.document.getElementById("pythonCode")
    value = code.value
    value = value.replace('\n', '\r\n')
    await sm.writeToSerial('\x05' + value + '\x04')
    reply = ''
    left = ''
    while not '>>>' in reply:
        left, reply = await sm.ReadLine(left)
        print(reply)
