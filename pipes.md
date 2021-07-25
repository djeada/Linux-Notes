Many Linux commands default to printing to “standard output,” which is the terminal screen. 
The pipe character (|) is used to reroute or divert output to another program or filter.

```bash
w # It shows who’s logged in.
w | less # redirects the output to the ‘less’ pager
w | grep ‘user’ | sed s/user/admin/g # replace all ‘user’ with ‘admin’
```

What is the key difference between a redirect (>) and piping to the tee command?
The tee command sends output to STDOUT and a file, whereas a redirect sends output only to a file.

In the Bash shell, what is the difference between piping into | and piping into |&?
Piping into | pipes stdout. Piping into |& pipes stdout and stderr.


You send an email to a remote client using the following syntax. What will be in the body of the email?
the current date and time
 
```bash
date | mail -s "This is a remote test" user1@rhhost1.localnet.com
```
