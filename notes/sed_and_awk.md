<h1>sed</h1>

Trim leading whitespaces and tabulations:

```bash
sed 's/^[ \t]*//' file_name.txt
```

Delete all blank lines:

```bash
sed '/^$/d' file_name.txt
```

Replace all occurences of old_string with new_strings in every file in current directory and it's subdirectories.

```bash
find . -type f -exec sed -i -e "s/old_string/new_string/g" {} \;
```

Delete anything following and including a line that contains special_string:

```bash
sed -n '/special_string/,$!p' file_name.txt
```

Convert all letters in a directory's text files to uppercase:

```bash
sed -i 's/.*/\U&/' *
```

<h1>awk</h1>

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
