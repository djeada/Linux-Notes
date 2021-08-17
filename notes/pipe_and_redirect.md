<h2>Pipe</h2>
Many Linux commands default to printing to “standard output,” which is the terminal screen. 
The pipe character (|) is used to reroute or divert output to another program or filter.

```bash
w # It shows who’s logged in.
w | less # redirects the output to the ‘less’ pager
w | grep ‘user’ | sed s/user/admin/g # replace all ‘user’ with ‘admin’
```

What is the difference between piping into | and piping into |& in the Bash shell?
Piping into | pipes stdout. Piping into |& pipes stdout and stderr.

The following syntax is used to send an email to a remote client.
The email's body will be the current time and date:

```bash
date | mail -s "This is a remote test" user1@rhhost1.localnet.com
```

<h2> Redirect</h2>
Program output is often shown on the screen, while program input is typically provided through the keyboard (if no file arguments are given). In technical terms, processes typically write to standard output (the screen) and receive input from standard input (the keyboard). In reality, there is another output channel called standard error where programs can post their error messages.

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

<h2>Sort</h2>

<i>sort</i> sorts lines contained in a group of files.
 
 ```bash
sort file_1.txt file_2.txt > file_name.txt
```

* <i>-n</i> numeric sorting
* <i>-r</i> reverse order
* <i>-t</i> sorting using a template, usually joined with <i>-kX</i> where X is the column number.

Sort using the third column, with columns separated by ':' sign:

 ```bash
sort -k3 -t : /etc/passwd
```

<h2>Tee</h2>
The <i>tee</i> command reads standard input and writes it to standard output as well as one or more files.

What is the key difference between a redirect (>) and piping to the tee command?
The tee command sends output to STDOUT and a file, whereas a redirect sends output only to a file.
