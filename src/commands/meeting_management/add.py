from ..command_factory import Command

from telebot import telebot  # type: ignore

class AddCommand(Command):
    def validate(self, *args: str) -> bool:
        if len(args) < 3:
            return False

        return args[1].capitalize() in ["Junta", "Asamblea"]

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
                "Error en comando: tipo_reunion \nEjecute /help add",
                message_thread_id=message.message_thread_id,
            )
            return

        meeting_type: str = args[1].capitalize()
        new_item: str = " ".join(args[2:])
        try:
            with open(f"src/meeting_files/items_{meeting_type}.txt", "r") as items_read:
                if any(new_item in line.split(":")[0] for line in items_read):
                    bot.reply_to(
                        message,
                        "Punto del día añadido anteriormente",
                        message_thread_id=message.message_thread_id,
                    )
                    return

            with open(
                f"src/meeting_files/items_{meeting_type}.txt", "a"
            ) as items_write:
                items_write.write(f"{new_item}: \n")
        except FileNotFoundError:
            bot.reply_to(
                message,
                "No existe ningún archivo de puntos del día, puede crearlo con /new",
                message_thread_id=message.message_thread_id,
            )
