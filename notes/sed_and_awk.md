## Command-Line Stream Editors

`sed` (Stream Editor) and `awk` are powerful command-line utilities that originated from Unix and have become indispensable tools in Unix-like operating systems, including Linux and macOS. They are designed for processing and transforming text, allowing users to perform complex text manipulations with simple commands. This guide provides a comprehensive overview of both utilities, including their history, usage, syntax, options, and practical examples.

### Sed

Developed in the 1970s by Lee E. McMahon of Bell Labs, `sed` is a non-interactive stream editor used to perform basic text transformations on an input stream (a file or input from a pipeline). It was designed to support scripting and command-line usage, automating repetitive editing tasks.

Main idea:

- Performs editing operations automatically without user interaction.
- Processes input line by line, making it efficient for large files.
- Supports powerful pattern matching using regular expressions.
- Allows the use of scripts for complex editing tasks.

#### Syntax

The basic syntax of `sed` is:

```bash
sed [OPTIONS] 'SCRIPT' INPUTFILE...
```

- **OPTIONS** are used to modify the behavior of `sed`, allowing customization of how the command processes and interprets input.
- The **SCRIPT** consists of one or more editing commands that `sed` applies to the input, defining specific transformations or modifications to be executed.
- **INPUTFILE** refers to one or more files that `sed` processes, enabling batch or single-file editing based on the specified script commands.

#### How `sed` Works

```
User
 |
 | Uses 'sed' with a script and input file(s)
 v
+-------------------------------+
| sed Command                   |
|  - Reads Input Line by Line   |
|  - Applies Script to Each Line|
|  - Outputs Modified Lines     |
+-------------------------------+
 |
 | Outputs to Terminal or File
 v
```

`sed` reads the input text line by line, applies the specified commands to each line, and outputs the result. If no input file is specified, `sed` reads from standard input.

#### Common Operations with `sed`

##### Substitution

The substitution command replaces text matching a pattern with new text.

**Syntax:**

```bash
sed 's/pattern/replacement/flags' inputfile
```

- **`s`**: Substitution command.
- **`pattern`**: The regular expression to search for.
- **`replacement`**: The text to replace the pattern with.
- **`flags`**: Optional flags to modify the behavior.

**Common Flags:**

- **`g`**: Global replacement in the line.
- **`i`**: Case-insensitive matching.
- **`p`**: Prints the line if a substitution occurred.

**Example: Replace 'apple' with 'orange' globally:**

```bash
sed 's/apple/orange/g' fruits.txt
```

##### Deletion

Delete lines matching a pattern or at a specific line number.

**Syntax:**

```bash
sed '/pattern/d' inputfile
```

**Example: Remove empty lines:**

```bash
sed '/^$/d' file.txt
```

**Explanation:**

- `^$` matches empty lines.
- `d` deletes the matching lines.

##### Insertion and Appending

Insert or append text before or after a line matching a pattern.

**Syntax:**

**Insert (`i`)**:

```bash
sed '/pattern/i\text to insert' inputfile
```

**Example: Insert a header before the first line:**

```bash
sed '1i\Header Text' file.txt
```

**Append (`a`)**:

```bash
sed '/pattern/a\text to append' inputfile
```

##### Transformation

Transform characters using the `y` command, similar to `tr`.

**Syntax:**

```bash
sed 'y/source/destination/' inputfile
```

**Example: Convert lowercase to uppercase:**

```bash
sed 'y/abcdefghijklmnopqrstuvwxyz/ABCDEFGHIJKLMNOPQRSTUVWXYZ/' file.txt
```

### Advanced `sed` Techniques

##### Regular Expressions in `sed`

`sed` supports regular expressions for pattern matching.

**Metacharacters:**

