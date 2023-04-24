## Files and dirs

These notes cover essential concepts of navigating and managing files and directories in the Linux file system.

## Absolute and Relative Paths 
Paths specify the location of files or directories:

* Absolute path: Starts from the root of the file system (`/`).
* Relative path: Starts from the current working directory.

Examples:

Absolute path:

```bash
/home/user/notes/file_name.txt
```

Relative path:

```bash
notes/file_name.txt
```

It's worth keeping in mind that using absolute paths is typically a better choice, as they provide more clarity and reduce the likelihood of mistakes. That being said, relative paths can come in handy when you need to define a path in relation to your current working directory.

## Navigating Files

Commands to navigate and manipulate files and directories:

### Print Working Directory (pwd)

Display the absolute path of the current directory:

```
pwd
```

### Change Directory (cd)

Change the current directory to another directory:

```
cd /path/to/directory
```

Go to your home directory:

```
cd ~
```

### List Directory Contents (ls)

To view the contents of a directory, use:

```
ls
```

For a more detailed list that includes hidden files and extra information, use:

```
ls -al
```

Use wildcards to display specific file groups. For example, to list all .txt files in the /home/mydirectory directory, use:
```
ls /home/mydirectory/*.txt
```

These are some common flags for the ls command:

| Flag | Description |
| ---  | ---         |
| `-l` | shows long format details like permissions, owner, group, size, and modification date|
| `-a` | reveals hidden files |
| `-t` | sorts by modification date |
| `-r` | reverses the list order |
| `-R` | lists subdirectories recursively |
| `-i` | shows each file's inode number |

The `ls` command provides information on:

* Type: a character indicating file or directory type ('d' for directory, '-' for normal file, 'l' for symbolic link, 'b' for block-oriented device, or 'c' for character-oriented device).
* Permissions: nine characters representing access permissions for the file or directory (read ('r'), write ('w'), and execute ('x') for the owner, the file's group, and other users).
* Links: the number of filesystem links to the file or directory.
* Owner: usually the creator of the file or directory.
* Group: a group of users with access based on group privileges defined in the permissions field.
* Size: file length in bytes, or space needed by the OS to hold a directory's file list.
* Date: the most recent file or directory modification date. The -u option shows the last access time (read).
* Name: the file or directory name.

### Display Files in a Tree Format
The tree command is a Linux utility that presents directory contents in a tree format. It's useful for quickly understanding a directory's structure and subdirectories.

Specify the directory path as an argument or use the default current directory:

```
tree /tmp
```

This example shows the contents of the /tmp directory in a tree format, with subdirectories and files indented beneath their parent directories.

Use options to modify the tree command output:

| Flag | Description |
| ---  | ---         |
| `-d` | shows only directories |
| `-L` | sets the tree depth (e.g., -L 2 displays the first two directory levels) |
| `-f` | shows the full path of files and directories |
| `-i` | hides indentation lines |

### Special Symbols

Use these special symbols when specifying paths:

| Symbol | Description |
| ---    | ---         |
| `/`    | root directory |
| `~`    | home directory |
| `.`    | current directory |
| `..`   | parent directory |
| `*`    | wildcard matching any filename |
| `?`    | wildcard matching any character |

## File operations

Commands to create, copy, move, remove, and display files.

### Creating files

Create a new empty file:

```
touch new_file.txt
```

Create a new directory:

```
mkdir test
```

### Copying files

Copy a file:

```
cp /path/to/source/file /path/to/target/dir/
```

Copy a directory and its contents:

```
cp -r /path/to/source_directory/dir/ destination
```

Modify the cp command with these options:

| Flag |	Description      |
| ---- | ---------------  |
| `-a`	| also copy permissions |
| `-A`	| copy all files (hidden and normal) |

### Moving files

The mv command moves or renames a file or directory.

To rename `file_1.txt` to `file_2.txt`, use:

```
mv file_1.txt file_2.txt
```

To move big_dir from the Downloads directory to the home directory, use:

```
mv ~/Downloads/big_dir ~
```

### Removing files

The rm command deletes file(s). Linux prompts for confirmation before removal.

```
rm file_1.txt file_2.txt
```

To remove a directory and its contents, use:

```
rm -r directory
```

Be cautious with wildcards.

### Displaying files

The cat command shows the entire contents of a file in the terminal.

To display a file named file.txt in the current working directory, use:

```
cat file.txt
```

The more and less commands display file contents page by page. more moves forward one page at a time, while less lets you scroll through the file contents.

```
more file.txt
less file.txt
```

The following commands might be useful:

| Command | Description |
| ---     | ---         |
| `Enter` | move forward one line |
| `Space` | move forward one page |
| `b`     | move one page backward |
| `q`     | end |
| `/pattern` | jump to the next occurrence of the text “pattern” |

Use the head and tail commands to view the beginning or end of a file, respectively.

```
head file.txt
tail file.txt
```

## Expansion and globs
Brace expansion and globs are techniques for working with file names that follow patterns. They are different in the following ways:

Brace expansion creates a list of strings that match a pattern. It uses a list of comma-separated values in curly braces with a preamble and optional postscript for each value. For example:

```bash
$ echo a{b,c}d
abd acd
```

Globs match the names of existing files. They use wildcards like `*` and `?` to represent patterns in filenames and can be used with commands like `ls` or `cp`. For example, the glob `*.txt` will match all files in the current directory with a `.txt` extension.

Brace expansion generates a list of strings based on the pattern in the curly braces, while globs match against the names of existing files.

Additionally, wildcards in globs have different meanings than in regular expressions (regex):

| Wildcard | Globs | Regex |
| --- | --- | --- |
| `*` | zero or more characters | zero or more instances of the preceding character |
| `?` | a single instance of a character | zero or one instance of the preceding character |
| `.` | dot as a literal character  | any single character |

Understanding the differences between brace expansion and globs can help you use them effectively in the Linux command line.

## Challenges

1. How do you identify hidden files in Linux?
2. What symbol represents the top-most directory in the file system hierarchy?
3. List several commands to display the contents of a file in the Linux command line.
4. Use the `cd` command to navigate to different directories, like your home directory, the root directory (`/`), `/var/log`, and your desktop. Try using both relative and absolute paths.
5. Use the `ls` command to list the files in the current directory, and try options to show hidden files and sort files by modification date.
6. Display the contents of hidden files from your home directory using `more`, `less`, or `cat`.
7. Create a temp directory in your home directory. Create three empty files in the temp directory using the touch command. Redirect the results of the ls command to each file. Display the contents of the files to the terminal.
8. Copy the contents of the `temp` directory to your home directory.
9. Create a temp directory in your home directory. Create three text files in the temp directory, redirecting text to each file using the `>` operator. Move the temp directory to a new location.
10. Practice using globs to match against the names of existing files. For example, show all files in the current directory with filenames of precisely five characters.
