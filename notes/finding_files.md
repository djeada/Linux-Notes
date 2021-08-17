<h2>Find</h2>

If you know where the file may reside in the directory tree, you can use <i>find</i>. General syntax is: 

<b>find WHERE_TO_LOOK_FOR -name REGEXP_WITH_FILE_NAME</b>

Flags:

* <i>-type f/d/l</i> look for files, dirs or symlinks. 
* <i>-user user_name</i> owner is user_name.

Find all files larger than 10 MB and long list them using the ls command:

```bash
find / -size +10M -exec ls -l {} ;
```

Find and remove all files with .bak extension:

```bash
find . -name \*.bak -type f -delete
```

Find all files larger than 2000 blocks and ask the user for permission to remove:

```bash
find $HOME -name '*' -type f -size +2000 -exec ls -s {} \; -ok rm -f {} \;
```
<h2>Locate</h2>

The <i>locate</i> command is a significantly quicker approach to find all files whose names match a certain search term.

Find all file paths that start with "/usr", include the word "pixmaps", and end with ".jpg":

```bash
locate --regexp '^/usr.*pixmaps.*jpg$'
```

One drawback of <i>locate</i> is that it saves all filenames on the system in an index, which is often only updated once per day (/etc/cron.daily/mlocate). This indicates that locate will not detect newly created files.

The database is normally stored at /var/lib/mlocate/mlocate.db.

You can force the update with:

```bash
updatedb
```

<h2>Which</h2>
If you can launch an application program or system utility by typing its name at the shell prompt, you can use <i>which</i> to find out where it is on disk.

```bash
which python
```
