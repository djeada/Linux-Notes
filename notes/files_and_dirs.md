## Absolute and Relative Paths 

A  path is a way to specify the location of a file or directory. There are two ways to specify a path:

* Absolute path: the path is specified with respect to the root of the file system (`/`). An absolute path always begins with the root directory.
* Relative path: the path is specified with respect to the current working directory. The current working directory is the directory that you are currently in.

Here are some examples of absolute and relative paths:

Absolute path:

```bash
/home/user/notes/file_name.txt
```

Relative path:

```bash
notes/file_name.txt
```

It is important to note that absolute paths are generally preferred, as they are more explicit and less prone to errors. However, relative paths can be useful when you want to specify a path that is relative to the current working directory.

## Navigating Files

You can use various commands to navigate and manipulate files and directories.

### Print Working Directory (pwd)

To show the complete absolute path to your current filesystem location, use the pwd command:

```
pwd
```

### Change Directory (cd)

The cd command allows you to change your current working directory to another directory specified by the path you provide as an argument. If you do not provide a path, the cd command will take you to your home directory. To go to your home directory, use:

```
cd ~
```

### List Directory Contents (ls)

The ls command lists the contents of a directory. You can use various flags to modify the output of the ls command:

| Flag | Description |
| --- | --- |
| `-l` | displays information in long format, including permissions, owner, group, size, and modification date|
| `-a` | shows hidden files |
| `-t` | sorts the list by modification date |
| `-r` | reverses the order of the list |
| `-R` | lists subdirectories recursively |
| `-i` | displays the inode number of each file |


To view all files (-a) and display extra information about them (-l), use the following command:

```
ls -al
```

The ls command displays the following information:

