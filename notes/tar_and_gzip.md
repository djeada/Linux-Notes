<h2>tar</h2>
The tar command can pack single files or all files in a directory tree into one file known as archive, which can be unpacked later.
An archive is a file that contains other files as well as information about them such as filenames, owners, timestamps, and access rights. 
By default, tar does not do any compression.

| Flag | Description |
| --- | --- |
| <i>-c</i> | pack |
| <i>-v</i> | list name of files |
| <i>-f</i> | pack into file |
| <i>-x</i> | extract |

To pack mytree file1 file2 into an archive called myfiles.tar, use:

```bash
tar -cvf myfiles.tar mytree file1 file2
```

To extract an archive called myfile.tar, use:

```bash
tar -xvf myfiles.tar
```

<h2>gzip</h2>

Compress with gzip:

```bash
gzip mytar.tar
```
