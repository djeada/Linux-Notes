## File System Metadata and Links

Inodes are critical as they store essential metadata about files, such as permissions and locations, allowing efficient file system management. Hard links are important because they let multiple file names point to the same inode, saving disk space by avoiding data duplication. Symlinks provide flexibility by creating references to files or directories, allowing for easier access and organization without duplicating the actual content. Together, these structures optimize storage, file access, and navigation in file systems.

### Inodes

An inode (short for "index node") is a fundamental concept in many filesystems, serving as a data structure that describes a file or a directory. Each inode contains crucial metadata about a file, but not the file's actual data.

```
+---------------------+          +-----------------------+
|      Directory      |          |      Inode            |
| (Directory Entry)   |          | (Metadata & Pointers) |
+---------------------+          +-----------------------+
| Filename: "file.txt"|   ---->  | Inode Number: 1234    |
| Inode Number: 1234  |          | Permissions: 0644     |
+---------------------+          | Owner UID: 1000       |
                                 | Size: 2048 bytes      |
                                 | Timestamps: ...       |
                                 | Pointers:             |
                                 |  +---------+          |
                                 |  | Block 1 |--+       |
                                 |  +---------+  |       |
                                 |               |       |
                                 |  +---------+  |       |
                                 |  | Block 2 |<-+       |
                                 |  +---------+          |
                                 +-----------------------+
```

Main idea:

- An inode stores essential metadata such as the file's owner, permissions, size, timestamps (creation, modification, and last accessed), and pointers to the file's data blocks.
- Every file or directory has a unique inode number within a given filesystem. This number helps the system efficiently manage and locate the file's data.
- Multiple filenames can point to the same inode (hard links).
- The number of inodes is fixed when the file system is created, limiting the number of files.
- When a file is deleted, the inode and data blocks are freed if no other links point to it.
- The **directory entry** contains the filename and the inode number.
- The **inode** stores metadata and pointers to the data blocks.
- The actual **data blocks** (Block 1, Block 2, etc.) contain the file's content.

To view the inode number and other details of files in a directory, use the `ls -li` command. The first column in the output displays the inode number. 

```
$ ls -li
total 8
684867 -rw-r--r-- 1 user user  41 Mar  1 12:34 file1
684868 -rw-r--r-- 1 user user  41 Mar  1 12:34 file2
684869 -rw-r--r-- 1 user user  41 Mar  1 12:34 file3
```

Here, the inode numbers for `file1`, `file2`, and `file3` are `684867`, `684868`, and `684869`.

For more detailed inode information about a particular file, use the `stat` command:

```
$ stat file1
  File: file1
  Size: 41        	Blocks: 8          IO Block: 4096   regular file
Device: 806h/2054d	Inode: 684867      Links: 1
Access: (0644/-rw-rw-r--)  Uid: ( 1000/    adam)   Gid: ( 1000/    adam)
```

An inode stores various types of metadata, but does not store the filename or the file's content. The breakdown of the inode metadata is as follows:

```
Inode Number: 1234
+--------------------------------+
| File Type and Permissions      |
| User ID (Owner)                |
| Group ID                       |
| File Size                      |
| Access Time                    |
| Modification Time              |
| Change Time                    |
| Block Pointers:                |
|  - Direct Blocks               |
|  - Single Indirect Block       |
|  - Double Indirect Block       |
|  - Triple Indirect Block       |
+--------------------------------+
```

- **Permissions** define the access rights for the file, such as read, write, and execute permissions for the owner, group, and others.
- **Owner UID** identifies the user who owns the file.
- **File size** is the total size of the file in bytes.
- **Timestamps** include the access time, modification time, and change time for the file.
- The inode does not store the actual content of the file but contains **pointers** that indicate the location of the file's data blocks on the disk. These pointers direct the system to the specific blocks where the file's data is stored.

### Hardlinks

A hardlink creates an additional reference to the existing inode of a file. It's essentially another name for an existing file on the same filesystem.

I. Use the `ln` command to crea a hardlink:

```
ln existing_file hardlink_name
```

II. Deleting a hardlink leaves the original file untouched. However, if you delete the source file, all its hardlinks will still point to its content, as they all reference the same inode.