* type: a single character indicating the type of file or directory. This can be 'd' (directory), '-' (normal file), 'l' (symbolic link), 'b' (block-oriented device), or 'c' (character-oriented device).
* permissions: a set of characters that describe the access permissions for the file or directory. There are nine permission characters that describe three types of access (read ('r'), write ('w'), and execute ('x')) granted to three user groups (the owner of the file, users in the file's group, and other users).
* links: the number of filesystem links leading to the file or directory (see the hard/soft link discussion in the next section).
* owner: typically, this is the user who created the file or directory.
* group: identifies a group of users who have access to the file based on the group access privileges defined in the permissions field.
* size: the length of a file in bytes, or the amount of space required by the operating system to hold a directory's list of files.
* date: the most recent modification date of the file or directory (written to). The -u option displays the last time the file was accessed (read).
* name: the file or directory name.

You can use wildcards to limit the displayed list to a particular group of files. For example, the following command will list all files with the .txt extension in the /home/mydirectory directory:

```
ls /home/mydirectory/*.txt
```
### List files in a tree-like format
The tree command is a Linux utility that displays the contents of a directory in a tree-like format. It is a useful tool for quickly getting an overview of the structure of a directory and its subdirectories.

To use the tree command, you can specify the path to the directory you want to list as an argument. If no directory is specified, the tree command will list the contents of the current directory by default.

Here is an example of using the tree command to list the contents of the `/tmp` directory:

```
tree /tmp
```

This will display the contents of the /tmp directory in a tree-like format, showing subdirectories and files indented under their parent directories.

You can use various options to modify the output of the tree command. Some common options include:

| Flag | Description |
| --- | --- |
| `-d` |only show directories |
| `-L` | specify the depth of the tree (e.g. -L 2 will only show the first two levels of the directory structure) |
| `-f` | show the full path of each file and directory |
| `-i` | do not show indentation lines |

### Special Symbols

There are several special symbols you can use when specifying paths:

| Symbol | Description |
| --- | --- |
| `/` | root directory |
| `~` | home directory |
| `.` | current directory |
| `..` | parent directory |
| `*` | wildcard matching any filename |
| `?` | wildcard matching any character |


## File operations

Let us cover a range of basic and advanced commands for managing files in Linux, including creating, copying, moving, removing, and displaying files.

### Creating files

The touch command creates a new empty file.

```
touch new_file.txt
```

The mkdir command creates a new directory. To create a directory called test in the current location, use:

```
mkdir test
```

### Copying files

The cp command makes a copy of a source file in the destination directory.

```
cp /path/to/source/file.txt /path/to/target/dir/
```

To copy a directory and its contents, use:

```
cp -r source destination
```

Some other flags include:

| Flag |	Description |
| ---- | ----------- |
| `-a`	| used to copy permissions as well |
| `-A`	| used to copy all files (hidden and normal) |

### Moving files

The mv command moves a file or directory to the destination directory.

To rename `file_1.txt` to `file_2.txt`, use:

```
mv file_1.txt file_2.txt
```
To move big_dir from the Downloads directory to the home directory, use:

```
mv ~/Downloads/big_dir ~
```

### Removing files

The rm command removes file(s). By default, Linux will prompt the user for confirmation before removing the file.

```
rm file_1.txt file_2.txt
```

To remove a directory and its contents, use:

```
rm -r directory
```

Be careful with wildcards.

### Displaying files

The cat command prints the entire contents of a file to the terminal.

To display a file named file.txt located in the current working directory, use:

```
cat file.txt
```

The more and less commands show the contents of a file page by page. more allows you to move forward one page at a time, while less allows you to scroll through the contents of the file.

```
more file.txt
less file.txt
```

| Command | Description |
| --- | --- |
| `Enter` | to move forward one line |
| `Space` | to move forward one page |
| `b` | to move one page backward |
| `q` | to end |
| `/pattern` | to jump to the next occurrence of the text “pattern” |

You can also use the head and tail commands to view the beginning or end of a file, respectively.

```
head file.txt
tail file.txt
```

## Expansion and globs
Brace expansion and globs are two similar techniques for representing files with names that follow a pattern. However, there are some key differences between the two.

Brace expansion generates a list of strings that match a pattern. It allows you to create a list of strings by enclosing a list of comma-separated values in curly braces, and appending a preamble and optional postscript to each value. For example, the command echo a{b,c}d will generate the strings abd and acd.

```bash
$ echo a{b,c}d
abd acd
```

Globs, on the other hand, are used to match against the names of existing files. They use wildcards like * and ? to represent patterns in filenames, and they can be used in combination with commands like ls or cp to operate on the matching files. For example, the glob *.txt will match against all files in the current directory that have a .txt extension.

It's important to note that brace expansion does not actually match against any existing files. It simply generates a list of strings based on the pattern specified in the curly braces. Globs, on the other hand, are used to match against the names of existing files.

In addition, it's worth noting that the wildcards used in globs have different meanings than those used in regular expressions (regex). In globs, the * wildcard represents zero or more characters, while in regex it represents zero or more instances of the preceding character. Similarly, the ? wildcard in globs represents a single character, while in regex it represents zero or one instance of the preceding character. The . wildcard in globs represents a literal dot character, while in regex it represents any single character.

| Wildcard | Globs | Regex |
| --- | --- | --- |
| `*` | zero or more characters | zero or more instances of the preceding character |
| `?` | a single instance of a character | zero or one instance of the preceding character |
| `.` | dot as a literal character  | any single character |

Overall, brace expansion and globs are useful tools for working with files in the Linux command line, and understanding the differences between the two can help you use them effectively.

## Challenges

1. How can you identify hidden files in Linux?
2. What is the symbol that represents the top-most directory in the file system hierarchy?
3. Can you list several commands that can be used to display the contents of a file in the Linux command line?
4. Use the cd command to navigate to different directories, including:
  - your home directory
  - the root directory (`/`)
  - the `/var/log` directory
  - your desktop

  Try using both relative and absolute paths.

5. Use the ls command to list the files in the current directory, and try using the following options to modify the output:
  - show hidden files
  - sort files by modification date

6. Use `more`, `less`, or `cat` to display the contents of some hidden files from your home directory. You may find `.bashrc` particularly interesting.
7. Create a temp directory in your home directory. Use the touch command to create three empty files in the temp directory. Save the results of the `ls` command to each of the created files using redirection. Display the contents of the files to the terminal.
8. Copy the contents of the temp directory to your home directory.
9. Create a temp directory in your home directory. Create three text files in the temp directory, redirecting some text to each file using the `>` operator. Move the temp directory to a new location.
10. Practice using globs to match against the names of existing files. Some examples include:
  - Show all files in the current directory with filenames of precisely five characters.
  - List all files that do not begin with the letter b.
  - List all files that begin with abc and end with a number.
