from ..command_factory import Command

from telebot import telebot  # type: ignore


class EditCommand(Command):
    def validate(self, *args: str) -> bool:
        if len(args) < 4:
            return False

        return args[1].capitalize() in ["Junta", "Asamblea"]

    def execute(
        self, 
        bot: telebot.TeleBot, 
        message: telebot.types.Message, 
        *args: str
    ) -> None:
        """
            Edit a item, editing or adding a description
        Args:
            bot (Telebot): GuiBot
            message (telebot.types.Message): message with command information
        """
        if not self.validate(*args):
            bot.reply_to(
                message,
                "Error en comando: tipo_reunion \nEjecute /help edit",
                message_thread_id=message.message_thread_id,
            )
            return

        meeting_type: str = args[1].capitalize()
        new_description: str = f"{' '.join(args[3:])}\n"
        try:
            item_num: int = int(args[2]) - 1
            try:
                with open(
                    f"src/meeting_files/items_{meeting_type}.txt", "r"
                ) as items_read:
                    items = items_read.readlines()

                if item_num not in range(len(items)):
                    bot.reply_to(
                        message,
                        "Error en comando: punto_del_día \nEjecute /help edit",
                        message_thread_id=message.message_thread_id,
                    )
                    return

                new_item = f"{items[item_num].split(': ')[0]}: {new_description}"
                items[item_num] = new_item
                with open(
                    f"src/meeting_files/items_{meeting_type}.txt", "w"
                ) as items_write:
                    items_write.writelines(items)

            except FileNotFoundError:
                bot.reply_to(
                    message,
                    "No existe ningún archivo de puntos del día, puede crearlo con /new",
                    message_thread_id=message.message_thread_id,
                )
        except ValueError:
            bot.reply_to(
                message,
                "Error en comando: punto_del_día \nEjecute /help edit",
                message_thread_id=message.message_thread_id,
            )
