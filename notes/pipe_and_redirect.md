## Working with Data Streams

Input redirection (`<`) allows a command to read from a file, while output redirection (`>`) sends a command's output to a file. Streams like stdin, stdout, and stderr control the flow of data between commands and the system, where stdin is the input, stdout is the standard output, and stderr is the error output. Pipes (`|`) connect the output of one command directly into the input of another, enabling you to chain commands together seamlessly. Filters, such as `grep` and `awk`, process these data streams, allowing you to search, manipulate, and extract information efficiently.

### Standard Streams

Unix and Unix-like operating systems use three primary standard streams for program interaction. These streams are set up at the start of a terminal session and act as the main channels for communication between a program and its environment:

I. **Standard Input**

- **stdin** is the input stream where data is fed into a program, acting as the primary source for reading input data.
- The default source for **stdin** is usually the keyboard.
- Programs commonly use **stdin** to read user input from the terminal, though this input stream can also be redirected from files.

II. **Standard Output**

- **stdout** serves as the primary output stream for a program, where it sends data that needs to be displayed.
- The default destination for **stdout** is typically the terminal screen or console.
- Programs use **stdout** to display results, messages, or general output data, and this output can be redirected to files or piped to other programs.

III. **Standard Error**

- **stderr** is a dedicated output stream for error messages and diagnostics, which are kept separate from regular output.
- Like **stdout**, the default destination for **stderr** is usually the terminal screen.
- Programs send error messages, such as those generated by failed operations like accessing a non-existent file, to **stderr**, which can be independently redirected from **stdout**.

```
+----------------------------+
|     Terminal / Screen      |
+----------------------------+
       ^                ^
       |                |
    stdout           stderr
       |                |
+------------------------------+
|         Process              |
|     (Unix Program)           |
+------------------------------+
       ^
       |
     stdin
       |
+------------------+
|  Keyboard/File   |
+------------------+
```

### Pipe

The pipe (`|`) character is an essential tool that allows for data to flow from one command to another. It's a form of redirection that captures the standard output (stdout) of one command and feeds it as the standard input (stdin) to another.

```
+--------------+         +--------------+
|   Process A  |         |   Process B  |
|  (Producer)  |         |  (Consumer)  |
+--------------+         +--------------+
      |                        ^
      | stdout                 | stdin
      |                        |
      +-----------[PIPE]-------+
```

#### Example 1: Filtering User Details
   
Suppose you want to see details about a person named "user_name" using the `w` command and subsequently modify "user_name" to "admin". This can be done with:

```bash
 w | grep user_name | sed s/user_name/admin/g
```

Here, the grep command filters the output of w to only lines containing "user_name", and then sed changes "user_name" to "admin".

#### Example 2: Sending Email with Current Date

You can combine the output of the date command (which gives the current date and time) with the mail command to send an email:

```bash
date | mail -s "This is a remote test" user1@rhhost1.localnet.com
```

#### Advanced Piping

- The traditional pipe `|` allows you to take the standard output (stdout) from one command and send it as input to another command, effectively chaining commands together while excluding any errors or standard error (stderr) streams.
- When both the standard output and standard error need to be captured and passed to another command, the `|&` syntax is utilized. This feature is particularly useful when you want to process both successful output and errors together in a pipeline.

**Example: Searching for Text Files with Error Inclusion**

Suppose you want to list all text files using `ls -l` and search for `.txt` files using `grep`. By including both output and error messages, you can ensure that any issues encountered during listing are also captured:

```bash
ls -l |& grep "\.txt$"
```

In this example, `ls -l` may produce both regular output and error messages (such as "Permission denied" errors). The `|&` operator ensures that both are passed to `grep`, which then filters the output for lines ending with `.txt`.

**Example: Displaying and Saving Output**

To display both stdout and stderr on the screen while saving them to a file named `output.txt`, you can use:

```bash
ls -l |& tee output.txt
```

Here, `ls -l |&` captures both the regular output and any errors, which are then passed to `tee`. The `tee` command displays the combined output on the terminal and writes it to `output.txt`.

### Redirection

