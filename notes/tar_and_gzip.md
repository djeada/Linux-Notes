## Essential File Compression and Archiving Commands 

An overview of two important tools for file compression and archiving: tar and gzip. It describes the flags and usage of these commands, and provides examples of how to create and extract archives. 

## The tar command
The tar command is a useful tool for packing and unpacking files and directories on a Linux system. It allows you to create an archive file that contains multiple files and directories, as well as information about them such as filenames, owners, timestamps, and access rights. By default, tar does not do any compression, but it can be used in conjunction with other tools like gzip to compress the archive.

Here are some common options for using tar:

| Flag | Description |
| --- | --- |
| `-c` | pack |
| `-v` | list name of files |
| `-f` | pack into file |
| `-z` | compress |
| `-x` | extract |

It's important to note that the `-f` flag should be placed before the name of the archive file.

To create an archive called "myfiles.tar" that includes the "mytree" directory and the "file1" and "file2" files, you would use the following command:

```bash
tar -cvf myfiles.tar mytree file1 file2
```

To extract the files from the "myfiles.tar" archive, you would use the following command:

```bash
tar -xvf myfiles.tar
```

## The gzip command

gzip is a file compression tool that can be used to reduce the size of a file. It's commonly used in conjunction with tar to compress an archive file. Here are some common options for using gzip:

| Flag | Description |
| --- | --- |
| `-d` | decompress files |
| `-l` | list compression information |

To compress the "mytar.tar" file and create a new file called "mytar.tar.gz", you would use the following command:

```bash
gzip mytar.tar
```

To decompress the "file_name.gz" file, you would use the following command:

```bash
gzip -d file_name.gz
```

## Challenges

1. Create an archive of your home directory using tar. To ensure that everything was included, copy your archives to the "/tmp" directory and extract the files there. Remove the copies from "/tmp" when you're finished.
1. Use tar with and without the `-z` option to create an archive of any directory. Compare the sizes of your original directory, the archive, and the compressed archive. 
