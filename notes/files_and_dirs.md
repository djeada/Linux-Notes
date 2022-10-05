## Absolute and relative paths

Whenever a script or program expects a path to be specified, it can be specified in two ways:
* Absolute path: the path is specified with respect to the root of the file system `/`.
* Relative path: the path is specified with respect to the current working directory.

An example of an absolute path:
```bash
/home/user/notes/file_name.txt
```

An example of a relative path:
```bash
current_dir/notes/file_name.txt
```

## Navigating files

To show the complete absolute path to your current filesystem location, use:

```bash
pwd
```

The `cd` command changes your location to another directory specified by the path you give as an argument. With no parameters, cd sends you to your home directory. To be taken to your home directory, use:

```bash
cd ~
```

The `ls` command lists contents of directories. Available flags:

| Flag | Description |
| --- | --- |
| `-l` | newlines and all info |
| `-a` | show hidden files |
| `-t` | sort modification date |
| `-r` | reverse order |
| `-R` |  list subdirectories recursively |
| `-i` | show inodes |

Use the following command to view all files (-a) and display extra information about them (-l):

```bash
ls -al
```

Following info will be displayed:

- `type` is a single character that can be 'd' (directory), '-' (normal file), 'l' (symbolic link), 'b' (block-oriented device), or 'c' (character-oriented device).
- `permissions` is a set of characters that describe access permissions. There are 9 permission characters that describe three sorts of access granted to three user groups. The three forms of access are read ('r'), write ('w'), and execute ('x'), and the three user categories are the user who owns the file, users in the file's group, and other users (the general public).
- `links` refers to the number of filesystem links leading to the file/directory (see the hard/soft link discussion in the next section).
- `owner` typically, this is the person who created the file or directory.
- `group` identifies a group of users who have access to the file based on the group access privileges defined in the permissions field.
- `size` is the length of a file, or the amount of bytes required by the operating system to hold a directory's list of files.
- `date` is the most recent modification date of the file or directory (written to). The -u option displays the last time the file was visited (read).
- `name` is the file or directory name.

You may use wildcards to limit the displayed list to a particular group of files:

```bash
ls /home/mydirectory/*.txt
```

| Symbol | Description |
| --- | --- |
| `/` | root directory |
| `~` | home directory |
| `.` | current directory |
| `..` | parent directory |
| `*` | wildcard matching any filename |
| `?` | wildcard matching any character |

## List files in a tree-like format
The tree command displays a tree-like listing of the contents of a specified directory. If no directory is given, the contents of the current directory are displayed by default.

```bash
tree /tmp
```

## Creating files

The `mkdir` command creates a new directory. To create a directory called test in a current location, use:

```bash
mkdir test
```

## Copy files

The `cp` command makes a copy of a source file in the destination directory.

```bash
cp /path/to/source/foo.txt /path/to/target/dir/
```

To copy a directory and its content, use:

```bash
cp –r source destination
```

Some other flags include:
| Flag | Description |
| --- | --- |
| `-a` | used to copy permissions as well |
| `-A` | used to copy all files (hidden and normal) |

## Move files

The `mv` command moves a file or directory to the destination directory. 

To rename file_1.txt to file_2.txt, use:

```bash
mv file_1.txt file_2.txt
```

To move big_dir from Downloads to Home directory, use:

```bash
mv ~/Download/big_dir ~/big_dir
```

## Remove files

The `rm` command removes file(s). By default Linux will prompt the user for confirmation before removing the file.

```bash
rm file_1.txt file_2.txt
```

To removy a directory and its content, use:

```bash
rm –r directory
```

Be careful with wildcards.

## Read files

`cat` command prints the whole file on the screen. 

To display a file named "file.txt" located in the current working directory, use:

```bash
cat file.txt
```

When used in conjunction with redirection, it will concatenate the files file_1 and file_2 into a single file named new_file.

```bash
cat file_1.txt file_2.txt > new_file.txt
```

You can also use the wildcards:

```bash
cat *.txt > new_file.txt
```

`more` shows a file page by page. A similar command is `less`, except that it shows more...

| Command | Description |
| --- | --- |
| `Enter` | to move forward one line |
| `Space` | to move forward one page |
| `b` | to move one page backward |
| `q` | to end |
| `/pattern` | to jump to the next occurrence of the text “pattern” |

## Expansion and globs
Brace expansion and globs are two comparable approaches for representing files with names that follow a pattern.
However, there is a distinction between the two techniques.
In a nutshell, brace expansion generates a list of strings that match a pattern, and globs correspond to the list of pathnames.

To make matters even more confusing, globs use the same wildcards as regex, but their meaning is significantly different. 

| Wildcard | Globs | Regex |
| --- | --- | --- |
| `*` | zero or more characters | zero or more instances of the preceding character |
| `?` | a single instance of a character | zero or one instance of the preceding character |
| `.` | dot as a literal character  | any single character |

Globbing is used by the command shell to complete filenames. If you write ls \*.txt, you'll obtain a list of all the files in the current directory that end in.txt. If you type ls a*.csv, you'll get a list of all the files that begin with the letter a and end in.csv. The asterisk (\*) is a wildcard that allows you to rapidly filter which files you're looking for.

If you only want to define one character, you can use a question mark in globbing. So, if you type ls abc??.txt, you'll get abcde.txt but not abcd.txt.

As a result of brace expansion, any string can be generated. However, unlike filename expansion, the generated filenames do not have to exist in order for this mechanism to work properly. It is possible for patterns to be brace-expanded to include a preamble and optional postscript. To each string enclosed in braces, the preamble is appended, and to each resultant string, the postscript is appended, expanding from left to right. 

```bash
echo a{b,c}d
#abd acd
```

## Challenges

1. Which type of files are prefixed with a dot?
2. What does a nameless directory represent?
3. What are the many ways to display the contents of a file?
 
5. To navigate to various directories, use `cd`. Try: 
  - your home directory 
  - root directory (/)
  - /var/log 
  - your desktop
  
  Experiment with both relative and absolute paths. 
 
2. Using `ls`, you may list the files in the current directory. Experiment with several options:
  - Display hidden files
  - Sort files by modification date 

3. Using `more`, `less` or `cat` display the contents of some hidden files from your home directory. You may find .bashrc particulary intresting.

4. Using `mkdir`, create a temp directory in your home directory. Create three empty files in the newly created temp dir using the `touch` command. Save the results of the `ls` command to each of the created files using redirection. Use `cat` to display their contents to the terminal.

5. Using `cp`, copy the contents of the temp directory to your home directory.

6. Using `mkdir`, create a temp directory in your home directory. Create three text files in the newly created temp dir using the `echo` command and redirecting some text to each of the created files. Using `mv`, move the temp directory to a new location.

7. Try your hand at globbing:

- Show all files in the current directory with filenames of precisely five characters.
- List all files that do not begin with the letter b.
- List all files that begin with abc and end with a number. 
