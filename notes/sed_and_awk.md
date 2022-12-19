## Command-Line Stream Editors

Sed and Awk are two command-line tools for performing text transformations on streams of data. Both tools are commonly used in Unix-like systems and can be used to perform various tasks such as replacing strings, deleting lines, and formatting text.

## Sed

Sed is a simple stream editor that processes text on a per-line basis. It uses a basic programming language with goto-style loops and simple conditionals (in addition to pattern matching and address matching). Sed has two main "variables": pattern space and hold space. One thing to note is that sed scripts can be difficult to read due to their concise syntax.

Here are some examples of common sed usage:

* Trim leading whitespaces and tabulations: `sed 's/^[ \t]*//' file_name.txt`
* Delete all blank lines: `sed '/^$/d' file_name.txt`
* Convert all letters in a directory's text files to uppercase: `sed -i 's/.*/\U&/' *`
* Delete anything following and including a line that contains special_string: `sed -n '/special_string/,$!p' file_name.txt`
* Replace all occurrences of old_string with new_string in every file in the current directory and its subdirectories: `find . -type f -exec sed -i -e "s/old_string/new_string/g" {} \;`

## AWK

Awk is a more advanced stream editor that is particularly useful for processing text that resembles rows and columns, or "records" and "fields," as awk calls them. It has a full programming language with support for variables, arrays, and various control structures such as `if/else`, `while`, `do/while`, and `for` loops. Awk also has a range of mathematical operations similar to those found in the C programming language.

By default, awk uses whitespace as delimiters. However, this can be changed using the `-F` flag. Here are some examples of common awk usage:

* Extract the first field (column) of a line: `echo 'abc efg hji' | awk '{print $1}' (output: abc)`
* Extract a field using a different delimiter: `echo 'abc,efg,hji' | awk -F , '{print $2}' (output: efg)`
* Extract multiple fields: `awk '{print $1,$5,$3}' file_name.txt`
* Print lines where the third field equals xxx: `awk '$3 == "xxx"' file_name.txt`
* Print lines where the third field does not equal xxx: `awk '$3 != "xxx"' file_name.txt`
* Print lines where the seventh field matches a regex: `awk '$7 ~ /^[a-d].[xyz]/' file_name.txt`
* Print lines where the seventh field does not match a regex: `awk '$7 !~ /^[a-d].[xyz]/' file_name.txt`
* Print lines with unique values in the third field: `awk '!arr[$3]++' file_name.txt`
* Print lines where the value in the second field is greater than the value in the first field: `awk '$2>$1' file_name.txt`
* Sum the values from the seventh field: `awk '{sum+=$7} END {print sum}' file_name.txt`
* Print the last field of each line: `awk '{print $NF}' file_name.txt`
* Print the middle field of each line: `awk '{print $((NF/2)+1)}' file_name.txt`
   
## Challenges

1. What is the main difference between `sed` and `awk`?
1. How does `sed` process text streams?
1. How can the delimiter be changed in `awk`?
1. How can you extract multiple fields in `awk`?
1. How can you print lines where a particular field does not match a regex in `awk`?
1. How can you sum the values of a particular field in `awk`?
1. How can you print the last field of each line in `awk`?
1. How can you print the middle field of each line in `awk`?
1. How can you replace all occurrences of a string in multiple files in a directory and its subdirectories using `sed`?
1. How can you delete anything following and including a line that contains a specific string using `sed`?
