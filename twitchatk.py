#credit to broken symmetry for like everything and emily for atk itself

import os, subprocess
from threading import Thread
from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatCommand
import asyncio

APP_ID = 'hv1j8m1pczb7law12cniet9tnmfvpg'
APP_SECRET = ''
USER_SCOPE = [AuthScope.CHAT_READ]
TARGET_CHANNEL = 'pizzart'
with open('token.txt', 'r') as f:
    APP_SECRET = f.read()

class ATK:
    def kill(self):
        self.process.kill()
    
    def __init__(self, game_path:str, atk_path:str=None):
        self.atk_path = atk_path or "{cwd}{sep}atk.js".format(sep=os.sep, cwd=os.getcwd() )
        self.game_path = game_path.split(os.sep)[-1:][0]

    def _launch(self):
        self.run_subprocess()

        self.thread = Thread(args = (self.process, ))
        self.thread.daemon = True
        self.thread.start()

    def write_stdin(self, msg:str):
        if msg[-1:] != "\n":
            msg += "\n"

        try:
            self.process.stdin.write(msg.encode())
            self.process.stdin.flush()
        except(KeyboardInterrupt, SystemExit):
            self.process.stdin.write("quit".encode())
            self.process.stdin.flush()

    def run_subprocess(self):
        MyLaunchString = 'frida -n \"{game_path}\" -l \"{atk_path}\" -- -W'.format(
        game_path=self.game_path,
        atk_path=self.atk_path
        )

        self.process = subprocess.Popen(
        MyLaunchString,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        # ^^^ COMMENT THIS LINE IF SOMETHING GOES WRONG
        stderr=subprocess.STDOUT
        )

class Process:
    def __init__(self) -> None:
        self.launchATK()

    def _kill_atk_process(self):
        try:
            self.subprocess.kill()
        except:
            pass
            
    def launchATK(self):
        self._kill_atk_process()
        self.subprocess = ATK('WALL-E.exe') # doesn't necessarily need to be wall-e
        self.subprocess._launch()
    
    def atk_enter_command(self, command):
        try:
            self.subprocess.write_stdin(command)
        except:
            pass

atk_process = Process()

async def on_ready(ready_event: EventData):
    await ready_event.chat.join_room(TARGET_CHANNEL)

async def run_atk_cmd(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        print('lol 0 length command')
    else:
        atk_process.atk_enter_command(f'runCommand("{cmd.parameter}")')


async def run():
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    chat = await Chat(twitch)


    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_command('atk', run_atk_cmd)

    chat.start()

    try:
        input('press ENTER to stop\n')
    finally:
        chat.stop()
        atk_process._kill_atk_process()
        await twitch.close()

asyncio.run(run())