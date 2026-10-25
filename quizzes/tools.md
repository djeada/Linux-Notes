# Command-Line Tools Quiz

Notes: [Grep](../notes/grep.md), [Sed and Awk](../notes/sed_and_awk.md), [Data Streams and Filters](../notes/pipe_and_redirect.md), [Finding Files](../notes/finding_files.md), [Xargs](../notes/xargs.md), [Tar and Gzip](../notes/tar_and_gzip.md), [Cron](../notes/cron_jobs.md)

Check your understanding of text-processing filters, redirection, searching, batch commands, archiving and scheduling. Unless a question says otherwise, assume GNU tools and Bash on Ubuntu.

#### Q. Which command finds lines containing `error`, `Error` or `ERROR` in `app.log`?

* [ ] `grep -r error app.log`
* [ ] `grep -v error app.log`
* [ ] `grep -w error app.log`
* [x] `grep -i error app.log`

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

* [x] It prints only the matched part of each line, one match per line
* [ ] It prints only the names of matching files
* [ ] It prints only the number of matching lines
* [ ] It prints only lines that do not match

> **Explanation:** `-o` outputs each matching substring on its own line, which is handy for extracting values such as IP addresses. Filenames only is `-l`, counts are `-c`, and inverted matching is `-v`.

#### Q. Which command shows the active lines of `sshd_config`, dropping both comment lines and empty lines?

* [ ] `grep '^#' /etc/ssh/sshd_config`
* [ ] `grep -v '#|$' /etc/ssh/sshd_config`
* [x] `grep -Ev '^(#|$)' /etc/ssh/sshd_config`
* [ ] `grep -E '^(#|$)' /etc/ssh/sshd_config`

> **Explanation:** `^(#|$)` matches lines that start with `#` or are empty, and `-v` removes them. Without `-E`, the `|` is a literal character, and without `-v` you would print only the lines you wanted to remove.

#### Q. Which command lists the files under `src/` that contain `main(`, printing only their names?

* [ ] `grep -c "main(" src/*`
* [x] `grep -rlF "main(" src/`
* [ ] `grep -rn "main(" src/`
* [ ] `grep -rL "main(" src/`

> **Explanation:** `-r` recurses, `-l` prints only the names of files with a match, and `-F` makes the pattern a fixed string, so `(` is never regex syntax (under `-E` it would open a group). `-L` lists files without a match, and `-n` prints the matching lines.

#### Q. Given these lines, which command matches `foo` and `bar foo` but not `foobar`?

```text
foo
foobar
bar foo
```

* [ ] `grep -x foo`
* [ ] `grep -F foo`
* [x] `grep -w foo`
* [ ] `grep -i foo`

> **Explanation:** `-w` requires the match to be a whole word, so `foobar` is excluded. `-x` would match only the line that is exactly `foo`. `-F` and `-i` would still match `foobar`.

#### Q. What does `grep '[^0-9]' data.txt` print for the lines below?

```text
12345
hello123
no_digits_here
```

* [ ] `12345` only
* [ ] `no_digits_here` only
* [ ] `12345`, `hello123` and `no_digits_here`
* [x] `hello123` and `no_digits_here`

> **Explanation:** `[^0-9]` matches one character that is not a digit, and a line matches if it contains such a character anywhere, so only the all-digit line is skipped. To print lines made only of digits, use `grep -E '^[0-9]+$'`.

#### Q. Why does `grep 'abc|def' file.txt` find nothing, while `grep -E 'abc|def' file.txt` finds both words?

* [x] In basic regex `|` is a literal character; `-E` turns on extended syntax
* [ ] Basic grep needs the pattern in double quotes to read `|`
* [ ] `-E` makes the search case-insensitive, so it finds more lines
* [ ] Basic grep stops reading the file after the first match

> **Explanation:** In basic regex `|` is literal. With `-E`, `|`, `+`, `?` and `()` work as operators. You can also use `grep -e abc -e def` to give several patterns.

#### Q. Which command searches for the literal string `1.2.3.4`, so that `.` does not match any character?

