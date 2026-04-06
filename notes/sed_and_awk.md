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

* `5` selects line 5
* `d` deletes that line
* all other lines are printed normally

This is useful when you know the exact line number you want to remove.

**Before — `file.txt`**

```txt
line one
line two
line three
line four
line five
line six
line seven
```

**After**

```txt
line one
line two
line three
line four
line six
line seven
```

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

* `s/.../.../` is the substitution command
* `apple` is the text to search for
* `orange` is the replacement text
* `g` means replace all matches on each line, not just the first one

This is useful when the same word may appear multiple times in a line and you want to replace every occurrence.

**Before — `fruits.txt`**

```txt
apple pie
green apple and red apple
pineapple apple
banana grape
```

**After**

```txt
orange pie
green orange and red orange
pineorange orange
banana grape
```

Notice that `sed` replaces the text wherever it appears, so `pineapple` becomes `pineorange` too.

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

* `/^Error/` limits the substitution to lines that start with `Error`
* `s/^Error/Warning/` replaces `Error` only at the beginning of the line
* lines that do not start with `Error` are left unchanged

This is useful when you want to change only leading status words without affecting the same word later in the line.

**Before — `logs.txt`**

```txt
Error disk full on /dev/sda1
Info service started
Error timeout while connecting
Warning retry scheduled
Critical Error in module loader
```

**After**

```txt
Warning disk full on /dev/sda1
Info service started
Warning timeout while connecting
Warning retry scheduled
Critical Error in module loader
```

Notice:

* `Error disk full on /dev/sda1` changed because the line starts with `Error`
* `Critical Error in module loader` did not change because `Error` is not at the start of the line

#### Extended regex

With `-E`, patterns are easier to read because you usually do not need escaped grouping and repetition syntax.
```bash
sed -E 's/([0-9]{3})-([0-9]{2})-([0-9]{4})/XXX-XX-\3/' ssn.txt
```

* `-E` enables extended regular expressions
* `([0-9]{3})` matches the first 3 digits
* `([0-9]{2})` matches the next 2 digits
* `([0-9]{4})` matches the last 4 digits
* `\3` reuses only the 3rd captured group
* the replacement changes the first five digits to `XXX-XX-`

This is useful when you want to hide sensitive data while keeping the last 4 digits visible.

**Before — `ssn.txt`**

```txt
Alice 123-45-6789
Bob 987-65-4321
Cara 555-11-2222
NoSSN here
```

**After**

```txt
Alice XXX-XX-6789
Bob XXX-XX-4321
Cara XXX-XX-2222
NoSSN here
```

Only text matching the `123-45-6789` style pattern is changed. Lines without that pattern stay the same.

#### Common examples

These are typical `sed` one-liners for replacing text, filtering lines, and making simple edits to files or streams. Each example below shows what the input file might look like before running the command, and what the output would look like after.

**Replace first match on each line**

```bash
sed 's/old/new/' file.txt
```

Replaces only the first occurrence of `old` on each line.

**Before — `file.txt`**

```txt
old value here
this old item has old twice
nothing to change
old old old
```

**After**

```txt
new value here
this new item has old twice
nothing to change
new old old
```

**Replace all matches**

```bash
sed 's/old/new/g' file.txt
```

Replaces every occurrence of `old` on each line. The `g` flag means “global” for that line.

**Before — `file.txt`**

```txt
old value here
this old item has old twice
nothing to change
old old old
```

**After**

```txt
new value here
this new item has new twice
nothing to change
new new new
```

**Delete lines containing a word**

```bash
sed '/unwanted/d' file.txt
```

Deletes every line that contains the text `unwanted`.

**Before — `file.txt`**

```txt
keep this line
this line is unwanted
another good line
unwanted content appears here too
final line
```

**After**

```txt
keep this line
another good line
final line
```

**Delete empty lines**

```bash
sed '/^$/d' file.txt
```

Deletes blank lines. `^$` matches lines that begin and end immediately, with nothing in between.

**Before — `file.txt`**

```txt
alpha

beta


gamma
delta
```

**After**

```txt
alpha
beta
gamma
delta
```

**Print only matching lines**

