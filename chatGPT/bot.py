from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage
from dotenv import load_dotenv
import asyncio
import os
import data.config as config
import data.commandList as commandList
import functions.cleanUp as cleanUp
import functions.gpt as gpt

load_dotenv(dotenv_path=os.path.join('secrets', '.env'))

class BOT:
    def __init__(self, app_id, app_secret, user_scope, target_channel, bot_name):
        self.app_id = app_id
        self.app_secret = app_secret
        self.user_scope = user_scope
        self.target_channel = target_channel
        self.bot = bot_name
        self.twitch = None
        self.chat = None


    async def on_ready(self, ready_event: EventData):
        print(f'{config.botname[1:4]}GPT has joined')
        await ready_event.chat.join_room(self.target_channel)


    async def on_message(self, msg: ChatMessage):
        print(f'{msg.user.name} said: {msg.text}')
        message = msg.text.lower().split()
        if msg.text[0] == '!' and message[0] not in commandList.commands:
            print('found a command to make up!', message[0])
            prompt = msg.text
            try:
                completion = gpt.create_prompt(prompt, command=True)
                response = completion.choices[0].message.content
                print(response)
                response_parts = cleanUp.split_response(response)
                for part in response_parts:
                    await self.chat.send_message(self.target_channel, part)
                    await asyncio.sleep(2)
            except Exception as e:
                print('An error occurred: ', e)
        elif self.bot in message:
            print('responding to a convo with, ', {msg.user.name})
            prompt = msg.text.replace(self.bot, '').strip()
            try:
                completion = gpt.create_prompt(prompt)
                response = completion.choices[0].message.content
                print(response)
                response_parts = cleanUp.split_response(response)
                for part in response_parts:
                    await self.chat.send_message(self.target_channel, part)
                    await asyncio.sleep(2)
            except Exception as e:
                print('An error occurred: ', e)


    async def run(self):
        self.twitch = await Twitch(self.app_id, self.app_secret)
        auth = UserAuthenticator(self.twitch, self.user_scope)
        token, refresh_token = await auth.authenticate()
        await self.twitch.set_user_authentication(token, self.user_scope, refresh_token)
        self.chat = await Chat(self.twitch)
        self.chat.register_event(ChatEvent.READY, self.on_ready)
        self.chat.register_event(ChatEvent.MESSAGE, self.on_message)
        self.chat.start()
        try:
            input('press ENTER to stop\n')
        finally:
            self.chat.stop()
            await self.twitch.close()


if __name__ == '__main__':
    APP_ID = os.environ['APP_ID']
    APP_SECRET = os.environ['APP_SECRET']
    USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
    TARGET_CHANNEL = config.targetchannel
    BOT_NAME = config.botname

    gptexe = BOT(APP_ID, APP_SECRET, USER_SCOPE, TARGET_CHANNEL, BOT_NAME)
    asyncio.run(gptexe.run())