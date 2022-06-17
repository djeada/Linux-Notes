## Pipe
Many Linux commands default to printing to “standard output,” which is the terminal screen. 
The pipe character (|) is used to reroute or divert output to another program or filter.

To display information about user_name, use the <code>w</code> command, but instead of his username, show admin:

```bash
w | grep user_name | sed s/user_name/admin/g
```

The following syntax is used to send an email to a remote client. The email's body will be the current time and date:

```bash
date | mail -s "This is a remote test" user1@rhhost1.localnet.com
```

### stderr
Program output is often shown on the screen, while program input is typically provided through the keyboard (if no file arguments are given). In technical terms, processes typically write to standard output (the screen) and receive input from standard input (the keyboard). In reality, there is another output channel called standard error where programs can post their error messages (stderr).

What is the difference between piping into | and piping into |& in the Bash shell?
* Piping into | pipes stdout. 
* Piping into |& pipes stdout and stderr.

## Redirect

The > operator is used to redirect standard output to a file rather than the screen:

```bash
echo "hello" > file.txt
```

If the file already exists, the contents of the file output will be deleted. Instead, we may use the >> operator to append the command's output to the file:

```bash
echo "Hello" > file.txt
echo "World!" >> file.txt
```

To capture standard error, prefix the > operator with a 2 (under UNIX, file numbers 0, 1, and 2 are assigned to standard input, standard output, and standard error, respectively), for example:

```bash
less non_existent_file 2> file.txt
```

Complete summary:
  
| Syntax     | StdOut visibility | StdErr visibility | StdOut in file | StdErr in file | existing file |
| --------   | ----------------- | ----------------- | -------------- | -------------- | ------------- |
| >          |   no              |   yes             |   yes          |   no           |  overwrite    |
| >>         |   no              |   yes             |   yes          |   no           |  append       |
| 2>         |   yes             |   no              |   no           |   yes          |  overwrite    |
| 2>>        |   yes             |   no              |   no           |   yes          |  append       |  
| &>         |   no              |   no              |   yes          |   yes          |  overwrite    |    
| &>>        |   no              |   no              |   yes          |   yes          |  append       |  
| tee        |   yes             |   yes             |   yes          |   no           |  overwrite    |  
| tee -a     |   yes             |   yes             |   yes          |   no           |  append       |
| n.e. (*)   |   yes             |   yes             |   no           |   yes          |  overwrite    |  
| n.e. (*)   |   yes             |   yes             |   no           |   yes          |  append       |
| \|& tee    |   yes             |   yes             |   yes          |   yes          |  overwrite    |
| \|& tee -a |   yes             |   yes             |   yes          |   yes          |  append       |  

## Filters

Filters are commands that are designed to be used with a pipe.
These filters are relatively little programs that accomplish one thing very well. 

### Sort

<code>sort</code> is a command that is frequently used with redirect. It sorts the lines from a collection of files.

```bash
sort file_1.txt file_2.txt > file_name.txt
```

* <code>-n</code> numeric sorting
* <code>-r</code> reverse order
* <code>-t</code> sorting using a template, usually joined with <code>-kX</code> where X is the column number.

Sort using the third column, with columns separated by ':' sign:

 ```bash
sort -k3 -t : /etc/passwd
```

### Tee
The <code>tee</code> command reads standard input and writes it to standard output as well as one or more files.

What is the key difference between a redirect (>) and piping to the tee command?
The tee command sends output to STDOUT and a file, whereas a redirect sends output only to a file.

### Cut
The <code>cut</code> filter can choose columns from files based on a delimiter or a bytes count. 

### Tr
Use <code>tr</code> to quickly replace a character with another. 

### Wc
With <code>wc</code>, you may easily count words, lines, and characters. 

### Uniq
When you need to remove duplicates from lists of values, use <code>uniq</code>. 

## Challenges

1. Count the number of people who are currently logged into the system. 
1. Display a sorted list of all system users (not only presently logged in). 
1. Make a list of all the filenames ending in.conf in /etc. Sort them according to string length. 
1. Print the first and seventh columns of /etc/passwd side by side.
1. Display each word from /etc/fstab on a separate line. Count how many lines there are. 
