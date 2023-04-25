## Finding Files

These notes talk about three useful Linux commands to look for files: `find`, `locate`, and `which`. `Find` looks for files using details like their name, size, and kind. `Locate` finds files by name fast, but relies on a list of names that's updated sometimes, so it might not see new files. `Which` shows where programs are saved on the computer. 

## Find

`Find` searches for files based on criteria like file name, size, and type. The general syntax is:

```bash
find WHERE_TO_LOOK_FOR -name REGEXP_WITH_FILE_NAME
```

Some useful flags include:

| Flag | Description |
| --- | --- |
| `-f` | search for files |
| `-d` | search for directories |
| `-l` | search for symlinks |
| `-user` *user_name* | search for files owned by a specific user |

For example, to find all files larger than 10MB and display them using the ls command, use:

```bash
find / -size +10M -exec ls -l {} ;
```

To find and remove all files with the .bak extension in the current directory and its subdirectories, use:

```bash
find . -name \*.bak -type f -delete
```

To find all files larger than 2000 blocks and ask the user for permission to remove them, use:

```bash
find $HOME -name '*' -type f -size +2000 -exec ls -s {} \; -ok rm -f {} \;
```

## Locate

`Locate` quickly searches for files by name. It uses an index of filenames, typically updated once per day, so it may not find new files.

To find all file paths that start with "/usr", include "pixmaps", and end with ".jpg", use:

```bash
locate --regexp '^/usr.*pixmaps.*jpg$'
```

To mute error messages, use the `-q` flag:

```bash
locate -q "*.py"
```

Use the `-i` flag to make the search case-insensitive:

```bash
locate -i "*.CPP"
```

The database of filenames is typically stored at `/var/lib/mlocate/mlocate.db`. You can update the database manually with the updatedb command.

## Which

`Which` identifies the location of executables on the file system. If you can run a program or system utility by typing its name in the terminal, you can use `which` to find out where it is stored on the disk.

To see the location of the python executable, use:

```bash
which python
```

To view the `PATH` environmental variable, which specifies the directories that the system searches when you type a command, use:

```bash
echo $PATH
```

## Challenges

* Use the which command to find the location of executable files for tools like `cat`, `ls`, `reboot`, and `chmod`.
* Find all files in your home directory larger than 1GB.
* Search for all `.mp3` files in your home directory.
* Search for `.txt` files in your home directory containing the string "linux."
* Search for all symbolic links in the `/usr/bin` directory.
* Display all subdirectories in the `/usr/local` directory owned by the root user.
* List all files in the `/var/log` directory modified within the past 24 hours.
