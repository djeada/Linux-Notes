# Command-Line Tools Quiz

Notes: [Grep](../notes/grep.md), [Sed and Awk](../notes/sed_and_awk.md), [Data Streams and Filters](../notes/pipe_and_redirect.md), [Finding Files](../notes/finding_files.md), [Xargs](../notes/xargs.md), [Tar and Gzip](../notes/tar_and_gzip.md), [Cron](../notes/cron_jobs.md)

Check your understanding of text-processing filters, searching, batch commands, archiving and scheduling.

#### Q. Which command finds lines containing `error`, `Error` or `ERROR` in `app.log`?

* [ ] `grep -r error app.log`
* [x] `grep -i error app.log`
* [ ] `grep -v error app.log`
* [ ] `grep -w error app.log`

> **Explanation:** `-i` ignores case. `-r` recurses into directories, `-v` inverts the match and `-w` matches whole words only, all of them still case-sensitive.

#### Q. `app.log` has 3 lines, one of which contains `error` twice. What does `grep -c error app.log` print?

```text
error: disk full, error: retry failed
ok
error: timeout
```

* [ ] `3`
* [x] `2`
* [ ] `1`
* [ ] `0`

> **Explanation:** `-c` counts matching lines, not matches. To count every occurrence, use `grep -o error app.log | wc -l`, which prints `3` here.

#### Q. What does `grep -o` change about the output?

* [ ] It prints only the names of matching files
* [x] It prints only the matched part of each line, one match per line
* [ ] It prints only the number of matching lines
* [ ] It prints only lines that do not match

> **Explanation:** `-o` outputs each matching substring on its own line, which is handy for extracting values such as IP addresses. Filenames only is `-l`, counts are `-c`, and inverted matching is `-v`.

#### Q. Which command shows the active lines of `sshd_config`, dropping both comment lines and empty lines?

* [ ] `grep '^#' /etc/ssh/sshd_config`
* [x] `grep -Ev '^(#|$)' /etc/ssh/sshd_config`
* [ ] `grep -v '#|$' /etc/ssh/sshd_config`
* [ ] `grep -E '^(#|$)' /etc/ssh/sshd_config`

> **Explanation:** `^(#|$)` matches lines that start with `#` or are empty, and `-v` removes them. Without `-E`, the `|` is a literal character, and without `-v` you would print only the lines you wanted to remove.

#### Q. Which command lists the files under `src/` that contain `main(`, printing only their names?

* [ ] `grep -c "main(" src/*`
* [x] `grep -rlF "main(" src/`
* [ ] `grep -rn "main(" src/`
* [ ] `grep -rL "main(" src/`

> **Explanation:** `-r` recurses, `-l` prints only the names of files with a match, and `-F` treats `(` literally. `-L` lists the files without a match, and `-n` prints matching lines with line numbers.

#### Q. Given these lines, which command matches `foo` and `bar foo` but not `foobar`?

```text
foo
foobar
bar foo
```

* [ ] `grep -x foo`
* [x] `grep -w foo`
* [ ] `grep -F foo`
* [ ] `grep -i foo`

> **Explanation:** `-w` requires the match to be a whole word, so `foobar` is excluded. `-x` would match only the line that is exactly `foo`. `-F` and `-i` would still match `foobar`.

#### Q. Which command matches only lines that consist entirely of `OK`, with nothing else on the line?

* [ ] `grep -w OK status.txt`
* [x] `grep -x OK status.txt`
* [ ] `grep -o OK status.txt`
* [ ] `grep -c OK status.txt`

> **Explanation:** `-x` anchors the pattern to the whole line, like `^OK$`. `-w` would also match `OK fine`, because `OK` is a separate word there.

#### Q. Why does `grep 'abc|def' file.txt` find nothing, while `grep -E 'abc|def' file.txt` finds both words?

* [ ] Basic grep needs the pattern in double quotes
* [x] In basic regular expressions `|` is a literal character; `-E` turns on extended syntax
* [ ] `-E` makes the search case-insensitive
* [ ] Basic grep reads only the first line of the file

