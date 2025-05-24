#### Q. How do you quit out of a `more` session before reaching the end?

* [ ] `:q`
* [ ] `Ctrl-C`
* [x] `q`
* [ ] `Esc`
* [ ] `ZZ`

#### Q. Which command displays the amount of free and used disk space on all mounted filesystems?

* [ ] `du -h`
* [x] `df -h`
* [ ] `lsblk`
* [ ] `fdisk -l`
* [ ] `free -h`

#### Q. What does the `-h` option do when used with `df` or `du`?

* [ ] Hides zero-size files
* [x] Shows sizes in human-readable format (e.g., K, M, G)
* [ ] Halts the command after first output
* [ ] Outputs headers only
* [ ] Highlights large files

#### Q. Which command summarizes disk usage of each subdirectory in the current directory, in human-readable form?

* [ ] `ls -lh .`
* [ ] `df -h .`
* [x] `du -sh *`
* [ ] `du --all .`
* [ ] `find . -type d -exec du -h {} \;`

#### Q. In the output of `df -h`, what does the “Available” column represent?

* [ ] Total capacity of the filesystem
* [ ] Percentage of used space
* [x] Amount of space free for non-root users
* [ ] Size of filesystem metadata
* [ ] Space reserved for snapshots

#### Q. How do you display memory usage (RAM and swap) in human-readable format?

* [ ] `df -m`
* [ ] `du -h /proc/meminfo`
* [x] `free -h`
* [ ] `top -m`
* [ ] `vmstat -h`

#### Q. Which `du` option excludes files and directories that are mounted on other filesystems?

* [ ] `--no-dereference`
* [x] `-x`
* [ ] `--exclude-type=other`
* [ ] `--one-file-system`
* [ ] `--max-depth=1`

#### Q. What does the “Used” column in `free -h` indicate?

* [ ] Total swap space used only
* [ ] Memory used by cache and buffers only
* [x] Total memory in use (including cache and buffers)
* [ ] Amount of free memory minus cache
* [ ] Memory currently locked by processes

#### Q. To include filesystem type in the output of `df`, which option is used?

* [ ] `df --verbose`
* [ ] `df -i`
* [x] `df -T`
* [ ] `df --type`
* [ ] `df -F`

#### Q. How can you display the top 5 largest directories under `/var` sorted by size?

* [ ] `du -h /var | sort -h | tail -5`
* [ ] `du -sh /var/* | sort -h | head -5`
* [x] `du -sh /var/* | sort -hr | head -5`
* [ ] `df -h /var | sort -hr | head -5`
* [ ] `ls -Sh /var`

#### Q. Which command shows the inode usage (number of files) for each mounted filesystem?

* [ ] `df -h`
* [x] `df -i`
* [ ] `du -i`
* [ ] `ls -l /`
* [ ] `stat -f /`


#### Q. Which option tells `more` to display line numbers before each line?

* [ ] `more -n`
* [ ] `more -l`
* [x] `more -d`
* [ ] `more -p`
* [ ] `more -c`

#### Q. What is the effect of the `-c` option when running `more -c file.txt`?

* [ ] Counts pages before display
* [ ] Continues from last position
* [x] Clears the screen before displaying each page
* [ ] Compresses output to one column
* [ ] Colors matching text

#### Q. Which command lists all files, including hidden ones, in long format?

* [ ] `ls -h`
* [ ] `ls -l`
* [x] `ls -la`
* [ ] `ls -a`
* [ ] `ls -lh`

#### Q. How do you copy a directory named `project` and all its contents to `/backup`?

* [ ] `cp project /backup`
* [ ] `cp -r project /backup/project`
* [x] `cp -a project /backup/`
* [ ] `cp -f project /backup/`
* [ ] `cp -d project /backup/`

#### Q. Which command moves `file1.txt` to `archive/` and overwrites without prompting?

* [ ] `mv -i file1.txt archive/`
* [x] `mv -f file1.txt archive/`
* [ ] `mv -u file1.txt archive/`
* [ ] `mv -n file1.txt archive/`
* [ ] `mv file1.txt archive/`

#### Q. To remove the directory `old_logs` and its contents recursively, which command is correct?

* [ ] `rm old_logs`
* [ ] `rmdir old_logs/*`
* [x] `rm -rf old_logs/`
* [ ] `rm -r old_logs/*`
* [ ] `rmdir -r old_logs`

#### Q. What does `touch newfile.txt` do if `newfile.txt` already exists?

* [ ] Deletes the file and recreates it
* [ ] Does nothing
* [x] Updates the file’s access and modification timestamps
* [ ] Opens the file in the default editor
* [ ] Converts it to an executable

