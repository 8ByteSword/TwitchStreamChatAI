from twitchio.ext import commands

class TwitchChat(commands.Bot):

    def __init__(self, twitch_credentials):
        super().__init__(
            irc_token=twitch_credentials['token'],
            client_id=twitch_credentials['client_id'],
            client_secret=twitch_credentials['client_secret'],
            nick='tu_nombre_de_usuario_twitch',
            prefix='!',
            initial_channels=['nombre_del_canal']
        )
        self.chat_history = []

    async def event_ready(self):
        print(f'{self.nick} está conectado a Twitch!')

    async def event_message(self, message):
        self.chat_history.append(message.content)
        await self.handle_commands(message)

    def get_chat_history(self):
        return ' '.join(self.chat_history)

    async def send_message(self, message):
        await self.get_channel('nombre_del_canal').send(message)
