<h1>History</h1>

* To see the n most recently used commands, use the <code>history</code> command.
You can change the n number (which are generally between 1000 and 5000).
* <code>Ctrl+R</code> looks for command alone, and pressing <code>Ctrl+R</code> again searches for next.
* <code>!number</code> executes the command with the given number, while <code>!text</code> executes the command which starts with the given text.

To clear the history, execute the following commands:

```bash
history -c
```

To delete the contents of bash history, run the following command:

```bash
history -w
```

<h1>Navigating commands in the terminal</h1>

* Uppwards arrow key: show the previous command from the history.
* Downwards arrow key: show the next command from the history.
* <code>tab</code> key: complete the command.

<h1>The manual</h1>

The <code>man</code> command is an abbreviation for manual. 
The <code>man</code> command displays the documentation for every command we execute on the terminal.

| Number | Description |
| --- | --- |
| <code><b>1</b></code> | executable programs or shell commands |
| <code>2</code> | system calls |
| <code>3</code> | library calls |
| <code>4</code> | special files |
| <code><b>5</b></code> | file formats and conventions |
| <code>6</code> | games |
| <code>7</code> | misc |
| <code><b>8</b></code> | system administration (root) commands |
| <code>9</code> | kernel routines |

Use 'man -f command_name' to display a short description of a command, for example:

```bash
man git
```

<h1>Apropos</h1>

When a user does not recall the specific command but knows a few keywords linked to the command that characterize its uses or capabilities, <code>apropos</code> command can help them to find the command they are looking for.

```bash
apropos zip
```

<h1>Challenges</h1>

1. How to find the command that is used to create a file?
2. Use the <code>man</code> command to display what does the command <code>cat</code> do.
3. Change the maximum number of commands to remember in the command history to 3000.
