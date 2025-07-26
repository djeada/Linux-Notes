#### Q. Which `sed` command deletes all lines containing the word “error” in-place in `log.txt`?

* [ ] `sed '/error/d' log.txt > log.txt`
* [x] `sed -i '/error/d' log.txt`
* [ ] `sed '/error/d' -o log.txt`
* [ ] `sed --delete /error/ log.txt`
* [ ] `sed -r '/error/d' -i log.txt`

#### Q. Which `grep` option makes the search case-insensitive?

* [ ] `-r`
* [x] `-i`
* [ ] `-v`
* [ ] `-n`
* [ ] `-c`

#### Q. How do you count the number of matching lines for “error” in `log.txt`?

* [ ] `grep "error" log.txt`
* [ ] `grep -n "error" log.txt`
* [x] `grep -c "error" log.txt`
* [ ] `grep -v "error" log.txt`
* [ ] `grep -l "error" log.txt`

#### Q. How do you replace the first occurrence of “foo” with “bar” on each line of standard input using `sed`?

* [ ] `sed 's/foo/bar/g'`
* [x] `sed 's/foo/bar/'`
* [ ] `sed 's|foo|bar|1'`
* [ ] `sed -r 's/foo/bar/'`
* [ ] `sed 's/foo/bar/1g'`

#### Q. In `awk`, which variable holds the number of fields in the current record?

* [x] `NF`
* [ ] `NR`
* [ ] `FNR`
* [ ] `FS`
* [ ] `OFS`

#### Q. What is the default field separator in `awk`?

* [ ] Comma (`,`)
* [ ] Tab (`\t`)
* [x] Whitespace (spaces and tabs)
* [ ] Semicolon (`;`)
* [ ] Pipe (`|`)

#### Q. Which `awk` command prints only the second column of a file `data.txt`?

* [ ] `awk '{print $1}' data.txt`
* [x] `awk '{print $2}' data.txt`
* [ ] `awk -F"," '{print $2}' data.txt`
* [ ] `awk '{print column 2}' data.txt`
* [ ] `awk 'print $2' data.txt`

#### Q. Which `find` command searches for files larger than 100MB in the current directory?

* [ ] `find . -size +100M`
* [x] `find . -size +100M`
* [ ] `find . -size 100M+`
* [ ] `find . --size >100M`
* [ ] `find . -bigger 100M`

#### Q. How do you display the last 20 lines of a file using `tail`?

* [ ] `tail -20 filename`
* [x] `tail -n 20 filename`
* [ ] `tail --lines=20 filename`
* [ ] `tail -l 20 filename`
* [ ] Both B and C are correct

#### Q. Which `chmod` command gives read, write, and execute permissions to the owner only?

* [ ] `chmod 777 file`
* [ ] `chmod 755 file`
* [x] `chmod 700 file`
* [ ] `chmod 644 file`
* [ ] `chmod 600 file`

#### Q. What does the `ps aux` command display?

* [ ] Only running processes
* [ ] Only system processes
* [x] All running processes with detailed information
* [ ] Only user processes
* [ ] Process tree structure

#### Q. Which `tar` command extracts a compressed archive `backup.tar.gz`?

* [ ] `tar -cf backup.tar.gz`
* [ ] `tar -tf backup.tar.gz`
* [x] `tar -xzf backup.tar.gz`
* [ ] `tar -czf backup.tar.gz`
* [ ] `tar -uzf backup.tar.gz`

#### Q. How do you check disk usage of the current directory with `du`?

* [ ] `du -a`
* [x] `du -sh`
* [ ] `du -l`
* [ ] `du --total`
* [ ] `du -c`

#### Q. Which `sort` option sorts lines numerically instead of alphabetically?

* [ ] `-a`
* [x] `-n`
* [ ] `-r`
* [ ] `-u`
* [ ] `-f`

#### Q. What does the `wc -l` command count?

* [ ] Number of words
* [ ] Number of characters
* [x] Number of lines
* [ ] Number of bytes
* [ ] Number of files