* [ ] `grep -E '1.2.3.4' hosts.txt`
* [x] `grep -F '1.2.3.4' hosts.txt`
* [ ] `grep -w '1.2.3.4' hosts.txt`
* [ ] `grep -P '1.2.3.4' hosts.txt`

> **Explanation:** `-F` treats the pattern as a fixed string. In every regex mode an unescaped `.` matches any character, so `1x2y3z4` would also match. You can also escape the dots instead.

#### Q. Which command shows each line containing `panic` along with the 3 lines that follow it?

* [x] `grep -A 3 panic kern.log`
* [ ] `grep -B 3 panic kern.log`
* [ ] `grep -C 3 panic kern.log`
* [ ] `grep -n 3 panic kern.log`

> **Explanation:** `-A` means "after" context. `-B` shows lines before the match, and `-C` shows lines on both sides.

#### Q. Which command searches the contents of every `*.conf` file anywhere under `/etc` for `Listen`?

* [ ] `grep -r Listen /etc --exclude='*.conf'`
* [ ] `grep -r Listen /etc/*.conf`
* [ ] `find /etc -name '*.conf' | grep Listen`
* [x] `grep -r Listen /etc --include='*.conf'`

> **Explanation:** `--include=GLOB` limits a recursive search to files whose base name matches; the quotes stop the shell expanding the glob. `/etc/*.conf` names only top-level files, and piping `find` into `grep` searches the list of names, not the files' contents.

#### Q. What does `sed 's/foo/bar/' input.txt` do to the line `foo foo foo`?

* [ ] Changes it to `bar bar bar`
* [ ] Changes it to `foo foo bar`
* [x] Changes it to `bar foo foo`
* [ ] Leaves it unchanged unless `-i` is given

> **Explanation:** Without flags, `s` replaces only the first match on each line. Add `g` (`s/foo/bar/g`) to replace every match. Without `-i`, `sed` prints the result and leaves the file alone.

#### Q. What does `echo 'concatenate cat' | sed 's/cat/dog/g'` print?

* [ ] `concatenate dog`
* [ ] `condogenate cat`
* [ ] `dog dog`
* [x] `condogenate dog`

> **Explanation:** `s` matches the text anywhere, including inside words, and `g` replaces every match on the line. To change only the whole word, GNU `sed` accepts `s/\bcat\b/dog/g`, which prints `concatenate dog`.

#### Q. Which command replaces `/usr/local` with `/opt/tools` on every line of `paths.txt`?

* [ ] `sed 's//usr/local//opt/tools/g' paths.txt`
* [ ] `sed 's/\/usr\/local/\/opt\/tools' paths.txt`
* [x] `sed 's|/usr/local|/opt/tools|g' paths.txt`
* [ ] `sed 'y|/usr/local|/opt/tools|' paths.txt`

> **Explanation:** The character after `s` is the delimiter, so `|` avoids escaping every `/`. Unescaped slashes end the fields early, the escaped version lacks its closing delimiter, and `y` maps single characters one-to-one instead of replacing strings.

#### Q. Which command deletes every line containing `DEBUG` from `app.log` in place, keeping a backup as `app.log.bak`?

* [x] `sed -i.bak '/DEBUG/d' app.log`
* [ ] `sed '/DEBUG/d' app.log > app.log`
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
* [ ] `sed -n '/^$/p' file.txt`
* [x] `sed '/^$/d' file.txt`
* [ ] `sed '/$/d' file.txt`

> **Explanation:** `^$` matches a line with nothing between the start and the end, and `d` deletes it. `s/^$//` replaces nothing with nothing, so the empty lines stay. `/$/` matches every line.

#### Q. With GNU `sed`, which command inserts a line `# generated` before the first line of `config.ini`, writing the result to stdout?

* [x] `sed '1i\# generated' config.ini`
* [ ] `sed '1a\# generated' config.ini`
* [ ] `sed '$i\# generated' config.ini`
* [ ] `sed '1c\# generated' config.ini`

