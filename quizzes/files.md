# Files Quiz

Notes: [Files and Directories](../notes/files_and_dirs.md), [Disk Usage](../notes/disk_usage.md), [Inodes and Symlinks](../notes/inodes_and_symlinks.md), [Finding Files](../notes/finding_files.md)

Check your understanding of paths, file manipulation, globbing, `rsync`, disk usage, quotas, inodes and links.

#### Q. Which of these is an absolute path?

* [ ] `notes/file_name.txt`
* [x] `/home/user/notes/file_name.txt`
* [ ] `./notes/file_name.txt`
* [ ] `../user/notes/file_name.txt`

> **Explanation:** An absolute path starts at the root directory `/`, so it points to the same place no matter where you are. The others are relative paths resolved from the current working directory.

#### Q. How can you recognize a hidden file in a Linux directory listing?

* [ ] It has no read permission for others
* [ ] It is owned by the root user
* [x] Its name begins with a dot (`.`)
* [ ] It is stored under `/tmp`

> **Explanation:** By convention any file whose name starts with `.` (such as `.bashrc`) is hidden from a plain `ls`. Permissions and ownership have nothing to do with it; `ls -a` reveals these files.

#### Q. Which command lists all files, including hidden ones, in long format with permissions, owner and size?

* [ ] `ls -l`
* [ ] `ls -a`
* [x] `ls -al`
* [ ] `ls -lh`

> **Explanation:** `-a` includes entries starting with a dot and `-l` gives the long format. `ls -l` alone hides dotfiles, and `ls -lh` only changes how sizes are printed.

#### Q. You run `cp project /backup/` where `project` is a directory. What happens?

* [ ] The directory and all its contents are copied to `/backup/project`
* [x] `cp` skips it with a message that `-r` was not specified
* [ ] Only the files at the top level of `project` are copied
* [ ] An empty directory named `project` is created in `/backup`

> **Explanation:** Without `-r` (or `-a`), `cp` refuses to copy directories and prints `-r not specified; omitting directory 'project'`. Use `cp -r project /backup/` to copy the whole tree.

#### Q. Which `cp` command copies the directory `project` recursively while preserving permissions, timestamps and symbolic links?

* [ ] `cp -r project /backup/`
* [ ] `cp -v project /backup/`
* [ ] `cp -i project /backup/`
* [x] `cp -a project /backup/`

> **Explanation:** `-a` (archive) recurses and preserves attributes and symlinks. `-r` recurses but gives the copies new timestamps and default ownership, `-v` only prints progress, and `-i` only prompts before overwriting.

#### Q. Which command copies `file.txt` into `/backup/` but asks for confirmation before overwriting an existing file?

* [ ] `cp -f file.txt /backup/`
* [x] `cp -i file.txt /backup/`
* [ ] `cp -p file.txt /backup/`
* [ ] `cp -u file.txt /backup/`

> **Explanation:** `-i` (interactive) prompts before overwriting. `-f` forces the copy, `-p` preserves mode and timestamps, and `-u` copies only when the source is newer, none of which ask first.

#### Q. What does `mv oldname.txt newname.txt` do when both names are in the same directory?

* [ ] Copies the file and keeps both names
* [x] Renames the file
* [ ] Fails because `mv` only moves files between directories
* [ ] Creates a hard link called `newname.txt`

> **Explanation:** `mv` both moves and renames. Within one filesystem it just changes the directory entry, so the data and inode stay the same and `oldname.txt` no longer exists afterwards.

#### Q. Which command removes the directory `old_logs` together with everything inside it?

* [ ] `rm old_logs`
* [ ] `rmdir old_logs`
* [x] `rm -r old_logs`
* [ ] `rm -r old_logs/*`

> **Explanation:** `rm -r` recurses into the directory and deletes it with its contents. Plain `rm` refuses to remove directories, `rmdir` only removes empty ones, and `old_logs/*` leaves the directory itself (and its hidden files) behind.

#### Q. What does adding `-f` to `rm -r` change?

* [ ] It makes `rm` descend into subdirectories
* [ ] It moves the files to a trash folder instead of deleting them
* [ ] It overwrites the file data before deleting it
* [x] It never prompts and ignores files that do not exist