#### Q. Which command creates a symbolic link named `link` pointing to `/usr/bin/python3`?

* [ ] `ln /usr/bin/python3 link`
* [ ] `ln -f /usr/bin/python3 link`
* [ ] `ln --hard /usr/bin/python3 link`
* [x] `ln -s /usr/bin/python3 link`
* [ ] `ln -r /usr/bin/python3 link`

#### Q. How do you change the owner of `script.sh` to user `alice` and group `devs`?

* [ ] `chmod alice:devs script.sh`
* [x] `chown alice:devs script.sh`
* [ ] `chgrp alice:devs script.sh`
* [ ] `chown -g devs alice script.sh`
* [ ] `chmod 750 script.sh`

#### Q. How do you invoke `more` to view the contents of `file.txt` one screen at a time?

* [ ] `more | file.txt`
* [x] `more file.txt`
* [ ] `cat more file.txt`
* [ ] `view file.txt`
* [ ] `less file.txt`

#### Q. Which command outputs the entire contents of `file.txt` to standard output?

* [ ] `head file.txt`
* [ ] `tail file.txt`
* [x] `cat file.txt`
* [ ] `more file.txt`
* [ ] `dd if=file.txt of=/dev/stdout`

#### Q. By default, how many lines does `head` display from the start of a file?

* [ ] 5
* [x] 10
* [ ] 15
* [ ] 20
* [ ] 25

#### Q. Which option shows the last 20 lines of `log.txt`?

* [ ] `tail log.txt 20`
* [x] `tail -n 20 log.txt`
* [ ] `tail -20 log.txt`
* [ ] `tail --head=20 log.txt`
* [ ] `tail -f log.txt 20`

#### Q. To follow new lines appended to `access.log` in real time, which command is used?

* [ ] `tail access.log`
* [ ] `cat access.log -f`
* [x] `tail -f access.log`
* [ ] `more +F access.log`
* [ ] `head -f access.log`

#### Q. Which command reverses the line order when displaying `notes.txt`?

* [ ] `rev notes.txt`
* [x] `tac notes.txt`
* [ ] `nl notes.txt`
* [ ] `tail -r notes.txt`
* [ ] `awk '1' notes.txt`

#### Q. How do you display lines 50 through 60 of `data.csv` using a single command?

* [ ] `head -n 60 data.csv \| tail -n +50`
* [ ] `tail -n +50 data.csv \| head -n 60`
* [x] `tail -n +50 data.csv | head -n 11`
* [ ] `sed -n '50,60p' data.csv`
* [ ] `awk 'NR>=50 && NR<=60' data.csv`

#### Q. Which tool numbers each output line when reading `script.sh`?

* [ ] `cat -n script.sh`
* [x] `nl script.sh`
* [ ] `sed = script.sh`
* [ ] `awk '{print NR, $0}' script.sh`
* [ ] `less -N script.sh`

#### Q. What does `dd if=/dev/zero of=out.bin bs=1M count=1` do?

* [ ] Reads one block of zeros from `out.bin`
* [x] Creates a 1 MiB file `out.bin` filled with zeros
* [ ] Appends 1 MiB of zeros to `/dev/zero`
* [ ] Copies `out.bin` to `/dev/zero`
* [ ] Displays the first megabyte of `/dev/zero`

#### Q. To split `large.txt` into 1000-line files named `xaa`, `xab`, etc., which command is correct?

* [ ] `split -b 1000 large.txt x`
* [x] `split -l 1000 large.txt x`
* [ ] `csplit -f x -l 1000 large.txt`
* [ ] `split --lines=1000 large.txt xaa`
* [ ] `split -n 1000 large.txt x`

#### Q. In a Bash script, which built-in reads a line of input into the variable `$line`?

* [ ] `cat line`
* [ ] `readfile line`
* [x] `read line`
* [ ] `getline line`
* [ ] `scanf "%s" line`

#### Q. Which key do you press to advance exactly one more line when viewing with `more`?

* [ ] Spacebar
* [x] Enter
* [ ] `n`
* [ ] `l`
* [ ] `→`

#### Q. What happens when you press the spacebar while in `more`?

* [x] It advances one full screen (page)
* [ ] It exits `more`
* [ ] It scrolls backwards one screen
* [ ] It searches for the next pattern
* [ ] It refreshes the display

#### Q. Which `rsync` option preserves symbolic links, devices, attributes, permissions, ownerships, and timestamps?

* [ ] `-r`
* [ ] `-a`
* [x] `-rlptgoD`
* [ ] `-z`
* [ ] `-v`

