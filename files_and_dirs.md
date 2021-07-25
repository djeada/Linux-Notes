<h2>Navigating files</h2>

* <i>pwd</i>: displays current directory.

Shows the complete absolute path to your current filesystem location.

* <i>cd directoryname</i>: makes directoryname your current directory. 

With no arguments, cd changes your location to your home directory.

* <i>ls directoryname</i>: lists contents of directories.

To see all files (-a) and display more informations abou them (-l) use:

```bash
ls -al
```

Following info will be displayed:

- <i>type</i> is a single character that can be 'd' (directory), '-' (normal file), 'l' (symbolic link), 'b' (block-oriented device), or 'c' (character-oriented device).
- <i>permissions</i> is a set of characters that describe access permissions. There are 9 permission characters that describe three sorts of access granted to three user groups. The three forms of access are read ('r'), write ('w'), and execute ('x'), and the three user categories are the user who owns the file, users in the file's group, and other users (the general public).
- <i>links</i> refers to the number of filesystem links leading to the file/directory (see the hard/soft link discussion in the next section).
- <i>owner</i> typically, this is the person who created the file or directory.
- <i>group</i> identifies a group of users who have access to the file based on the group access privileges defined in the permissions field.
- <i>size</i> is the length of a file, or the amount of bytes required by the operating system to hold a directory's list of files.
- <i>date</i> is the most recent modification date of the file or directory (written to). The -u option displays the last time the file was visited (read).
- <i>name</i> is the file or directory name.

You may narrow the list by using wildcards:

```bash
ls /home/mydirectory/*.txt
```

| Command | Description |
| --- | --- |
| <i>~</i> | home directory |
| <i>.</i> | current directory |
| <i>..</i> | parent directory |
| <i>*</i> | wildcard matching any filename |
| <i>?</i> | wildcard matching any character |

<h2>Creating files</h2>

* <i>mkdir directoryname</i> : creates a new directory.

<h2>Copying files</h2>

* <i>cp source destination</i> : makes a copy of a file named “source” to “destination”.

* To copy a directory and its content:

```bash
cp –r source destination
```

<h2>Moving files</h2>

* <i>mv source destination</i>: moves a file or directory.

<h2>Remove files</h2>

* <i>rm filenamelist</i>: removes/deletes file(s). Be careful with wildcards.
* To removy a directory and its content:

```bash
rm –r directory
```

If the rm command is used to remove a file, Linux will prompt the user for confirmation if it is set to do so.

<h2>Reading files</h2>

* <i>cat file</i>: prints the whole file on the screen. 

When used in conjunction with redirection, it will concatenate the files file_1 and file_2 into a single file named new_file.

```bash
cat file_1.txt file_2.txt > new_file.txt
```

You can also use wildcards:

```bash
cat *.txt > new_file.txt
```

* <i>more file</i>: shows a file page by page. 

| Command | Description |
| --- | --- |
| <i>Enter</i> | to move forward one line |
| <i>Space</i> | to move forward one page |
| <i>b</i> | to move one page backward |
| <i>q</i> | to end |
| <i>/pattern</i> | to jump to the next occurrence of the text “pattern” |

<h2>Expansion ang globs</h2>
What is one major difference between brace expansion and globs?
Brace expansion creates a list; globs match the list of pathnames.
