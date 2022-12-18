## The grep Utility

The grep command is a powerful tool for searching through text-based files for lines that match a specific pattern. It is commonly used to search for specific words or phrases within a file or group of files, but it is also capable of using regular expressions for more advanced searching. By default, grep prints out the lines that match the search pattern, but it has a variety of options for controlling its output.

To search for the word key in a file named `file_name.txt`, you can use the following command:

```
grep key file_name.txt
```

## Flags

grep has a number of options, or "flags," that allow you to customize its behavior. Some useful flags include:

| Flag | Description |
| ------ | ----------- |
| `-c` | count the number of lines matching the pattern |
| `-i` | ignore case when searching |
| `-v` | print the lines that do not match the pattern |
| `-n` | print the line number before each match |
| `-e` | specify a pattern to match |

For example, to search for either of the patterns `pattern1` and `pattern2` in the file file_name, you can use the following command:

```
grep -e 'pattern1' -e 'pattern2' file_name
```

Suppose you have a file called file_name that contains the following text:

```
This is a line containing abc.
This is another line with def.
This line does not contain either pattern.
```

To search for lines that contain either the pattern `abc` or the pattern `def`, you can use the following grep command:

```
grep -e 'abc' -e 'def' file_name
```

This will output the following lines, since they contain either `abc` or `def`:

```
This is a line containing abc.
This is another line with def.
```

Alternatively, you can use regular expressions to search for the same patterns. For example, the following grep command uses a regular expression to search for lines that contain either `abc` or `def`:

```
grep -E 'a(bc|def)' file_name
```

## Regular Expressions

grep can also use regular expressions to match patterns in the text. Regular expressions are a set of symbols that can be used to define a pattern for searching. Some common regular expression symbols include:

| Symbol | Description |
| ------ | ----------- |
| `.` | match any single character (except for a newline) |
| `^` | match the start of the line |
| `$` | match the end of the line |
| `*` | match the preceding character zero or more times |
| `\` | escape the following character |
| `()` | match a set of regular expressions |
| `?` | match the preceding character zero or one time |

For example, to search for lines in the file /opt/test.txt that begin with the character #, you could use the following command:

```
grep '^#' /opt/test.txt
```

To search for lines that end with the string xxx, you could use the following command:

```
grep 'xxx$' /opt/test.txt
```

To search for lines that contain either abc or abz, you could use the following command:

```
grep ab[cz] /opt/test.txt
```

## Quantifiers

Regular expression quantifiers allow you to specify the number of instances of a character or pattern that should be matched. Some common quantifiers include:

| Symbol | Description |
| ------ | ----------- |
| `*` | match the preceding character zero or more times |
| `?` | match the preceding character zero or one time |
| `+` | match the preceding character one or more times |
| `{n}` | match the preceding character exactly n times |
| `{n,}` | match the preceding character at least n times |
| `{,m}` | match the preceding character at most m times |
| `{n,m}` | match the preceding character from n to m times |

For example, the following regular expression will match any word with 8 to 12 characters in length:

```bash
grep -nE "[[:alpha:]]{8,12}" file_name
```

## Challenges

1. List all files and subdirectories in the current directory, and use grep to filter out any hidden files or subdirectories that do not contain the word test.
1. Search through your command history for any commands that contain the word clone and were executed within the last week.
1. Check if a user with name `adam` exists in the system, and display their home directory and default shell if they do.
1. Search for lines in a file called `file.txt` that contain the word "apple", and count the number of lines that match.
1. Search for lines in a file called `file.txt` that match the regular expression pattern `[A-Z]{3}`, and print the lines in uppercase.