> **Explanation:** `-f` (force) suppresses confirmation prompts and errors about missing files. Recursion comes from `-r`; `rm` has no trash and does not securely erase data, which is why `rm -rf` must be used with care.

#### Q. How many files does this command create?

```bash
touch file{1..4}{a..f}
```

* [ ] 10
* [x] 24
* [ ] 4
* [ ] 6

> **Explanation:** Brace expansion produces every combination: 4 numbers times 6 letters gives 24 names, `file1a` through `file4f`, and `touch` creates each one.

#### Q. What does this brace expansion print?

```bash
echo a{b,c}d
```

* [x] `abd acd`
* [ ] `abcd`
* [ ] `a{b,c}d`
* [ ] `ab cd`

> **Explanation:** Brace expansion turns `{b,c}` into two words and attaches the prefix `a` and suffix `d` to each, giving `abd` and `acd`.

#### Q. What does this nested brace expansion print?

```bash
echo {A,B{1..3},C}
```

* [ ] `A B C 1 2 3`
* [ ] `A B1 C B2 B3`
* [x] `A B1 B2 B3 C`
* [ ] `AB1C AB2C AB3C`

> **Explanation:** The inner range `{1..3}` expands with the prefix `B` to `B1 B2 B3`, and those words sit in the outer list between `A` and `C`.

#### Q. In a directory containing `file.txt`, `file1.txt` and `file12.txt`, which files does `ls file?.txt` list?

* [ ] `file.txt` and `file1.txt`
* [x] Only `file1.txt`
* [ ] `file1.txt` and `file12.txt`
* [ ] All three files

> **Explanation:** In a glob, `?` matches exactly one character. `file.txt` has none in that position and `file12.txt` has two, so only `file1.txt` matches.

#### Q. Which filename is matched by the glob `file[12].txt`?

* [ ] `file3.txt`
* [ ] `file12.txt`
* [ ] `file_1.txt`
* [x] `file2.txt`

> **Explanation:** `[12]` matches a single character that is either `1` or `2`. `file12.txt` would need two characters in that position, and `3` or `_` are not in the set.

#### Q. In Bash with default settings, what does `echo *.txt` print in a directory that contains no `.txt` files?

* [ ] An empty line
* [ ] An error saying no files were found
* [x] The literal text `*.txt`
* [ ] The names of all files in the directory

> **Explanation:** Globs only match existing files. When nothing matches, Bash leaves the pattern unchanged (unless `nullglob` or `failglob` is set), so `echo` prints `*.txt`. Brace expansion, by contrast, always generates its words.

#### Q. In a shell glob, what does `?` match?

* [ ] Zero or one occurrence of the preceding character
* [x] Exactly one character of any kind
* [ ] Any number of characters, including none
* [ ] Only a literal question mark

> **Explanation:** In globs `?` is a one-character wildcard. "Zero or one of the preceding element" is its meaning in regular expressions, as in `colou?r`, and "any number of characters" is what `*` does in a glob.

#### Q. While viewing a file with `more`, what does pressing Enter do?

* [ ] Scrolls forward one full screen
* [x] Scrolls forward one line
* [ ] Scrolls back one screen
* [ ] Jumps to the next search match

> **Explanation:** Enter advances one line and Space advances one page. Scrolling backward and search are better handled in `less`, which supports full navigation in both directions.

#### Q. Which key quits both the `more` and `less` pagers?

* [ ] `x`
* [ ] `e`
* [x] `q`
* [ ] `w`

> **Explanation:** `q` exits either pager and returns you to the shell. In `less`, `e` and `w` are navigation keys, and `x` is not a quit command in either program.

#### Q. Why is `less` usually a better choice than `cat` for reading a very large log file?

* [x] It shows one screen at a time and lets you scroll backward and search
* [ ] It compresses the file so it loads faster
* [ ] It shows only the last 10 lines of the file
* [ ] It lets you edit the file in place

> **Explanation:** `cat` dumps the whole file to the terminal at once. `less` pages the content, supports backward movement and `/pattern` searches, and does not modify the file.

#### Q. How many lines does `head file.txt` print when no option is given?

* [ ] 5
* [ ] 20
* [ ] 25
* [x] 10

> **Explanation:** Both `head` and `tail` default to 10 lines. Use `-n` to choose another count, for example `head -n 3 file.txt`.