```bash
sed -n '/error/p' log.txt
```

Prints only lines containing `error`. The `-n` option suppresses normal output, and `p` prints only matched lines.

**Before — `log.txt`**

```txt
info: service started
warning: low memory
error: failed to connect
info: retrying
error: timeout reached
```

**After**

```txt
error: failed to connect
error: timeout reached
```

**Insert a line before line 1**

```bash
sed '1i\Header Text' file.txt
```

Inserts `Header Text` before the first line of the file.

**Before — `file.txt`**

```txt
apple
banana
cherry
```

**After**

```txt
Header Text
apple
banana
cherry
```

**Append text after matching lines**

```bash
sed '/pattern/a\New line of text' file.txt
```

Adds a new line immediately after every line that matches `pattern`.

**Before — `file.txt`**

```txt
start section
pattern found here
middle line
pattern appears again
end section
```

**After**

```txt
start section
pattern found here
New line of text
middle line
pattern appears again
New line of text
end section
```

**Edit file in place with backup**

```bash
sed -i.bak 's/foo/bar/g' file.txt
```

Modifies `file.txt` directly and saves the original file as `file.txt.bak`.

**Before — `file.txt`**

```txt
foo is here
foo and foo again
no match here
```

**After — `file.txt`**

```txt
bar is here
bar and bar again
no match here
```

**Backup — `file.txt.bak`**

```txt
foo is here
foo and foo again
no match here
```

This is useful when you want to change a file directly but still keep a copy of the original.

**Convert commas to pipes**

```bash
sed 's/,/|/g' data.csv > data.psv
```

Replaces all commas with pipe characters and writes the result to a new file.

**Before — `data.csv`**

```txt
name,age,city
Alice,29,Berlin
Bob,34,Paris
Cara,41,Rome
```

**After — `data.psv`**

```txt
name|age|city
Alice|29|Berlin
Bob|34|Paris
Cara|41|Rome
```

This is a simple way to convert comma-separated data into pipe-separated data without changing the original file.

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

**Before — `file.txt`**

```txt
first line
second line
third line
fourth line
fifth line
sixth line
```

**After**

```txt
second line
first line
fourth line
third line
sixth line
fifth line
```

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
        │   e.g. $2 > 10 or /error/       │
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

`awk` programs are built from simple **pattern → action** rules: for each line of input, it checks the pattern and runs the action if it matches.

```bash
awk 'PATTERN { ACTION }' file
```

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

Useful for extracting only the columns you need from plain text data.

**Before — `data.txt`**

```txt
Alice Sales 5400 Berlin
Bob HR 4200 Paris
Cara IT 6100 Rome
Dina Finance 5800 Madrid
```

**After**

```txt
Alice 5400
Bob 4200
Cara 6100
Dina 5800
```

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

Useful for filtering log files or structured text by status, level, or category.

**Before — `logs.txt`**

```txt
2026-04-01 Info Started
2026-04-01 Error DiskFull
2026-04-02 Warning Retry
2026-04-02 Error Timeout
2026-04-03 Info Recovered
```

**After**

```txt
2026-04-01 Error DiskFull
2026-04-02 Error Timeout
```

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

**Before — sample `/etc/passwd` content**

```txt
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```

**After**

```txt
root 0
daemon 1
nobody 65534
```

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

**Before — `data.txt`**

```txt
apple red 80
banana yellow 120
grape purple 140
melon green 95
orange orange 101
```

**After**

```txt
banana 120
grape 140
orange 101
```

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

**Before — `file.txt`**

```txt
alpha
beta
gamma
```

**After**

