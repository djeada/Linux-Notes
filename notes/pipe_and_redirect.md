## Standard Streams

* `stdin` refers to the default source of input for a command. It is typically the keyboard, but it can also be a file or the output of another command.
* `stdout` refers to the default destination for a command's output. It is typically the terminal screen, but it can also be a file or the input of another command.
* `stderr` is a separate output stream for error messages. It is also typically the terminal screen, but it can also be redirected to a file or the input of another command.

## Pipe

Many commands default to printing to "standard output," which is the terminal screen. The pipe character (`|`) is used to redirect or divert output to another program or filter.

For example, to display information about a user named "user_name," you can use the w command, but instead of displaying their username, you can show "admin" by using grep and sed to filter and modify the output:

```bash
w | grep user_name | sed s/user_name/admin/g
```

You can also use the pipe to send the output of one command as the input of another command. For example, the following syntax is used to send an email to a remote client, with the email's body being the current time and date:

```bash
date | mail -s "This is a remote test" user1@rhhost1.localnet.com
```

Besides standard piping of stdout (`|`) there is also option to pipe the stdout and stderr (`|&`).

For example, to pipe both stdout and stderr to `grep` command, use:

```bash
ls -l |& grep "\.txt$"
```

For example, to pipe both stdout and stderr to `tee` command, which writes to both the screen and a file, use:

```bash
ls -l |& tee output.txt
```

## Redirect

The `>` operator is used to redirect standard output to a file rather than the screen. For example:

```bash
echo "hello" > file.txt
```

If the file already exists, the contents of the file will be deleted. Instead, you can use the `>>` operator to append the command's output to the file:

```bash
echo "Hello" > file.txt
echo "World!" >> file.txt
```

To capture standard error, you can prefix the `>` operator with a 2 (under UNIX, file numbers 0, 1, and 2 are assigned to standard input, standard output, and standard error, respectively). For example:

```bash
less non_existent_file 2> file.txt
```

You can also append standard error to a file using `2>>` instead of `>`.

To redirect both standard output and standard error to a single file, you can use the `&>` operator to overwrite the file, or `&>>` to append to the file.

To view the output of a command on the screen and save it to a file at the same time, you can use the `tee` command. For example, to overwrite the file output.txt, you can use `tee output.txt`, or to append to the file, you can use `tee -a output.txt`.

### A workaround for buffering 

Buffering occurs when a program holds onto its output in a buffer rather than immediately sending it to its destination. This can cause issues when trying to redirect the output of a command, as the buffered output may not be immediately available.

A possible workaround for this is to use the script command, which allows you to capture the output of a command to a file or to a variable in your shell script. For example, to capture the output of a command to a variable called output, you can use the following syntax:

```bash
output=$(script -c command_you_want_to_use /dev/null)
echo "$output"
```

The -c option specifies the command to run, and the /dev/null argument redirects any input to the command to the null device, which discards it. The output of the command is captured in the output variable, which can then be displayed or processed as needed.

Keep in mind that the script command has its own limitations and may not work with all programs. In these cases, you may need to use other techniques or tools to capture the output of the command.

## Complete summary
  
| Syntax     | StdOut visibility | StdErr visibility | StdOut in file | StdErr in file | existing file |
| --------   | ----------------- | ----------------- | -------------- | -------------- | ------------- |
| `>`          |   no              |   yes             |   yes          |   no           |  overwrite    |
| `>>`         |   no              |   yes             |   yes          |   no           |  append       |
| `2>`         |   yes             |   no              |   no           |   yes          |  overwrite    |
| `2>>`        |   yes             |   no              |   no           |   yes          |  append       |  
| `&>`         |   no              |   no              |   yes          |   yes          |  overwrite    |    
| `&>>`        |   no              |   no              |   yes          |   yes          |  append       |  
| `tee`        |   yes             |   yes             |   yes          |   no           |  overwrite    |  
| `tee -a`     |   yes             |   yes             |   yes          |   no           |  append       |
| `n.e. (*)`   |   yes             |   yes             |   no           |   yes          |  overwrite    |  
| `n.e. (*)`   |   yes             |   yes             |   no           |   yes          |  append       |
| `\|& tee`    |   yes             |   yes             |   yes          |   yes          |  overwrite    |
| `\|& tee -a` |   yes             |   yes             |   yes          |   yes          |  append       |  


## Filters

Filters are commands that are designed to be used with a pipe (`|`) to process the output of another command. These filters are relatively small programs that accomplish one specific task very well. Some common filters include:

* `sort`: Sorts the lines from a collection of files alphabetically or numerically. You can use the `-n` flag to sort numerically and the `-r` flag to sort in reverse order.
* `uniq`: Removes adjacent duplicate lines from a sorted file. The `-c` flag prefixes the output with a count of the number of occurrences of each line.
* `cut`: Selects specific columns or fields from each line of a file based on a delimiter (such as a tab or a comma) or a range of bytes, characters, or fields. The `-d` flag specifies the delimiter, and the `-f` flag specifies the fields to include.
* `tr`: Replaces or deletes specific characters or ranges of characters in input text. You can use the `-d` flag to delete characters and the `-s` flag to squeeze multiple occurrences of the specified characters into a single instance.
* `wc`: Counts the number of lines, words, and characters in input text. The `-l` flag counts lines, the `-w` flag counts words, and the `-c` flag counts characters.
* `grep`: Searches for specific patterns or regular expressions in input text and prints lines that match the pattern. You can use the `-v` flag to invert the match and print lines that do not contain the pattern.
* `awk`: Searches for patterns in input text and performs actions on the lines that match the pattern. You can use awk to extract specific fields from a file, perform calculations, and print custom output.
    
Here are some examples of how these filters can be used:

```bash
# Sort the lines in file1.txt and file2.txt and save the result in sorted.txt
sort file1.txt file2.txt > sorted.txt

# Remove adjacent duplicate lines from sorted.txt and save the result in deduped.txt
uniq sorted.txt > deduped.txt

# Search for the pattern "error" in deduped.txt and print the matching lines to the screen
grep error deduped.txt

# Search for lines containing the pattern "error" in deduped.txt and print the matching lines to the screen, along with the line number
awk '/error/{print NR, $0}' deduped.txt
```

## Challenges

1. Determine the number of users currently logged into the system.
1. Generate a sorted list of all system users, including those who are not currently logged in.
1. Create a list of all filenames ending in `.conf` located in the `/etc` directory, and sort them by string length.
1. Print the first and seventh columns of the `/etc/passwd` file side by side.
1. Display each word from the `/etc/fstab` file on a separate line, and count the number of lines in the file.
