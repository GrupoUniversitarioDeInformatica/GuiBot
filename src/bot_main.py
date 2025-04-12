"""
GuiBot - Telegram bot to manage the meeting documents of Universidad
de Valladolid's Grupo Universitario de Informática (GUI).
Copyright (C) 2024  Obi-Juan-NoSeEnoje17

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import time
import os
from typing import Callable
from datetime import datetime

import telebot  # type: ignore
from dotenv import load_dotenv

from commands.command_factory import CommandFactory, Command
from utils import log_writer

load_dotenv()
TOKEN = os.getenv("TOKEN")
BOARD_WHILELIST_FILE = os.getenv("BOARD_WHITELIST")
SENIOR_MEMBER_WHITELIST_FILE = os.getenv("SENIOR_MEMBER_WHITELIST")
FILES_DIR = os.getenv("FILES_DIR")
LOGS_DIR1 = os.getenv("LOGS_DIR")

if (
    not TOKEN
    or not BOARD_WHILELIST_FILE
    or not SENIOR_MEMBER_WHITELIST_FILE
    or not FILES_DIR
    or not LOGS_DIR1
):
    raise EnvironmentError("Missing critical environment variables. Check .env file.")

try:
    with open(BOARD_WHILELIST_FILE, "r") as f:
        BOARD_WHITELIST = set(line.strip() for line in f)
    with open(SENIOR_MEMBER_WHITELIST_FILE, "r") as f:
        SENIOR_MEMBER_WHITELIST = set(line.strip() for line in f)

except FileNotFoundError:
    raise FileNotFoundError(
        f"Whitelist file not found: {BOARD_WHILELIST_FILE} and {SENIOR_MEMBER_WHITELIST_FILE}\n"
    )

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=["start"])
def start_handler(message: telebot.types.Message) -> None:
    bot.send_message(
        message.chat.id,
        "Hello, this is GuiBot.\n Telegram bot to manage the meeting documents of Universidad \
        de Valladolid's Grupo Universitario de Informática (GUI). If u want to know the source code or our license execute /source or /license",
        message_thread_id=message.message_thread_id
    )

@bot.message_handler(commands=["source"])
def source_handler(message: telebot.types.Message) -> None:
    bot.send_message(
        message.chat.id,
        "My source code is on https://github.com/GrupoUniversitarioDeInformatica/GuiBot.git",
        message_thread_id=message.message_thread_id
    )

@bot.message_handler(commands=["license"])
def license_handler(message: telebot.types.Message) -> None: 
    bot.send_message(
        message.chat.id,
        r"""
            GuiBot - Telegram bot to manage the meeting documents of Universidad
            de Valladolid's Grupo Universitario de Informática (GUI).
            Copyright (C) 2024  Obi-Juan-NoSeEnoje17\n\n
            This program is free software: you can redistribute it and/or modify
            it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or
            (at your option) any later version.\n\n
            This program is distributed in the hope that it will be useful,
            but WITHOUT ANY WARRANTY; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
            GNU Affero General Public License for more details.\n\n
            You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
        """,
        message_thread_id=message.message_thread_id
    )


def board_check(command: Callable) -> Callable:
    """
    Decorator that checks whether the user executing the command is part of the authorized board.

    Args:
        command (Callable): The function that handles the command execution.

    Returns:
        Callable: A wrapped function that only runs if the user is in the BOARD_WHITELIST.
    """
    def wrapper(message: telebot.types.Message) -> None:
        username: str = message.from_user.username
        if username in BOARD_WHITELIST:
            command(message)
        else:
            bot.reply_to(
                message, 
                "Lo siento, pero no puedes ejecutar este comando",
                message_thread_id=message.message_thread_id
            )

    return wrapper


def sennior_member_check(command: Callable) -> Callable:
    """
    Decorator that checks whether the user executing the command is part of the sennior members.

    Args:
        command (Callable): The function that handles the command execution.

    Returns:
        Callable: A wrapped function that only runs if the user is in the SENNIOR_WHITELIST.
    """
    def wrapper(message: telebot.types.Message) -> None:
        username: str = message.from_user.username
        if username in SENIOR_MEMBER_WHITELIST:
            command(message)
        else:
            bot.reply_to(
                message,
                "Lo siento, pero no puedes ejecutar este comando",
                message_thread_id=message.message_thread_id
            )

    return wrapper
    

@bot.message_handler(commands=["help", "incoming", "changeLogs"])
def handle_info_commands(message: telebot.types.Message) -> None:
    """
        Bot info commands handleer
    Args:
        message (telebot.types.message): Command Message
    """
    command_args: list[str] = message.text.replace("/", "").split(" ")
    command: Command | None = CommandFactory.get_command(command_args[0])

    if command:
        command.execute(bot, message, *command_args)
        log_writer.write_usage(
            f"{message.from_user.username}->/{' '.join(command_args)}"
        )
    else:
        bot.reply_to(
            message,
            "Comando no reconocido. \nEjecute /help para listar los comandos disponibles",
            message_thread_id=message.message_thread_id,
        )


@bot.message_handler(commands=["list"])
@sennior_member_check
def handle_meeting_info_commands(message: telebot.types.Message) -> None:
    """
        Meeting info commands handleer
    Args:
        message (telebot.types.Message): Command Message
    """
    command_args: list[str] = message.text.replace("/", "").split(" ")
    command: Command | None = CommandFactory.get_command(command_args[0])

    if command:
        command.execute(bot, message, *command_args)
        log_writer.write_usage(
            f"{message.from_user.username}->/{' '.join(command_args)}"
        )
    else:
        bot.reply_to(
            message,
            "Comando no reconocido. \nEjecute /help para listar los comandos disponibles",
            message_thread_id=message.message_thread_id,
        )


@bot.message_handler(commands=["new", "add", "edit", "rm", "change", "roadmap"])
@board_check
def handle_meeting_management_commands(message: telebot.types.Message) -> None:
    """
        Meeting management commands handler
    Args:
        message (telebot.types.Message): Command Message
    """
    command_args: list[str] = message.text.replace("/", "").split(" ")
    command: Command | None = CommandFactory.get_command(command_args[0])

    if command:
        command.execute(bot, message, *command_args)
        log_writer.write_usage(
            f"{message.from_user.username}->/{' '.join(command_args)}"
        )
    else:
        bot.reply_to(
            message,
            "Comando no reconocido. \nEjecute /help para listar los comandos disponibles",
            message_thread_id=message.message_thread_id,
        )


# Comandos brooma del presi
@bot.message_handler(commands=["gj"])
def good_awfull_job(message: telebot.types.Message) -> None:
    """
        Send recognition to a member
    Args:
        message (telebot.types.Message): Command Message
    """
    if message.from_user.username == "NoSeEnoje17":
        bot.send_message(
            message.chat.id,
            f"Muy bien {message.text.split()[1]}. Estás haciendo un buen trabajo, sigue así",
            message_thread_id=message.message_thread_id,
        )
        
        
@bot.message_handler(commands=["notasFoe"]) 
def handle_command(message:telebot.types.Message) -> None:
    """
    Notas Foe
    Args:
        message (telebot.types.Message): notasFoe
    """
    bot.send_message(
        message.chat.id,
        f"Bro, estamos a {datetime.now().year}",
        message_thread_id = message.message_thread_id
    )
    time.sleep(3)
    bot.send_message(
        message.chat.id,
        "/notasFoe\njeje",
        message_thread_id = message.message_thread_id
    )

def run_bot() -> None:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        log_writer.write_error("Bot detenido por el usuario (Ctrl+C)\n")
        bot.stop_polling()
    except Exception as e:
        log_writer.write_error(f" Error: {e}. Reintentando en 5 segundos...\n")
        time.sleep(5)
        run_bot()


if __name__ == "__main__":
    run_bot()
