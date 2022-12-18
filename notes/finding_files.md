## Finding Files: An Overview of Find, Locate, and Which

An overview of three useful Linux commands for finding files: `find`, `locate`, and `which`. `Find` allows you to search for files based on various criteria, such as the file name, size, and type. `Locate` is a faster way to search for files based on their names, but it uses an index of filenames that is only updated periodically, so it may not find newly created files. `Which` allows you to determine the location of executables on the file system. The article provides examples of how to use each of these commands.

## Find

The find command allows you to search for files based on various criteria, such as the file name, size, and type. The general syntax is:

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

For example, to find all files larger than 10MB and display them using the ls command, you can use:

```bash
find / -size +10M -exec ls -l {} ;
```

To find and remove all files with the .bak extension in the current directory and its subdirectories, you can use:

```bash
find . -name \*.bak -type f -delete
```

To find all files larger than 2000 blocks and ask the user for permission to remove them, you can use:

```bash
find $HOME -name '*' -type f -size +2000 -exec ls -s {} \; -ok rm -f {} \;
```

## Locate

The locate command allows you to quickly search for files based on their names. It uses an index of filenames, which is typically updated once per day, so it may not find newly created files.

To find all file paths that start with "/usr", include the word "pixmaps", and end with ".jpg", you can use:

```bash
locate --regexp '^/usr.*pixmaps.*jpg$'
```

To mute error messages, you can use the -q flag:

```bash
locate -q "*.py"
```

Use the -i flag to make the search case-insensitive:

```bash
locate -i "*.CPP"
```

The database of filenames is typically stored at `/var/lib/mlocate/mlocate.db`. You can update the database manually with the updatedb command.

## Which

The which command allows you to determine the location of executables on the file system. If you can run a program or system utility by typing its name in the terminal, you can use which to find out where it is stored on the disk.

To see the location of the python executable, you can use:

```bash
which python
```

To view the PATH environmental variable, which specifies the directories that the system searches when you type a command, you can use:

```bash
echo $PATH
```

## Challenges

* Use the which command to determine the location of the executable files for the following tools:
  - `cat`
  - `ls`
  - `reboot`
  - `chmod`

* Find all files in your home directory that are larger than 1GB.
* Search for all files in your home directory with the `.mp3` extension.
* Sarch for files with the `.txt` extension that include the string "linux."
* Search for all symbolic links in the `/usr/bin` directory.
* Display all subdirectories in the `/usr/local` directory that are owned by the root user.
* List all files in the `/var/log directory` that were modified within the past 24 hours.