> **Explanation:** `i\` inserts text before the addressed line, `a\` appends after it, and `c\` replaces it. Address `1` is the first line and `$` is the last. The one-line form is a GNU extension; POSIX `sed` wants the text on the next line.

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
* [ ] `sed 's/^.{3}//'`
* [ ] `sed 'y/3//'`
* [x] `sed -E 's/^(..)./\1/'`

> **Explanation:** `^(..).` captures two characters and matches the third, and `\1` puts back only the two. `s/.//3g` deletes the third and every later character, basic regex reads `{3}` literally, and `y` needs two equal-length character lists.

#### Q. Which `awk` command prints the username (field 1) and UID (field 3) from `/etc/passwd`?

* [ ] `awk '{print $1, $3}' /etc/passwd`
* [ ] `awk -F: 'print $1 $3' /etc/passwd`
* [x] `awk -F: '{print $1, $3}' /etc/passwd`
* [ ] `awk -v FS=, '{print $1, $3}' /etc/passwd`

> **Explanation:** `/etc/passwd` is colon-separated, so set the field separator with `-F:`. By default `awk` splits on runs of whitespace. The action must be inside braces.

#### Q. What does `awk '{ print NF, $NF }'` print for the line `a b c d`?

* [ ] `1 a`
* [ ] `4 4`
* [ ] `d 4`
* [x] `4 d`

> **Explanation:** `NF` is the number of fields in the current line, and `$NF` is the last field. `NR` would be the line (record) number.

#### Q. Which command prints the total of the numbers in column 2 of `sales.txt`?

* [x] `awk '{s += $2} END {print s}' sales.txt`
* [ ] `awk '{print sum += $2}' sales.txt`
* [ ] `awk 'BEGIN {print s += $2}' sales.txt`
* [ ] `awk '{s = $2} END {print s}' sales.txt`

> **Explanation:** The main block runs for every line, adding up `$2`, and `END` runs once after the last line. `print sum += $2` prints a running total on every line, and `BEGIN` runs before any input is read.

#### Q. Which command prints the names of users whose UID is 1000 or higher?

* [ ] `awk -F: '$3 > 1000 {print $1}' /etc/passwd`
* [x] `awk -F: '$3 >= 1000 {print $1}' /etc/passwd`
* [ ] `awk -F: '{if $3 >= 1000 print $1}' /etc/passwd`
* [ ] `awk -F: '/1000/ {print $1}' /etc/passwd`

> **Explanation:** A condition before the action limits which lines it runs on. `> 1000` would leave out UID 1000 itself, `if` needs parentheses around its condition, and `/1000/` matches the text `1000` anywhere in the line.

#### Q. The shell variable `limit` holds a number. Which command prints field 1 of every line whose field 3 is greater than it?

* [ ] `awk '$3 > $limit {print $1}' data.txt`
* [x] `awk -v min="$limit" '$3 > min {print $1}' data.txt`
* [ ] `awk '$3 > "$limit" {print $1}' data.txt`
* [ ] `awk -F "$limit" '$3 > min {print $1}' data.txt`

> **Explanation:** `-v name=value` sets an awk variable before input is read. Inside single quotes the shell expands nothing, so awk reads `$limit` as a field reference and `"$limit"` as literal text. `-F` sets the field separator.

#### Q. Which command prints `x,z` for the input `x:y:z`?

* [ ] `awk -F, '{print $1, $3}'`
* [ ] `awk -F: -v RS=, '{print $1, $3}'`
* [ ] `awk -F: '{print $1 $3}'`
* [x] `awk -F: -v OFS=, '{print $1, $3}'`

> **Explanation:** `-F:` splits the input on colons, and `OFS` is the output field separator that `print` places between comma-separated items. `RS` is the record separator, and `$1 $3` joins the fields with nothing in between.

#### Q. What does this command print?

```bash
printf 'a\nb\n' | awk '{ printf "%s", $1 }'
```

* [ ] `a` and `b` on separate lines
* [ ] `a b`
* [x] `ab`, with no newline at the end
* [ ] `%s%s`

