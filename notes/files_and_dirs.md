<h2>Navigating files</h2>

To show the complete absolute path to your current filesystem location, use:

```bash
pwd
```

The <i>cd</i> command changes your location to another directory specified by the path you give as an argument. With no parameters, cd sends you to your home directory. To be taken to your home directory, use:

```bash
cd ~
```

The <i>ls</i> command lists contents of directories. Available flags:

| Flag | Description |
| --- | --- |
| <i>-l</i> | newlines and all info |
| <i>-a</i> | show hidden files |
| <i>-t</i> | sort modification date |
| <i>-r</i> | reverse order |
| <i>-R</i> |  list subdirectories recursively |
| <i>-i</i> | show inodes |

Use the following command to view all files (-a) and display extra information about them (-l):

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

You may use wildcards to limit the displayed list to a particular group of files:

```bash
ls /home/mydirectory/*.txt
```

| Symbol | Description |
| --- | --- |
| <i>~</i> | home directory |
| <i>.</i> | current directory |
| <i>..</i> | parent directory |
| <i>*</i> | wildcard matching any filename |
| <i>?</i> | wildcard matching any character |

<h2>List files in a tree-like format</h2>
The tree command displays a tree-like listing of the contents of a specified directory. If no directory is given, the contents of the current directory are displayed by default.

```bash
tree /tmp
```

<h2>Creating files</h2>

The <i>mkdir</i> command creates a new directory. To create a directory called test in a current location, use:

```bash
mkdir test
```

<h2>Copying files</h2>

The <i>cp</i> command makes a copy of a source file in the destination directory.

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
| <i>-a</i> | used to copy permissions as well |
| <i>-A</i> | used to copy all files (hidden and normal) |

<h2>Moving files</h2>

The <i>mv</i> command moves a file or directory to the destination directory. 

To rename file_1.txt to file_2.txt, use:

```bash
mv file_1.txt file_2.txt
```

To move big_dir from Downloads to Home directory, use:

```bash
mv ~/Download/big_dir ~/big_dir
```

<h2>Remove files</h2>

The <i>rm</i> command removes file(s). By default Linux will prompt the user for confirmation before removing the file.

```bash
rm file_1.txt file_2.txt
```

To removy a directory and its content, use:

```bash
rm –r directory
```

Be careful with wildcards.

<h2>Reading files</h2>

<i>cat</i> command prints the whole file on the screen. 

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

<i>more</i> shows a file page by page. A similar command is <i>less</i>, except that it shows more...

| Command | Description |
| --- | --- |
| <i>Enter</i> | to move forward one line |
| <i>Space</i> | to move forward one page |
| <i>b</i> | to move one page backward |
| <i>q</i> | to end |
| <i>/pattern</i> | to jump to the next occurrence of the text “pattern” |

<h2>Expansion and globs</h2>
Brace expansion and globs are two comparable approaches for representing files with names that follow a pattern.
However, there is a distinction between the two techniques.
In a nutshell, brace expansion generates a list of strings that match a pattern, and globs correspond to the list of pathnames.

To make matters even more confusing, globs use the same wildcards as regex, but their meaning is significantly different. 

| Wildcard | Globs | Regex |
| --- | --- | --- |
| <i>*</i> | zero or more characters | zero or more instances of the preceding character |
| <i>?</i> | a single instance of a character | zero or one instance of the preceding character |
| <i>.</i> | dot as a literal character  | any single character |

Globbing is used by the command shell to complete filenames. If you write ls \*.txt, you'll obtain a list of all the files in the current directory that end in.txt. If you type ls a*.csv, you'll get a list of all the files that begin with the letter a and end in.csv. The asterisk (\*) is a wildcard that allows you to rapidly filter which files you're looking for.

If you only want to define one character, you can use a question mark in globbing. So, if you type ls abc??.txt, you'll get abcde.txt but not abcd.txt.

As a result of brace expansion, any string can be generated. However, unlike filename expansion, the generated filenames do not have to exist in order for this mechanism to work properly. It is possible for patterns to be brace-expanded to include a preamble and optional postscript. To each string enclosed in braces, the preamble is appended, and to each resultant string, the postscript is appended, expanding from left to right. 

```bash
echo a{b,c}d
#abd acd
```
