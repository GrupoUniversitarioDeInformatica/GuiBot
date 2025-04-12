from ..command_factory import Command

from telebot import telebot  # type: ignore

class RmCommand(Command):
    def validate(self, *args: str) -> bool:
        if len(args) != 3:
            return False
        return args[1].capitalize() in ["Junta", "Asamblea"]

    def execute(
        self, 
        bot: telebot.TeleBot, 
        message: telebot.types.Message, 
        *args: str
    ) -> None:
        """
            Remove a item of the meeting file
        Args:
            bot (Telebot): GuiBot
            message (Message): message with command information
        """
        if not self.validate(*args):
            bot.reply_to(
                message,
                "Error en comando: formato \nEjecute /help remove",
                message_thread_id=message.message_thread_id,
            )
            return

        meeting_type: str = args[1].capitalize()
        try:
            item_to_remove: int = int(args[2]) - 1
            try:
                with open(
                    f"src/meeting_files/items_{meeting_type}.txt", "r"
                ) as items_read:
                    items = items_read.readlines()
                    if item_to_remove not in range(len(items)):
                        bot.reply_to(
                            message,
                            "Error en comando: punto_del_día \nEjecute /help rm",
                            message_thread_id=message.message_thread_id,
                        )
                        return
                    actual_items = [
                        item
                        for line_number, item in enumerate(items)
                        if line_number != item_to_remove
                    ]

                with open(
                    f"src/meeting_files/items_{meeting_type}.txt", "w"
                ) as items_write:
                    items_write.writelines(actual_items)

            except IOError:
                bot.reply_to(
                    message,
                    "No existe ningúnrchivo de puntos del día",
                    message_thread_id=message.message_thread_id,
                )
        except ValueError:
            bot.reply_to(
                message,
                "Error en comando: punto_del_dia \nEjecute /help remove",
                message_thread_id=message.message_thread_id,
            )
