#### Q. Which `sed` command deletes all lines containing the word “error” in-place in `log.txt`?

* [ ] `sed '/error/d' log.txt > log.txt`
* [x] `sed -i '/error/d' log.txt`
* [ ] `sed '/error/d' -o log.txt`
* [ ] `sed --delete /error/ log.txt`
* [ ] `sed -r '/error/d' -i log.txt`

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