#### Q. How do you copy a file `file.txt` to `/backup/` using `cp`, prompting before overwrite?

* [ ] `cp file.txt /backup/`
* [x] `cp -i file.txt /backup/`
* [ ] `cp -f file.txt /backup/`
* [ ] `cp -r file.txt /backup/`
* [ ] `cp -p file.txt /backup/`

#### Q. What does the `-n` (or `--dry-run`) flag do when used with `rsync`?

* [ ] Enables network compression
* [ ] Forces overwrite without prompt
* [x] Shows what would be transferred without making changes
* [ ] Limits bandwidth usage
* [ ] Deletes extraneous files from destination

#### Q. Which `mv` command renames a file `old.txt` to `new.txt`, overwriting without prompting?

* [ ] `mv -i old.txt new.txt`
* [x] `mv -f old.txt new.txt`
* [ ] `mv old.txt new.txt --no-clobber`
* [ ] `mv --backup=existing old.txt new.txt`
* [ ] `mv -n old.txt new.txt`

#### Q. To remove a directory named `data` and all its contents, which `rm` command is correct?

* [ ] `rm data`
* [ ] `rm -r data`
* [x] `rm -rf data`
* [ ] `rm --recursive data`
* [ ] `rm -i data`

#### Q. How can you use `rsync` to delete files in the destination that no longer exist in the source?

* [ ] `rsync -a /src/ /dest/`
* [ ] `rsync --delete-excluded /src/ /dest/`
* [x] `rsync -a --delete /src/ /dest/`
* [ ] `rsync -d --remove-source-files /src/ /dest/`
* [ ] `rsync -z --prune-empty-dirs /src/ /dest/`

#### Q. Which `cp` option copies directories recursively, preserving symlinks?

* [ ] `cp -lR`
* [ ] `cp -R`
* [x] `cp -a`
* [ ] `cp -d`
* [ ] `cp -H`

#### Q. What happens if you run `rm *` in a directory without write permission on the parent?

* [ ] Files are removed regardless
* [x] You cannot remove files, permission denied
* [ ] Files are moved to trash
* [ ] Parent directory is deleted
* [ ] Only files with execute bit are removed

#### Q. To move all `.jpg` files from `/tmp` to `/images` and show progress, which command is appropriate?

* [ ] `mv /tmp/*.jpg /images`
* [ ] `mv -v /tmp/*.jpg /images`
* [x] `mv -v /tmp/*.jpg /images/`
* [ ] `rsync -a --progress /tmp/*.jpg /images/`
* [ ] `cp -v /tmp/*.jpg /images/ && rm /tmp/*.jpg`

#### Q. Which `rsync` option enables compression during transfer?

* [ ] `-r`
* [ ] `-a`
* [ ] `--delete`
* [x] `-z`
* [ ] `--checksum`


#### Q. Which key lets you move backward one screen in `more` (if supported)?

* [ ] Spacebar
* [ ] `Enter`
* [x] `b`
* [ ] `q`
* [ ] `u`

#### Q. How can you search forward for the next occurrence of “ERROR” while inside `more`?

* [ ] `/ERROR` then Enter
* [x] `?ERROR` then Enter
* [ ] `ERROR` then Space
* [ ] `nERROR` then Enter
* [ ] `fERROR` then Enter

#### Q. To pipe the output of `ls -lR /var` through `more`, which command is correct?

* [ ] `ls -lR /var > more`
* [ ] `more ls -lR /var`
* [x] `ls -lR /var | more`
* [ ] `cat ls -lR /var | more`
* [ ] `pipe ls -lR /var more`

#### Q. Which pager is generally considered more feature-rich compared to `more`?

* [ ] `view`
* [x] `less`
* [ ] `pg`
* [ ] `morex`
* [ ] `lined`


#### Q. To find all `.log` files under `/var` modified in the last 7 days, which command would you use?

* [ ] `find /var -name "*.log" -mtime +7`
* [ ] `grep "*.log" /var -mtime -7`
* [x] `find /var -name "*.log" -mtime -7`
* [ ] `locate /var/*.log --time -7`
* [ ] `find /var -type f -newermt 7days`

#### Q. Which command displays disk usage of each file and directory in the current path, human-readable?

* [ ] `df -h .`
* [ ] `ls -lh`
* [x] `du -sh *`
* [ ] `du -h /`
* [ ] `stat --human *`

#### Q. What does the `file` command do when run on `example.bin`?

* [ ] Opens the file in a pager
* [ ] Calculates a checksum of the file
* [x] Determines and prints the file type
* [ ] Converts it to a text file
* [ ] Edits the file in vi mode
