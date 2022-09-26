### Find

If you know where the file may reside in the directory tree, you can use <code>find</code>. General syntax is: 

    find WHERE_TO_LOOK_FOR -name REGEXP_WITH_FILE_NAME

Flags:

* <code>-type f/d/l</code> look for files, dirs or symlinks. 
* <code>-user user_name</code> owner is user_name.

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
### Locate

The <code>locate</code> command is a significantly quicker approach to find all files whose names match a certain search term.

Find all file paths that start with "/usr", include the word "pixmaps", and end with ".jpg":

```bash
locate --regexp '^/usr.*pixmaps.*jpg$'
```

To mute error messages use <code>-q</code> flag: 

```bash
locate -q "*.py"
```

Use the <code>-i</code> flag to make the search case insensitive:

```bash
locate -i "*.CPP"
```

One drawback of <code>locate</code> is that it saves all filenames on the system in an index, which is often only updated once per day (/etc/cron.daily/mlocate). This indicates that locate will not detect newly created files.

The database is normally stored at /var/lib/mlocate/mlocate.db.

You can force the update with:

```bash
updatedb
```

### Which
If you can run a program or system utility by typing its name in the terminal, you can use <code>which</code> to determine where it is located on the disk.

Have you ever wondered where executables for common tools like <code>cat</code>, <code>sed</code>, and so on come from? The system will generally look through the places specified in your "path."

To view the PATH environmental variable, use:

```bash
echo $PATH
```

To see path of <code>python</code>, use:

```bash
which python
```

## Challenges

1. Determine the location of the executable files for the following tools:
  - cat
  - ls
  - reboot
  - chmod
2. Find all files in your home directory that are larger than 1GB. 
3. Find all files in your home directory with.mp3 extensions. 
