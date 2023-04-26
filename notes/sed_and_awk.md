## Command-Line Stream Editors

Sed and Awk are command-line utilities to modify text in data streams. These tools are helpful in Unix-like systems for tasks such as replacing text, erasing lines, and formatting text.

## Sed

Sed is a straightforward editor that processes text one line at a time. It uses a basic language featuring loops and conditions. Sed has two primary "variables": pattern space and hold space. Due to their compact syntax, Sed scripts might be challenging to read.

Examples of using Sed:

* Erase spaces and tabs at line beginnings: `sed 's/^[ \t]*//' file_name.txt`
* Remove blank lines: `sed '/^$/d' file_name.txt`
* Convert all characters in text files to uppercase: `sed -i 's/.*/\U&/' *`
* Erase everything after and including a line with a special_string: `sed -n '/special_string/,$!p' file_name.txt`
* Substitute old_string with new_string in every file in the current folder and its subfolders: `find . -type f -exec sed -i -e "s/old_string/new_string/g" {} \;`

## AWK

Awk is a more sophisticated editor suitable for handling text resembling rows and columns. It features a complete language with variables, arrays, and control structures like `if/else`, `while`, `do/while`, and `for` loops. Awk also supports mathematical operations similar to those in the C programming language.

By default, Awk employs whitespace as delimiters. This can be altered using the `-F` flag. Examples of Awk usage:

* Extract the first part (column) of a line: `echo 'abc efg hji' | awk '{print $1}' (output: abc)`
* Retrieve a part using a custom delimiter: `echo 'abc,efg,hji' | awk -F , '{print $2}' (output: efg)`
* Obtain several parts: `awk '{print $1,$5,$3}' file_name.txt`
* Display lines where the third part equals xxx: `awk '$3 == "xxx"' file_name.txt`
* Show lines where the third part is not xxx: `awk '$3 != "xxx"' file_name.txt`
* Reveal lines where the seventh part matches a pattern: `awk '$7 ~ /^[a-d].[xyz]/' file_name.txt`
* Indicate lines where the seventh part doesn't match a pattern: `awk '$7 !~ /^[a-d].[xyz]/' file_name.txt`
* Present lines with unique values in the third part: `awk '!arr[$3]++' file_name.txt`
* Illustrate lines where the value in the second part is greater than the first part: `awk '$2>$1' file_name.txt`
* Compute the sum of values from the seventh part: `awk '{sum+=$7} END {print sum}' file_name.txt`
* Show the last part of each line: `awk '{print $NF}' file_name.txt`
* Display the middle part of each line: `awk '{print $((NF/2)+1)}' file_name.txt`
   
## Challenges

1. Contrast the primary differences between `sed` and `awk`.
2. Describe the process by which `sed` operates on text streams.
3. Explain how to modify the delimiter in `awk`.
4. Demonstrate how to extract multiple parts in `awk`.
5. Illustrate how to display lines where a specific part doesn't match a pattern in `awk`.
6. Describe how to calculate the sum of values of a particular part in `awk`.
