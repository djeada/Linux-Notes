<h2>history</h2>

* To see the n most recently used commands, use the <i>history</i> command.
You can change the n number (which are generally between 1000 and 5000).
* <i>Ctrl+R</i> looks for command alone, and pressing <i>Ctrl+R</i> again searches for next.
* <i>!number</i> executes the command with the given number, while <i>!text</i> executes the command which starts with the given text.

To clear the history, execute the following commands:

```bash
history -c
```

To delete the contents of.bash history, run the following command:

```bash
history -w
```

<h2>man</h2>

The <i>man</i> command is an abbreviation for manual. 
The <i>man</i> command displays the documentation for every command we execute on the terminal.

| Number | Description |
| --- | --- |
| <i>1</i> | executable programs or shell commands |
| <i>5</i> | file formats and conventions |
| <i>8</i> | system administration commands |

Use man -f command name to display a short description of a command, for example:

```bash
man git
```

<h2>apropos</h2>
When a user does not recall the specific command but knows a few keywords linked to the command that characterize its uses or capabilities, <i>apropos</i> command can help them find it.

```bash
apropos zip
```