> **Explanation:** Unlike `print`, `printf` adds neither `OFS` nor a newline, so the fields run together. Put `\n` in the format string, as in `printf "%s\n", $1`, to get one value per line.

#### Q. Which command counts how often each value in column 1 of `access.log` appears?

* [x] `awk '{c[$1]++} END {for (k in c) print k, c[k]}' access.log`
* [ ] `awk '{print $1, NR}' access.log`
* [ ] `awk 'END {print $1, NF}' access.log`
* [ ] `awk '{c++} END {print $1, c}' access.log`

> **Explanation:** `c[$1]++` uses an associative array keyed by the first field, and the `END` loop prints each key with its count. The order of `for (k in c)` is unspecified, so pipe the output to `sort` if needed.

#### Q. What does `sort numbers.txt` output for lines `10`, `9` and `100`?

* [ ] `9`, `10`, `100`
* [ ] `100`, `10`, `9`
* [ ] `9`, `100`, `10`
* [x] `10`, `100`, `9`

> **Explanation:** Without options, `sort` compares lines as text, character by character, so `1…` sorts before `9`. Use `sort -n` to compare numerically and get `9`, `10`, `100`.

#### Q. Which command sorts `scores.txt` numerically by its second column, highest first?

* [x] `sort -k2 -nr scores.txt`
* [ ] `sort -k2 scores.txt`
* [ ] `sort -n scores.txt -r 2`
* [ ] `sort -t2 -n scores.txt`

> **Explanation:** `-k2` sorts on a key starting at field 2 (`-k2,2` stops it there), `-n` compares numbers and `-r` reverses the order. `-t` sets the field delimiter, not the key.

#### Q. Why does `uniq` usually appear after `sort` in a pipeline?

* [ ] `uniq` only works on numeric data
* [ ] `uniq` reverses the order of its input
* [x] `uniq` removes only adjacent duplicate lines
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
* [ ] `echo 'hello world' | tr -d '[:lower:]'`
* [x] `echo 'hello world' | tr '[:lower:]' '[:upper:]'`
* [ ] `echo 'hello world' | tr -s '[:lower:]'`

> **Explanation:** `tr SET1 SET2` maps each character in the first set to the matching one in the second. `'a-z' 'A-Z'` also works for ASCII text. `-d` deletes characters and `-s` squeezes repeats.

#### Q. What does `echo 'a1b2c3' | tr -d '0-9'` print?

* [x] `abc`
* [ ] `123`
* [ ] `a1b2c3`
* [ ] `a b c`

> **Explanation:** `tr -d` deletes every character in the given set, here the digits, leaving `abc`.

#### Q. What does this command print?

```bash
printf 'first\nsecond' | wc -l
```

* [ ] `2`
* [ ] `0`
* [ ] `12`
* [x] `1`

> **Explanation:** `wc -l` counts newline characters, and the last line, `second`, has no trailing newline, so the count is 1. `12` is what `wc -c` would print, since the input is 12 bytes.

#### Q. What ends up in `out.txt` after you run this command?

```bash
ls /nonexistent . 2>&1 > out.txt
```

* [ ] Both the listing of `.` and the error message
* [x] Only the listing of `.`; the error still appears on the terminal
* [ ] Only the error message
* [ ] Nothing, because the two redirections cancel out

> **Explanation:** Redirections are applied left to right. `2>&1` points stderr at the current stdout, the terminal, and only then does `> out.txt` move stdout to the file. Write `> out.txt 2>&1`, or `&> out.txt` in Bash, to capture both.

#### Q. What does this script print?

```bash
name=World
cat <<'EOF'
Hello $name
EOF
```

* [ ] `Hello World`
* [ ] `Hello ` followed by an empty value
* [ ] Nothing; `cat` waits for keyboard input
* [x] `Hello $name`

> **Explanation:** Quoting the delimiter (`'EOF'`) turns off expansion in the here-document, so `$name` is printed literally. With an unquoted `EOF`, the shell expands the variable and prints `Hello World`.

