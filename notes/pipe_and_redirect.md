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

<h2>Sort</h2>

<i>sort</i> sorts lines contained in a group of files.
 
 ```bash
sort file_1.txt file_2.txt > file_name.txt
```

<h2>Tee</h2>
The <i>tee</i> command reads standard input and writes it to standard output as well as one or more files.

What is the key difference between a redirect (>) and piping to the tee command?
The tee command sends output to STDOUT and a file, whereas a redirect sends output only to a file.