Redirection is a mechanism that controls the destination of a command's output, directing it to another command, a file, or even discarding it. It also allows commands to receive input from files instead of the keyboard.

```
+------------------------+
|       Process          |
|------------------------|
| stdin:  from file      |◄───────── input.txt
| stdout: to file        |─────────► output.txt
| stderr: to file        |─────────► error.txt
+------------------------+
```

#### I. Redirecting Standard Output

The `>` symbol redirects the standard output of a command to a file. For example:

```bash
echo "hello" > file.txt
```

If the file already exists, it will be overwritten. To append to an existing file, use `>>`:

```bash
echo "Hello" > file.txt
echo "World!" >> file.txt
```

#### II. Redirecting Standard Error

Errors can be separately redirected using `2>`:

```bash
less non_existent_file 2> errors.txt
```

To append errors to an existing file, use `2>>`:

```bash
less non_existent_file 2>> errors.txt
```

#### III. Redirecting Both Standard Output and Error

Use `&>` to overwrite a file with both outputs or `&>>` to append both to the file:

```bash
command &> output.txt
command &>> output.txt
```

#### IV. Redirecting Standard Input

The `<` symbol redirects the standard input of a command to come from a file instead of the keyboard. For example:

```bash
sort < unsorted_list.txt
```

In this example, the `sort` command takes its input from `unsorted_list.txt` instead of waiting for user input.

#### V. Using Input and Output Redirection Together

Commands can utilize both input and output redirection simultaneously. For example:

```bash
sort < unsorted.txt > sorted.txt
```

In this case, the `sort` command reads the contents of `unsorted.txt`, sorts the lines, and writes the sorted output to `sorted.txt`. This demonstrates how input redirection (`<`) takes data from a file, while output redirection (`>`) sends the processed result to another file.

#### VI. Here-Documents with `<<`

The `<<` operator, known as a here-document, allows you to provide multi-line input directly within the shell script or command line, ending the input with a specified delimiter. For example:

```bash
cat <<EOF
This is a test file
with multiple lines
of text.
EOF
```

In this example, everything between `<<EOF` and `EOF` is treated as input to the `cat` command. The delimiter `EOF` can be replaced with any token, and it marks the end of the input block.

#### VII. View and Save Output Simultaneously

The `tee` command is useful for displaying output on the screen while also saving it to a file:

```bash
command | tee output.txt      # overwrite the file
command | tee -a output.txt   # append to the file
```

#### VIII. Handling Buffering Issues

Sometimes, programs buffer their output, causing delays or issues when trying to redirect. The `script` command can be a solution:

```bash
output=$(script -c your_command /dev/null)
echo "$output"
```

Here, the `-c` option specifies the command to run, while `/dev/null` discards any input. The result is captured in the `output` variable.

#### Summary Table

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

### Filters

Filters are specialized commands designed to process text, typically working with streams of text data. They are predominantly used with pipes (`|`) to modify or analyze the output of another command. A filter reads input line by line, transforms it in some way, and then outputs the result. This processing method is particularly useful in Unix-like operating systems, where filters can be combined with other commands in a pipeline to perform complex text transformations and data analysis. Common examples of filters include `grep` for searching text, `sort` for arranging lines in a particular order, and `awk` for pattern scanning and processing. Filters are a fundamental part of command-line data manipulation, allowing users to efficiently process large amounts of text with simple, concise commands.
```
+---------------+          +-------------+          +---------------+
|   Producer    |          |   Filter    |          |   Consumer    |
|   (Process)   |─────────▶| (Transformer|─────────▶|   (Process)   |
|   stdout      |─────────▶|   process)  |─────────▶|   stdin       |
+---------------+          +-------------+          +---------------+
```

#### Common Unix Filters

