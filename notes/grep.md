## The grep tool

Grep helps to search for specific words or phrases in text files. It can also use regular expressions for advanced searching.

To search for the word "key" in a file called `file_name.txt`, use this command:

```
grep key file_name.txt
```

## Options

Grep has options called "flags" that can change how it works. Some useful flags are:

| Flag | What it does |
| ---- | ------------ |
| `-c` | count lines that match |
| `-i` | don't care about upper or lower case |
| `-v` | show lines that don't match |
| `-n` | show line number before each match |
| `-e` | choose a pattern to match |

For example, to search for `pattern1` or `pattern2` in a file, use this command:

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

Regular expressions are symbols that help define a pattern for searching. Some common symbols are:

| Symbol | What it does |
| ------ | ------------ |
| `.` | match any character (except newline) |
| `^` | match start of the line |
| `$` | match end of the line |
| `*` | match previous character many times |
| `\` | escape next character |
| `()` | match a set of regular expressions |
| `?` | match previous character once or not at all |

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

Quantifiers help specify how many times a character or pattern should match. Some common quantifiers are:

| Symbol | What it does |
| ------ | ------------ |
| `*` | match previous character many times |
| `?` | match previous character once or not at all |
| `+` | match previous character one or more times |
| `{n}` | match previous character exactly n times |
| `{n,}` | match previous character at least n times |
| `{,m}` | match previous character at most m times |
| `{n,m}` | match previous character from n to m times |

For example, to find words with 8 to 12 letters, use this command:

```bash
grep -nE "[[:alpha:]]{8,12}" file_name
```

## Challenges

1. Show files and folders in the current directory, but don't show hidden ones without the word "test".
2. Find commands with the word "clone" that were used in the last week.
3. Check if a user named adam exists, and show their home folder and default shell if they do.
4. Find lines with the word "apple" in a file called `file.txt`, and count the lines.
5. Find lines with the pattern `[A-Z]{3}` in a file called `file.txt`, and show the lines in uppercase.
