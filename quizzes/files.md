# Files Quiz

Notes: [Files and Directories](../notes/files_and_dirs.md), [Disk Usage](../notes/disk_usage.md), [Inodes and Symlinks](../notes/inodes_and_symlinks.md), [Finding Files](../notes/finding_files.md)

Check your understanding of paths, file manipulation, globbing, `rsync`, disk usage, quotas, inodes, links and finding files.

#### Q. Which of these is an absolute path?

* [ ] `notes/file_name.txt`
* [ ] `./notes/file_name.txt`
* [ ] `../user/notes/file_name.txt`
* [x] `/home/user/notes/file_name.txt`

> **Explanation:** An absolute path starts at the root directory `/`, so it points to the same place no matter where you are. The others are relative paths resolved from the current working directory.

#### Q. Your current directory is `/home/user/Documents`. Which relative path refers to `/home/user/notes/todo.txt`?

* [x] `../notes/todo.txt`
* [ ] `./notes/todo.txt`
* [ ] `notes/todo.txt`
* [ ] `../../notes/todo.txt`

> **Explanation:** `..` moves up one level to `/home/user`, and `notes/todo.txt` continues from there. `notes/...` and `./notes/...` look inside `Documents`, and `../..` climbs too far, to `/home`.

#### Q. How can you recognize a hidden file in a Linux directory listing?

* [ ] It has no read permission for others
* [ ] It is owned by the root user
* [x] Its name begins with a dot (`.`)
* [ ] It is stored under `/tmp`

> **Explanation:** By convention any file whose name starts with `.` (such as `.bashrc`) is hidden from a plain `ls`. Permissions and ownership have nothing to do with it; `ls -a` reveals these files.

#### Q. Which command lists all files, including hidden ones, in long format with permissions, owner and size?

* [ ] `ls -l`
* [x] `ls -al`
* [ ] `ls -a`
* [ ] `ls -lh`

> **Explanation:** `-a` includes entries starting with a dot and `-l` gives the long format. `ls -l` alone hides dotfiles, and `ls -lh` only changes how sizes are printed.

#### Q. `mkdir projects/2024/q1` fails with "No such file or directory" because `projects` does not exist yet. Which command creates the whole path?

* [x] `mkdir -p projects/2024/q1`
* [ ] `mkdir -r projects/2024/q1`
* [ ] `mkdir -m 755 projects/2024/q1`
* [ ] `touch projects/2024/q1`

> **Explanation:** `-p` creates every missing parent directory and does not complain if the path already exists. `mkdir` has no `-r` option, `-m` only sets the mode, and `touch` creates files, not directories.

#### Q. You run `cp project /backup/` where `project` is a directory. What happens?

* [x] `cp` skips it with a message that `-r` was not specified
* [ ] The directory and all its contents are copied to `/backup/project`
* [ ] Only the files at the top level of `project` are copied
* [ ] An empty directory named `project` is created in `/backup`

> **Explanation:** Without `-r` (or `-a`), GNU `cp` refuses to copy directories and prints `-r not specified; omitting directory 'project'`. Use `cp -r project /backup/` to copy the whole tree.

#### Q. Which `cp` command copies the directory `project` recursively while preserving permissions, timestamps and symbolic links?

* [ ] `cp -r project /backup/`
* [ ] `cp -v project /backup/`
* [ ] `cp -i project /backup/`
* [x] `cp -a project /backup/`

> **Explanation:** `-a` (archive) recurses and preserves mode, ownership, timestamps and symlinks. `-r` recurses but gives the copies new timestamps and the copying user's ownership, `-v` only prints progress, and `-i` only prompts before overwriting.

#### Q. Which command copies `file.txt` into `/backup/` but asks for confirmation before overwriting an existing file?

* [x] `cp -i file.txt /backup/`
* [ ] `cp -f file.txt /backup/`
* [ ] `cp -p file.txt /backup/`
* [ ] `cp -u file.txt /backup/`

> **Explanation:** `-i` (interactive) prompts before overwriting. `-f` forces the copy, `-p` preserves mode and timestamps, and `-u` copies only when the source is newer, none of which ask first.

#### Q. What does `mv oldname.txt newname.txt` do when both names are in the same directory?

* [x] Renames the file
* [ ] Copies the file and keeps both names
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
* [ ] 4
* [ ] 6
* [x] 24

