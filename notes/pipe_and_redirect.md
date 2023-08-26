## Standard Streams

In Unix and Unix-like operating systems, there are three primary standard streams that interact with a program. These are established when a terminal session starts and serve as the default communication channels between the program and its environment:

1. **`stdin` (Standard Input)**
   - **Description**: `stdin` is the standard source for input data. It reads data that is passed into a program.
   - **Default Source**: Typically, the keyboard.
   - **Common Usage**: When a program waits for the user to type something into the terminal, it's reading from `stdin`. You can also redirect input from files into a program using `stdin`.

2. **`stdout` (Standard Output)**
   - **Description**: `stdout` is the conventional destination where a program writes its output data.
   - **Default Destination**: Usually, the terminal screen or console.
   - **Common Usage**: When a program displays results, messages, or any regular data, it writes to `stdout`. This output can be redirected to files or piped to other programs.

3. **`stderr` (Standard Error)**
   - **Description**: `stderr` is a separate output stream dedicated for error messages or diagnostics. By default, error messages are separated from regular output to allow users or other programs to handle them differently if needed.
   - **Default Destination**: Like `stdout`, it's typically the terminal screen.
   - **Common Usage**: If a program encounters an error, such as trying to read a non-existent file, it will send an error message to `stderr`. This stream can also be redirected independently of `stdout`.

## Pipe

The pipe (`|`) character is an essential tool that allows for data to flow from one command to another. It's a form of redirection that captures the standard output (stdout) of one command and feeds it as the standard input (stdin) to another.

### Basic Usage

When you run commands in a terminal, they often display their results directly to the terminal. This display is known as "standard output." With the pipe (`|`), you can change this behavior and direct the output to another command.

### Examples

1. **Filtering User Details**
   
Suppose you want to see details about a person named "user_name" using the `w` command and subsequently modify "user_name" to "admin". This can be done with:

 ```bash
 w | grep user_name | sed s/user_name/admin/g
```

Here, the grep command filters the output of w to only lines containing "user_name", and then sed changes "user_name" to "admin".

2. **Sending Email with Current Date**

You can combine the output of the date command (which gives the current date and time) with the mail command to send an email:

```bash
date | mail -s "This is a remote test" user1@rhhost1.localnet.com
```

### Advanced Piping (| vs. |&)

1. **Piping Standard Output Only (|)**: The traditional pipe | will only take the standard output of a command. Errors or standard error (stderr) are not captured.

2. **Piping Both Standard Output and Error (|&)**: Sometimes you might want to capture both the standard output and the standard error. The |& syntax achieves this.

To filter both standard output and error outputs for text files:

``` bash
ls -l |& grep "\.txt$"
```

To display both outputs on the screen and simultaneously save to a file:

```bash
ls -l |& tee output.txt
```

## Redirection

Redirection allows you to control where the output of a command goes, be it another command, a file, or nowhere at all.

### Basic Redirection

1. **Redirecting Standard Output**

The `>` symbol is used to redirect the standard output to a file:

```bash
echo "hello" > file.txt
```

If the file already exists, it will be overwritten. To append to an existing file, use `>>`:

```bash
echo "Hello" > file.txt
echo "World!" >> file.txt
```

2. **Redirecting Standard Error**

Errors can be separately redirected using `2>`:

```bash
less non_existent_file 2> errors.txt
```

To append errors to an existing file, use `2>>`.

3. **Redirecting Both Standard Output and Error**

Use `&>` to overwrite a file with both outputs or `&>>` to append both to the file:

```bash
command &> output.txt
command &>> output.txt
```

4. **View and Save Output Simultaneously**

The `tee` command can be used to display the output on the screen and save it to a file:

```bash
command | tee output.txt      # overwrite the file
command | tee -a output.txt   # append to the file
```

### Advanced Redirection

1. **Handling Buffering Issues**

Sometimes, programs buffer their output, causing delays or issues when trying to redirect. The `script` command can be a solution:

```bash
output=$(script -c your_command /dev/null)
echo "$output"
```

Here, the `-c` option specifies the command to run, while `/dev/null` discards any input. The result is captured in the `output` variable.

### Summary Table of Redirection Techniques

