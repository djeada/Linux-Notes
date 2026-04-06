## Command-Line Stream Editors

`sed` (Stream Editor) and `awk` are powerful command-line utilities that originated from Unix and have become indispensable tools in Unix-like operating systems, including Linux and macOS. They are designed for processing and transforming text, allowing users to perform complex text manipulations with simple commands. 

### `sed`

`sed` is a **stream editor** used to transform text from files or pipelines without opening an interactive editor.

It works **line by line**:

1. read a line
2. apply the command(s)
3. print the result

This makes it fast and useful for automation, scripting, filtering, and bulk text edits.

Originally developed in the 1970s at Bell Labs by **Lee E. McMahon**, `sed` is one of the standard Unix text-processing tools.

#### Basic syntax

`sed` takes a set of options, a script describing the edits to perform, and one or more input sources. It processes the input line by line, applies the script, and prints the result (unless told otherwise).

```bash
sed [OPTIONS] 'SCRIPT' file...
```

* **`OPTIONS`** change how `sed` behaves
* **`SCRIPT`** contains the editing command(s)
* **`file...`** is one or more input files

If no file is given, `sed` reads from **standard input**.

#### Mental model

`sed` works as a simple pipeline: it reads one line at a time, applies the given commands, and outputs the result. Each line is processed independently unless you explicitly use multi-line features.

```text
input -> sed reads one line -> applies commands -> prints result
```

By default, `sed` does **not** modify the original file. It prints the transformed output to the terminal.

#### Common options

These options control how `sed` reads input, applies commands, and produces output. You’ll mainly use them to suppress default behavior, combine scripts, or modify files directly.

| Option          | Meaning                                |
| --------------- | -------------------------------------- |
| `-n`            | Suppress automatic printing            |
| `-e 'script'`   | Add a script/command                   |
| `-f script.sed` | Read commands from a script file       |
| `-i`            | Edit file in place                     |
| `-i.bak`        | Edit file in place and create a backup |
| `-E`            | Use extended regular expressions       |

#### Command structure

A `sed` script often looks like this:

```bash
sed 'address command' file
```

* **address** decides **where** the command applies
* **command** decides **what** to do

Example:

```bash
sed '5d' file.txt
```

Delete line 5.

#### Addresses

Addresses tell `sed` **which lines** a command should apply to. They can target specific line numbers, ranges, or patterns, making it easy to operate on only part of the input.

| Address         | Meaning                    | Example                         |
| --------------- | -------------------------- | ------------------------------- |
| `5`             | line 5 only                | `sed '5d' file.txt`             |
| `2,4`           | lines 2 through 4          | `sed '2,4d' file.txt`           |
| `/pattern/`     | lines matching a pattern   | `sed '/error/d' log.txt`        |
| `/start/,/end/` | range between two patterns | `sed '/start/,/end/d' file.txt` |
| `$`             | last line                  | `sed '$d' file.txt`             |

#### Operations and flags

This table combines the most useful commands and the most common substitution flags in one place.

| Form          | What it does                          | Notes / Example                               |
| ------------- | ------------------------------------- | --------------------------------------------- |
| `s/old/new/`  | Replace first match on a line         | `sed 's/apple/orange/' file.txt`              |
| `s/old/new/g` | Replace all matches on a line         | `sed 's/apple/orange/g' file.txt`             |
| `s/old/new/i` | Case-insensitive match                | GNU `sed` commonly supports this              |
| `s/old/new/p` | Print line if substitution happened   | Usually paired with `-n`                      |
| `d`           | Delete line                           | `sed '/^$/d' file.txt` removes empty lines    |
| `p`           | Print line                            | `sed -n '/error/p' log.txt`                   |
| `i\text`      | Insert text before line               | `sed '1i\Header' file.txt`                    |
| `a\text`      | Append text after line                | `sed '/pattern/a\extra line' file.txt`        |
| `c\text`      | Change matched line(s) to new text    | Replaces the whole addressed line             |
| `y/abc/ABC/`  | Translate characters                  | Like `tr`; character-by-character replacement |
| `q`           | Quit early                            | Useful when you only need first match/range   |
| `n`           | Read next line                        | Often used in advanced scripts                |
| `N`           | Append next line to pattern space     | Useful for multi-line processing              |
| `h`           | Copy pattern space to hold space      | Advanced use                                  |
| `H`           | Append pattern space to hold space    | Advanced use                                  |
| `g`           | Copy hold space back to pattern space | Advanced use                                  |
| `G`           | Append hold space to pattern space    | Advanced use                                  |
| `x`           | Swap pattern and hold space           | Advanced use                                  |