> **Explanation:** Brace expansion produces every combination: 4 numbers times 6 letters gives 24 names, `file1a` through `file4f`, and `touch` creates each one.

#### Q. What does this command do?

```bash
cp config.yml{,.bak}
```

* [ ] It fails, because a brace list cannot contain an empty item
* [ ] It copies `config.yml` and a file named `.bak` into the current directory
* [x] It copies `config.yml` to a new file named `config.yml.bak`
* [ ] It creates a directory `config.yml` that contains `.bak`

> **Explanation:** Brace expansion runs before `cp` and turns the word into `config.yml config.yml.bak` (empty item, then `.bak`), so `cp` receives a source and a destination. It is a common shortcut for making a backup copy.

#### Q. What does this nested brace expansion print?

```bash
echo {A,B{1..3},C}
```

* [x] `A B1 B2 B3 C`
* [ ] `A B1 C B2 B3`
* [ ] `A B C 1 2 3`
* [ ] `AB1C AB2C AB3C`

> **Explanation:** The inner range `{1..3}` expands with the prefix `B` to `B1 B2 B3`, and those words sit in the outer list between `A` and `C`.

#### Q. In a directory containing `file.txt`, `file1.txt` and `file12.txt`, which files does `ls file?.txt` list?

* [x] Only `file1.txt`
* [ ] `file.txt` and `file1.txt`
* [ ] `file1.txt` and `file12.txt`
* [ ] All three files

> **Explanation:** In a glob, `?` matches exactly one character. `file.txt` has none in that position and `file12.txt` has two, so only `file1.txt` matches. In a regular expression, by contrast, `?` means "zero or one of the preceding element".

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

#### Q. A directory contains `.env`, `a.txt` and `b.log`. In Bash with default settings, what does `echo *` print?

* [ ] `.env a.txt b.log`
* [ ] `*`
* [ ] `.env`
* [x] `a.txt b.log`

> **Explanation:** A leading dot must be matched explicitly, so `*` skips hidden files (unless `dotglob` is set). That is also why `rm -r dir/*` leaves dotfiles behind; `.*` would match `.env`.

#### Q. While viewing a file with `more`, what does pressing Enter do?

* [x] Scrolls forward one line
* [ ] Scrolls forward one full screen
* [ ] Scrolls back one screen
* [ ] Jumps to the next search match

> **Explanation:** Enter advances one line and Space advances one page. Moving backward is limited in `more` (`b` works only on files, not pipes), while `less` supports full navigation in both directions.

#### Q. While reading a log in `less`, which keys search backward from the current position for the text `ERROR`?

* [ ] `/ERROR`
* [ ] `:ERROR`
* [x] `?ERROR`
* [ ] `bERROR`

> **Explanation:** In `less`, `/pattern` searches forward and `?pattern` searches backward; `n` repeats the last search. `b` scrolls back one page and is not a search command.

#### Q. Why is `less` usually a better choice than `cat` for reading a very large log file?

* [x] It shows one screen at a time and lets you scroll backward and search
* [ ] It compresses the file so it loads faster
* [ ] It shows only the last 10 lines of the file
* [ ] It lets you edit the file in place

> **Explanation:** `cat` dumps the whole file to the terminal at once. `less` pages the content, supports backward movement and `/pattern` searches, and does not modify the file.

#### Q. What does `head -n 2 a.txt b.txt` print?

* [ ] The first 2 lines of `a.txt` followed by those of `b.txt`, with no separator
* [ ] Only the first 2 lines of `a.txt`, because the second name is ignored
* [ ] An error, because `head` accepts only one file at a time
* [x] The first 2 lines of each file, each block preceded by a `==> name <==` header

> **Explanation:** With several files, `head` (and `tail`) prints a header line such as `==> a.txt <==` before each file's lines. Without `-n` the default is 10 lines; `-q` suppresses the headers.

#### Q. What does `tail -n +2 data.csv` output?

* [x] Every line from line 2 to the end, skipping the header line
* [ ] The last 2 lines of the file
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

#### Q. The directory `dest/` already exists. After running `rsync -a src dest/` (no trailing slash on `src`), where does the file `src/f1` end up?

