<h1>tar</h1>
The tar command can pack single files or all files in a directory tree into one file known as archive, which can be unpacked later.
An archive is a file that contains other files as well as information about them such as filenames, owners, timestamps, and access rights. 
By default, tar does not do any compression.

| Flag | Description |
| --- | --- |
| <i>-c</i> | pack |
| <i>-v</i> | list name of files |
| <i>-f</i> | pack into file |
| <i>-z</i> | compress |
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

<h1>gzip</h1>
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

<h1>Challenges</h1>

1. Create an archive of your home directory with tar. To ensure that everything was included, copy your archives to /tmp and extract the files there. Remove the copies from /tmp.

2. Use tar without and with the -z option to create an archive of any directory. Compare sizes of your original directory, archive, and compressed archive. 

