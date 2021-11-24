<h1>Absolute and relative paths</h1>

Whenever a script or program expects a path to be specified, it can be specified in two ways:
* Absolute path: the path is specified with respect to the root of the file system <code>/</code>.
* Relative path: the path is specified with respect to the current working directory.

An example of an absolute path:
```bashFc
/home/user/notes/file_name.txt
```

An example of a relative path:
```bash
current_dir/notes/file_name.txt
```

<h1>Navigating files</h1>

To show the complete absolute path to your current filesystem location, use:

```bash
pwd
```

The <code>cd</code> command changes your location to another directory specified by the path you give as an argument. With no parameters, cd sends you to your home directory. To be taken to your home directory, use:

```bash
cd ~
```

The <code>ls</code> command lists contents of directories. Available flags:

| Flag | Description |
| --- | --- |
| <code>-l</code> | newlines and all info |
| <code>-a</code> | show hidden files |
| <code>-t</code> | sort modification date |
| <code>-r</code> | reverse order |
| <code>-R</code> |  list subdirectories recursively |
| <code>-i</code> | show inodes |

Use the following command to view all files (-a) and display extra information about them (-l):

```bash
ls -al
```

Following info will be displayed:

- <code>type</code> is a single character that can be 'd' (directory), '-' (normal file), 'l' (symbolic link), 'b' (block-oriented device), or 'c' (character-oriented device).
- <code>permissions</code> is a set of characters that describe access permissions. There are 9 permission characters that describe three sorts of access granted to three user groups. The three forms of access are read ('r'), write ('w'), and execute ('x'), and the three user categories are the user who owns the file, users in the file's group, and other users (the general public).
- <code>links</code> refers to the number of filesystem links leading to the file/directory (see the hard/soft link discussion in the next section).
- <code>owner</code> typically, this is the person who created the file or directory.
- <code>group</code> identifies a group of users who have access to the file based on the group access privileges defined in the permissions field.
- <code>size</code> is the length of a file, or the amount of bytes required by the operating system to hold a directory's list of files.
- <code>date</code> is the most recent modification date of the file or directory (written to). The -u option displays the last time the file was visited (read).
- <code>name</code> is the file or directory name.

You may use wildcards to limit the displayed list to a particular group of files:

```bash
ls /home/mydirectory/*.txt
```

| Symbol | Description |
| --- | --- |
| <code>/</code> | root directory |
| <code>~</code> | home directory |
| <code>.</code> | current directory |
| <code>..</code> | parent directory |
| <code>*</code> | wildcard matching any filename |
| <code>?</code> | wildcard matching any character |

<h1>List files in a tree-like format</h1>
The tree command displays a tree-like listing of the contents of a specified directory. If no directory is given, the contents of the current directory are displayed by default.

```bash
tree /tmp
```

<h1>Creating files</h1>

The <code>mkdir</code> command creates a new directory. To create a directory called test in a current location, use:

```bash
mkdir test
```

<h1>Copy files</h1>

The <code>cp</code> command makes a copy of a source file in the destination directory.

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
| <code>-a</code> | used to copy permissions as well |
| <code>-A</code> | used to copy all files (hidden and normal) |

<h1>Move files</h1>

The <code>mv</code> command moves a file or directory to the destination directory. 

To rename file_1.txt to file_2.txt, use:

```bash
mv file_1.txt file_2.txt
```

To move big_dir from Downloads to Home directory, use:

```bash
mv ~/Download/big_dir ~/big_dir
```

<h1>Remove files</h1>

The <code>rm</code> command removes file(s). By default Linux will prompt the user for confirmation before removing the file.

```bash
rm file_1.txt file_2.txt
```

To removy a directory and its content, use:

```bash
rm –r directory
```

Be careful with wildcards.

<h1>Read files</h1>

<code>cat</code> command prints the whole file on the screen. 

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

<code>more</code> shows a file page by page. A similar command is <code>less</code>, except that it shows more...

| Command | Description |
| --- | --- |
| <code>Enter</code> | to move forward one line |
| <code>Space</code> | to move forward one page |
| <code>b</code> | to move one page backward |
| <code>q</code> | to end |
| <code>/pattern</code> | to jump to the next occurrence of the text “pattern” |

<h1>Expansion and globs</h1>
Brace expansion and globs are two comparable approaches for representing files with names that follow a pattern.
However, there is a distinction between the two techniques.
In a nutshell, brace expansion generates a list of strings that match a pattern, and globs correspond to the list of pathnames.

To make matters even more confusing, globs use the same wildcards as regex, but their meaning is significantly different. 

| Wildcard | Globs | Regex |
| --- | --- | --- |
| <code>*</code> | zero or more characters | zero or more instances of the preceding character |
| <code>?</code> | a single instance of a character | zero or one instance of the preceding character |
| <code>.</code> | dot as a literal character  | any single character |

Globbing is used by the command shell to complete filenames. If you write ls \*.txt, you'll obtain a list of all the files in the current directory that end in.txt. If you type ls a*.csv, you'll get a list of all the files that begin with the letter a and end in.csv. The asterisk (\*) is a wildcard that allows you to rapidly filter which files you're looking for.

If you only want to define one character, you can use a question mark in globbing. So, if you type ls abc??.txt, you'll get abcde.txt but not abcd.txt.

As a result of brace expansion, any string can be generated. However, unlike filename expansion, the generated filenames do not have to exist in order for this mechanism to work properly. It is possible for patterns to be brace-expanded to include a preamble and optional postscript. To each string enclosed in braces, the preamble is appended, and to each resultant string, the postscript is appended, expanding from left to right. 

```bash
echo a{b,c}d
#abd acd
```

<h1>Challenges</h1>

1. To navigate to various directories, use <code>cd</code>. Try: 
  - your home directory 
  - root directory (/)
  - /var/log 
  - your desktop
  
  Experiment with both relative and absolute paths. 
 
2. Using <code>ls</code>, you may list the files in the current directory. Experiment with several options:
  - Display hidden files
  - Sort files by modification date 

3. Using <code>more</code>, <code>less</code> or <code>cat</code> display the contents of some hidden files from your home directory. You may find .bashrc particulary intresting.

4. Using <code>mkdir</code>, create a temp directory in your home directory. Create three empty files in the newly created temp dir using the <code>touch</code> command. Save the results of the <code>ls</code> command to each of the created files using redirection. Use <code>cat</code> to display their contents to the terminal.

5. Using <code>cp</code>, copy the contents of the temp directory to your home directory.

6. Using <code>mkdir</code>, create a temp directory in your home directory. Create three text files in the newly created temp dir using the <code>echo</code> command and redirecting some text to each of the created files. Using <code>mv</code>, move the temp directory to a new location.
