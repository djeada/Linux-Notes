

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