#### Q. What does `tail -n +2 data.csv` output?

* [ ] The last 2 lines of the file
* [x] Every line from line 2 to the end, skipping the header line
* [ ] Only line 2 of the file
* [ ] The file with every second line removed

> **Explanation:** A leading `+` makes `tail` start output at that line number instead of counting from the end. It is a common way to drop a CSV header.

#### Q. Which lines of `data.csv` does this pipeline print?

```bash
tail -n +50 data.csv | head -n 11
```

* [ ] Lines 39 to 50
* [ ] Lines 50 to 61
* [x] Lines 50 to 60
* [ ] The last 50 lines, then the first 11 lines

> **Explanation:** `tail -n +50` starts output at line 50 and `head -n 11` keeps the next 11 lines, which are lines 50 through 60.

#### Q. What is the effect of the trailing slash on the source in `rsync -av /home/user/documents/ /mnt/backup/documents/`?

* [ ] It makes `rsync` follow symbolic links
* [ ] It makes `rsync` delete files missing from the source
* [x] It copies the contents of `documents` rather than creating a nested `documents/documents`
* [ ] It makes the transfer recursive

> **Explanation:** With a trailing `/`, `rsync` copies what is inside the source directory. Without it, the directory itself is copied into the destination, producing an extra nested folder.

#### Q. Which command makes `/dest/` an exact mirror of `/src/`, removing files that no longer exist in the source?

* [ ] `rsync -az /src/ /dest/`
* [x] `rsync -a --delete /src/ /dest/`
* [ ] `rsync -a --dry-run /src/ /dest/`
* [ ] `rsync -aP /src/ /dest/`

> **Explanation:** `--delete` removes destination files that are absent from the source. Without it `rsync` only adds and updates files; `--dry-run` changes nothing and `-P` only shows progress.

#### Q. What does `rsync --dry-run` (`-n`) do?

* [ ] Copies only files whose checksums differ
* [ ] Transfers files without compression
* [x] Shows what would be transferred without changing anything
* [ ] Deletes extra files in the destination

> **Explanation:** A dry run simulates the transfer and lists the actions. It is a good habit before a run that uses `--delete`.

#### Q. Which `rsync` option compresses data during the transfer to save bandwidth?

* [x] `-z`
* [ ] `-a`
* [ ] `-v`
* [ ] `-n`

> **Explanation:** `-z` compresses data in transit, which helps over slow links such as SSH to a remote host. `-a` is archive mode, `-v` is verbose and `-n` is a dry run.

#### Q. A large `rsync` transfer keeps getting interrupted. Which option shows per-file progress and keeps partially transferred files so the next run can resume?

* [ ] `-z`
* [ ] `--delete`
* [ ] `--exclude`
* [x] `-P`

> **Explanation:** `-P` combines `--progress` and `--partial`, so you can watch each file and avoid restarting large files from zero after an interruption.

#### Q. Why is `rsync` usually preferred over `cp` for repeated backups of the same directory?

* [ ] It always compresses files stored on the destination
* [x] It transfers only the differences between source and destination
* [ ] It can copy files that `cp` is not permitted to read
* [ ] It keeps old versions of every changed file

> **Explanation:** `rsync` compares source and destination and skips what is already up to date, so later runs are much faster. It does not bypass permissions or keep version history by itself.

#### Q. What is the main difference between `df` and `du`?

* [ ] `df` counts files, while `du` counts directories
* [ ] `df` works only on the root filesystem, while `du` works on any filesystem
* [ ] `df` shows memory usage, while `du` shows disk usage
* [x] `df` reports usage per mounted filesystem, while `du` estimates space used by given files and directories

> **Explanation:** `df` asks each mounted filesystem for its size, used and available space. `du` walks a directory tree and adds up what the files occupy, which is how you find space hogs.

#### Q. Which command prints a human-readable size summary for each file and directory in the current directory?

* [ ] `df -h .`
* [x] `du -sh *`
* [ ] `ls -h`
* [ ] `du -h /`

> **Explanation:** `du -s` gives one total per argument and `-h` uses K, M and G units; the glob passes each item as an argument. `df -h .` reports the whole filesystem, not individual items.