Example:

```bash
sed '/^$/d' file.txt
```

* `^$` matches an empty line
* `d` deletes it

So this removes all empty lines.

#### Substitution command

The most common `sed` command is substitution:

```bash
sed 's/pattern/replacement/flags' file
```

* **`s`** = substitute
* **`pattern`** = text or regex to search for
* **`replacement`** = replacement text
* **`flags`** = optional modifiers

Common substitution flags:

| Flag | Meaning                            |
| ---- | ---------------------------------- |
| `g`  | replace all matches in the line    |
| `p`  | print line if replacement happened |
| `i`  | case-insensitive matching          |

Example:

```bash
sed 's/apple/orange/g' fruits.txt
```

Replace every `apple` with `orange`.

#### Regular expressions

`sed` supports regular expressions for matching text.

| Symbol    | Meaning                            |
| --------- | ---------------------------------- |
| `.`       | any single character               |
| `*`       | zero or more of previous character |
| `[]`      | character class                    |
| `^`       | start of line                      |
| `$`       | end of line                        |
| `\`       | escape special character           |
| `\(` `\)` | capture group in basic regex       |
| `\{m,n\}` | repetition in basic regex          |

Example:

```bash
sed '/^Error/s/^Error/Warning/' logs.txt
```

For lines starting with `Error`, replace that beginning with `Warning`.

#### Extended regex

With `-E`, patterns are easier to read because you usually do not need escaped grouping and repetition syntax.

```bash
sed -E 's/([0-9]{3})-([0-9]{2})-([0-9]{4})/XXX-XX-\3/' ssn.txt
```

This masks the first five digits of an SSN-like pattern.

#### Common examples

These are typical `sed` one-liners for replacing text, filtering lines, and making simple edits to files or streams.

**Replace first match on each line**

```bash id="x4j2k8"
sed 's/old/new/' file.txt
```

**Replace all matches**

```bash id="r7m1qp"
sed 's/old/new/g' file.txt
```

**Delete lines containing a word**

```bash id="h9t3zn"
sed '/unwanted/d' file.txt
```

**Delete empty lines**

```bash id="k2v8sx"
sed '/^$/d' file.txt
```

**Print only matching lines**

```bash id="p5c1df"
sed -n '/error/p' log.txt
```

**Insert a line before line 1**

```bash id="z8q4lm"
sed '1i\Header Text' file.txt
```

**Append text after matching lines**

```bash id="w6n2ba"
sed '/pattern/a\New line of text' file.txt
```

**Edit file in place with backup**

```bash id="t3y7ke"
sed -i.bak 's/foo/bar/g' file.txt
```

This modifies `file.txt` and keeps a backup as `file.txt.bak`.

**Convert commas to pipes**

```bash id="m1x9rv"
sed 's/,/|/g' data.csv > data.psv
```

#### Multi-line and hold space

`sed` normally works on one line at a time, but it also has:
 Editor) and awk are powerful command-line utilities that originated from Unix and have become indispensable tools in Unix-like operating systems, including Linux and macOS. They are designed for processing and transforming text, allowing users to perform complex text manipulations with simple commands. This guide provides a comprehensive overview of both utilities, including their history, usage, syntax, options, and practical examples.

* **pattern space** = current working text
* **hold space** = temporary storage

Example: swap adjacent lines

```bash
sed 'N; s/\(.*\)\n\(.*\)/\2\n\1/' file.txt
```

* `N` reads the next line into the pattern space
* now two lines are available together
* the substitution swaps them

This is more advanced, but useful for multi-line edits.

#### Practical tips

* Put scripts in **single quotes** to avoid shell interference
* Test without `-i` first
* Use `-i.bak` when editing files directly
* Use `-E` when regex becomes hard to read
* Escape `/`, `&`, and `\` when needed

Example with another delimiter:

```bash
sed 's|/usr/local|/opt/tools|g' file.txt
```

Using `|` instead of `/` makes path replacements easier to read.

Here’s the same treatment for **`awk`**: cleaner structure, flatter explanations, more readable, with **one main table** covering fields, variables, operators, blocks, and common functions.

### `awk`

`awk` is a **text-processing language** designed for extracting, filtering, calculating, and formatting data.

It is especially useful when your input is structured into **lines** and **fields**.

`awk` was developed at Bell Labs in the 1970s by **Alfred Aho, Peter Weinberger, and Brian Kernighan**. The name comes from their surnames: **A-W-K**.

#### Main idea

`awk` treats input like a table:

* each **line** is a **record**
* each record is split into **fields**
* you write **patterns** to choose lines
* you write **actions** to say what to do with them

```
                INPUT FILE (text data)
        -------------------------------------
        line 1: field1 field2 field3 ...
        line 2: field1 field2 field3 ...
        line 3: field1 field2 field3 ...
        -------------------------------------
                     │
                     ▼
            awk reads line by line
            (each line = RECORD)
                     │
                     ▼
        -------------------------------------
        RECORD (line)
        ┌───────────────┬────────┬────────┐
        │   field1      │ field2 │ field3 │
        └───────────────┴────────┴────────┘
           $1              $2        $3
        -------------------------------------
                     │
                     ▼
        ┌─────────────────────────────────┐
        │        PATTERN (condition)      │
        │   e.g. $2 > 10 or /error/      │
        └─────────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
       MATCH                 NO MATCH
          │                     │
          ▼                     ▼
