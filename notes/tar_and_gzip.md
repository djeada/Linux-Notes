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

Important: -f flag should be put before the file name.

To pack mytree file1 file2 into an archive called myfiles.tar, use:

```bash
tar -cvf myfiles.tar mytree file1 file2
```

To extract an archive called myfile.tar, use:

```bash
tar -xvf myfiles.tar
```

<h2>gzip</h2>
It is a file compression tool that is used to reduce file size.

| Flag | Description |
| --- | --- |
| <i>-d</i> | decompress files |
| <i>-l</i> | list compression information |

To compress a mytar.tar to  mytar.tar.gz, use:

```bash
gzip mytar.tar
```

To unpack file_name.gz, use:

```bash
gzip -d file_name.gz
```