#### Q. Which Bash command compares the sorted contents of `a.txt` and `b.txt` without creating temporary files?

* [ ] `diff $(sort a.txt) $(sort b.txt)`
* [ ] `sort a.txt | diff b.txt`
* [x] `diff <(sort a.txt) <(sort b.txt)`
* [ ] `diff < sort a.txt < sort b.txt`

> **Explanation:** Process substitution `<(command)` runs the command and passes `diff` a path such as `/dev/fd/63` to read its output from. `$(...)` would paste the sorted lines in as file names, and `<` redirects from a file, not a command.

#### Q. Which command finds regular files larger than 100 MiB under the current directory?

* [x] `find . -type f -size +100M`
* [ ] `find . -type f -size 100M`
* [ ] `find . -type f -size -100M`
* [ ] `find . -type f -bigger 100M`

> **Explanation:** `+N` means more than N, `-N` means less than N, and a bare `N` means exactly N (rounded up to whole units). A bare number with no suffix counts 512-byte blocks. `find` has no `-bigger` test.

#### Q. A directory holds three files of 0 bytes, 100 bytes and 500 KiB. Which of them does GNU `find . -type f -size -1M` list?

* [ ] All three files
* [ ] The 100-byte and 500 KiB files
* [ ] None of them
* [x] Only the 0-byte file

> **Explanation:** `find` rounds each size up to whole units before comparing, so every non-empty file counts as 1 MiB, and "less than 1" leaves only empty files. Use `-size -1024k` (or `-size -1048576c`) for files under 1 MiB.

#### Q. The current directory contains `a.log`, and `sub/` contains `a.log` and `b.log`. What does `find . -name *.log` (unquoted) print?

* [x] `./a.log` and `./sub/a.log`
* [ ] All three `.log` files
* [ ] Only `./a.log`
* [ ] An error saying paths must precede the expression

> **Explanation:** The shell expands `*.log` to `a.log` before `find` runs, so `find` looks for files named exactly `a.log`. If two names matched in the current directory, `find` would fail with "paths must precede expression". Quote the pattern: `-name '*.log'`.

#### Q. Which command finds files under `/home` that are not owned by `guest`?

* [ ] `find /home -user guest`
* [x] `find /home ! -user guest`
* [ ] `find /home -user !guest`
* [ ] `find /home -not guest`

> **Explanation:** `!` (or `-not`) negates the test that follows it. `-user !guest` would look for a user literally named `!guest`.

#### Q. What is the difference between `-exec rm -- {} \;` and `-exec rm -- {} +` in `find`?

* [ ] `\;` deletes directories and `+` deletes only files
* [ ] `+` asks before each deletion, while `\;` does not
* [x] `\;` runs `rm` once per file, while `+` passes many files to each `rm`
* [ ] `\;` is for GNU `find` only, while `+` works everywhere

> **Explanation:** `{} +` batches pathnames like `xargs`, creating far fewer processes. Both forms handle spaces in names safely. Asking before each command is what `-ok` does.

#### Q. Which `find` action asks for confirmation before running the command on each match?

* [ ] `-exec rm {} \;`
* [ ] `-delete`
* [ ] `-print0`
* [x] `-ok rm {} \;`

> **Explanation:** `-ok` works like `-exec` but prompts before each command, which is a safer way to delete. `-delete` removes matches without asking.

#### Q. Which command uses the `locate` database to find paths containing `readme`, whether written `README`, `Readme` or `readme`?

* [ ] `locate readme`
* [x] `locate -i readme`
* [ ] `locate -b readme`
* [ ] `locate -c readme`

> **Explanation:** `-i` ignores case. `-b` matches only the base name and `-c` prints the number of matches, both still case-sensitive. `locate` searches a prebuilt database, so run `sudo updatedb` first if the files are very new.

#### Q. In Bash on Ubuntu, `which ls` prints `/usr/bin/ls`, but typing `ls` runs `ls --color=auto`. Which command shows the alias as well as the files on `PATH`?