- `.` : Matches any single character.
- `*` : Matches zero or more occurrences of the preceding character.
- `[]`: Character class; matches any one character inside the brackets.
- `^` : Matches the start of a line.
- `$` : Matches the end of a line.
- `\` : Escapes a metacharacter.

**Example: Replace lines starting with 'Error':**

```bash
sed '/^Error/s/^Error/Warning/' logs.txt
```

##### Addressing

Specify lines to apply commands to using line numbers or patterns.

**Syntax:**

```bash
sed 'address command' inputfile
```

**Address Types:**

- **Single Line**: `sed '5d' file.txt` deletes line 5.
- **Line Range**: `sed '2,4d' file.txt` deletes lines 2 to 4.
- **Pattern Range**: `sed '/start/,/end/d' file.txt` deletes from 'start' to 'end'.

##### Holding Space

`sed` has a pattern space and a hold space for complex text manipulations.

**Example: Swap adjacent lines:**

```bash
sed 'N; s/\(.*\)\n\(.*\)/\2\n\1/' file.txt
```

**Explanation:**

- `N` reads the next line into the pattern space.
- The `s` command swaps the two lines.

#### Practical Examples and Use Cases

I. Replace All Occurrences of a String:

```bash
sed 's/old/new/g' file.txt
```

II. Delete Lines Containing a Pattern:

```bash
sed '/unwanted_pattern/d' file.txt
```

III. Insert Text After a Line Matching a Pattern:

```bash
sed '/pattern/a\New line of text' file.txt
```

IV. Edit Files In-Place with Backup:

```bash
sed -i.bak 's/foo/bar/g' file.txt
```

`-i.bak` edits the file in-place and creates a backup with `.bak` extension.

V. Change Delimiters in CSV Files:

```bash
sed 's/,/|/g' data.csv > data.psv
```

Converts comma-separated values to pipe-separated values.

#### Tips and Best Practices

- Enclose scripts in single quotes to prevent shell interpretation.
- Use backslashes to escape characters like `/`, `&`, and `\`.
- Use without `-i` to test commands before modifying files in-place.
- With `-E` (or `sed -r` in GNU `sed`), you can use extended regex syntax.

**Example:**

```bash
sed -E 's/([0-9]{3})-([0-9]{2})-([0-9]{4})/XXX-XX-\3/' ssn.txt
```

### Awk

Developed in the 1970s by Alfred Aho, Peter Weinberger, and Brian Kernighan at Bell Labs (hence the name `awk`), `awk` is a powerful text-processing language. It is designed for data extraction and reporting, offering a programming language with C-like syntax and features.

Main idea:

- Treats each line as a record and fields separated by delimiters.
- Executes actions based on pattern matches.
- Supports variables, arrays, and control flow statements.
- Provides functions for string manipulation, arithmetic, and more.
- Allows user-defined functions.

#### Syntax

The basic syntax of `awk` is:

```bash
awk 'PATTERN { ACTION }' INPUTFILE
```

- The **PATTERN** represents a regular expression or condition that `awk` uses to identify matching lines or data segments within the input.
- The **ACTION** includes the commands that `awk` executes whenever it finds a match for the specified pattern, determining how matching data is processed.
- The **INPUTFILE** is the file that `awk` processes, allowing it to apply the pattern and action rules across the contents of the specified file.

#### How `awk` Works

```
User
 |
 | Uses 'awk' with a program and input file(s)
 v
+-------------------------------+
| awk Command                   |
|  - Reads Input Line by Line   |
|  - Splits Line into Fields    |
|  - Applies Pattern and Action |
+-------------------------------+
 |
 | Outputs to Terminal or File
 v
