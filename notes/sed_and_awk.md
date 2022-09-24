## Sed

`Sed` is a command-line stream editor.
Wherever there are patterns in the text that you wish to replace, use `sed`.
`Sed` deals with character streams on a per-line basis.
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

## AWK
The main advantage of `awk` is it's focus on delimited fields (text with columns).
Use `awk` when the text resembles rows and columns, or "records" and "fields," as `awk` calls them.
When compared to `sed`, it is much more advanced since it uses real programming constructs like `if/else`, `while`, `do/while` and `for` loops.
Variables and single-dimension associative arrays are also fully supported, as are multi-dimension arrays.
Available mathematical operations are similar to those used in the C programming language.

By default, *awk* uses whitespace as delimiters. In the example below *awk* will extract the first word of the sentence:

```bash
echo 'abc efg hji' | awk '{print $1}' # prints abc
```

To change the delimiter, use the `-F` flag:

```bash
echo 'abc,efg,hji' | awk -F , '{print $2}' # prints efg
```

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

Awk uses `$NF` variable to store the number of fields. We can use it to get the last column:

```bash
awk '{print $NF}' file_name.txt
```

Similarly we can get the middle column:

```bash
awk '{print $((NF/2)+1)}' file_name.txt
```