```txt
Start
alpha
beta
gamma
Done
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

Prints the 1st and 2nd fields from each line, separated by a space.

**Before — `file.txt`**

```txt
Alice Sales Berlin
Bob HR Paris
Cara IT Rome
```

**After**

```txt
Alice Sales
Bob HR
Cara IT
```

**`printf`**

Formatted output with full control over layout:

```bash
awk '{ printf "%-10s %-10s %5.2f\n", $1, $2, $3 }' data.txt
```

* no automatic newline (must use `\n`)
* supports formatting (width, alignment, decimals)
* ideal for aligned columns and numeric output

Formats the output into neat aligned columns:

* `%-10s` = left-aligned string in a 10-character field
* `%5.2f` = floating-point number with 2 decimals

**Before — `data.txt`**

```txt
Alice Sales 42.5
Bob HR 7
Cara IT 128.345
```

**After**

```txt
Alice      Sales      42.50
Bob        HR          7.00
Cara       IT        128.34
```

Note that `printf` does not add a newline automatically, so `\n` is required at the end of the format string.

#### Common examples

These are typical one-liners that cover the most common `awk` use cases: selecting fields, filtering rows, and doing simple calculations. Each example below shows sample input and the resulting output.

**Print specific columns**

```bash
awk '{ print $1, $3 }' data.txt
```

Prints the 1st and 3rd whitespace-separated fields from each line.

**Before — `data.txt`**

```txt
Alice Sales 5400 Berlin
Bob HR 4200 Paris
Cara IT 6100 Rome
```

**After**

```txt
Alice 5400
Bob 4200
Cara 6100
```

**Print lines matching a condition**

```bash
awk '$2 == "Error" { print }' logs.txt
```

Prints only lines where the 2nd field is exactly `Error`.

**Before — `logs.txt`**

```txt
2026-04-01 Info Started
2026-04-01 Error DiskFull
2026-04-02 Warning Retry
2026-04-02 Error Timeout
```

**After**

```txt
2026-04-01 Error DiskFull
2026-04-02 Error Timeout
```

**Sum a column**

```bash
awk '{ sum += $3 } END { print "Total:", sum }' data.txt
```

Adds up all values in the 3rd field and prints the total at the end.

**Before — `data.txt`**

```txt
itemA north 12
itemB south 8
itemC west 15
itemD east 10
```

**After**

```txt
Total: 45
```

**Compute an average**

```bash
awk '{ total += $3; count++ } END { print "Average:", total/count }' data.txt
```

Adds the 3rd field for every line, counts the rows, and prints the average.

**Before — `data.txt`**

```txt
itemA north 12
itemB south 8
itemC west 16
itemD east 14
```

**After**

```txt
Average: 12.5
```

**Filter rows by numeric value**

```bash
awk '$4 >= 50 { print }' scores.txt
```

Prints only rows where the 4th field is greater than or equal to `50`.

**Before — `scores.txt`**

```txt
Lina Math Midterm 48
Omar Math Midterm 77
Nia Math Midterm 50
Jules Math Midterm 39
```

**After**

```txt
Omar Math Midterm 77
Nia Math Midterm 50
```

**Convert a field to uppercase**

```bash
awk '{ $2 = toupper($2); print }' data.txt
```

Converts the 2nd field to uppercase, then prints the whole line.

**Before — `data.txt`**

```txt
100 apple red
101 banana yellow
102 grape purple
```

**After**

```txt
100 APPLE red
101 BANANA yellow
102 GRAPE purple
```

**Count repeated values**

```bash
awk '{ count[$1]++ } END { for (word in count) print word, count[word] }' words.txt
```

Counts how many times the 1st field appears.

**Before — `words.txt`**

```txt
apple
banana
apple
orange
banana
apple
```

**After**

```txt
orange 1
banana 2
apple 3
```

The output order may vary because associative arrays in `awk` are not always printed in insertion order.

**Print line number with content**

```bash
awk '{ print NR, $0 }' file.txt
```

Prints each line prefixed with its line number. `NR` is the current record number.

**Before — `file.txt`**

```txt
first task
second task
third task
```

**After**

```txt
1 first task
2 second task
3 third task
```

**Use a custom field separator**

```bash
awk -F ':' '{ print $1, $3 }' /etc/passwd
```

Uses `:` as the field separator instead of spaces, then prints the 1st and 3rd fields.

**Before — sample colon-separated file**

```txt
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```

**After**

```txt
root 0
daemon 1
nobody 65534
```

#### Control structures

`awk` includes basic programming constructs like conditionals and loops, allowing you to apply more complex logic during text processing.

**`if`**

Use `if` to conditionally execute code based on field values or expressions:

```bash
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

```bash
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