> **Explanation:** In basic regex `|` is literal. With `-E`, `|`, `+`, `?` and `()` work as operators. You can also use `grep -e abc -e def` to give several patterns.

#### Q. Which command searches for the literal string `1.2.3.4`, so that `.` does not match any character?

* [ ] `grep -E '1.2.3.4' hosts.txt`
* [x] `grep -F '1.2.3.4' hosts.txt`
* [ ] `grep -w '1.2.3.4' hosts.txt`
* [ ] `grep -P '1.2.3.4' hosts.txt`

> **Explanation:** `-F` treats the pattern as a fixed string. In every regex mode an unescaped `.` matches any character, so `1x2y3z4` would also match. You can also escape the dots instead.

#### Q. Which command shows each line containing `panic` along with the 3 lines that follow it?

* [ ] `grep -B 3 panic kern.log`
* [x] `grep -A 3 panic kern.log`
* [ ] `grep -C 3 panic kern.log`
* [ ] `grep -n 3 panic kern.log`

> **Explanation:** `-A` means "after" context. `-B` shows lines before the match, and `-C` shows lines on both sides.

#### Q. Which command searches only the `*.conf` files under `/etc` for `Listen`?

* [ ] `grep -r Listen /etc --exclude='*.conf'`
* [x] `grep -r Listen /etc --include='*.conf'`
* [ ] `grep -l '*.conf' Listen /etc`
* [ ] `grep -r '*.conf' /etc Listen`

> **Explanation:** `--include=GLOB` limits a recursive search to files whose base name matches. `--exclude` does the opposite. Quoting the glob stops the shell from expanding it first.

#### Q. What does `sed 's/foo/bar/' input.txt` do to the line `foo foo foo`?

* [ ] Changes it to `bar bar bar`
* [x] Changes it to `bar foo foo`
* [ ] Changes it to `foo foo bar`
* [ ] Leaves it unchanged unless `-i` is given

> **Explanation:** Without flags, `s` replaces only the first match on each line. Add `g` (`s/foo/bar/g`) to replace every match. Without `-i`, `sed` prints the result and leaves the file alone.

#### Q. Which command deletes every line containing `DEBUG` from `app.log` in place, keeping a backup as `app.log.bak`?

* [ ] `sed '/DEBUG/d' app.log > app.log`
* [x] `sed -i.bak '/DEBUG/d' app.log`
* [ ] `sed -n '/DEBUG/d' app.log.bak`
* [ ] `sed -i '/DEBUG/p' app.log.bak`

> **Explanation:** `-i.bak` edits the file in place after saving the original with a `.bak` suffix. Redirecting to the same file truncates it before `sed` reads it, so you lose the data.

#### Q. Which command prints only the lines from `START` to `END`, inclusive?

* [ ] `sed '/START/,/END/p' file.txt`
* [x] `sed -n '/START/,/END/p' file.txt`
* [ ] `sed -n '/START/,/END/d' file.txt`
* [ ] `sed -n '/START/p;/END/p' file.txt`

> **Explanation:** A `/start/,/end/` address selects a range of lines. `-n` turns off automatic printing, so only `p` produces output. Without `-n`, every line prints once and the range prints twice. `/START/p;/END/p` prints only the two marker lines.

#### Q. Which command deletes all empty lines from `file.txt`, printing the result?

* [ ] `sed 's/^$//' file.txt`
* [x] `sed '/^$/d' file.txt`
* [ ] `sed -n '/^$/p' file.txt`
* [ ] `sed '/$/d' file.txt`

> **Explanation:** `^$` matches a line with nothing between the start and the end, and `d` deletes it. `s/^$//` replaces nothing with nothing, so the empty lines stay. `/$/` matches every line.

#### Q. Which command inserts a line `# generated` before the first line of `config.ini`, writing the result to stdout?

* [ ] `sed '1a\# generated' config.ini`
* [x] `sed '1i\# generated' config.ini`
* [ ] `sed '$i\# generated' config.ini`
* [ ] `sed '1c\# generated' config.ini`

