# GuiBot

**GuiBot** is a Telegram bot used by the *Grupo Universitario de Informática* of Valladolid to manage meeting documents.

This bot helps the team to organize and handle various documents efficiently, providing a set of commands to interact with the system and retrieve necessary files.

---

## Getting Started

To run the bot, follow these simple steps:

1. **Clone the repository:**
    ```bash
    git clone https://your-repository-url.git
    ```

2. **Set up the environment:**
    Run the `setup.sh` script to prepare the environment with all necessary dependencies:
    ```bash
    bash setup.sh
    ```

3. **Run the bot:**
    The main program is located in `/src/bot_main.py`. To start the bot, simply execute:
    ```bash
    python src/bot_main.py
    ```

---

## License

GuiBot is released under the **AGPL License**. See the [LICENSE](LICENSE) file for more details.

---

## Adding a New Command

If you'd like to add a new command to the bot, follow these steps:

1. **Create a new command class** that inherits from the `Command` class.
    - Implement the `execute()` method to handle the command's logic.
    - Optionally, implement a `validate()` method to validate input arguments.
    - Make sure its in the rigth category, or make a new one
    - Imports it to command_factory.py before COMMANDS dict

2. **Add the new command to the `COMMANDS` dictionary** in the `CommandFactory`.
    ```python
    COMMANDS: Dict[str, Command] = {
        "new_command": NewCommand(),  # Add your new command here
    }
    ```

3. **Add command handler**
    - Add the command to an existing message handler or a new one
    - If new one, creates its function to call the command_factory
    - Optionally, supply info with a send_message or monitor the command execution with log writer

4. **Test your command** to make sure everything works correctly.

---

## Additional Information

- For more details about how the bot works or to contribute, please check the source code in `/src`.
- Feel free to open an issue or submit a pull request if you find any bugs or have suggestions for improvements!

Made by 
 - @NoSeEnoje17 / Obi-Juan-NoSeEnoje17