| Command | Description | Basic Usage | Common Options | Examples |
|---------|-------------|-------------|----------------|----------|
| `sort`  | Orders lines in text alphabetically or numerically. | `sort [options] [file]` | - `-n`: Sort numerically. <br> - `-r`: Reverse order. <br> - `-k`: Specify sort key. | `sort -n numbers.txt` sorts `numbers.txt` numerically. |
| `uniq`  | Filters out repeated lines in adjacent positions, simplifying repeated content. | `uniq [options] [file]` | - `-c`: Count occurrences. <br> - `-d`: Only show duplicates. <br> - `-u`: Only show unique lines. | `uniq -c sorted.txt` counts occurrences of unique lines in `sorted.txt`. |
| `cut`   | Extracts specific columns or fields from each line, useful for structured text. | `cut [options] [file]` | - `-f`: Specify delimiter. <br> - `-d`: Use a custom delimiter. <br> - `-c`: Choose column or range of characters. | `cut -f1,3 -d',' data.csv` extracts columns 1 and 3 from `data.csv`, using ',' as a delimiter. |
| `tr`    | Transforms characters into others or removes specific characters. | `tr [options] [string1] [string2]` | - `-d`: Delete characters in `string1`. <br> - `-s`: Squeeze repeated characters. <br> - `-c`: Compliment `string1`. | `tr 'a-z' 'A-Z' < input.txt` converts lowercase to uppercase in `input.txt`. |
| `wc`    | Counts lines, words, and characters in text. | `wc [options] [file]` | - `-l`: Line count. <br> - `-w`: Word count. <br> - `-c`: Character count. | `wc -l file.txt` returns the line count for `file.txt`. |
| `grep`  | Searches input for lines matching a pattern or regular expression. | `grep [options] pattern [file]` | - `-i`: Ignore case. <br> - `-v`: Invert match. <br> - `-r`: Search recursively in directories. | `grep 'error' logfile.txt` searches for 'error' in `logfile.txt`. |
| `awk`   | Processes text by extracting fields and performing actions based on conditions. | `awk 'pattern {action}' [file]` | - `-F`: Specify field separator. <br> - `-v`: Invert match. <br> - `-f`: Use file for program script. | `awk '{print $1, $3}' data.txt` prints columns 1 and 3 from `data.txt`. |

#### Examples

Let's take a look at a few examples:

I. **Combine and sort the content of file1.txt and file2.txt, and redirect the sorted output to sorted.txt:**

This command uses the `sort` utility to combine the contents of both `file1.txt` and `file2.txt` while sorting all the lines alphabetically (or numerically, if options are provided). By using the redirection operator `>`, the sorted output is saved into a new file called `sorted.txt`.  
 
Suppose **file1.txt** contains:  

```
banana
apple
```

And **file2.txt** contains:  

```
cherry
apple
```

Running the command:  

```bash
sort file1.txt file2.txt > sorted.txt
```

The content in **sorted.txt** might be:  

```
apple
apple
banana
cherry
```  

II. **Eliminate any adjacent duplicate lines from sorted.txt and save the result in deduped.txt:**

After sorting, duplicate lines become adjacent. The `uniq` command then reads the sorted file and removes any consecutive duplicate lines. The output, which has duplicates eliminated, is redirected into a new file called `deduped.txt`. This is particularly useful when you need a list where each line is unique.  
  
Given the **sorted.txt** content from the previous step:  

```
apple
apple
banana
cherry
```  

Running:  

```bash
uniq sorted.txt > deduped.txt
```  

The resulting **deduped.txt** would be:  

```
apple
banana
cherry
```  

III. **Display lines containing the word "error" from deduped.txt:**

The `grep` command is used to search within **deduped.txt** for lines that include the word "error". It is case-sensitive by default, so only lines with exactly "error" (all lowercase) will be matched. The matched lines are then printed to the terminal.  
   
If **deduped.txt** contains:  

```
apple
error: file not found
banana
cherry
Error: system crash
```  

Running:  

```bash
grep 'error' deduped.txt
```  

The output will be:  

```
error: file not found
```  

(Note: "Error: system crash" is not matched because `grep` is case-sensitive.)

IV. **Show lines from deduped.txt that contain the pattern "error", along with the line number:**

Using `awk`, this command searches for lines containing "error" in **deduped.txt** and prints the line number (`NR`, which represents the current record or line number) followed by the entire line. This gives you context on where each occurrence is located in the file.  
  
Consider **deduped.txt** with the following content:  

