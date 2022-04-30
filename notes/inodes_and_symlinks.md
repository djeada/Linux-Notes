## The Inode

The inode is a filesystem object that contains details about:
* the user and group that owns a file, 
* the file's permissions, 
* size, 
* timestamps with the last file's access and its modifications.


```bash
ls -li
```

* first column - inode number
* third column - hardlink counter

## Hardlink
The same file can have different name and appear in different places.

```bash
ln existing_file hardlink_name
```

## Symlink

It is a file that points to another file.

```bash
ln -s existing_file symlink_name
```

To identify the source file of a symbolic link, use:

```bash
readlink -f symlink_name
```

## Differences

| Feature | Hardlink | Symlink |
| --- | --- | --- |
| can be pointed to a file on another filesystem  | no | yes | 
| changing link's names and attributes affects the source | yes | no |
| can link to any directory | no | yes |


## Challanges

1. Create a text file and a hard link to it in another directory. Remove the hard link. What has happened to the original file?
1. Display the inode number of any file and its symlinks. Is there a difference?
1. Look for any links in the /lib directory. Make use of the <code>ls</code> command. 
