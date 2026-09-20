import sys
from typing import Callable

class Terminal_Commands:
    def __init__(self, valid_commands: dict[str, Callable] | None = None) -> None:
        if valid_commands is None:
            self.__valid_commands: dict[str, Callable] = {
                "echo": self.handle_echo, 
                "type": self.handle_type, 
                "exit": self.handle_exit
            }
        else:
            self.__valid_commands = valid_commands

    def handle_echo(self, user_input: list[str]) -> None:
        result = " ".join(user_input)
        print(result)

    def handle_type(self, user_input: list[str]) -> None:
        for input in user_input:
            if self.get_handler(input):
                print(f"{input} is a shell builtin")
            elif len(input) == 0:
                # user did type __ just empty
                return
            else:
                print(f"{input}: not found")

    @staticmethod
    def handle_exit(_) -> None:
        sys.exit()

    def get_handler(self, command: str) -> None | Callable:
        return self.__valid_commands.get(command.lower())
    

def handle_user_input(user_input: str, terminal_commands: Terminal_Commands) -> None:
    if user_input == "":
        print(end="\r")

    elif user_input:
        user_input_as_list = user_input.split()
        command_to_execute = user_input_as_list[0]
        remaining_user_text = user_input_as_list[1:]

        is_valid_command = terminal_commands.get_handler(command_to_execute) # lower case the command for easier lookup

        if is_valid_command:
            execute = is_valid_command
            execute(remaining_user_text)
        else:
            print(f"{command_to_execute}: command not found")
        

def main():
    terminal_commands = Terminal_Commands()
    while True:
        try:
            sys.stdout.write("$ ") 
            sys.stdout.flush() # flush is needed because python buffers meaning, it waits for sys input before executing the code
            user_input = sys.stdin.readline()
            
            handle_user_input(user_input.strip(), terminal_commands) # strip because if not, there is a new line that is added with user input (always), so we want to rmv that so text appears on same line
        except KeyboardInterrupt:
            sys.exit(0)



if __name__ == "__main__":
    main()