#### Q. Which `cut` command extracts characters 1-5 from each line of `file.txt`?

* [x] `cut -c 1-5 file.txt`
* [ ] `cut -f 1-5 file.txt`
* [ ] `cut -d: -f1-5 file.txt`
* [ ] `cut --chars=1-5 file.txt`
* [ ] `cut -b 1-5 file.txt`

#### Q. How do you display only unique lines from a sorted file using `uniq`?

* [x] `uniq filename`
* [ ] `uniq -d filename`
* [ ] `uniq -c filename`
* [ ] `uniq -u filename`
* [ ] `uniq --unique filename`

#### Q. Which `ln` command creates a symbolic link?

* [ ] `ln file link`
* [x] `ln -s file link`
* [ ] `ln -h file link`
* [ ] `ln --symbolic file link`
* [ ] Both B and D are correct

#### Q. What does the `head -n 5` command do?

* [ ] Shows the first 5 characters of a file
* [x] Shows the first 5 lines of a file
* [ ] Shows the first 5 words of a file
* [ ] Shows files starting with "5"
* [ ] Shows the 5th line of a file

#### Q. Which `rsync` option preserves permissions and timestamps during synchronization?

* [ ] `-v`
* [ ] `-r`
* [x] `-a`
* [ ] `-z`
* [ ] `-n`

#### Q. How do you search for processes containing "nginx" using `pgrep`?

* [ ] `pgrep -f nginx`
* [x] `pgrep nginx`
* [ ] `pgrep --full nginx`
* [ ] `pgrep -n nginx`
* [ ] Both A and C are correct

#### Q. Which `df` option shows disk usage in human-readable format?

* [ ] `-a`
* [x] `-h`
* [ ] `-i`
* [ ] `-T`
* [ ] `-l`

#### Q. What does the `watch` command do by default?

* [ ] Monitors file changes
* [x] Runs a command repeatedly every 2 seconds
* [ ] Watches network traffic
* [ ] Monitors system performance
* [ ] Tracks user activity

#### Q. Which `less` command allows you to search forward for a pattern?

* [ ] `?pattern`
* [x] `/pattern`
* [ ] `grep pattern`
* [ ] `find pattern`
* [ ] `s/pattern`

#### Q. How do you kill a process with PID 1234 using `kill`?

* [x] `kill 1234`
* [ ] `kill -9 1234`
* [ ] `kill --pid 1234`
* [ ] `kill -TERM 1234`
* [ ] All except C are correct

#### Q. Which `crontab` entry runs a script every day at 3:30 AM?

* [ ] `30 3 * * * /path/to/script`
* [x] `30 3 * * * /path/to/script`
* [ ] `3 30 * * * /path/to/script`
* [ ] `30 03 * * * /path/to/script`
* [ ] `* 3:30 * * * /path/to/script`

#### Q. What does the `tee` command do?

* [ ] Splits files into multiple parts
* [x] Writes output to both stdout and a file
* [ ] Merges multiple files
* [ ] Creates symbolic links
* [ ] Displays file contents in reverse

#### Q. Which flag in `grep` inverts the match, showing only non-matching lines?

* [ ] `-e`
* [ ] `-n`
* [x] `-v`
* [ ] `-l`
* [ ] `-H`

#### Q. To search recursively in all files under the current directory for “TODO”, which command is correct?

* [ ] `grep TODO *`
* [ ] `grep -c TODO .`
* [x] `grep -r "TODO" .`
* [ ] `grep -R "TODO" log.txt`
* [ ] `grep --recursive-only TODO .`

#### Q. What does the `-n` option do when used with `grep`?

* [ ] Highlights matches in color
* [x] Prefixes each matching line with its line number
* [ ] Treats the pattern as a fixed string
* [ ] Counts total matches
* [ ] Lists only filenames with matches

#### Q. Which `grep` option treats the pattern as a list of fixed strings, one per line?

* [x] `-f patterns.txt`
* [ ] `-e patterns.txt`
* [ ] `-F patterns.txt`
* [ ] `-x patterns.txt`
* [ ] `-P patterns.txt`

