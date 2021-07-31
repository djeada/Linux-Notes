<h2>Types of items stored in UNIX filesystem </h2>

1. Ordinary files: Text, data, and code information can all be found in ordinary files. 
  Files and folders can not be contained within other files or directories. 
  Unlike other operating systems, UNIX filenames do not have a name and an extension .

1. Directories: In Linux, files are arranged into directories (analogous to folders in Windows). 
  The root directory is simply referred to as "/."
  Users' files are stored in their home folders, which are located in "/home/." For instance, "/home/adam/."

1. Devices: To provide applications simple access to hardware devices, UNIX permits them to be utilized in the same manner that regular files are. In UNIX, there are two sorts of devices: block-oriented devices that transport data in blocks (e.g., hard drives) and character-oriented devices that send data byte by byte (e.g. modems and dumb terminals).

1. Links: A link is a reference to another file. There are two kinds of links: hard links and soft links. A hard link to a file is indistinguishable from the file itself. A soft link (also known as a symbolic link) is an indirect pointer or shortcut to a file. A soft link is created as a directory file entry with a pathname.

<h2>Special directory names</h2> 

* “./” is a reference to the current directory;
* “../” is a reference  to the directory one level above the current directory; 
* “~/” is a reference  to your home directory.

<h2>File names</h2> 
Unlike Windows, Linux distinguishes between upper and lower case letters in file names.
That is, the file names "Test," "TEST," and "test" all refer to distinct files.

<h2>Hidden files</h2> 
Hidden files have filenames that begin with “.” (period). 
These are generally system files that do not appear when you list the contents of a directory. 

<h2>Permissions</h2>
Files are given "permissions" that specify who has access to them and what kind of access they have.
The three most basic forms of access are read, write, and execute. 
You can read the content of a file (e.g., make your own copy) if you have read access. 
You can remove, edit, or replace files with write access.
Execute access is necessary to run programs or access the contents of folders.


<h2>UNIX Directory Structure</h2>

| Command | Description |
| --- | --- |
| <i>/</i> | home directory |
| <i>/bin</i> | low-level system utilities |
| <i>/usr/bin</i> | system utilities for normal users |
| <i>/sbin</i> | system utilities for superusers |
| <i>/lib</i> | low-level system utility program libraries |
| <i>/usr/lib</i> | library programs for higher-level user programs |
| <i>/tmp</i> | storage for temporary files |
| <i>/home</i> | Each user's home directory has personal file space. Each directory is named after the user's login. |
| <i>/etc</i> | system configuration |
| <i>/dev</i> | info about hardware devices |

<h2>Second Extended File System (ext2)</h2>

* Maximum file size: 2 TB
* Maximum volume size: 4 TB
* File name size: 255 characters
* Supports: POSIX permissions and compression
* If a system shuts down unexpectedly, it takes an EXTREMELY LONG TIME to recover.

<h2>Second Extended File System (ext3)</h2>

* Does everything ext2 does (you can upgrade 2 to 3).
* It comes with a journal (before making a transaction it will describe it in the journal and mark it as incomplete). It is a lifesaver.
* Security over slightly slower I/O actions.

<h2>Reiser File System </h2>

* Uses journaling.
* Maximum file size: 8 TB
* Maximum volume size: 16 TB
* Faster than ext2 and ext3.

<h2>Fourth Extended File System (ext4)</h2>

* Maximum file size: 16 TB
* Maximum volume size: 1 exabyte
* Maximum number of files: 4 billion
* Maximum file name length: 255 characters
* Uses a journal.

