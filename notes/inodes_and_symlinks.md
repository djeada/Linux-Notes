## The Inode

Inodes are parts of a filesystem that store information about a file, like who owns it, permissions, size, and when it was last accessed or changed. Inodes are saved on disk and help find the data blocks for a file.

To see inodes for files in a folder, use `ls -li`. The first column shows the inode number, and the third column shows the hardlink count, or the number of names linked to the same inode.

Example:

```
$ ls -li
total 8
684867 -rw-r--r-- 1 user user  41 Mar  1 12:34 file1
684868 -rw-r--r-- 1 user user  41 Mar  1 12:34 file2
684869 -rw-r--r-- 1 user user  41 Mar  1 12:34 file3
```

Here, the inode numbers for `file1`, `file2`, and `file3` are `684867`, `684868`, and `684869`.

Use `stat` to see inode information for a specific file or folder:

```
$ stat file1
  File: file1
  Size: 41        	Blocks: 8          IO Block: 4096   regular file
Device: 806h/2054d	Inode: 684867      Links: 1
Access: (0644/-rw-rw-r--)  Uid: ( 1000/    adam)   Gid: ( 1000/    adam)
```

## Hardlinks

A hardlink is another name for a file on the same filesystem. Hardlinks let a file have multiple names and be in different places on the same filesystem.

Create a hardlink using `ln`:

```
ln existing_file hardlink_name
```

Deleting a hardlink doesn't affect the original file or other hardlinks. But if you delete the original file, all hardlinks become invalid because they can't access the file's data blocks.

## Symlinks

A symlink is a special file that has a reference to another file or folder. Unlike hardlinks, symlinks can point to files or folders on other filesystems or even non-existent files.

Create a symlink using `ln -s`:

```
ln -s existing_file symlink_name
```

Deleting a symlink doesn't affect the file or folder it points to. But if you delete the file or folder it points to, the symlink becomes invalid.

Find the source file or folder for a symlink using `readlink -f`:

```
readlink -f symlink_name
```

## Differences

Here's a summary of differences between hardlinks and symlinks:

| Feature | Hardlink | Symlink |
| --- | --- | --- |
| Can point to file or folder on another filesystem | No | Yes | 
| Changing link's names or attributes affects source | Yes | No |
| Can link to any file or folder | No | Yes |

## Challenges

1. Make a text file and a hard link to it in another folder. Remove the hard link. What happened to the original file?
2. Show the inode number of a file and its symlinks. Is there a difference?
3. Find any links in the `/lib` folder. Hint: Use the `ls` command.