#### Q. When running `du` on `/`, which option keeps it from descending into other mounted filesystems such as `/proc` or a network share?

* [ ] `-s`
* [ ] `-a`
* [x] `-x`
* [ ] `-c`

> **Explanation:** `-x` (`--one-file-system`) skips directories on different filesystems. `-s` summarizes, `-a` lists files too and `-c` prints a grand total.

#### Q. Why should you use `sort -h` rather than `sort -n` on the output of `du -sh *`?

* [ ] `sort -n` cannot read tab-separated input
* [ ] `sort -h` is faster on large inputs
* [ ] `sort -n` sorts in reverse order by default
* [x] `sort -n` ignores unit suffixes, so `900K` would sort above `2.0G`

> **Explanation:** `-n` compares only the leading number (900 versus 2.0). `-h` understands human-readable suffixes, so `du -sh * | sort -hr` correctly lists the largest items first.

#### Q. Creating a file fails with "No space left on device", yet `df -h` shows the filesystem only 40% full. What should you check next?

* [ ] `free -h`, because RAM may be full
* [x] `df -i`, because the filesystem may have run out of inodes
* [ ] `du -sh /tmp`, because temporary files are not counted by `df`
* [ ] `ls -l`, because the directory may be read-only

> **Explanation:** Every file needs an inode. On filesystems with a fixed inode count, such as ext4, millions of tiny files can use them all while blocks remain free. `df -i` shows inode usage.

#### Q. You delete a 10 GB log file with `rm`, but `df` shows no space was freed. What is the most likely reason?

* [x] A running process still has the file open
* [ ] `rm` only removes the filename after a reboot
* [ ] `df` caches its results for an hour
* [ ] Log files are always stored in a reserved area

> **Explanation:** `rm` removes the name, but the inode and data are kept until every open file descriptor is closed. Restarting the process that writes the log releases the space.

#### Q. With disk quotas, what distinguishes a soft limit from a hard limit?

* [ ] The soft limit applies to inodes and the hard limit applies to blocks
* [ ] The soft limit applies to groups and the hard limit applies to users
* [x] The soft limit can be exceeded for a grace period; the hard limit can never be exceeded
* [ ] The soft limit only produces log entries and is never enforced

> **Explanation:** A user above the soft limit gets a grace period (set with `edquota -t`) before writes are refused. The hard limit is an absolute ceiling. Both block and inode limits have soft and hard values.

#### Q. Which mount options must be added to a filesystem's `/etc/fstab` entry to enable user and group quotas?

* [ ] `quota=on`
* [x] `usrquota,grpquota`
* [ ] `uquota,acl`
* [ ] `limits`

> **Explanation:** After adding `usrquota,grpquota` and remounting, `quotacheck -cug` creates the quota files and `quotaon` starts enforcement.

#### Q. Which command opens an editor to set the soft and hard quota limits for user `alice`?

* [ ] `quota -u alice`
* [ ] `repquota alice`
* [ ] `quotaon alice`
* [x] `edquota -u alice`

> **Explanation:** `edquota` edits limits. `quota -u` only displays a user's usage, `repquota` reports on all users of a filesystem, and `quotaon` turns enforcement on for a filesystem.

#### Q. Which piece of information is stored in the directory entry rather than in the file's inode?

* [ ] The file's permissions
* [ ] The owner's UID
* [x] The filename
* [ ] The modification time

> **Explanation:** A directory entry maps a name to an inode number; the inode holds the metadata and data block pointers but not the name. That is why one inode can have several names (hard links).

#### Q. Which command shows each file's inode number in the first column?

* [ ] `ls -n`
* [x] `ls -li`
* [ ] `ls -s`
* [ ] `ls -F`

> **Explanation:** `-i` prints inode numbers, and `-l` adds the long listing. `-n` shows numeric UIDs and GIDs, `-s` shows allocated blocks and `-F` appends type indicators.

#### Q. What does a file's `ctime` record?

* [x] When its inode metadata (or content) last changed
* [ ] When the file was created
* [ ] When the file was last read
* [ ] When the file was last copied

> **Explanation:** `ctime` is the status change time, updated by changes such as `chmod`, `chown` or writing to the file. It is not creation time; reads update `atime` and content changes update `mtime`.

