Why doesn't passwd -l keep a user from logging in via other methods?
 It locks only the password, not the account, so users can still authenticate with keys or other methods.

 Why is the passwd command able to modify the /etc/passwd file?
 It has the SUID permission mode and is owned by root.