#### Q. How do you limit grep to match the whole line exactly to the pattern “OK”?

* [ ] `grep OK file.txt`
* [ ] `grep -i OK file.txt`
* [x] `grep -x "OK" file.txt`
* [ ] `grep -w "OK" file.txt`
* [ ] `grep -E "OK" file.txt`

#### Q. Which flag enables Perl-compatible regular expressions in `grep`?

* [ ] `-E`
* [ ] `-G`
* [x] `-P`
* [ ] `-F`
* [ ] `-X`

#### Q. To show only the names of files containing “main()” under `src/`, which command would you use?

* [ ] `grep "main()" src/`
* [x] `grep -l "main()" src/*`
* [ ] `grep -H "main()" src/`
* [ ] `grep -c "main()" src/`
* [ ] `grep -o "main()" src/*`

#### Q. What does the `-o` option do in `grep`?

* [ ] Outputs filenames only
* [ ] Counts matching lines
* [x] Prints only the matched portions of a line
* [ ] Inverses match
* [ ] Displays context around matches

#### Q. How do you use `sed` to insert the line “# HEADER” before every line matching “^Record:” in `file.txt`?

* [ ] `sed '/^Record:/i # HEADER' file.txt`
* [x] `sed '/^Record:/i\# HEADER' file.txt`
* [ ] `sed 'i\# HEADER /^Record:/' file.txt`
* [ ] `sed -e '^Record:/a # HEADER' file.txt`
* [ ] `sed -n '/^Record:/i # HEADER' file.txt`
#### Q. Which command creates a tar archive named `archive.tar` containing the `docs` directory?

* [ ] `gzip -c docs > archive.tar`
* [ ] `tar -xvf archive.tar docs`
* [x] `tar -cvf archive.tar docs`
* [ ] `tar -zcvf docs.tar.gz docs`
* [ ] `tar -tvf docs archive.tar`

#### Q. How do you list the contents of a gzip-compressed tar file `backup.tar.gz` without extracting?

* [ ] `gzip -l backup.tar.gz`
* [x] `tar -tzvf backup.tar.gz`
* [ ] `tar -cvf backup.tar.gz`
* [ ] `gunzip -l backup.tar.gz`
* [ ] `ls backup.tar.gz`

#### Q. Which option tells `tar` to extract files verbosely from `files.tar`?

* [ ] `tar -czf files.tar`
* [ ] `tar -xzf files.tar`
* [x] `tar -xvf files.tar`
* [ ] `tar -tvf files.tar`
* [ ] `tar --create files.tar`

#### Q. What does the `-z` flag do when used with `tar` (e.g., `tar -czf`)?

* [ ] Encrypts the archive with AES
* [x] Filters the archive through `gzip`
* [ ] Splits the archive into volumes
* [ ] Verifies checksums on extraction
* [ ] Uses `bzip2` compression

#### Q. To compress a single file `log.txt` with `gzip` and keep the original file, which command is correct?

* [ ] `gzip log.txt`
* [ ] `tar -zcf log.txt.gz log.txt`
* [x] `gzip -k log.txt`
* [ ] `gzip -dk log.txt`
* [ ] `gzip --remove log.txt`

#### Q. Which `tr` command converts all lowercase letters to uppercase?

* [ ] `tr 'a-z' 'A-Z'`
* [x] `tr 'a-z' 'A-Z'`
* [ ] `tr [:lower:] [:upper:]`
* [ ] `tr '[:lower:]' '[:upper:]'`
* [ ] Both A and D are correct

#### Q. How do you display the first 10 lines of multiple files using `head`?

* [ ] `head -10 file1 file2`
* [x] `head file1 file2`
* [ ] `head -n 10 file1 file2`
* [ ] `head --lines=10 file1 file2`
* [ ] All except A are correct

#### Q. Which `xargs` command removes all `.tmp` files found by `find`?