┌───────────────────┐     (skip record)
│   ACTION          │
│ { print $1, $3 }  │
│ { sum += $2 }     │
└───────────────────┘
          │
          ▼
     OUTPUT RESULT
```

This makes `awk` very good for:

* selecting rows
* printing columns
* filtering by conditions
* computing sums, counts, and averages
* reformatting output

#### Basic syntax

```bash
awk 'PATTERN { ACTION }' file
```

### Parts

* **`PATTERN`** decides which lines to match
* **`ACTION`** says what to do for matching lines
* **`file`** is the input file

If you omit the pattern, the action runs on **every line**.
If you omit the action, `awk` prints the matching line by default.

#### Common options

These options control how `awk` reads input, initializes variables, and loads programs. They are commonly used when working with structured data or larger scripts.

| Option          | Meaning                                      |
| --------------- | -------------------------------------------- |
| `-F ':'`        | Set input field separator                    |
| `-v var=value`  | Set an awk variable before processing starts |
| `-f script.awk` | Read program from a file                     |

#### Main building blocks

This table gives the most useful `awk` pieces in one place.

| Form               | Meaning                            | Example                                   |
| ------------------ | ---------------------------------- | ----------------------------------------- |
| `$1`, `$2`, ...    | field 1, field 2, etc.             | `awk '{ print $1, $3 }' file`             |
| `$0`               | entire current line                | `awk '{ print $0 }' file`                 |
| `NF`               | number of fields in current line   | `awk '{ print NF }' file`                 |
| `NR`               | current record number              | `awk '{ print NR, $0 }' file`             |
| `BEGIN { ... }`    | run before input is read           | initialize variables, print header        |
| `END { ... }`      | run after all input is processed   | print totals, summaries                   |
| `pattern { ... }`  | run action only if pattern matches | `awk '$2=="Error" { print }' log.txt`     |
| `/regex/ { ... }`  | match lines by regular expression  | `awk '/error/ { print }' file`            |
| `condition`        | logical condition                  | `awk '$3 > 100' file`                     |
| `print`            | print output with separators       | `awk '{ print $1, $2 }' file`             |
| `printf`           | formatted output                   | `awk '{ printf "%s %d\n", $1, $2 }' file` |
| `sum += $3`        | numeric accumulation               | used for totals                           |
| `count[$1]++`      | associative array counter          | count repeated values                     |
| `if (...)`         | conditional logic                  | choose between outputs                    |
| `for (...)`        | loop                               | iterate through arrays or counters        |
| `function name(x)` | user-defined function              | reusable logic                            |

#### What `$1`, `$0`, `NR`, and `NF` mean

These are the most important `awk` variables:

| Variable | Meaning                          |
| -------- | -------------------------------- |
| `$0`     | whole current line               |
| `$1`     | first field                      |
| `$2`     | second field                     |
| `$NF`    | last field                       |
| `NR`     | current line number              |
| `NF`     | number of fields in current line |

Example:

```bash
awk '{ print $1, $3 }' data.txt
```

Print the first and third fields from each line.

#### Patterns and actions

The usual shape of an `awk` command is:

```bash
awk 'pattern { action }' file
```

Example:

```bash
awk '$2 == "Error" { print }' logs.txt
```

* `$2 == "Error"` = match lines where field 2 is `Error`
* `{ print }` = print those lines

#### Field separators

By default, `awk` splits fields on spaces and tabs.

To use a different separator, use **`-F`**.

Example:

```bash
awk -F ':' '{ print $1, $3 }' /etc/passwd
```

* `-F ':'` = fields are separated by `:`
* `$1` = first field
* `$3` = third field

#### Common operators and tests

These operators are used in `awk` patterns and conditions to compare values, combine logic, and match text using regular expressions.

| Form | Meaning               |   |            |
| ---- | --------------------- | - | ---------- |
| `==` | equal to              |   |            |
| `!=` | not equal to          |   |            |
| `>`  | greater than          |   |            |
| `<`  | less than             |   |            |
| `>=` | greater than or equal |   |            |
| `<=` | less than or equal    |   |            |
| `&&` | logical AND           |   |            |
| `    |                       | ` | logical OR |
| `!`  | logical NOT           |   |            |
| `~`  | matches regex         |   |            |
| `!~` | does not match regex  |   |            |

Example:

```bash
awk '$3 > 100 { print $1, $3 }' data.txt
```

Print fields 1 and 3 only when field 3 is greater than 100.

#### `BEGIN` and `END`

These are special blocks.

| Block           | When it runs         | Common use                 |
| --------------- | -------------------- | -------------------------- |
| `BEGIN { ... }` | before reading input | setup, headers, variables  |
| `END { ... }`   | after all input      | totals, summaries, cleanup |

Example:

```bash
awk 'BEGIN { print "Start" } { print $0 } END { print "Done" }' file.txt
```

#### Common functions and features

These built-in functions cover the most common string manipulation, text replacement, and numeric operations in `awk`. They are frequently used for data cleaning and transformation.

| Form                      | Meaning                 | Example            |
| ------------------------- | ----------------------- | ------------------ |
| `length(str)`             | length of a string      | `length($1)`       |
| `substr(str, start, len)` | substring               | `substr($1,1,3)`   |
| `tolower(str)`            | lowercase conversion    | `tolower($2)`      |
| `toupper(str)`            | uppercase conversion    | `toupper($2)`      |
| `split(str, arr, sep)`    | split string into array | advanced use       |
| `gsub(r, s, str)`         | replace all matches     | text cleanup       |
| `sub(r, s, str)`          | replace first match     | text cleanup       |
| `int(x)`                  | integer part            | numeric processing |
| `sqrt(x)`                 | square root             | math               |
| `rand()`                  | random number           | math/scripts       |

#### `print` vs `printf`

`awk` provides two main ways to produce output: `print` for simple cases and `printf` for precise formatting.

**`print`**

Simple output with automatic spacing and a newline at the end:

```bash
awk '{ print $1, $2 }' file.txt
```

* separates fields with a space (default `OFS`)
* automatically adds a newline

**`printf`**

Formatted output with full control over layout:

```bash
awk '{ printf "%-10s %-10s %5.2f\n", $1, $2, $3 }' data.txt
```

* no automatic newline (must use `\n`)
* supports formatting (width, alignment, decimals)
* ideal for aligned columns and numeric output

#### Common examples

These are typical one-liners that cover the most common `awk` use cases: selecting fields, filtering rows, and doing simple calculations.

**Print specific columns**

```bash id="v3f4xl"
awk '{ print $1, $3 }' data.txt
```

**Print lines matching a condition**

```bash id="c6t9z2"
awk '$2 == "Error" { print }' logs.txt
```

**Sum a column**

```bash id="0g8m8c"
awk '{ sum += $3 } END { print "Total:", sum }' data.txt
```

**Compute an average**

```bash id="v1y3d7"
awk '{ total += $3; count++ } END { print "Average:", total/count }' data.txt
```

**Filter rows by numeric value**

```bash id="9q1l5r"
awk '$4 >= 50 { print }' scores.txt
```

**Convert a field to uppercase**

```bash id="2g6p1n"
awk '{ $2 = toupper($2); print }' data.txt
```

**Count repeated values**

```bash id="5d7w9k"
awk '{ count[$1]++ } END { for (word in count) print word, count[word] }' words.txt
```

**Print line number with content**

```bash id="p3k8u2"
awk '{ print NR, $0 }' file.txt
```

**Use a custom field separator**

```bash id="x8n2c4"
awk -F ':' '{ print $1, $3 }' /etc/passwd
```

#### Control structures

`awk` includes basic programming constructs like conditionals and loops, allowing you to apply more complex logic during text processing.

**`if`**

Use `if` to conditionally execute code based on field values or expressions:

```bash id="v0pf5l"
awk '{
  if ($3 > 100) {
    print $1, $2, "High"
  } else {
    print $1, $2, "Low"
  }
}' data.txt
```

**`for`**

Often used with arrays to iterate over collected values:

```bash id="m6hj4y"
awk '{ count[$1]++ } END { for (x in count) print x, count[x] }' file.txt
```

* loops over all keys in the `count` array
* commonly used for counting and aggregating data

#### Arrays

`awk` arrays are **associative arrays**, which means keys can be strings.

Example:

```bash
awk '{ count[$1]++ } END { for (k in count) print k, count[k] }' words.txt
```

This counts how many times each first-field value appears.

#### User-defined functions

You can define reusable functions.

Example:

```bash
awk 'function square(x) { return x * x }
     { print $1, square($2) }' data.txt
