## Standard Streams

* `stdin`: Default input source, usually keyboard.
* `stdout`: Default output destination, usually terminal screen.
* `stderr`: Separate output stream for error messages.

## Pipe

Many commands default to printing to "standard output," which is the terminal screen. The pipe character (`|`) is used to redirect or divert output to another program or filter.

For example, to show details about a person called "user_name," use the w command, and change "user_name" to "admin" like:

```bash
w | grep user_name | sed s/user_name/admin/g
```

You can also send the result of one command into another command. For example, this code sends an email with the current time and date:

```bash
date | mail -s "This is a remote test" user1@rhhost1.localnet.com
```

There are different ways to send results (`|` and `|&`).

To send both normal and error results to `grep` command, use:

```bash
ls -l |& grep "\.txt$"
```

To send both normal and error results to `tee` command, which shows on the screen and saves to a file, use:

```bash
ls -l |& tee output.txt
```

## Redirect

Use `>` to send results to a file instead of the screen:

```bash
echo "hello" > file.txt
```

If the file is there already, the old contents will be deleted. You can use `>>` to add the new result to the file:

```bash
echo "Hello" > file.txt
echo "World!" >> file.txt
```

To save error results, use `2>`:

```bash
less non_existent_file 2> file.txt
```

You can also add error results to a file using `2>>`.

To save both normal and error results to one file, use `&>` to overwrite the file, or `>>` to add to the file.

To see the result on the screen and save it to a file at the same time, use the `tee` command:

```bash
command | tee output.txt
command | tee -a output.txt
```

### A workaround for buffering 

Buffering is when a program keeps its result in a buffer before sending it. This can make problems when trying to save the result.

You can use the script command to fix this. It lets you save the result of a command to a file or a variable. For example, to save the result of a command to a variable called output, do this:

```bash
output=$(script -c command_you_want_to_use /dev/null)
echo "$output"
```

The `-c` option tells what command to run. The `/dev/null` part sends any input to the command to a place that throws it away. The result is saved in the output variable, and you can show or use it as needed.

Remember that the script command might not work with all programs. In these cases, you might need to use other ways or tools to save the result.

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
