# Reading User Input in Python

A shell is a loop that prints a prompt, waits for a line of text, and acts on it. Getting that input step right was the first thing I had to figure out.

## What I used

```python
sys.stdout.write("$ ")
sys.stdout.flush()
user_input = sys.stdin.readline()
handle_user_input(user_input.strip(), terminal_commands)
```

## What I learned

- `sys.stdin` **and** `sys.stdout` **are streams.** I found it pretty cool that this is very similar to how C ++handles I/O.++ `sys.stdin.readline()` ++plays the role of++ `std::cin` ++/++ `std::getline`++, and++ `sys.stdout.write()` ++is close to++ `std::cout`++. Both languages treat the terminal as a stream you read from and write to, so the mental model carried over from C++.
- **Output is buffered, so the prompt needs a flush.** Python holds output in a buffer and doesn't always write it out right away. The `$`  prompt has no newline, so without `sys.stdout.flush()` it may not show up before the program blocks waiting for input. Flushing forces it to appear first. C++ has the same idea with `std::flush`.
- `readline()` **keeps the trailing newline.** The Enter key adds `\n` to whatever was typed, so I call `.strip()` to remove it before parsing. Otherwise `echo` would print an extra blank line and `exit\n` wouldn't match `exit`.
- **An empty line is different from end of input.** `readline()` returns `"\n"` when the user just presses Enter, which becomes `""` after stripping. It returns `""` (with no newline at all) only at end of input. I handle the empty command as a no-op.
- **Ctrl+C raises** `KeyboardInterrupt`**.** Wrapping the loop in `try/except KeyboardInterrupt` lets the shell exit cleanly.



## Why not `input()`?

`input("$ ")` would have been simpler, since it prints the prompt and strips the newline for me. I went with `sys.stdin` and `sys.stdout` directly because it made the mechanics visible: buffering, newlines, and the stream model. That was more useful for learning how a shell works.