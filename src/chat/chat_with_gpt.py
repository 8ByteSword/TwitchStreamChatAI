import openai

class ChatWithGPT:
    def __init__(self, credentials):
        self.api_key = credentials['api_key']
        openai.api_key = self.api_key
        self.prefix = '!'

    def chat(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = response.choices[0].text.strip()
        return message

    def is_command(self, message):
        return message.content.startswith(self.prefix)

    async def handle_command(self, twitch_chat, message):
        command = message.content[1:]  # Quita el prefijo '!' del mensaje
        prompt = f"Responde al comando: {command}"
        response = self.chat(prompt)

        await twitch_chat.send_message(response)