> **Explanation:** `i\` inserts text before the addressed line, `a\` appends after it, and `c\` replaces it. Address `1` is the first line and `$` is the last.

#### Q. What does this `sed` command with capture groups print?

```bash
echo 'user=alice' | sed -E 's/(.*)=(.*)/\2=\1/'
```

* [ ] `user=alice`
* [x] `alice=user`
* [ ] `\2=\1`
* [ ] `=alice user`

> **Explanation:** With `-E`, parentheses are capture groups, and `\1` and `\2` in the replacement refer back to them. Without `-E` you would write `\(.*\)=\(.*\)`.

#### Q. Which command removes the third character from every line?

* [ ] `sed 's/.//3g'`
* [x] `sed -E 's/^(..)./\1/'`
* [ ] `sed 's/^.{3}//'`
* [ ] `sed 'y/3//'`

> **Explanation:** `^(..).` captures the first two characters and matches the third, then `\1` puts back only the two. In basic regex, `{3}` must be written `\{3\}`, and `y` translates characters rather than deleting them.

#### Q. Which `awk` command prints the username (field 1) and UID (field 3) from `/etc/passwd`?

* [ ] `awk '{print $1, $3}' /etc/passwd`
* [x] `awk -F: '{print $1, $3}' /etc/passwd`
* [ ] `awk -F: 'print $1 $3' /etc/passwd`
* [ ] `awk -v FS=, '{print $1, $3}' /etc/passwd`

> **Explanation:** `/etc/passwd` is colon-separated, so set the field separator with `-F:`. By default `awk` splits on runs of whitespace. The action must be inside braces.

#### Q. What does `awk '{ print NF, $NF }'` print for the line `a b c d`?

* [ ] `1 a`
* [x] `4 d`
* [ ] `4 4`
* [ ] `d 4`

> **Explanation:** `NF` is the number of fields in the current line, and `$NF` is the last field. `NR` would be the line (record) number.

#### Q. Which command prints the total of the numbers in column 2 of `sales.txt`?

* [ ] `awk '{print sum += $2}' sales.txt`
* [x] `awk '{s += $2} END {print s}' sales.txt`
* [ ] `awk 'BEGIN {print s += $2}' sales.txt`
* [ ] `awk '{s = $2} END {print s}' sales.txt`

> **Explanation:** The main block runs for every line, adding up `$2`, and `END` runs once after the last line. The first option prints a running total on every line, and `BEGIN` runs before any input is read.

#### Q. Which command prints the names of users whose UID is 1000 or higher?

* [ ] `awk -F: '$3 > 1000 {print $1}' /etc/passwd`
* [x] `awk -F: '$3 >= 1000 {print $1}' /etc/passwd`
* [ ] `awk -F: '{if $3 >= 1000 print $1}' /etc/passwd`
* [ ] `awk -F: '/1000/ {print $1}' /etc/passwd`

> **Explanation:** A condition before the action limits which lines it runs on. `> 1000` would leave out UID 1000 itself, and `/1000/` matches the text `1000` anywhere in the line.

#### Q. Which command prints `x,z` for the input `x:y:z`?

* [ ] `awk -F, '{print $1, $3}'`
* [x] `awk -F: -v OFS=, '{print $1, $3}'`
* [ ] `awk -F: -v RS=, '{print $1, $3}'`
* [ ] `awk -F: '{print $1 $3}'`

> **Explanation:** `-F:` splits the input on colons, and `OFS` is the output field separator that `print` places between comma-separated items. `RS` is the record separator, and `$1 $3` joins the fields with nothing in between.

#### Q. Which command counts how often each value in column 1 of `access.log` appears?

* [ ] `awk '{print $1, NR}' access.log`
* [x] `awk '{c[$1]++} END {for (k in c) print k, c[k]}' access.log`
* [ ] `awk 'END {print $1, NF}' access.log`
* [ ] `awk '{c++} END {print $1, c}' access.log`

> **Explanation:** `c[$1]++` uses an associative array keyed by the first field, and the `END` loop prints each key with its count. The order of `for (k in c)` is unspecified, so pipe the output to `sort` if needed.

#### Q. What does `sort numbers.txt` output for lines `10`, `9` and `100`?

* [ ] `9`, `10`, `100`
* [x] `10`, `100`, `9`
* [ ] `100`, `10`, `9`
* [ ] `9`, `100`, `10`

> **Explanation:** Without options, `sort` compares lines as text, character by character, so `1…` sorts before `9`. Use `sort -n` to compare numerically and get `9`, `10`, `100`.

#### Q. Which command sorts `scores.txt` numerically by its second column, highest first?

* [ ] `sort -k2 scores.txt`
* [x] `sort -k2 -nr scores.txt`
* [ ] `sort -n scores.txt -r 2`
* [ ] `sort -t2 -n scores.txt`

> **Explanation:** `-k2` sorts on the second field, `-n` compares numbers and `-r` reverses the order. `-t` sets the field delimiter, not the key.

#### Q. Why does `uniq` usually appear after `sort` in a pipeline?

* [ ] `uniq` only works on numeric data
* [x] `uniq` removes only adjacent duplicate lines
* [ ] `uniq` reverses the order of its input
* [ ] `sort` adds the line numbers that `uniq` needs

> **Explanation:** `uniq` compares each line with the one before it. Sorting first puts identical lines next to each other, so `printf 'b\na\nb\n' | uniq` keeps all three lines. `sort -u` does both steps at once.

#### Q. Which pipeline lists the most frequent lines in `ips.txt` first, each with its count?

* [ ] `uniq -c ips.txt | sort -n`
* [x] `sort ips.txt | uniq -c | sort -rn`
* [ ] `sort -u ips.txt | uniq -c`
* [ ] `sort ips.txt | uniq -d | sort -r`

> **Explanation:** `sort` groups duplicates, `uniq -c` prefixes each distinct line with its count, and `sort -rn` puts the biggest counts first. `uniq -d` prints only the duplicated lines, without counts.

#### Q. Which command prints the usernames (the first colon-separated field) from `/etc/passwd`?

* [ ] `cut -c1 /etc/passwd`
* [x] `cut -d: -f1 /etc/passwd`
* [ ] `cut -f1 /etc/passwd`
* [ ] `cut -d' ' -f1 /etc/passwd`

> **Explanation:** `-d:` sets the delimiter and `-f1` picks the first field. Without `-d`, `cut` splits on tabs, and `-c1` would print only the first character.

#### Q. Which command turns `hello world` into `HELLO WORLD`?

* [ ] `echo 'hello world' | tr 'A-Z' 'a-z'`
* [x] `echo 'hello world' | tr '[:lower:]' '[:upper:]'`
* [ ] `echo 'hello world' | tr -d '[:lower:]'`
* [ ] `echo 'hello world' | tr -s '[:lower:]'`

> **Explanation:** `tr SET1 SET2` maps each character in the first set to the matching one in the second. `'a-z' 'A-Z'` also works for ASCII text. `-d` deletes characters and `-s` squeezes repeats.

#### Q. What does `echo 'a1b2c3' | tr -d '0-9'` print?

* [ ] `123`
* [x] `abc`
* [ ] `a1b2c3`
* [ ] `a b c`

> **Explanation:** `tr -d` deletes every character in the given set, here the digits, leaving `abc`.

#### Q. Which command counts the lines in `access.log`?

* [ ] `wc -w access.log`
* [x] `wc -l access.log`
* [ ] `wc -c access.log`
* [ ] `wc -m access.log`

> **Explanation:** `-l` counts newline characters, which is the number of lines. `-w` counts words, `-c` bytes and `-m` characters.

#### Q. Which command finds regular files larger than 100 MiB under the current directory?

* [ ] `find . -type f -size 100M`
* [x] `find . -type f -size +100M`
* [ ] `find . -type f -size -100M`
* [ ] `find . -type f -bigger 100M`

> **Explanation:** `+N` means more than N, `-N` means less than N, and a bare `N` means exactly N (rounded up to whole units). A bare number with no suffix counts 512-byte blocks.

#### Q. Which command lists only the directories under `/usr/local`?

* [ ] `find /usr/local -name d`
* [x] `find /usr/local -type d`
* [ ] `find /usr/local -type f`
* [ ] `find /usr/local -dir`

> **Explanation:** `-type d` matches directories, `f` regular files and `l` symbolic links. `-name d` matches entries literally named `d`.

#### Q. Which command finds files under `/home` that are not owned by `guest`?

* [ ] `find /home -user guest`
* [x] `find /home ! -user guest`
* [ ] `find /home -user !guest`
* [ ] `find /home -not guest`

> **Explanation:** `!` (or `-not`) negates the test that follows it. `-user !guest` would look for a user literally named `!guest`.

#### Q. What is the difference between `-exec rm -- {} \;` and `-exec rm -- {} +` in `find`?

* [ ] `\;` deletes directories and `+` deletes only files
* [x] `\;` runs `rm` once per file, while `+` passes many files to each `rm`
* [ ] `+` asks before each deletion, while `\;` does not
* [ ] `\;` is for GNU `find` only, while `+` works everywhere

> **Explanation:** `{} +` batches pathnames like `xargs`, creating far fewer processes. Both forms handle spaces in names safely. Asking before each command is what `-ok` does.

#### Q. Which `find` action asks for confirmation before running the command on each match?

* [ ] `-exec rm {} \;`
* [x] `-ok rm {} \;`
* [ ] `-delete`
* [ ] `-print0`

> **Explanation:** `-ok` works like `-exec` but prompts before each command, which is a safer way to delete. `-delete` removes matches without asking.

#### Q. Which command uses the `locate` database to find paths containing `readme`, whether written `README`, `Readme` or `readme`?

* [ ] `locate readme`
* [x] `locate -i readme`
* [ ] `locate -l readme`
* [ ] `locate -S readme`

> **Explanation:** `-i` ignores case. `-l N` limits the number of results and `-S` prints database statistics. `locate` searches a prebuilt database, so run `sudo updatedb` first if files are very new.

#### Q. `which ls` prints `/usr/bin/ls`, but typing `ls` runs `ls --color=auto`. Which command shows the alias as well as the files on `PATH`?

* [ ] `which -a ls`
* [x] `type -a ls`
* [ ] `locate ls`
* [ ] `whereis -b ls`

> **Explanation:** `type` is a Bash builtin that reports aliases, functions, builtins and files on `PATH`, in the order the shell resolves them. An external `which` searches only `PATH`.

#### Q. What does this `xargs -n 2` pipeline print?

```bash
printf '%s\n' one two three four five | xargs -n 2 echo
```

* [ ] `one two three four five` on one line
* [x] `one two`, `three four`, then `five` on separate lines
* [ ] Each word on its own line
* [ ] `one two` only

> **Explanation:** `-n 2` passes at most two arguments to each `echo`, so `echo` runs three times. Without `-n`, `xargs` puts as many arguments as fit into a single command.

#### Q. Which pipeline safely deletes every `*.tmp` file, even when names contain spaces or newlines?

* [ ] `find . -name '*.tmp' | xargs rm`
* [x] `find . -name '*.tmp' -print0 | xargs -0 rm --`
* [ ] `ls *.tmp | xargs rm -rf`
* [ ] `find . -name '*.tmp' | xargs -n 1 rm`

> **Explanation:** `-print0` ends each pathname with a NUL byte, and `xargs -0` splits only on NUL, so whitespace stays part of the name. By default `xargs` splits on blanks, so `a b.tmp` becomes two bad arguments.

#### Q. In `xargs rm --`, which program is the `--` for, and why is it there?

* [ ] It is for `xargs`, telling it to read NUL-separated input
* [x] It is for `rm`, so that file names starting with `-` are not read as options
* [ ] It is for the shell, to end the pipeline
* [ ] It is for `rm`, to make it delete directories recursively

> **Explanation:** `xargs` adds the input items after `rm --`, and `--` tells `rm` that everything after it is a filename. Without it, a file named `-rf` would be read as options.

#### Q. Which command runs `gzip` on each listed file, with up to 4 compressions running at once?

* [ ] `xargs -n 4 gzip < files.txt`
* [x] `xargs -n 1 -P 4 gzip < files.txt`
* [ ] `xargs -I 4 gzip < files.txt`
* [ ] `xargs -t 4 gzip < files.txt`

> **Explanation:** `-P 4` allows four parallel processes, and `-n 1` gives each `gzip` a single file. `-n 4` alone runs `gzip` with four files at a time, one invocation after another.

#### Q. What does `printf '%s\n' web1 web2 | xargs -I {} ssh {} uptime` do?

* [ ] Runs a single `ssh` with both hostnames as arguments
* [x] Runs `ssh web1 uptime`, then `ssh web2 uptime`
* [ ] Runs `ssh` in parallel on both hosts
* [ ] Prints the commands without running them

> **Explanation:** `-I {}` swaps each input line in for `{}` and runs one command per item. Parallelism needs `-P`, and printing each command as it runs needs `-t`.

#### Q. On GNU systems, `find . -name '*.bak' -print0 | xargs -0 rm --` finds no files. How do you stop `rm` from running at all in that case?

* [ ] Add `-n 1` to `xargs`
* [x] Add `-r` to `xargs`
* [ ] Add `-t` to `xargs`
* [ ] Add `-f` to `rm`

> **Explanation:** GNU `xargs` normally runs the command once even with empty input; `-r` (`--no-run-if-empty`) skips it. `-r` is not in POSIX, so `find ... -exec rm -- {} +` is the portable alternative.

#### Q. Which command creates a gzip-compressed archive `project.tar.gz` from the directory `project/`?

* [ ] `tar -xzf project.tar.gz project/`
* [x] `tar -czf project.tar.gz project/`
* [ ] `tar -tzf project.tar.gz project/`
* [ ] `gzip -r project/ > project.tar.gz`

> **Explanation:** `-c` creates, `-z` compresses through gzip and `-f` names the archive. `-x` extracts and `-t` lists. `gzip -r` compresses each file separately and makes no archive.

#### Q. Why does `tar -cfz backup.tar.gz project/` not create a compressed `backup.tar.gz`?

* [ ] `-z` must always come before `-c`
* [x] `-f` takes the next text, `z`, as the archive name, so `backup.tar.gz` is read as a file to add
* [ ] `tar` refuses to create files with a `.gz` extension
* [ ] `-cfz` creates a bzip2 archive instead

> **Explanation:** `-f` needs an argument, and in a bundled option group it takes the rest of the group. Keep `f` last, as in `-czf backup.tar.gz project/`.

#### Q. How do you list the contents of `backup.tar.gz` without extracting anything?

* [ ] `tar -xzvf backup.tar.gz`
* [x] `tar -tzvf backup.tar.gz`
* [ ] `tar -czvf backup.tar.gz`
* [ ] `gzip -d backup.tar.gz`

> **Explanation:** `-t` lists the archive's members, and with `-v` it shows permissions, owner, size and date like `ls -l`. `gzip -d` would decompress the file into `backup.tar`.

#### Q. Which command extracts `project.tar.gz` into `/opt/restore` instead of the current directory?

* [ ] `tar -xzf project.tar.gz > /opt/restore`
* [x] `tar -xzf project.tar.gz -C /opt/restore`
* [ ] `tar -xzf /opt/restore project.tar.gz`
* [ ] `tar -czf project.tar.gz -C /opt/restore`

> **Explanation:** `-C DIR` makes `tar` change into that directory before extracting. Redirecting stdout does not move the extracted files, and `-c` would create an archive instead.

#### Q. Which command extracts only `docs/readme.txt` from `archive.tar.gz`?

* [ ] `tar -tzf archive.tar.gz docs/readme.txt`
* [x] `tar -xzf archive.tar.gz docs/readme.txt`
* [ ] `gzip -d archive.tar.gz docs/readme.txt`
* [ ] `tar -xzf docs/readme.txt archive.tar.gz`

> **Explanation:** Member names given after the archive limit extraction to those paths, which must match how they appear in `tar -tzf`. The archive name must come straight after `-f`.

#### Q. Which command archives `app/` but leaves out its `app/tmp/` contents?

* [ ] `tar -czf app.tar.gz app/ --exclude='app/tmp/*'`
* [x] `tar --exclude='app/tmp/*' -czf app.tar.gz app/`
* [ ] `tar -czf app.tar.gz app/ -x app/tmp`
* [ ] `tar -czf app.tar.gz app/ | grep -v tmp`

> **Explanation:** In GNU tar, `--exclude` is position-sensitive and must come before the file operands it applies to. The quotes stop the shell from expanding the pattern. `-x` means extract.

#### Q. Which `tar` option compresses with `xz`, as in `archive.tar.xz`?

* [ ] `-z`
* [ ] `-j`
* [x] `-J`
* [ ] `-x`

> **Explanation:** `-z` is gzip (`.tar.gz`), `-j` is bzip2 (`.tar.bz2`) and capital `-J` is xz (`.tar.xz`). Lowercase `-x` means extract.

#### Q. You need to split `big.tar` into 100 MB pieces for upload, then rebuild it later. Which pair of commands works?

* [ ] `tar --split=100M big.tar`, then `tar --join big.tar.*`
* [x] `split -b 100M big.tar part_`, then `cat part_* > big.tar`
* [ ] `gzip -b 100M big.tar`, then `gunzip big.tar.gz`
* [ ] `split -l 100 big.tar part_`, then `tar -xf part_*`

> **Explanation:** `split -b` cuts the file into byte-sized chunks named `part_aa`, `part_ab` and so on. The glob expands in sorted order, so `cat` puts them back together correctly. `-l` splits by lines.

#### Q. Which command compresses `log.txt` to `log.txt.gz` but also keeps the original file?

* [ ] `gzip log.txt`
* [x] `gzip -k log.txt`
* [ ] `gzip -d log.txt`
* [ ] `gzip -l log.txt`

> **Explanation:** By default `gzip` replaces the file with the `.gz` version. `-k` keeps the original, `-d` decompresses and `-l` lists compression statistics.

#### Q. Which crontab line runs `/opt/backup.sh` at 7:30 AM, Monday to Friday?

* [ ] `7 30 * * 1-5 /opt/backup.sh`
* [x] `30 7 * * 1-5 /opt/backup.sh`
* [ ] `30 7 1-5 * * /opt/backup.sh`
* [ ] `30 7 * 1-5 * /opt/backup.sh`

> **Explanation:** The five fields are minute, hour, day of month, month and day of week. `1-5` in the fifth field means Monday to Friday; in the third field it would mean the 1st to the 5th of the month.

#### Q. When does the crontab entry `*/15 * * * * /opt/check.sh` run?

* [ ] 15 minutes after cron starts, then every 15 minutes from that point
* [x] At minutes 0, 15, 30 and 45 of every hour
* [ ] Once at 15 minutes past each hour
* [ ] Every 15 seconds

> **Explanation:** Cron schedules are calendar matches, not timers. `*/15` in the minute field is a step value that matches minutes divisible by 15. `15` alone would run once an hour at minute 15.

#### Q. A cron job `0 2 * * * tar -czf /backup/$(date +%F).tar.gz /data` never produces a correctly named file. Why?

* [ ] Cron cannot run `tar`
* [x] An unescaped `%` is special in crontab commands and must be written as `\%`
* [ ] `$(...)` is not allowed in cron jobs
* [ ] Cron jobs cannot write to `/backup`

> **Explanation:** Cron treats `%` as a newline, and text after the first `%` is sent to the command's stdin. Write `date +\%F`, or move the logic into a script.

#### Q. How do lines in `/etc/crontab` differ from lines you add with `crontab -e`?

* [ ] They have no time fields
* [x] They have an extra username field between the time fields and the command
* [ ] They use seconds as the first field
* [ ] They must use full month names

> **Explanation:** System crontabs (`/etc/crontab` and `/etc/cron.d/`) say which user runs each job. User crontabs already belong to one user, so they have only the five time fields and the command.

#### Q. A laptop is often off at night, and you want a daily job to still run once it boots. Which tool suits this better than plain cron?

* [ ] `at`
* [x] `anacron`
* [ ] `watch`
* [ ] `nohup`

> **Explanation:** Plain cron skips jobs whose time passes while the machine is off. `anacron` tracks when each periodic job last ran and catches up after boot, which suits machines that are not always on.
