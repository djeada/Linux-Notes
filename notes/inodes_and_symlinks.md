## The Inode

The inode is a filesystem object that contains detailed information about a file, such as the user and group ownership, file permissions, size, and timestamps for the last file access and modification. Inodes are stored on disk and are used to locate the data blocks for a file.

To view the inodes for the files in a directory, you can use the `ls -li` command. The first column of the output shows the inode number, and the third column shows the hardlink count, which is the number of names that are linked to the same inode.

For example:

```
$ ls -li
total 8
684867 -rw-r--r-- 1 user user  41 Mar  1 12:34 file1
684868 -rw-r--r-- 1 user user  41 Mar  1 12:34 file2
684869 -rw-r--r-- 1 user user  41 Mar  1 12:34 file3
```

In this example, the inode numbers for `file1`, `file2`, and `file3` are `684867`, `684868`, and `684869`, respectively.

In addition to the `ls` command, you can use the `stat` command to view the inode information for a specific file or directory. For example:

```
$ stat file1
  File: file1
  Size: 41        	Blocks: 8          IO Block: 4096   regular file
Device: 806h/2054d	Inode: 684867      Links: 1
Access: (0644/-rw-rw-r--)  Uid: ( 1000/    adam)   Gid: ( 1000/    adam)
```

## Hardlinks

A hardlink is a second name for an existing file that is stored on the same filesystem. Hardlinks allow a single file to have multiple names and appear in multiple locations within the same filesystem.

To create a hardlink, you can use the ln command and specify the existing file as the source and the desired hardlink name as the target:

```
ln existing_file hardlink_name
```

If you delete a hardlink, it does not affect the original file or any other hardlinks to the same file. However, if you delete the original file, all hardlinks to the file will become invalid, as they will no longer be able to access the file's data blocks.

## Symlinks

A symlink (short for "symbolic link") is a special type of file that contains a reference to another file or directory. Unlike a hardlink, a symlink can point to a file or directory on another filesystem or even to a non-existent file.

To create a symlink, you can use the `ln -s` command and specify the existing file or directory as the source and the desired symlink name as the target:

```
ln -s existing_file symlink_name
```

If you delete a symlink, it does not affect the file or directory that it points to. However, if you delete the file or directory that the symlink points to, the symlink will become invalid, as it will no longer be able to access the target file or directory.

To identify the source file or directory of a symbolic link, you can use the `readlink -f` command and specify the symlink name as the argument:

```
readlink -f symlink_name
```

## Differences

Here is a summary of the differences between hardlinks and symlinks:

| Feature | Hardlink | Symlink |
| --- | --- | --- |
| Can be pointed to a file or directory on another filesystem	  | No | Yes | 
| Changing the link's names or attributes affects the source | Yes | No |
| Can link to any file or directory | No | Yes |

## Challenges

1. Create a text file and a hard link to it in another directory. Remove the hard link. What has happened to the original file?
1. Display the inode number of any file and its symlinks. Is there a difference?
1. Look for any links in the `/lib` directory. Hint: Make use of the `ls` command.
