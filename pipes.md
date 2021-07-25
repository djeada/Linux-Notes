Many Linux commands default to printing to “standard output,” which is the terminal screen. 
The pipe character (|) is used to reroute or divert output to another program or filter.

```bash
w # It shows who’s logged in.
w | less # redirects the output to the ‘less’ pager
w | grep ‘user’ | sed s/user/admin/g # replace all ‘user’ with ‘admin’
```