```
apple
error: file not found
banana
error: network timeout
cherry
```  
Executing:  

```bash
awk '/error/ {print NR, $0}' deduped.txt
```  

Expected output:  

```
2 error: file not found
4 error: network timeout
```  

V. **Replace all occurrences of 'old_word' with 'new_word' in file.txt:**

The `sed` (Stream Editor) command in this example performs a substitution. The command will search through **file.txt** for every instance of `old_word` and replace it with `new_word`. The `g` flag at the end ensures that all occurrences on each line are replaced. Note that this command writes the changes to standard output; to update the file itself, you may need to use the `-i` (in-place) option depending on your shell or operating system.  
  
Assume **file.txt** contains:  

```
This is the old_word in a line.
Another line with old_word and old_word again.
```

Running:  

```bash
sed 's/old_word/new_word/g' file.txt
```  

Would output:  

```
This is the new_word in a line.
Another line with new_word and new_word again.
```

#### Combining Filters

When you chain multiple filters using the pipe operator (`|`), the output of one command becomes the input of the next. This allows you to perform complex text transformations and analyses using just one command line. Let's take a look a the following example:

```bash
# Sort the content of a file, eliminate duplicates, and then display only lines containing "error"
cat arduino_log.txt | sort | uniq | grep 'error'
```

I. **cat arduino_log.txt**  

The `cat` command reads the contents of the file `arduino_log.txt` and sends it to standard output. This file might contain log messages from your Arduino or sensor readings.

Suppose **arduino_log.txt** contains:

```
SensorTemp: 23.5
error: voltage drop detected
ArduinoInit: Success
SensorTemp: 23.5
error: sensor timeout
ArduinoInit: Success
```

The output is exactly what’s contained in the file:

```
SensorTemp: 23.5
error: voltage drop detected
ArduinoInit: Success
SensorTemp: 23.5
error: sensor timeout
ArduinoInit: Success
```

II. **sort** 

The `sort` command reads the incoming text and arranges the lines in lexicographical order. Sorting helps to group identical or similar log messages together.

After sorting:  

```
ArduinoInit: Success
ArduinoInit: Success
SensorTemp: 23.5
SensorTemp: 23.5
error: sensor timeout
error: voltage drop detected
```

III. **uniq**  

The `uniq` command removes any adjacent duplicate lines. Since the logs have been sorted, identical messages are now consecutive, so this command filters out the duplicates.

After removing duplicates:

```
ArduinoInit: Success
SensorTemp: 23.5
error: sensor timeout
error: voltage drop detected
```

IV. **grep 'error'**  
The `grep` command then filters the output, selecting only the lines that contain the word "error". This command is case-sensitive by default.

After filtering:

```
error: sensor timeout
error: voltage drop detected
```

Filters are very important components in the Unix philosophy of creating simple, modular tools that do one job and do it well. When used effectively, they provide powerful text processing capabilities with just a few keystrokes.

## Challenges

1. Find the number of users currently logged in. Hint: Use the `who` or `w` command followed by a line count.
2. Generate a sorted list of all system users. Hint: The `/etc/passwd` file contains user information.
3. List `.conf` filenames in the `/etc` directory and sort them by string length. You may need to use `ls`, `awk`, and `sort`.
4. Print the first and seventh columns of the `/etc/passwd` file. These columns represent the username and the user's shell, respectively.
5. Display each word from the `/etc/fstab` file on a separate line, and then count the total number of lines in the file. This file provides information on disk drives and their mount points.
6. Find out how many users have a unique shell (i.e., they're the only ones using a particular shell). Use `/etc/passwd` as your source.
7. From any text file of your choice, identify the ten most frequently occurring words and display their counts.
8. Examine the `/etc/systemd/system` directory and list the service files that are currently active on the system.
9. Search for words in a text file that are longer than 7 characters, contain the letter 'z', and display them sorted in reverse alphabetical order.
10. Find the top five directories that consume the most disk space in your home directory. Hint: Use the `du` and `sort` commands.
11. Starting from your home directory, list all files (recursively, including subdirectories) that were modified in the last 24 hours, sorted by their modification time. 
