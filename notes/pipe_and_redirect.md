## Standard Streams

* `stdin`: Default input source, usually keyboard.
* `stdout`: Default output destination, usually terminal screen.
* `stderr`: Separate output stream for error messages.

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

- `sort`: Sort lines alphabetically or numerically.
- `uniq`: Remove adjacent duplicate lines from a sorted file.
- `cut`: Select specific columns or fields from each line.
- `tr`: Replace or delete specific characters or ranges of characters.
- `wc`: Count the number of lines, words, and characters.
- `grep`: Search for specific patterns or regular expressions.
- `awk`: Search for patterns and perform actions on matching lines.
    
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

1. Find the number of users currently logged in.
2. Generate a sorted list of all system users.
3. List `.conf` filenames in `/etc` directory, sorted by string length.
4. Print first and seventh columns of `/etc/passwd` file.
5. Display each word from the `/etc/fstab` file on a separate line, and count the number of lines in the file.
