## Essential File Compression and Archiving Commands 

Notes on two essential tools for file compression and archiving: tar and gzip. This guide covers the flags and usage of these commands and provides examples of creating and extracting archives.

## The tar command

The `tar` command is a helpful tool for packing and unpacking files and folders on a Linux system. It lets you create an archive file containing multiple files and folders, as well as details like filenames, owners, timestamps, and access rights. By default, `tar` does not compress files, but it can be used with other tools like `gzip` to compress the archive.

Common options for using tar:

| Flag | Description |
| --- | --- |
| `-c` | Pack |
| `-v` | List file names |
| `-f` | Pack into a file |
| `-z` | Compress |
| `-x` | Extract |

It's essential to place the `-f` flag before the archive file name.

To create an archive called "myfiles.tar" with the "mytree" folder and "file1" and "file2" files, use this command:

```bash
tar -cvf myfiles.tar mytree file1 file2
```

To extract files from the "myfiles.tar" archive, use this command:

```bash
tar -xvf myfiles.tar
```

## The gzip command

The `gzip` is a file compression tool for reducing a file's size. It's often used with `tar` to compress an archive file. Common options for using `gzip`:

| Flag | Description |
| --- | --- |
| `-d` | decompress files |
| `-l` | list compression information |

To compress the "mytar.tar" file and create a new file called "mytar.tar.gz", use this command:

```bash
gzip mytar.tar
```

To decompress the "file_name.gz" file, use this command:

```bash
gzip -d file_name.gz
```

## Challenges

1. Make an archive of your home folder using `tar`. To check that everything was included, copy your archives to the `/tmp` folder and extract the files there. Delete the copies from `/tmp` when done.
2. Use `tar` with and without the `-z` option to create an archive of any folder. Compare the sizes of your original folder, the archive, and the compressed archive.
3. Create a script that compresses all `.txt` files in a given folder using `gzip`. The script should skip already compressed files (with `.gz` extension).
4. Use a combination of `tar` and `gzip` commands to create a compressed archive of a folder. Then, extract the archive to a new location and compare the contents of the original folder and the extracted folder to ensure they are identical.
5. Create a compressed archive using tar and gzip. Then, use the `gzip -l` command to view the compression ratio and other details about the compressed archive.
6. Write a script that takes a folder as input and creates an archive for each subfolder within that folder. The script should name the archives based on the subfolder names.
7. Compress a folder using tar and `gzip`, then decompress it using the same tools. Time how long each operation takes and compare the results.
8. Create a compressed archive of a folder containing various file types (e.g., text files, images, audio files). Use the `file` command to determine the types of files in the compressed archive without extracting it.
9. Write a script that finds the largest file in a directory and compresses it using `gzip`. The script should display the file name and its size before and after compression.
