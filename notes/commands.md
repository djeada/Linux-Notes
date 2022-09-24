## History

* To see the n most recently used commands, use the <code>history</code> command.
You can change the number n (it is generally between 1000 and 5000).
* Use <code>Ctrl+R</code> to search the history.
* <code>!number</code> executes the command with the given number, while <code>!text</code> executes the command which starts with the given text.
* Important: Lines which begin with a space character are not saved in the history list! So, if you copy and paste a command into the terminal and it doesn't appear in history, it most likely had a space as the first character. 

To clear the history, execute the following commands:

```bash
history -c
```

To delete the contents of bash history, run the following command:

```bash
history -w
```

## Navigating commands in the terminal

* Uppwards arrow key: show the previous command from the history.
* Downwards arrow key: show the next command from the history.
* <code>tab</code> key: complete the command.

## The manual

The <code>man</code> command is an abbreviation for manual. 
It may be used to display the documentation for various built-in command line utilities.

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

## Apropos

When a user does not recall the specific command but knows a few keywords linked to the command that characterize its uses or capabilities, <code>apropos</code> command can help them to find the command they are looking for.

```bash
apropos zip
```

## Challenges

1. How to find the command that is used to create a file?
1. Use the <code>man</code> command to display what does the command <code>cat</code> do.
1. Increase the amount of commands your command history "remembers" to 3000.
1. Show the last five commands you typed.
1. When you close the shell, where do the history commands go?
1. What happens to history when you have multiple terminals open?
