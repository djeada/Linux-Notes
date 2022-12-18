# Command Information and Navigation

An overview of various commands and tools for finding and accessing information about command line utilities in Linux. It covers the history, man, and apropos commands, as well as tips for navigating and using the terminal. 

## History and Navigation

The history command allows you to view the most recently used commands. You can specify the number of commands to display (it is generally between 1000 and 5000). Use `Ctrl+R` to search through your command history. You can also execute a specific command from the history using `!number` (where number is the number of the command in the history) or `!text` (where text is the beginning of the command you want to execute). Note that lines that begin with a space character are not saved in the history list.

To clear the history, use the `history -c` command. To delete the contents of the bash history, use `history -w`.

You can navigate through previously used commands in the terminal using the `up arrow key` and `down arrow key`. The `tab key` can also be used to complete a command.

## The Manual

The man command (short for manual) allows you to view the documentation for various built-in command line utilities. The manual is organized into sections, each corresponding to a different type of utility:

| Number | Description |
| --- | --- |
| **`1`** | executable programs or shell commands |
| `2` | system calls |
| `3` | library calls |
| `4` | special files |
| **`5`** | file formats and conventions |
| `6` | games |
| `7` | misc |
| **`8`** | system administration (root) commands |
| `9` | kernel routines |

To display the man page for the `ls` command, you would enter the following in the terminal:

```
man ls
```

This will display the documentation for the `ls` command in the terminal, with details about its options, usage, and examples. You can navigate the man page using the up and down arrow keys, and you can exit the man page by pressing `q`.

You can also specify a specific section of the man pages to view using the `-s` flag followed by the section number. For example, to view the man page for the `ls` command in section 1 (executable programs or shell commands), you would use the following command:

```
man -s 1 ls
```

## Apropos

If you know a few keywords related to a command but can't remember the specific command, you can use the `apropos` command to search for it. For example, `apropos zip` will display a list of commands related to zip files.

## Challenges

1. How can you find the command used to create a file?
1. Use the man command to display the description of the `cat` command.
1. Increase the number of commands your command history "remembers" to 3000.
1. Show the last five commands you typed.
1. When you close the shell, where do the history commands go?
1. What happens to the history when you have multiple terminals open?