* [ ] `which -a ls`
* [ ] `locate ls`
* [x] `type -a ls`
* [ ] `whereis -b ls`

> **Explanation:** `type` is a Bash builtin that reports aliases, functions, builtins and files on `PATH`, in the order the shell resolves them. Ubuntu's external `which` searches only `PATH`, and `whereis` only standard directories.

#### Q. What does this `xargs -n 2` pipeline print?

```bash
printf '%s\n' one two three four five | xargs -n 2 echo
```

* [x] `one two`, `three four`, then `five` on separate lines
* [ ] `one two three four five` on one line
* [ ] Each word on its own line
* [ ] `one two` only

> **Explanation:** `-n 2` passes at most two arguments to each `echo`, so `echo` runs three times. Without `-n`, `xargs` puts as many arguments as fit into a single command.

#### Q. Why does `printf '%s\n' a.tmp b.tmp | rm` fail with `rm: missing operand`?

* [ ] `printf` writes to stderr, so the pipe receives nothing
* [ ] `rm` needs `-f` before it reads names from a pipe
* [ ] The names must be separated by NUL bytes, not newlines
* [x] `rm` takes file names as arguments and ignores stdin; `xargs rm --` would pass them

> **Explanation:** A pipe connects stdout to stdin, but `rm` never reads stdin. `xargs` turns its input into command-line arguments (stdin to argv). NUL separators make that safe for odd names, but they are not what is missing here.

#### Q. Which pipeline safely deletes every `*.tmp` file, even when names contain spaces or newlines?

* [ ] `find . -name '*.tmp' | xargs rm`
* [ ] `ls *.tmp | xargs rm -rf`
* [x] `find . -name '*.tmp' -print0 | xargs -0 rm --`
* [ ] `find . -name '*.tmp' | xargs -n 1 rm`

> **Explanation:** `-print0` ends each pathname with a NUL byte, and `xargs -0` splits only on NUL, so whitespace stays part of the name. By default `xargs` splits on blanks, so `a b.tmp` becomes two bad arguments.

#### Q. In `xargs rm --`, which program is the `--` for, and why is it there?

* [x] It is for `rm`, so that file names starting with `-` are not read as options
* [ ] It is for `xargs`, telling it to read NUL-separated input
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
* [ ] Add `-t` to `xargs`
* [ ] Add `-f` to `rm`
* [x] Add `-r` to `xargs`

> **Explanation:** GNU `xargs` normally runs the command once even with empty input; `-r` (`--no-run-if-empty`) skips it. `-r` is not in POSIX, so `find ... -exec rm -- {} +` is the portable alternative.

#### Q. Which command creates a gzip-compressed archive `project.tar.gz` from the directory `project/`?

* [x] `tar -czf project.tar.gz project/`
* [ ] `tar -xzf project.tar.gz project/`
* [ ] `tar -tzf project.tar.gz project/`
* [ ] `gzip -r project/ > project.tar.gz`

> **Explanation:** `-c` creates, `-z` compresses through gzip and `-f` names the archive. `-x` extracts and `-t` lists. `gzip -r` compresses each file separately and makes no archive.

#### Q. Why does `tar -cfz backup.tar.gz project/` not create a compressed `backup.tar.gz`?

* [ ] `-z` must always come before `-c` in a bundled option group
* [ ] `tar` refuses to create archive names that end in `.gz`
* [x] `-f` takes `z` as the archive name, so `backup.tar.gz` is treated as a file to add
* [ ] `-cfz` creates a bzip2-compressed archive instead of gzip

> **Explanation:** `-f` needs an argument, and in a bundled option group it takes the rest of the group. GNU tar writes an uncompressed archive named `z` and complains that `backup.tar.gz` does not exist. Keep `f` last: `-czf backup.tar.gz project/`.

#### Q. How do you list the contents of `backup.tar.gz` without extracting anything?

* [ ] `tar -xzvf backup.tar.gz`
* [x] `tar -tzvf backup.tar.gz`
* [ ] `tar -czvf backup.tar.gz`
* [ ] `gzip -d backup.tar.gz`

