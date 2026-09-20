# Dictionary Lookup and the Dispatcher Pattern

## The problem

The shell has to turn the text a user typed (`"echo hello"`) into the right piece of code to run. The obvious approach is a chain of `if` / `elif` checks:

```python
if command == "echo":
    ...
elif command == "type":
    ...
elif command == "exit":
    ...
```

That works, but every new command means editing that chain, and it gets messy as the shell grows.

## My idea: a dictionary of valid commands

I had the idea of using a dictionary that maps each command name to the method that handles it:

```python
self.__valid_commands = {
    "echo": self.handle_echo,
    "type": self.handle_type,
    "exit": self.handle_exit,
}
```

Looking up a command is then a single `.get()` call, and the result doubles as the validity check: if the lookup returns a handler the command exists, and if it returns `None` the shell prints `command not found`.

## The design pattern behind it

I later realized this is a **strategy / dispatcher** style design. Each command is its own interchangeable behaviour, and the dictionary picks which one to run at runtime based on the input. The main loop doesn't need to know what any command does. It asks for a handler and calls it:

```python
handler = terminal_commands.get_handler(command)
if handler:
    handler(arguments)
else:
    print(f"{command}: command not found")
```

## What I got out of it

- **Functions are values in Python.** Storing bound methods in a dictionary and calling them later felt natural in Python. In C++ I would have needed function pointers or `std::function`.
- **Adding a command is a one-line change.** Write a `handle_*` method and add it to the dictionary. The main loop stays the same.
- **The lookup is easy to reuse.** `type` uses the same `get_handler` lookup to decide whether something is a builtin, so there's a single source of truth for what counts as a valid command.
- **The commands can be injected.** The constructor accepts an optional dictionary, which makes it possible to swap in a different set of commands, for example in tests.
