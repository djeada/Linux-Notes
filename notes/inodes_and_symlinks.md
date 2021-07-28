<h1>The Inode</h1>

The inode is a filesystem object that contains details about:
* the user and group that owns a file, 
* the file's permissions, 
* size, 
* timestamps with the last file's access and its modifications.


```bash
ls -i
```

* first column - inode number
* third column - hardlink counter

<h1>Hardlink</h1>
The same file can have different name and appear in different places.

```bash
ln existing_file hardlink_name
```

<h1>Symlink</h1>

It is a file that points to another file.

```bash
ln -s existing_file symlink_name
```

Identifying the source file of a symbolic link.

```bash
readlink -f symlink_name
```

<h1>Differences</h1>

| Feature | Hardlink | Symlink |
| --- | --- | --- |
| can be pointed to a file on another filesystem  | no | yes | 
| changing link's names and attributes affects the source | yes | no |
| can link to any directory | no | yes |