> **Explanation:** `-t` lists the archive's members, and with `-v` it shows permissions, owner, size and date like `ls -l`. `gzip -d` would decompress the file into `backup.tar`.

#### Q. Which command extracts `project.tar.gz` into `/opt/restore` instead of the current directory?

* [ ] `tar -xzf project.tar.gz > /opt/restore`
* [ ] `tar -xzf /opt/restore project.tar.gz`
* [ ] `tar -czf project.tar.gz -C /opt/restore`
* [x] `tar -xzf project.tar.gz -C /opt/restore`

> **Explanation:** `-C DIR` makes `tar` change into that directory before extracting. Redirecting stdout does not move the extracted files, and `-c` would create an archive instead.

#### Q. Which command extracts only `docs/readme.txt` from `archive.tar.gz`?

* [ ] `tar -tzf archive.tar.gz docs/readme.txt`
* [ ] `gzip -d archive.tar.gz docs/readme.txt`
* [x] `tar -xzf archive.tar.gz docs/readme.txt`
* [ ] `tar -xzf docs/readme.txt archive.tar.gz`

> **Explanation:** Member names given after the archive limit extraction to those paths, which must match how they appear in `tar -tzf`. The archive name must come straight after `-f`.

#### Q. Which command archives `app/` but leaves out its `app/tmp/` contents?

* [x] `tar --exclude='app/tmp/*' -czf app.tar.gz app/`
* [ ] `tar -czf app.tar.gz app/ --exclude='app/tmp/*'`
* [ ] `tar -czf app.tar.gz app/ -x app/tmp`
* [ ] `tar -czf app.tar.gz app/ | grep -v tmp`

> **Explanation:** In GNU tar, `--exclude` is position-sensitive and must come before the file operands it applies to; placed last, tar 1.35 warns that it "has no effect" and keeps the files. The quotes stop the shell from expanding the pattern.

#### Q. Which `tar` option compresses with `xz`, as in `archive.tar.xz`?

* [x] `-J`
* [ ] `-z`
* [ ] `-j`
* [ ] `-x`

> **Explanation:** `-z` is gzip (`.tar.gz`), `-j` is bzip2 (`.tar.bz2`) and capital `-J` is xz (`.tar.xz`). Lowercase `-x` means extract.

#### Q. In `ssh user@host 'tar -czf - /srv/data' > data.tar.gz`, what does the `-` after `-f` do?

* [ ] It tells `tar` to read the list of files from standard input
* [x] It makes `tar` write the archive to stdout, which `ssh` carries to the local file
* [ ] It turns off compression for the network transfer
* [ ] It names the archive `-` on the remote host

> **Explanation:** As the archive name, `-` means standard output when creating (and standard input when extracting). The archive travels over the SSH connection and the local shell redirects it into `data.tar.gz`, so no copy is left on the remote host.

#### Q. You need to split `big.tar` into 100 MiB pieces for upload, then rebuild it later. Which pair of commands works?

* [ ] `tar --split=100M big.tar`, then `tar --join big.tar.*`
* [ ] `gzip -b 100M big.tar`, then `gunzip big.tar.gz`
* [x] `split -b 100M big.tar part_`, then `cat part_* > big.tar`
* [ ] `split -l 100 big.tar part_`, then `tar -xf part_*`

> **Explanation:** `split -b` cuts the file into byte-sized chunks named `part_aa`, `part_ab` and so on (`100M` means 100 MiB). The glob expands in sorted order, so `cat` puts them back together correctly. `-l` splits by lines.

#### Q. Which command compresses `log.txt` to `log.txt.gz` but also keeps the original file?

* [ ] `gzip log.txt`
* [ ] `gzip -d log.txt`
* [ ] `gzip -l log.txt`
* [x] `gzip -k log.txt`

> **Explanation:** By default `gzip` replaces the file with the `.gz` version. `-k` keeps the original, `-d` decompresses and `-l` lists compression statistics.

#### Q. Which crontab line runs `/opt/backup.sh` at 7:30 AM, Monday to Friday?

