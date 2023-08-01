## Command-Line Stream Editors

`Sed` (Stream Editor) and `Awk` are powerful command-line utilities used for manipulating text in data streams or files. Originating from Unix, they have become indispensable tools in Unix-like systems for various tasks that involve text processing.

## Sed

`Sed` stands for Stream Editor, and is a potent command-line utility for parsing and transforming text. It operates on a text input stream, either from a file or from a pipeline, applies a set of specified commands, and outputs the transformed text. Being non-interactive, `sed` shines when it comes to automating a wide range of text manipulation tasks including, but not limited to:

- Searching for specific patterns within the text
- Substitution and deletion of text
- Inserting and appending text
- Reading from and writing to files

```
User
 |
 | Uses 'sed' with arguments (script & input file)
 v
+-------------------------------+
| sed Command                   |
|  - Reads File Line by Line    |
|  - Applies Script to Each Line|
+-------------------------------+
 |
 | Outputs modified lines
 v
Terminal/Shell (or output file if specified)
```

Here are some practical examples of using `sed` to demonstrate its capabilities:

1. **Trimming Leading White Spaces**: This command eliminates spaces and tabs at the beginning of lines in a file.

```bash
sed 's/^[ \t]*//' file_name.txt
```

2. **Removing Empty Lines**: This command removes all blank lines from a file.

```bash
sed '/^$/d' file_name.txt
```

3. **Converting Text to Uppercase**: This command converts all characters in text files to uppercase. The `-i` flag allows in-place modification.

```bash
sed -i 's/.*/\U&/' file_name.txt
```

4. **Deleting Lines After a Specific Pattern**: This command deletes everything after and including a line containing a 'special_string'.

```bash
sed -n '/special_string/,$!p' file_name.txt
```

5. **Global String Replacement in Multiple Files**: This command substitutes 'old_string' with 'new_string' in every file in the current directory and its subdirectories. 

```bash
find . -type f -exec sed -i -e "s/old_string/new_string/g" {} \;
```

## AWK

`Awk` is a comprehensive command-line tool for manipulating data structured in rows and columns. It comes equipped with its own programming language featuring variables, arrays, and control structures such as `if/else`, `while`, `do/while`, and `for` loops. Additionally, `awk` supports a range of mathematical operations akin to those found in the C programming language.

Unlike `sed`, `awk` goes beyond line-oriented processing and offers more intricate programmatic constructs, including conditionals and loops. This makes it not only suitable for use directly from the command line but also incredibly powerful when used to author scripts.

Typical uses for `awk` encompass:

- Data extraction and reporting
- Text analysis
- Text transformations
- Formatting output

```
User
 |
 | Uses 'awk' with arguments (program & input file)
 v
+-------------------------------+
| awk Command                   |
|  - Reads File Line by Line    |
|  - Splits Line into Fields    |
|  - Applies Filter to Fields   |
+-------------------------------+
 |
 | Outputs results
 v
Terminal/Shell (or output file if specified)
```

`Awk` treats whitespace as a delimiter by default, but this can be modified using the `-F` flag. Let's explore some examples of `awk` usage to better understand its potential:

1. **Extracting Column Data**: This command extracts the first column of a line.

```bash
echo 'abc efg hji' | awk '{print $1}' 
```

Output: `abc`

2. **Using Custom Delimiter**: This command retrieves a column using a custom delimiter (comma in this case).

```bash
echo 'abc,efg,hji' | awk -F , '{print $2}'
```

Output: `efg`

3. **Obtaining Multiple Columns**: This command retrieves multiple columns from a file.

```bash
awk '{print $1,$5,$3}' file_name.txt
```

4. **Filtering Rows by Column Value**: This command displays lines where the third column equals 'xxx'.

```bash
awk '$3 == "xxx"' file_name.txt
```

5. **Pattern Matching**: This command reveals lines where the seventh column matches a pattern.

```bash
awk '$7 ~ /^[a-d].[xyz]/' file_name.txt
```

6. **Data Aggregation**: This command computes the sum of values from the seventh column.

```bash
awk '{sum+=$7} END {print sum}' file_name.txt
```

7. **Accessing the Last Column**: This command shows the last column of each line.

```bash
awk '{print $NF}' file_name.txt
```

## Challenges

1. Examine the core differences between `sed` and `awk`. What are their primary functionalities? How do their capabilities differ when it comes to handling text streams and structured data?
2. Describe the sequence of operations that `sed` performs on a text stream. What is the role of pattern space in `sed`?
3. `awk` uses whitespace as a delimiter by default to separate columns in a line. Explain the steps to modify this default setting to use a different delimiter. For instance, how would you instruct `awk` to recognize a comma `,` or a colon `:` as a delimiter instead?
4. Demonstrate with an example how you would extract data from multiple columns in `awk`. How does the syntax differ when you want to retrieve data from the first, third, and fifth columns simultaneously as opposed to extracting them one at a time?
5. How do you filter lines in `awk` where a particular column does not match a given pattern? Explain and provide an example illustrating this use case.
6. Explain how `awk` can be used to perform data aggregation tasks. For instance, if you have a file with several rows of data, how would you use `awk` to compute the sum of values in a specific column? Provide an example to illustrate your explanation.
