from ..command_factory import Command

from telebot import telebot  # type: ignore

class ListCommand(Command):
    def validate(self, *args: str) -> bool:
        if len(args) != 2 and len(args) != 3:
            return False
        if args[1].capitalize() not in ("Junta", "Asamblea"):
            return False
        return True

    def execute(
        self, 
        bot: telebot.TeleBot, 
        message: telebot.types.Message, 
        *args: str
    ) -> None:
        """
            List all te current points of day of the meeting, or list the description of a determine item
        Args:
            bot (Telebot): GuiBot
            message (Message): message with command information
        """
        if not self.validate(*args):
            bot.reply_to(
                message,
                "Error en comando: formato \nEjecute /help list",
                message_thread_id=message.message_thread_id,
            )
            return

        meeting_type: str = args[1].capitalize()
        if len(args) == 2:
            items_list: str = f"Puntos del día de la próxima {meeting_type}:\n"
            try:
                with open(
                    f"src/meeting_files/items_{meeting_type}.txt", "r"
                ) as items_read:
                    for number, item in enumerate(items_read, start=1):
                        items_list = f"{items_list} {str(number)}. {item.split(":")[0]}\n"
                bot.send_message(
                    message.chat.id,
                    items_list,
                    message_thread_id=message.message_thread_id,
                )
                return
            except FileNotFoundError:
                bot.reply_to(
                    message,
                    "No existe ningún archivo de puntos del día, puede crearlo con /new",
                    message_thread_id=message.message_thread_id,
                )
                return

        try:
            command_number: int = int(args[2])
            try:
                items_desc: str = "Descripción de "
                with open(
                    f"src/meeting_files/items_{meeting_type}.txt", "r"
                ) as items_read:
                    for line_number, item in enumerate(items_read, start=1):
                        if line_number == command_number:
                            bot.send_message(
                                message.chat.id,
                                f"{items_desc}{item.split(': ')[0]} \n{item.split(': ')[1]}",
                                message_thread_id=message.message_thread_id,
                            )
                            return
            except FileNotFoundError:
                bot.reply_to(
                    message,
                    "No existe ningún archivo de puntos del día, puede crearlo con /new",
                    message_thread_id=message.message_thread_id,
                )
        except ValueError:
            bot.reply_to(
                message,
                "Error en comando: punto_del_día \nEjecute /help list",
                message_thread_id=message.message_thread_id,
            )
