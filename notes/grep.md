## The grep utility
The command `grep` looks for lines that match a given pattern in the given files or standard input if no files are specified. `Grep`'s default behavior is to print out the lines that match the search pattern.

To print all lines containing the word `key` in a file named *file_name.txt*, use:

```bash
grep key file_name.txt
```

### Flags
There are number of useful flags:

| Flag | Description |
| --- | --- |
| `-c` | count the number of lines matching the pattern |
| `-i` | ignore case |
| `-v` | print the lines that do not match to the pattern |
| `-n` | print out the number of lines before the match |
| `-e` | a pattern to match |

Match two patterns, pattern1 and pattern2 in a file named file_name:

```bash
grep -e 'pattern1' -e 'pattern2' file_name
```

### Regex

| Symbol | Description |
| --- | --- |
| `.` | Match any one character other than the new line. |
| `^` | Match the start of the string. |
| `$` | Match the end of the string. |
| `*` | Match any number of times of the character of the string. |
| `\\` | Escape following character. |
| `()` | Match for a set of regular expressions. |
| `?` | Match exactly one character in the string. |

Display all the lines that begin with '#' from the file /opt/test.txt using ^ pattern:

```bash
grep '^#' /opt/test.txt
```

Display all the lines that begin with 'xxx' from the file /opt/test.txt using $ pattern:

```bash
grep 'xxx$' /opt/test.txt
```

Display all the lines that contain 'abc' or 'abz' from the file /opt/test.txt using \[\] pattern:

```bash
grep ab[cz] /opt/test.txt
```

### Quantifiers

Quantifiers enable you to define the amount of instances of elements required for a match to occur.

| Flag | Description |
| --- | --- |
| `*` | Match the preceding character zero or more times. |
| `?` | Match the preceding character zero or one time. |
| `+` | Match the preceding character one or more times. |
| `{n}` | Match the preceding character exactly n times. |
| `{n,}` | Match the preceding character at least n times. |
| `{,m}` | Match the preceding character at most m times. |
| `{n,m}` | Match the preceding character from n to m times. |

The regex will match any word of 8-12 characters in length:

```bash
grep -nE "[[:alpha:]]{8,12}" file_name
```

## Challenges

1. List all files and subdirectories in the current directory, then use grep to remove all of the listed files and subdirectories except those that contain the word `test`. 
2. Search through your command history for any commands that contain the word *clone*.
3. Check if a user with name *adam* exists in the system.