* [ ] `find . -name "*.tmp" | xargs rm`
* [x] `find . -name "*.tmp" | xargs rm`
* [ ] `find . -name "*.tmp" | xargs -I {} rm {}`
* [ ] `find . -name "*.tmp" | xargs -0 rm`
* [ ] All are correct depending on filenames

#### Q. What does the `nohup` command do?

* [ ] Prevents process termination by SIGHUP
* [ ] Runs commands in background
* [x] Runs commands immune to hangups
* [ ] Creates daemon processes
* [ ] Prevents process interruption

#### Q. Which `stat` option shows only the file type and permissions?

* [ ] `stat -c %A filename`
* [x] `stat -c '%F %A' filename`
* [ ] `stat --format=%A filename`
* [ ] `stat -f filename`
* [ ] `stat --type filename`

#### Q. How do you compress a directory `mydir` into `archive.tar.bz2`?

* [ ] `tar -cjf archive.tar.bz2 mydir`
* [x] `tar -cjf archive.tar.bz2 mydir`
* [ ] `tar -czf archive.tar.bz2 mydir`
* [ ] `tar --bzip2 -cf archive.tar.bz2 mydir`
* [ ] Both A and D are correct

#### Q. Which `locate` command finds all files containing "config" in their name?

* [ ] `locate config`
* [x] `locate "*config*"`
* [ ] `locate -i config`
* [ ] `locate --regexp config`
* [ ] `locate -b config`

#### Q. What does the `jobs` command display?

* [ ] All running processes
* [ ] System jobs
* [x] Active jobs in current shell
* [ ] Scheduled cron jobs
* [ ] Background processes

#### Q. Which `mount` command mounts a USB device at `/dev/sdb1` to `/mnt/usb`?

* [ ] `mount /dev/sdb1 /mnt/usb`
* [x] `mount /dev/sdb1 /mnt/usb`
* [ ] `mount -t auto /dev/sdb1 /mnt/usb`
* [ ] `mount --type=auto /dev/sdb1 /mnt/usb`
* [ ] All are correct

#### Q. How do you display network connections using `netstat`?

* [ ] `netstat -a`
* [ ] `netstat -tuln`
* [x] `netstat -an`
* [ ] `netstat --all`
* [ ] `netstat -tcp -udp`

#### Q. Which `file` command determines the type of a file?

* [x] `file filename`
* [ ] `file -t filename`
* [ ] `file --type filename`
* [ ] `file -i filename`
* [ ] `file --mime filename`

#### Q. What does the `uptime` command show?

* [ ] System boot time only
* [ ] Current time only
* [ ] Load average only
* [x] Current time, uptime, users, and load average
* [ ] Process runtime

#### Q. Which `alias` command creates a shortcut `ll` for `ls -la`?

* [x] `alias ll='ls -la'`
* [ ] `alias ll "ls -la"`
* [ ] `alias ll=ls -la`
* [ ] `alias 'll'='ls -la'`
* [ ] `alias set ll='ls -la'`

#### Q. How do you view the last 50 lines of `/var/log/messages` and follow new entries?

* [ ] `tail -50 -f /var/log/messages`
* [x] `tail -n 50 -f /var/log/messages`
* [ ] `tail --lines=50 --follow /var/log/messages`
* [ ] `tail -50f /var/log/messages`
* [ ] All are correct

#### Q. Which `whoami` command shows the current user?

* [x] `whoami`
* [ ] `who am i`
* [ ] `id -u`
* [ ] `echo $USER`
* [ ] All show user information

#### Q. What does the `diff` command with `-u` option produce?

* [ ] Context diff format
* [x] Unified diff format
* [ ] Side-by-side comparison
* [ ] Brief summary only
* [ ] Ignores whitespace

#### Q. Which `history` command shows the last 20 commands?

* [ ] `history 20`
* [x] `history | tail -20`
* [ ] `history -20`
* [ ] `history --last=20`
* [ ] Both A and B are correct

#### Q. How do you create a hard link named `link.txt` to `original.txt`?

* [x] `ln original.txt link.txt`
* [ ] `ln -s original.txt link.txt`
* [ ] `ln --hard original.txt link.txt`
* [ ] `link original.txt link.txt`
* [ ] `hardlink original.txt link.txt`

