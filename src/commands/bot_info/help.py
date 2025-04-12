from ..command_factory import Command, COMMANDS_INFO

from telebot import telebot  # type: ignore


class HelpCommand(Command):
    def validate(self, *args: str) -> bool:
        return len(args) <= 2

    def execute(
        self, 
        bot: telebot.TeleBot, 
        message: telebot.types.Message, 
        *args: str
    ) -> None:
        if not self.validate(*args):
            bot.reply_to(
                message,
                "Error en formato.\nEjecute /help help",
                message_thread_id=message.message_thread_id,
            )
            return

        if len(args) == 1:
            commands_info: str = "Comandos existentes: \nEjecute /help comando para más\n"
            for command in COMMANDS_INFO.keys():
                commands_info += f" -{command}\n"
            bot.send_message(
                message.chat.id,
                commands_info,
                message_thread_id=message.message_thread_id,
            )

        bot.send_message(
            message.chat.id,
            COMMANDS_INFO.get(args[1], "Comando desconocido"),
            message_thread_id=message.message_thread_id,
        )
