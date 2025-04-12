from ..command_factory import Command

from telebot import telebot  # type: ignore

class NewCommand(Command):
    def validate(self, *args: str) -> bool:
        if len(args) != 3:
            return False
        return (
            args[1].capitalize() in ("Junta", "Asamblea") and args[2] == "confirmacion"
        )

    def execute(
        self, 
        bot: telebot.TeleBot, 
        message: telebot.types.Message, 
        *args: str
    ) -> None:
        """
            Creates new file to save points of day
        Args:
            bot (Telebot): GuiBot
            message (telebot.types.Message): message with command information
        """
        if not self.validate(*args):
            bot.reply_to(
                message,
                "Error en comando: tipo_reunion \nEjecute /help new",
                message_thread_id=message.message_thread_id,
            )
            return

        meeting_type: str = args[1].capitalize()
        try:
            with open(
                f"src/meeting_files/items_{meeting_type}.txt", "w"
            ) as items_write:
                items_write.write("")
            bot.send_message(
                message.chat.id,
                "Archivo creado con éxito\n",
                message_thread_id=message.message_thread_id,
            )
        except Exception as e:
            bot.reply_to(
                message,
                f"Error al crear el archivo nuevo {str(e)}",
                message_thread_id=message.message_thread_id,
            )
