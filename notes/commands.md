## Command Information and Navigation

Overview of commands and tools for finding information about command line utilities in Linux. Covers history, man, apropos commands, and terminal navigation tips.

## History and Navigation

- `history` command: view recent commands
- `Ctrl+R`: search command history
- `!number` or `!text`: execute specific command from history
- Lines with space at beginning not saved in history
- `history -c`: clear history
- `history -w`: delete bash history contents
- `up arrow key` and `down arrow key`: navigate previous commands
- `tab key`: complete command

## The Manual (man)

- `man`: view documentation for command line utilities
- Sections in manual:
  - `1`: executable programs or shell commands
  - `2`: system calls
  - `3`: library calls
  - `4`: special files
  - `5`: file formats and conventions
  - `6`: games
  - `7`: miscellaneous
  - `8`: system administration (root) commands
  - `9`: kernel routines
- `man ls`: display man page for `ls` command
- `man -s 1 ls`: display man page for `ls` command in section 1

## Apropos

- `apropos`: search for commands using keywords
- Example: `apropos zip`

## Challenges

1. Find a way to determine the command used to create a file.
2. Display the description of the `cat` command using the man command.
3. Increase the number of commands your command history "remembers" to 3000.
4. Show the last five commands you typed.
5. When you close the shell, where do the history commands go?
6. What happens to the history when you have multiple terminals open?
