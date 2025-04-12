from ..command_factory import Command
from .roadmap_utils import (
    check_date,
    create_latex_content,
    format_date_date,
    format_date_title,
)  # type: ignore

from telebot import telebot  # type: ignore

class RoadMapCommand(Command):
    def validate(self, *args: str) -> bool:
        if len(args) != 3:
            return False

        return args[1].capitalize() in ["Junta", "Asamblea"] and check_date(args[2])

    def execute(
        self, 
        bot: telebot.TeleBot, 
        message: telebot.types.Message, 
        *args: str
    ) -> None:
        """
            Add a point of day to the current meeting file
        Args:
            bot (Telebot): GuiBot
            message (telebot.types.Message): message with command information
        """
        if not self.validate(*args):
            bot.reply_to(
                message,
                "Error en comando: fecha\nEjecute /help roadmap",
                message_thread_id=message.message_thread_id,
            )
        else:
            meeting_type: str = args[1].capitalize()
            date: str = args[2]
            try:
                latex_content: str = create_latex_content(
                    meeting_type, format_date_date(date)
                )
                roadmap_name: str = f"../../../tex_files/{format_date_title(date)}.tex"
                with open(roadmap_name, "w") as new_roadmap:
                    new_roadmap.write(latex_content)

                with open(roadmap_name, "rb") as send_roadmap:
                    bot.send_document(
                        message.chat.id,
                        send_roadmap,
                        message_thread_id=message.message_thread_id,
                    )
                    bot.send_message(
                        message.chat.id,
                        "Para eliminar el arhicvo con los puntos del día puede ejecutar /delete o /new",
                        message_thread_id=message.message_thread_id,
                    )
            except Exception as e:
                bot.reply_to(
                    message,
                    "Error al crear el PDF\n" + str(e),
                    message_thread_id=message.message_thread_id,
                )