#### Q. Which `env` command displays all environment variables?

* [x] `env`
* [ ] `env -a`
* [ ] `env --all`
* [ ] `printenv`
* [ ] Both A and D are correct

#### Q. What does the `touch` command do when the file already exists?

* [ ] Creates a new file
* [ ] Deletes the file
* [x] Updates the timestamp
* [ ] Copies the file
* [ ] Does nothing

#### Q. Which `ping` option sends only 5 packets?

* [ ] `ping -5 hostname`
* [x] `ping -c 5 hostname`
* [ ] `ping --count=5 hostname`
* [ ] `ping -n 5 hostname`
* [ ] Both B and C are correct

#### Q. After running `gzip file1 file2`, which files remain in the directory?

* [ ] `file1`, `file2`
* [x] `file1.gz`, `file2.gz`
* [ ] `file1.tar`, `file2.tar`
* [ ] `file1.gz`, `file2`
* [ ] `file1`, `file2.gz`

#### Q. How do you extract only `dir/subfile.txt` from `archive.tar.gz` into the current directory?

* [ ] `tar -xzf archive.tar.gz dir/subfile.txt -C dir/`
* [ ] `gzip -d archive.tar.gz dir/subfile.txt`
* [x] `tar -xzf archive.tar.gz dir/subfile.txt`
* [ ] `tar --extract-file dir/subfile.txt archive.tar.gz`
* [ ] `tar -tzf archive.tar.gz dir/subfile.txt -O`

#### Q. Which command recompresses `data.gz` to use a higher compression level?

* [ ] `gzip data.gz`
* [ ] `tar --level=9 data.gz`
* [x] `gzip -9 data.gz`
* [ ] `gzip -r9 data.gz`
* [ ] `gzip --best data`

#### Q. What is the effect of the `--remove-files` option when used with `tar`?

* [ ] Leaves the original files intact after archiving
* [ ] Deletes the tarball after extraction
* [x] Removes files from disk after adding them to the archive
* [ ] Prevents overwriting existing files on extraction
* [ ] Encrypts files before adding to the archive

#### Q. How can you split a large tar archive into 100MB chunks while creating it?

* [ ] `tar -cvf archive.tar.gz --split=100M`
* [ ] `gzip -c docs | split -b 100M - archive.tar.gz-`
* [x] `tar -cvf - docs | split -b 100M - archive.part.`
* [ ] `tar -czf archive.tar.gz docs --chunk-size=100M`
* [ ] `tar -cv 100M docs | gzip > archive.tar.gz`

#### Q. To change the output field separator to a comma in `awk`, you would set:

* [ ] `BEGIN { FS = "," }`
* [x] `BEGIN { OFS = "," }`
* [ ] `BEGIN { RS = "," }`
* [ ] `BEGIN { ORS = "," }`
* [ ] `BEGIN { OFMT = "," }`

#### Q. Which `awk` script counts and prints the total number of lines in `input.txt`?

* [ ] `awk '{count++} END {print count}' input.txt`
* [ ] `awk 'END {print NR}' input.txt`
* [x] `awk '{ } END {print NR}' input.txt`
* [ ] `awk 'BEGIN {c=0} {c++} END {print c}' input.txt`
* [ ] `awk 'print NR' input.txt`

#### Q. How do you delete the third character on each line using `sed`?

* [ ] `sed 's/^./ /3'`
* [ ] `sed 's/^.{3}//'`
* [x] `sed 's/^\(.\{2\}\)./\1/'`
* [ ] `sed 'cut -c3d'`
* [ ] `sed 'y/3//'`

#### Q. Which command prints only lines 5 through 10 from `file.log` using `sed`?

* [ ] `sed -n '5,10p' file.log`
* [x] `sed -n '5,10p' file.log`
* [ ] `sed '5;10!p' file.log`
* [ ] `sed '5,10d' file.log`
* [ ] `sed 'p;5,10' file.log`


