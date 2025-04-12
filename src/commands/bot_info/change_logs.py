from ..command_factory import Command

from telebot import telebot  # type: ignore


class ChangeLogsCommand(Command):
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
                "Error en formato.\nEjecute /help changeLogs",
                message_thread_id=message.message_thread_id,
            )
            return

        change_logs: str = "Mejoras introfucidas:\n"
        with open("src/commands/bot_info/change_logs.txt", "r") as f:
            for change in f.readlines():
                change_logs += f" -{change}"
        bot.send_message(
            message.chat.id, change_logs, message_thread_id=message.message_thread_id
        )