#### Q. You run `ln report.txt copy.txt` and then delete `report.txt`. What happens to `copy.txt`?

* [ ] It becomes a broken link
* [x] It still works and shows the same content
* [ ] It is deleted as well
* [ ] It becomes an empty file

> **Explanation:** Without `-s`, `ln` creates a hard link, a second name for the same inode. The data is kept until the last name is removed, so `copy.txt` is unaffected.

#### Q. Right after running `ln report.txt copy.txt`, what link count does `stat report.txt` show?

* [ ] 0
* [ ] 1
* [x] 2
* [ ] 3

> **Explanation:** The inode now has two directory entries pointing at it, so its link count is 2. A symlink would not change the target's link count.

#### Q. Why does `ln /mnt/usb/data.txt ~/data.txt` fail when `/mnt/usb` is a separate filesystem?

* [ ] Hard links require root privileges
* [ ] Hard links only work for files in the same directory
* [ ] USB drives do not support links of any kind
* [x] A hard link refers to an inode number, which is only meaningful within one filesystem

> **Explanation:** Inode numbers are unique only within a filesystem, so hard links cannot cross filesystems (error: invalid cross-device link). A symbolic link, which stores a path, works instead.

#### Q. What happens to a symbolic link when its target file is deleted?

* [ ] The symlink is deleted automatically
* [ ] The symlink keeps a copy of the target's data
* [x] The symlink remains but is dangling and fails when accessed
* [ ] The system refuses to delete the target

> **Explanation:** A symlink stores only a path. Once nothing exists at that path, opening the link gives "No such file or directory", although the link itself is still listed.

#### Q. The symlink `/opt/app/current` stores the relative target `releases/v2`. Where does the system look for that target?

* [ ] In the current working directory of the process using the link
* [x] In `/opt/app`, the directory that contains the symlink
* [ ] In the user's home directory
* [ ] In `/`, the root directory

> **Explanation:** Relative symlink targets are resolved from the directory containing the link, so this one points to `/opt/app/releases/v2` no matter where you run commands from.

#### Q. Which command prints the fully resolved, canonical absolute path that the symlink `mylink` points to?

* [ ] `readlink mylink`
* [x] `readlink -f mylink`
* [ ] `ls -i mylink`
* [ ] `stat -L mylink`

> **Explanation:** `readlink -f` follows every link in the chain and prints an absolute path. Plain `readlink` prints the stored target text, which may be relative.

#### Q. The symlink `mylink` currently points to `fileA.txt`. Which command makes it point to `fileB.txt` instead?

* [ ] `ln -s fileB.txt mylink`
* [ ] `ln fileB.txt mylink`
* [x] `ln -sfn fileB.txt mylink`
* [ ] `readlink -f fileB.txt mylink`

> **Explanation:** A symlink cannot be edited in place. `-f` replaces the existing link and `-n` stops `ln` from descending into `mylink` if it points to a directory. Without `-f`, `ln` fails with "File exists".

#### Q. Which command finds `.log` files under `/var` whose contents were modified within the last 7 days?

* [ ] `find /var -name "*.log" -mtime +7`
* [ ] `find /var -name "*.log" -atime -7`
* [ ] `find /var -name "*.log" -mmin -7`
* [x] `find /var -name "*.log" -mtime -7`

> **Explanation:** `-mtime -7` means modified less than 7 days ago; `+7` means more than 7 days ago. `-atime` checks access time and `-mmin` counts minutes, not days.

#### Q. What does `find . -type f -newer file2` list?

* [ ] Files created after `file2` was first created
* [x] Regular files modified more recently than `file2`
* [ ] Files that are larger than `file2`
* [ ] Files with a higher inode number than `file2`

> **Explanation:** `-newer` compares modification times against the reference file. Adding `-type f` restricts results to regular files.

#### Q. You create `report.txt` and immediately run `locate report.txt`, but it finds nothing. Why?

* [ ] `locate` only searches the current directory
* [ ] `locate` needs the `-i` option for exact names
* [ ] `locate` ignores files owned by regular users
* [x] `locate` searches a prebuilt database that has not been updated yet

> **Explanation:** `locate` is fast because it queries a database built by `updatedb`, which usually runs periodically. Newly created files appear after the next update; `find` searches the live filesystem.
