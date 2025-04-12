from ..command_factory import Command

from telebot import telebot  # type: ignore

class IncomingCommand(Command):
    def validate(self, *args: str) -> bool:
        return len(args) == 1

    def execute(
        self, 
        bot: telebot.TeleBot, 
        message: telebot.types.Message, 
        *args: str
    ) -> None:
        if not self.validate(*args):
            bot.reply_to(
                message,
                "Error en formato.\nEjecute /help incoming",
                message_thread_id=message.message_thread_id,
            )
            return

        incoming: str = "Mejoras futuras:\n"
        with open("src/commands/bot_info/incoming.txt", "r") as f:
            for improvement in f.readlines():
                incoming += f" -{improvement}"
        bot.send_message(
            message.chat.id, incoming, message_thread_id=message.message_thread_id
        )