* [x] `dest/src/f1`
* [ ] `dest/f1`
* [ ] `dest/src/src/f1`
* [ ] Nowhere; `rsync` requires a trailing slash on a directory source

> **Explanation:** Without a trailing slash, `rsync` copies the directory itself into the destination. `rsync -a src/ dest/` copies only the contents of `src`, so the file would land at `dest/f1`.

#### Q. Which command makes `/dest/` an exact mirror of `/src/`, removing files that no longer exist in the source?

* [ ] `rsync -az /src/ /dest/`
* [ ] `rsync -a --dry-run /src/ /dest/`
* [x] `rsync -a --delete /src/ /dest/`
* [ ] `rsync -aP /src/ /dest/`

> **Explanation:** `--delete` removes destination files that are absent from the source. Without it `rsync` only adds and updates files; `--dry-run` changes nothing and `-P` only shows progress.

#### Q. What does `rsync --dry-run` (`-n`) do?

* [ ] Copies only files whose checksums differ
* [x] Shows what would be transferred without changing anything
* [ ] Transfers files without compression
* [ ] Deletes extra files in the destination

> **Explanation:** A dry run simulates the transfer and lists the actions (add `-v` to see them). It is a good habit before a run that uses `--delete`.

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
* [ ] It can copy files that `cp` is not permitted to read
* [ ] It keeps old versions of every changed file
* [x] It skips files that are already up to date at the destination

> **Explanation:** `rsync` compares source and destination (by size and modification time by default) and transfers only what changed, so later runs are much faster. It does not bypass permissions or keep version history by itself.

#### Q. What is the main difference between `df` and `du`?

* [ ] `df` counts files, while `du` counts directories
* [x] `df` reports usage per filesystem, while `du` sums the given files and directories
* [ ] `df` reads only `/`, while `du` reads every mounted filesystem
* [ ] `df` reports memory usage, while `du` reports disk usage

> **Explanation:** `df` asks each mounted filesystem for its size, used and available space. `du` walks a directory tree and adds up what the files occupy, which is how you find space hogs.

#### Q. Which command prints a human-readable size summary for each file and directory in the current directory?

* [ ] `df -h .`
* [x] `du -sh *`
* [ ] `ls -h`
* [ ] `du -h /`

> **Explanation:** `du -s` gives one total per argument and `-h` uses K, M and G units; the glob passes each non-hidden item as an argument. `df -h .` reports the whole filesystem, not individual items.

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
* [x] `sort -n` ignores unit suffixes, so it treats `900K` as larger than `2.0G`

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

> **Explanation:** `rm` removes the name, but the inode and data are kept until every open file descriptor is closed. `lsof +L1` lists such deleted-but-open files; restarting the process that writes the log releases the space.

#### Q. With disk quotas, what distinguishes a soft limit from a hard limit?

* [ ] The soft limit applies to inodes and the hard limit applies to blocks
* [ ] The soft limit applies to groups and the hard limit applies to users
* [x] The soft limit can be exceeded for a grace period; the hard limit can never be exceeded
* [ ] The soft limit only produces log entries and is never enforced

> **Explanation:** A user above the soft limit gets a grace period (set with `edquota -t`) before writes are refused. The hard limit is an absolute ceiling. Both block and inode limits have soft and hard values.

#### Q. Which mount options must be added to an ext4 filesystem's `/etc/fstab` entry to enable user and group quotas?

* [ ] `quota=on`
* [x] `usrquota,grpquota`
* [ ] `uquota,acl`
* [ ] `limits`

> **Explanation:** After adding `usrquota,grpquota` and remounting, `quotacheck -cug` creates the quota files and `quotaon` starts enforcement. `uquota` is XFS's spelling for user quotas, and `acl` enables access control lists, not quotas.

#### Q. Which command opens an editor to set the soft and hard quota limits for user `alice`?

* [ ] `quota -u alice`
* [ ] `repquota alice`
* [ ] `quotaon alice`
* [x] `edquota -u alice`

> **Explanation:** `edquota` edits limits. `quota -u` only displays a user's usage, `repquota` reports on all users of a filesystem, and `quotaon` turns enforcement on for a filesystem.

#### Q. In `repquota /home` output, user bob's line shows `+-` right after his name. What does that mean?

