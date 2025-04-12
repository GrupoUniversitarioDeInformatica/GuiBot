from ..command_factory import Command

from telebot import telebot  # type: ignore

class ChangeCommand(Command):
    def validate(self, *args: str) -> bool:
        if len(args) != 4:
            return False
        return args[1].capitalize() in ["Junta", "Asamblea"]

    def execute(
        self, 
        bot: telebot.TeleBot, 
        message: telebot.types.Message, 
        *args: str
    ) -> None:
        """
            Change the order of the points of day of the meeting file
        Args:
            bot (Telebot): GuiBot
            message (Message): message with command information
        """
        if not self.validate(*args):
            bot.reply_to(
                message,
                "Error en comando: formato \nEjecute /help change",
                message_thread_id=message.message_thread_id,
            )
            return

        try:
            meeting_type: str = args[1].capitalize()
            first_item: int = int(args[2]) - 1
            second_item: int = int(args[3]) - 1
            try:
                with open(
                    f"src/meeting_files/items_{meeting_type}.txt", "r"
                ) as items_read:
                    list_items = items_read.readlines()

                if first_item not in range(len(list_items)) or second_item not in range(
                    len(list_items)
                ):
                    bot.reply_to(
                        message,
                        "Error en comando: item \nEjecute /help change",
                        message_thread_id=message.message_thread_id,
                    )
                else:
                    list_items[first_item - 1], list_items[second_item - 1] = (
                        list_items[second_item - 1],
                        list_items[first_item - 1],
                    )
                    with open(
                        f"src/meeting_files/items_{meeting_type}.txt", "w"
                    ) as items_write:
                        items_write.writelines(list_items)

            except FileNotFoundError:
                bot.reply_to(
                    message,
                    "No existe ningún archivo de puntos del día, puede crearlo con /new",
                    message_thread_id=message.message_thread_id,
                )

        except ValueError:
            bot.reply_to(
                message,
                "Error en comando: punto_del_día \nEjecute /help change",
                message_thread_id=message.message_thread_id,
            )