```
+----------------------+      +-----------------------+
|  Directory Entry 1   |      |  Directory Entry 2    |
| Filename: "file1.txt"|      | Filename: "file2.txt" |
| Inode Number: 1234   |      | Inode Number: 1234    |
+----------------------+      +-----------------------+
                \                 /
                 \               /
                  \             /
                   \           /
                 +-------------------+
                 |      Inode 1234   |
                 | (File Metadata)   |
                 +-------------------+
```

- Both "file1.txt" and "file2.txt" point to the same inode (1234).
- They are indistinguishable at the file content level.
- Deleting one link does not delete the inode until all links are removed.

### Symlinks (Symbolic Links)

Symlinks are special pointers that reference the path to another file or directory.

I. Unlike hardlinks, symlinks can point to objects across different filesystems or even non-existent targets.

II. Use the `ln -s` command to create a symlink:

```
ln -s existing_file symlink_name
```

III. To determine the target of a symlink, use the `readlink -f` command:

```
readlink -f symlink_name
```

IV. Deleting the symlink doesn't affect the target, but if the target file or directory is removed, the symlink becomes a "dangling link", pointing to a non-existent location.

```
+-----------------------+         +-----------------------+
|    Symlink File       |  ---->  |    Target File        |
| Filename: "link.txt"  |         | Filename: "file.txt"  |
| Inode Number: 5678    |         | Inode Number: 1234    |
+-----------------------+         +-----------------------+
| Inode 5678 contains:  |         | Inode 1234 (Metadata) |
| Path to "file.txt"    |         +-----------------------+
+-----------------------+
```

- The symlink "link.txt" has its own inode (5678) and contains the path to "file.txt".
- Accessing "link.txt" redirects to "file.txt".
- If "file.txt" is deleted, "link.txt" becomes a broken link.

### Key Differences Between Hardlinks and Symlinks

| Feature                                        | Hardlink                | Symlink                              |
| ---------------------------------------------- | ----------------------- | ------------------------------------ |
| Points across different filesystems            | No                      | Yes                                  |
| Affected by changes to its target's attributes | Yes (Shares same inode) | No (Points to a path, not an inode) |
| Points to non-existent files                   | No                      | Yes (Can create "dangling links")    |
| Reference                                      | Inode of the target     | Path to the target                   |

### Challenges

1. Create a text file named `myfile.txt` in a directory. In another directory, create a hard link to `myfile.txt` called `myhardlink`. Delete `myhardlink` and observe what happens to the original `myfile.txt`. Reflect on whether `myfile.txt` is still accessible and why hard links work this way.
2. Create a text file named `inodefile.txt`. Then, in the same directory, create a symlink to `inodefile.txt` named `symlink_to_inodefile`. Use `ls -li` to display the inode numbers for both files and compare them. Discuss why the inode numbers are different and how symlinks are managed differently from hard links.
3. Navigate to the `/lib` folder and use the `ls -l` command to list all files, identifying which ones are symlinks. Distinguish between hard links and symlinks, using link count and symbolic link indicators. Explain how you identified each type and what they reveal about the library files.
4. Create a text file named `original.txt` and a symlink to it named `dangling_symlink`. Delete `original.txt` and try to access `dangling_symlink`. Discuss what happens and why the symlink is now considered "dangling."
5. Research whether it’s possible for a filesystem to run out of inodes even if there is still disk space available. Explain the circumstances in which this could happen and why inode availability is essential for file storage.
6. Try creating a hard link to a directory. Document what happens and explain why most filesystems do not allow hard links to directories, considering potential risks or technical limitations.
7. Create a text file named `multi.txt` and make three hard links to it in different locations. Modify the contents of `multi.txt` and check the content of all three hard links. Describe your observations and explain how hard links reflect changes to the original file.
8. Use the `ls` command with a flag that shows the file type for each item in the `/etc` directory. Identify the flag to use and describe the indicators for different types of items (regular files, directories, symlinks, etc.).
9. Create two text files, `fileA.txt` and `fileB.txt`. Then create a symlink named `mylink` that points to `fileA.txt`. Without deleting `mylink`, change its target to `fileB.txt` and explain the process you used. Discuss how this method avoids recreating the symlink.
10. Research the typical space consumption of an inode on a filesystem. Explain how inode size can vary based on the filesystem and why inode space consumption is an important factor in filesystem design.