```

`awk` reads the input file line by line, splits each line into fields based on a delimiter (default is whitespace), and then executes the specified actions on lines matching the pattern.

#### Common Operations with `awk`

##### Field and Record Processing

- **Fields**: Accessed using `$1`, `$2`, ..., `$NF` (number of fields).
- **Records**: Each line is a record, accessed using `NR` (record number).

**Example: Print the first and third fields:**

```bash
awk '{ print $1, $3 }' data.txt
```

##### Patterns and Actions

Execute actions only on lines matching a pattern.

**Example: Print lines where the second field equals 'Error':**

```bash
awk '$2 == "Error" { print }' logs.txt
```

##### Variables and Operators

`awk` supports arithmetic and string operations.

**Example: Sum values in the third field:**

```bash
awk '{ sum += $3 } END { print "Total:", sum }' data.txt
```

#### Advanced `awk` Techniques

##### Control Structures

`awk` supports `if`, `while`, `for`, and other control structures.

**Example: Conditional Processing**

```bash
awk '{
  if ($3 > 100) {
    print $1, $2, "High"
  } else {
    print $1, $2, "Low"
  }
}' data.txt
```

##### Built-in Functions

`awk` provides numerous built-in functions for mathematical and string operations.

**String Functions:**

- `length(str)`: Returns the length of `str`.
- `substr(str, start, length)`: Extracts substring.
- `tolower(str)`: Converts to lowercase.
- `toupper(str)`: Converts to uppercase.

**Example: Convert the second field to uppercase:**

```bash
awk '{ $2 = toupper($2); print }' data.txt
```

##### User-Defined Functions

Define custom functions for reuse.

**Example: Define a function to calculate the square:**

```bash
awk 'function square(x) { return x * x }
     { print $1, square($2) }' data.txt
```

#### Practical Examples and Use Cases

I. Calculate Average of a Column:

```bash
awk '{ total += $3; count++ } END { print "Average:", total/count }' data.txt
```

II. Filter Rows Based on Field Value:

```bash
awk '$4 >= 50 { print }' scores.txt
```

III. Reformat Output:

```bash
awk '{ printf "%-10s %-10s %5.2f\n", $1, $2, $3 }' data.txt
```

Formats output with fixed-width columns and two decimal places.

IV. Count Occurrences of Unique Values:

```bash
awk '{ count[$1]++ } END { for (word in count) print word, count[word] }' words.txt
```

V. Process Delimited Data with Custom Field Separator:

```bash
awk -F ':' '{ print $1, $3 }' /etc/passwd
```

- `:` sets the field separator to colon.
- Prints username and UID.

#### Tips and Best Practices

- Enclose scripts in single quotes to prevent shell interpretation.
- Use backslashes to escape characters like `/`, `&`, and `\`.
- Use without `-i` to test commands before modifying files in-place.
- With `-E` (or `sed -r` in GNU `sed`), you can use extended regex syntax.

**Example:**

```bash
sed -E 's/([0-9]{3})-([0-9]{2})-([0-9]{4})/XXX-XX-\3/' ssn.txt
```

- Ensure variables are initialized to avoid unexpected results.
- Use `-F` to set custom field separators.
- For actions before processing starts or after it ends.

**Example:**

```bash
awk 'BEGIN { print "Start Processing" } { print $0 } END { print "End Processing" }' file.txt
```

### Challenges

1. Examine the core differences between `sed` and `awk`. What are their primary functionalities? How do their capabilities differ when it comes to handling text streams and structured data?
2. Describe the sequence of operations that `sed` performs on a text stream. What is the role of pattern space in `sed`?
3. `awk` uses whitespace as a delimiter by default to separate columns in a line. Explain the steps to modify this default setting to use a different delimiter. For instance, how would you instruct `awk` to recognize a comma `,` or a colon `:` as a delimiter instead?
4. Demonstrate with an example how you would extract data from multiple columns in `awk`. How does the syntax differ when you want to retrieve data from the first, third, and fifth columns simultaneously as opposed to extracting them one at a time?
5. How do you filter lines in `awk` where a particular column does not match a given pattern? Explain and provide an example illustrating this use case.
6. Explain how `awk` can be used to perform data aggregation tasks. For instance, if you have a file with several rows of data, how would you use `awk` to compute the sum of values in a specific column? Provide an example to illustrate your explanation.