* [x] `30 7 * * 1-5 /opt/backup.sh`
* [ ] `7 30 * * 1-5 /opt/backup.sh`
* [ ] `30 7 1-5 * * /opt/backup.sh`
* [ ] `30 7 * 1-5 * /opt/backup.sh`

> **Explanation:** The five fields are minute, hour, day of month, month and day of week. `1-5` in the fifth field means Monday to Friday; in the third field it would mean the 1st to the 5th of the month.

#### Q. When does the crontab entry `*/15 * * * * /opt/check.sh` run?

* [ ] 15 minutes after cron starts, then every 15 minutes from that point
* [ ] Once at 15 minutes past each hour
* [ ] Every 15 seconds
* [x] At minutes 0, 15, 30 and 45 of every hour

> **Explanation:** Cron schedules are calendar matches, not timers. `*/15` in the minute field is a step value that matches minutes divisible by 15. `15` alone would run once an hour at minute 15.

#### Q. When does the crontab entry `0 9 13 * 5 /opt/report.sh` run?

* [ ] At 9:00 only on Fridays that fall on the 13th
* [x] At 9:00 on every 13th of the month and also on every Friday
* [ ] At 9:00 on the 13th of May
* [ ] At 13:09 every Friday

> **Explanation:** When both day of month and day of week are restricted (neither is `*`), cron runs the job when either one matches. To run only on Friday the 13th, keep one field and test the other inside the command.

#### Q. A cron job `0 2 * * * tar -czf /backup/$(date +%F).tar.gz /data` never produces a correctly named file. Why?

* [ ] Cron cannot run `tar` unless it is given as `/usr/bin/tar`
* [ ] Command substitution `$(...)` is not allowed in cron jobs
* [x] An unescaped `%` is special in crontab commands and must be written as `\%`
* [ ] Cron jobs are not permitted to write into `/backup`

> **Explanation:** Cron turns `%` into a newline, and text after the first `%` is sent to the command's stdin. Write `date +\%F`, or move the logic into a script.

#### Q. A script runs fine from your terminal, but its cron job fails with `mytool: command not found`. What is the most likely cause?

* [ ] Cron cannot run shell scripts, only binaries
* [ ] Cron jobs always run as root, which cannot see user programs
* [ ] The crontab line is missing the username field
* [x] Cron starts jobs with a minimal environment whose `PATH` lacks the directory of `mytool`

> **Explanation:** Cron runs jobs through `/bin/sh` with a small environment (typically `PATH=/usr/bin:/bin`), without your shell startup files. Use absolute paths or set `PATH=` at the top of the crontab. User crontabs have no username field.

#### Q. How do lines in `/etc/crontab` differ from lines you add with `crontab -e`?

* [x] They have an extra username field between the time fields and the command
* [ ] They have no time fields, only a user and a command
* [ ] They use seconds as an extra first field before the minute
* [ ] They must spell out months and weekdays by full name

> **Explanation:** System crontabs (`/etc/crontab` and `/etc/cron.d/`) say which user runs each job. User crontabs already belong to one user, so they have only the five time fields and the command.

#### Q. A laptop is often off at night, and you want a daily job to still run once it boots. Which tool suits this better than plain cron?

* [ ] `at`
* [x] `anacron`
* [ ] `watch`
* [ ] `nohup`

> **Explanation:** Plain cron skips jobs whose time passes while the machine is off. `anacron` tracks when each periodic job last ran and catches up after boot, which suits machines that are not always on.

#### Q. In the `/etc/anacrontab` line `7 10 cron.weekly run-parts /etc/cron.weekly`, what does `10` mean?

* [ ] Run the job at 10:00
* [ ] Run the job every 10 days
* [x] Wait 10 minutes after anacron starts before running the job
* [ ] Keep the last 10 timestamps for the job

> **Explanation:** The fields are the period in days (`7`), the delay in minutes (`10`), the job identifier, which names its timestamp file in `/var/spool/anacron/`, and the command. Anacron has no time-of-day field.
