What is one major difference between brace expansion and globs?
Brace expansion creates a list; globs match the list of pathnames.

<h2>Navigating files</h2>
pwd: shows current directory.
cd directoryname: makes directoryname your current directory. 

cd with no parameters switches to your home directory

ls directoryname: lists contents of directories.
You can limit the list with wildcards

```bash
ls /home/mydirectory/*.txt
```

Use ls -l for more information about the files.

| Command | Description |
| --- | --- |
| <i>~</i> | home directory |
| <i>.</i> | current directory |
| <i>..</i> | parent directory |
| <i>*</i> | wildcard matching any filename |
| <i>?</i> | wildcard matching any character |

<h2>Creating files</h2>
mkdir directoryname: creates a new directory.

<h2>Copying files</h2>
cp source destination: makes a copy of a file named “source” to “destination”.
cp –r source destination: copies a directory and its content

<h2>Moving files</h2>
mv source destination: moves a file or directory.

<h2>Remove files</h2>
rm filenamelist: removes/deletes file(s). Be careful with wildcards.
rm –r directory: removes directory (-ies) including its content 

When a user deletes a file using the rm command, Linux will ask for confirmation if configured to do so

<h2>Reading files</h2>

cat file: prints the whole file on the screen. 

When used in conjunction with redirection, it will concatenate the files file_1 and file_2 into a single file named new_file.

```bash
cat file_1.txt file_2.txt > new_file.txt
```

You can also use wildcards:

```bash
cat *.txt > new_file.txt
```

more file: shows a file page by page. 

<h2>Editing</h2>

| Command | Description |
| --- | --- |
| <i>Enter</i> | to move forward one line |
| <i>Space</i> | to move forward one page |
| <i>b</i> | to move one page backward |
| <i>q</i> | to end |
| <i>/pattern</i> | to jump to the next occurrence of the text “pattern” |
