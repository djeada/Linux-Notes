<h1>Sed</h1>

<i>sed</i> is a command-line stream editor.
Wherever there are patterns in the text that you wish to replace, use <i>sed</i> .
<i>sed</i> deals with character streams on a per-line basis.
It uses a basic programming language with goto-style loops and simple conditionals (in addition to pattern matching and address matching).
There are just two "variables" in this case: pattern space and hold space.
Bare in mind that sed scripts might be tough to read.

Trim leading whitespaces and tabulations:

```bash
sed 's/^[ \t]*//' file_name.txt
```

Delete all blank lines:

```bash
sed '/^$/d' file_name.txt
```

Convert all letters in a directory's text files to uppercase:

```bash
sed -i 's/.*/\U&/' *
```

Delete anything following and including a line that contains special_string:

```bash
sed -n '/special_string/,$!p' file_name.txt
```

Replace all occurences of old_string with new_strings in every file in current directory and it's subdirectories.

```bash
find . -type f -exec sed -i -e "s/old_string/new_string/g" {} \;
```

<h1>AWK</h1>
On a per-line level, <i>awk</i> is geared toward delimited fields.
Use <i>awk</i> when the text resembles rows and columns, or "records" and "fields," as <i>awk</i> calls them.
When compared to <i>sed</i>, it uses far more robust programming constructs like if/else, while, do/while and for loops.
Variables and single-dimension associative arrays are fully supported, as are multi-dimension arrays.
Mathematical operations are similar to those used in the C programming language.


Extract fields 1, 5, and 3:

```bash
awk '{print $1,$5,$3}' file_name.txt
```

Each line when the third field equals ‘xxx' should be printed:

```bash
awk '$3 == "xxx"' file_name.txt
```

Each line when the third field does not equal ‘xxx' should be printed:

```bash
awk '$3 != "xxx"' file_name.txt
```

Each line whose 7th field matches the regex should be displayed:

```bash
awk '$7  ~ /^[a-d].[xyz]/' file_name.txt
```

Each line whose 7th field does not match the regex should be displayed:

```bash
awk '$7 !~ /^[a-d].[xyz]/' file_name.txt
```

Display lines with unique values in third column:

```bash
awk '!arr[$3]++' file_name.txt
```
Lines where the value in column 2 is greater than in column 1 should be displayed:

```bash
awk '$2>$1' file_name.txt
```

Sum the values from column 7:

```bash
awk '{sum+=$7} END {print sum}' file_name.txt
```
