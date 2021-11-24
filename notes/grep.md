<h1>The grep utility</h1>
<code>grep</code> looks for lines that match a given pattern in the listed files (or standard input if no files are specified). <code>grep</code>'s default behavior is to print out the lines that match.

Print all lines containing word <code>test</code> in a file named file_name:

```bash
grep test file_name
```

<h2>Flags</h2>
There are number of useful flags:

| Flag | Description |
| --- | --- |
| <code>-c</code> | count the number of lines matching the pattern |
| <code>-i</code> | ignore case |
| <code>-v</code> | print the lines that do not match to the pattern |
| <code>-n</code> | print out the number of lines before the match |
| <code>-e</code> | pattern to match |

Match two patterns, pattern1 and pattern2 in a file named file_name:

```bash
grep -e 'pattern1' -e 'pattern2' file_name
```

<h2>Regex</h2>

| Symbol | Description |
| --- | --- |
| <code>.</code> | Match any one character other than the new line. |
| <code>^</code> | Match the start of the string. |
| <code>$</code> | Match the end of the string. |
| <code>*</code> | Match any number of times of the character of the string. |
| <code>\\</code> | Escape following character. |
| <code>()</code> | Match for a set of regular expressions. |
| <code>?</code> | Match exactly one character in the string. |

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

<h2>Quantifiers</h2>

Quantifiers enable you to define the amount of instances of elements required for a match to occur.

| Flag | Description |
| --- | --- |
| <code>*</code> | Match the preceding character zero or more times. |
| <code>?</code> | Match the preceding character zero or one time. |
| <code>+</code> | Match the preceding character one or more times. |
| <code>{n}</code> | Match the preceding character exactly n times. |
| <code>{n,}</code> | Match the preceding character at least n times. |
| <code>{,m}</code> | Match the preceding character at most m times. |
| <code>{n,m}</code> | Match the preceding character from n to m times. |

The regex will match any word of 8-12 characters in length:

```bash
grep -nE "[[:alpha:]]{8,12}" file_name
```
