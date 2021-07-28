<i>grep</i> looks for lines that match a given pattern in the listed files (or standard input if no files are specified). <i>grep</i>'s default behavior is to print out the lines that match.

Print all lines containing word <i>test</i> in a file named file_name:

```bash
grep test file_name
```

<h2>Flags</h2>
There are number of useful flags:

| Flag | Description |
| --- | --- |
| <i>-c</i> | count the number of lines matching the pattern |
| <i>-i</i> | ignore case |
| <i>-v</i> | print the lines that do not match to the pattern |
| <i>-n</i> | print out the number of lines before the match |
| <i>-e</i> | pattern to match |

Match two patterns, pattern1 and pattern2 in a file named file_name:

```bash
grep -e 'pattern1' -e 'pattern2' file_name
```

<h2>Quantifiers</h2>

Quantifiers enable you to define the amount of instances of elements required for a match to occur.

| Flag | Description |
| --- | --- |
| <i>*</i> | Match the preceding item zero or more times. |
| <i>?</i> | Match the preceding item zero or one time. |
| <i>+</i> | Match the preceding item one or more times. |
| <i>{n}</i> | Match the preceding item exactly n times. |
| <i>{n,}</i> | Match the preceding item at least n times. |
| <i>{,m}</i> | Match the preceding item at most m times. |
| <i>{n,m}</i> | Match the preceding item from n to m times. |

The regex will match any word of 8-12 characters in length:

```bash
grep -nE "[[:alpha:]]{8,12}" file_name
```