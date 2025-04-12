from abc import ABC, abstractmethod
from typing import Dict

from telebot import telebot  # type: ignore

COMMANDS_INFO: Dict[str, str] = {
    "help": "/help [comando] \n"
    "Muestra ayuda general o de dicho comando. \n"
    "Argumentos: \n"
    " - comando: comando existente.",
    
    "incoming": "/incoming \nMuestra las mejoras venideras.",
    
    "changeLogs": "/changeLogs \nMuestra los cambios de la última actualización.",
    
    "new": "/new tipo_reunión \n"
    "Genera un nuevo documento para guardar los puntos del día. Puede haber un documento abierto por cada tipo. \n"
    "Argumentos: \n"
    " - tipo_reunión: 'Junta' o 'Asamblea'.",
    
    "add": "/add tipo_reunión punto_del_día\n"
    "Añade un punto del día con su descripción. \n"
    "Argumentos: \n"
    " - tipo_reunión: 'Junta' o 'Asamblea'. \n"
    " - punto_del_día: Título del punto del día a añadir. \n",
    
    "list": "/list tipo_reunión [punto_del_día] \n"
    "Muestra todos los puntos del día existentes o la descripción de un punto del día. \n"
    "Argumentos: \n"
    " - tipo_reunión: 'Junta' o 'Asamblea'. \n"
    " - punto_del_día: Número del punto del día a ver su descripción.",
    
    "change": "/cambio tipo_reunión punto_del_día_1 punto_del_día_2 [punto_del_día_3] \n"
    "Cambia el orden del punto del día 1 por el punto del día 2, si se indica un tercero, se coloca el primero entre los dos siguientes. \n"
    "Argumentos: \n"
    " - tipo_reunión: 'Junta' o 'Asamblea'. \n"
    " - punto_del_día_n: Número de un punto del día.",
    
    "edit": "/edit tipo_reunión punto_del_día descripción \n"
    "Añade o edita la descripción del punto del día \n"
    "Argumentos: \n"
    " - tipo_reunión: 'Junta' o 'Asamblea'. \n"
    " - punto_del_día: Número del punto del día a ver su descripción. \n"
    " - nueva_descripción: Descripción del punto del día.",
    
    "rm": "/rm tipo_reunión punto_del_día \n"
    "Elimina uno de los puntos del día \n"
    "Argumentos: \n"
    " - tipo_reunión: 'Junta' o 'Asamblea'. \n"
    " - punto_del_día: Número del punto del día a eliminar.",
    
    "roadmap": "/roadmap tipo_reunión fecha_reunión \n"
    "Genera el documento .tex de la reunión \n"
    "Argumentos: \n"
    " - tipo_reunión: 'Junta' o 'Asamblea'. \n"
    " - fecha_reunión: fecha de reunión en formato dd-mm-aaaa.",
}

class Command(ABC):
    @abstractmethod
    def validate(self, *args: str) -> bool:
        pass
    
    @abstractmethod
    def execute(
        self, 
        bot: telebot.TeleBot, 
        message: telebot.types.Message, 
        *args: str
    ) -> None:
        pass


from .bot_info import help, incoming, change_logs
from .meeting_info import list
from .meeting_management import new, add, rm, change, edit, roadmap


COMMANDS: Dict[str, Command] = {
    "help": help.HelpCommand(),
    "incoming": incoming.IncomingCommand(),
    "changeLogs": change_logs.ChangeLogsCommand(),
    "list": list.ListCommand(),
    "new": new.NewCommand(),
    "edit": edit.EditCommand(),
    "add": add.AddCommand(),
    "change": change.ChangeCommand(),
    "rm": rm.RmCommand(),
    "roadmap": roadmap.RoadMapCommand()
    }


class CommandFactory:
    """
    Factory class for retrieving command instances based on the command name.

    This class provides a method to fetch a command object given a command name
    as a string. The command object returned will be an instance of a subclass
    of the `Command` base class.

    Example:
        command = CommandFactory.get_command("help")
    """

    @staticmethod
    def get_command(command_name: str) -> Command | None:
        """
        Retrieve the command instance associated with the provided command name.

        Args:
            command_name (str): The name of the command to retrieve.

        Returns:
            Command | None: The corresponding command object if found, 
            or None if the command name is not recognized.
        
        Example:
            command = CommandFactory.get_command("help")
            # Returns an instance of HelpCommand or None if not found.
        """
        return COMMANDS.get(command_name, None)