```

This prints field 1 and the square of field 2.

#### Practical tips

* Use **single quotes** around the awk program
* Use **`-F`** when the input is not whitespace-separated
* Use **`BEGIN`** for setup and **`END`** for summaries
* Prefer `print` for simple output and `printf` for formatted output
* Remember that numeric calculations often need counters to avoid divide-by-zero mistakes

#### Quick reference

| Goal                | Command pattern                                             |
| ------------------- | ----------------------------------------------------------- |
| print whole line    | `awk '{ print $0 }' file`                                   |
| print first column  | `awk '{ print $1 }' file`                                   |
| filter by condition | `awk '$3 > 10' file`                                        |
| filter by regex     | `awk '/error/' file`                                        |
| sum a column        | `awk '{ s += $2 } END { print s }' file`                    |
| average a column    | `awk '{ s += $2; n++ } END { print s/n }' file`             |
| count values        | `awk '{ c[$1]++ } END { for (k in c) print k, c[k] }' file` |
| custom delimiter    | `awk -F ':' '{ print $1 }' file`                            |
| formatted output    | `awk '{ printf "%s %d\n", $1, $2 }' file`                   |

### Challenges

1. Research and describe the core differences between `sed` and `awk`, focusing on their primary functionalities. Compare how each tool handles text streams and structured data, and discuss when it might be more appropriate to use `sed` versus `awk`.
2. Describe the sequence of operations `sed` performs on a text stream, including how it reads input, processes it in the pattern space, and outputs results. Explain the purpose of the pattern space and how `sed` uses it to manage the text transformations on each line.
3. By default, `awk` uses whitespace as a delimiter to separate columns. Explain how to modify this default setting to use other delimiters, such as a comma (`,`) or a colon (`:`). Provide examples demonstrating how to set these delimiters with the `-F` option in `awk`.
4. Demonstrate how to extract data from multiple columns in `awk` with a specific example. Show how to retrieve data from the first, third, and fifth columns simultaneously, and explain how this syntax differs from extracting each column individually.
5. Use `awk` to filter lines where a particular column does not match a specific pattern. Provide an example that demonstrates this process, such as displaying lines from a file where the second column does not contain the word "error."
6. Explain how `awk` can perform data aggregation tasks, such as calculating the sum of values in a specific column. Provide an example of using `awk` to read a file with multiple rows of numeric data and compute the sum of all values in a given column.
7. Show how to use `sed` to replace all occurrences of a word in a text file with another word. Demonstrate how `sed` can be used both to perform a global replacement within each line and to limit replacements to the first occurrence of the word on each line.
8. Explain how to use `awk` to format and print data in a specific way. For instance, given a file with names and scores, demonstrate how you could use `awk` to print the names and scores in a formatted table with aligned columns.
9. Use `sed` to delete lines containing a specific pattern from a text file. Describe the command you used and explain how `sed` processes the file to selectively remove lines based on pattern matching.
10. Combine `sed` and `awk` in a pipeline to perform more complex text transformations. For example, use `sed` to remove blank lines from a file, and then use `awk` to calculate the average of numeric values in a specific column. Explain how combining these tools in a pipeline can solve more advanced text processing tasks.