| Syntax      | StdOut Visible | StdErr Visible | StdOut in File | StdErr in File | Existing File Behavior |
| ----------- | -------------- | -------------- | -------------- | -------------- | ---------------------- |
| `>`         | No             | Yes            | Yes            | No             | Overwrite               |
| `>>`        | No             | Yes            | Yes            | No             | Append                  |
| `2>`        | Yes            | No             | No             | Yes            | Overwrite               |
| `2>>`       | Yes            | No             | No             | Yes            | Append                  |
| `&>`        | No             | No             | Yes            | Yes            | Overwrite               |
| `&>>`       | No             | No             | Yes            | Yes            | Append                  |
| `tee`       | Yes            | Yes            | Yes            | No             | Overwrite               |
| `tee -a`    | Yes            | Yes            | Yes            | No             | Append                  |
| `\|& tee`   | Yes            | Yes            | Yes            | Yes            | Overwrite               |
| `\|& tee -a`| Yes            | Yes            | Yes            | Yes            | Append                  |

## Filters

Filters are specialized commands designed to process text, typically working with streams of text data. They are predominantly used with pipes (`|`) to modify or analyze the output of another command. A filter reads input line by line, transforms it in some way, and then outputs the result.

### Common Unix Filters

- **`sort`**: Orders lines in text alphabetically or numerically.
- **`uniq`**: Filters out repeated lines in adjacent positions. It's useful for simplifying text that has repeated content.
- **`cut`**: Extracts specific columns or fields from each line. Handy for data extraction from structured text.
- **`tr`**: Transforms certain characters into other characters or removes specific characters.
- **`wc`**: Provides a count of lines, words, and characters in text.
- **`grep`**: Searches input for lines that match a given pattern or regular expression. One of the most powerful text search tools.
- **`awk`**: A text processing tool that is particularly good at extracting fields from lines and performing actions based on conditional matches.

### Examples Using Filters

```bash
# Combine and sort the content of file1.txt and file2.txt, and redirect the sorted output to sorted.txt
sort file1.txt file2.txt > sorted.txt

# Eliminate any adjacent duplicate lines from sorted.txt and save the result in deduped.txt
uniq sorted.txt > deduped.txt

# Display lines containing the word "error" from deduped.txt
grep 'error' deduped.txt

# Show lines from deduped.txt that contain the pattern "error", along with the line number
awk '/error/ {print NR, $0}' deduped.txt

# Replace all occurrences of 'old_word' with 'new_word' in file.txt
sed 's/old_word/new_word/g' file.txt
```

### Combining Filters

Filters become even more powerful when combined. By chaining together multiple filters using the pipe (|), you can perform complex text transformations and analyses with a single command.

```bash
# Sort the content of a file, eliminate duplicates, and then display only lines containing "error"
cat file.txt | sort | uniq | grep 'error'
```

Unix filters are foundational components in the Unix philosophy of creating simple, modular tools that do one job and do it well. When used effectively, they provide powerful text processing capabilities with just a few keystrokes.

## Challenges

1. **Logged-in Users**: Find the number of users currently logged in. Hint: Use the `who` or `w` command followed by a line count.
2. **System Users List**: Generate a sorted list of all system users. Hint: The `/etc/passwd` file contains user information.
3. **Configuration Files**: List `.conf` filenames in the `/etc` directory and sort them by string length. You may need to use `ls`, `awk`, and `sort`.
4. **User Data Extraction**: Print the first and seventh columns of the `/etc/passwd` file. These columns represent the username and the user's shell, respectively.
5. **System Mount Points Analysis**: Display each word from the `/etc/fstab` file on a separate line, and then count the total number of lines in the file. This file provides information on disk drives and their mount points.
6. **Unique System Shells**: Find out how many users have a unique shell (i.e., they're the only ones using a particular shell). Use `/etc/passwd` as your source.
7. **Most Common Words**: From any text file of your choice, identify the ten most frequently occurring words and display their counts.
8. **Active Services**: Examine the `/etc/systemd/system` directory and list the service files that are currently active on the system.
9. **Custom Word Search**: Search for words in a text file that are longer than 7 characters, contain the letter 'z', and display them sorted in reverse alphabetical order.
10. **Disk Space Usage**: Find the top five directories that consume the most disk space in your home directory. Hint: Use the `du` and `sort` commands.
11. **Recursive File Analysis**: Starting from your home directory, list all files (recursively, including subdirectories) that were modified in the last 24 hours, sorted by their modification time. 