* [ ] bob has exceeded both his block and inode hard limits
* [x] bob's block usage is over its soft limit, but his file count is not
* [ ] bob's block quota is disabled, but his inode quota is enabled
* [ ] bob is under every limit and his grace period was reset

> **Explanation:** The first character refers to block limits and the second to inode (file) limits; `+` means usage is above the soft limit. bob can keep writing until he hits the hard limit or the grace period shown in the grace column expires.

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

#### Q. You create a new file `report.txt` and then run `ln report.txt copy.txt`. What link count does `stat report.txt` show?

* [ ] 0
* [ ] 1
* [x] 2
* [ ] 3

> **Explanation:** The inode now has two directory entries pointing at it, so its link count is 2. A symlink would not change the target's link count.

#### Q. After `ln -s a.txt link`, what does `ls -li a.txt link` show?

* [ ] The same inode number for both names, and a link count of 2
* [x] Different inode numbers, and `a.txt` still has a link count of 1
* [ ] The same inode number, with `link` marked by an `l` type
* [ ] Only `a.txt`, because symlinks have no inode of their own

> **Explanation:** A symlink is a separate small file with its own inode that stores the path `a.txt`. It adds no directory entry for the target's inode, so the target's link count is unchanged.

#### Q. Why does `ln /mnt/usb/data.txt ~/data.txt` fail when `/mnt/usb` is a separate filesystem?

* [ ] Hard links require root privileges
* [ ] Hard links only work within one directory
* [ ] USB drives do not support links of any kind
* [x] Inode numbers are only meaningful within one filesystem

> **Explanation:** A hard link is a directory entry pointing at an inode number, and those are unique only within a filesystem, so `ln` fails with "Invalid cross-device link". A symbolic link, which stores a path, works instead.

#### Q. What happens when you run `ln dir1 dir2`, where `dir1` is a directory?

* [ ] `dir2` becomes a second name for `dir1`
* [x] `ln` refuses, because hard links to directories are not allowed
* [ ] `dir2` is created as a symbolic link to `dir1`
* [ ] `dir1` is copied recursively to `dir2`

> **Explanation:** GNU `ln` prints "hard link not allowed for directory". Directory hard links could create loops in the tree and confuse `..` and tools that walk it; use `ln -s dir1 dir2` for a second path to a directory.

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

> **Explanation:** `readlink -f` follows every link in the chain and prints an absolute path. Plain `readlink` prints the stored target text, which may be relative, and `stat -L` shows the target's metadata rather than its path.

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

#### Q. With GNU `find`, which files does `find . -type f -size +2000` match?

* [ ] Files larger than 2000 bytes
* [ ] Files larger than 2000 KiB
* [x] Files using more than 2000 blocks of 512 bytes (about 1 MB)
* [ ] Files containing more than 2000 lines

> **Explanation:** A `-size` number without a suffix counts 512-byte blocks, rounded up. Suffixes change the unit, for example `-size +10M` for more than 10 MiB or `c` for bytes.

#### Q. You want `find` to ask before deleting each matching `.bak` file. Which command does that?

* [ ] `find . -name "*.bak" -delete`
* [ ] `find . -name "*.bak" -exec rm {} \;`
* [x] `find . -name "*.bak" -ok rm {} \;`
* [ ] `find . -name "*.bak" -print -delete`

> **Explanation:** `-ok` works like `-exec` but prompts before each command and runs it only on a `y` answer. `-delete` and `-exec rm` remove matches without asking.

#### Q. You create `report.txt` and immediately run `locate report.txt`, but it finds nothing. Why?

* [ ] `locate` only searches the current directory
* [ ] `locate` needs the `-i` option for exact names
* [ ] `locate` ignores files owned by regular users
* [x] `locate` searches a prebuilt database that has not been updated yet

> **Explanation:** `locate` is fast because it queries a database built by `updatedb`, which usually runs periodically. Newly created files appear after the next update; `find` searches the live filesystem.

#### Q. In Bash, `ls` is an alias for `ls --color=auto`. Which command shows the alias as well as every `ls` executable found in `PATH`?

* [ ] `which ls`
* [x] `type -a ls`
* [ ] `locate -b ls`
* [ ] `which -a ls`

> **Explanation:** `type` is a shell builtin, so it knows about aliases, functions and builtins, and `-a` lists every match. `which` is an external program that only searches `PATH` for files, even with `-a`.
