## Variable Types

In Unix-style shells, variables let you store and reuse pieces of information, such as your preferred editor:

```bash
EDITOR=vim
```

the directories where executables are searched:

```bash
PATH=/usr/local/bin:$PATH
```

or temporary data inside a script:

```bash
count=0
```

You will mainly encounter two related but different concepts:

1. **Shell variables**
2. **Environment variables**

The most important distinction is this:

> A shell variable belongs only to the current shell.
> An environment variable is exported so that child processes can inherit it.

### Shell Variables

A **shell variable** exists only inside the current shell process.

Example:

```bash
count=5
echo "$count"
```

Example output:

```bash
5
```

This variable is available to the current shell, but it is **not automatically available to programs started from the shell**.

For example:

```bash
count=5
python3 -c 'import os; print(os.environ.get("count"))'
```

Example output:

```bash
None
```

Why?

Because `count` is only a shell variable. It has not been exported into the environment.

To make it visible to child processes, you must use `export`:

```bash
export count=5
python3 -c 'import os; print(os.environ.get("count"))'
```

Example output:

```bash
5
```

So:

```bash
VAR=value
```

creates a shell variable.

```bash
export VAR=value
```

creates or updates a shell variable **and marks it for inheritance by child processes**.

### Environment Variables

Environment variables are key-value pairs that a process passes to its child processes. They are commonly used for configuration, such as executable search paths, language settings, home directories, credentials, and feature flags.

Examples include:

```bash
PATH=/usr/local/bin:/usr/bin:/bin
HOME=/home/ahmad
LANG=en_US.UTF-8
EDITOR=vim
DATABASE_URL=postgres://user:pass@localhost/db
```

A process has its own environment. When it starts another process, the child receives a **copy** of that environment.

That copy is extremely important:

> Environment variables flow downward from parent to child.
> They do not flow upward from child to parent.

#### Listing Environment Variables

Use `printenv` to list environment variables visible to the current process:

```bash
printenv
```

Example output:

```bash
PATH=/usr/local/bin:/usr/bin:/bin:/home/ahmad/bin
HOME=/home/ahmad
LANG=en_US.UTF-8
```

Each line has this form:

```bash
VARIABLE=value
```

You can also print one variable:

```bash
printenv HOME
```

Example output:

```bash
/home/ahmad
```

Or use shell expansion:

```bash
echo "$HOME"
```

Example output:

```bash
/home/ahmad
```

#### Shell Variable vs Environment Variable

Consider this example:

```bash
name=Ahmad
echo "$name"
```

Example output:

```bash
Ahmad
```

The shell can see the variable.

But a child process cannot:

```bash
name=Ahmad
python3 -c 'import os; print(os.environ.get("name"))'
```

Example output:

```bash
None
```

Now export it:

```bash
export name=Ahmad
python3 -c 'import os; print(os.environ.get("name"))'
```

Example output:

```bash
Ahmad
```

So the rule is:

| Assignment          | Visible in current shell? | Visible to child processes? |
| ------------------- | ------------------------: | --------------------------: |
| `VAR=value`         |                       Yes |                          No |
| `export VAR=value`  |                       Yes |                         Yes |
| `VAR=value command` |     Only for that command |  Yes, for that command only |

Example of a temporary environment variable for one command:

```bash
DATABASE_URL='postgres://localhost/test' python3 -c 'import os; print(os.environ["DATABASE_URL"])'
```

Example output:

```bash
postgres://localhost/test
```

After the command finishes:

```bash
echo "$DATABASE_URL"
```

Example output:

```bash
```

It is empty because `DATABASE_URL=value command` only applies to that one command invocation.

#### How Long Do Environment Variables Persist?

Environment variables do **not** automatically persist forever. Their lifetime depends on where they were defined.

##### 1. Current Terminal Session

If you run:

```bash
export API_KEY=abc123
```

then `API_KEY` exists in the current shell process and is inherited by child processes started from that shell.

Example:

```bash
export API_KEY=abc123
python3 -c 'import os; print(os.environ.get("API_KEY"))'
```

Example output:

```bash
abc123
```

But when you close the terminal, that shell process exits, and the variable disappears.

##### 2. Between Different Terminals

Environment variables do **not** automatically propagate between separate terminal windows.

Terminal 1:

```bash
export PROJECT=backend
echo "$PROJECT"
```

Example output:

```bash
backend
```

Terminal 2:

```bash
echo "$PROJECT"
```

Example output:

```bash
```

The second terminal does not see it because each terminal starts its own shell process. They are usually siblings or independent descendants of some terminal emulator process, not parent and child of each other.

So:

> Terminal 1 variables do not magically appear in Terminal 2.

If you want variables available in every new terminal, put them in a shell startup file such as:

```bash
~/.bashrc
~/.zshrc
~/.profile
~/.bash_profile
```

For example:

```bash
echo 'export EDITOR=vim' >> ~/.bashrc
source ~/.bashrc
```

Now future interactive Bash sessions that read `~/.bashrc` will set `EDITOR`.

##### 3. Permanent Variables via Startup Files

To persist a variable across new shell sessions, add it to a shell startup file.

For Bash interactive shells:

```bash
echo 'export EDITOR=vim' >> ~/.bashrc
source ~/.bashrc
```

Then:

```bash
echo "$EDITOR"
```

Example output:

```bash
vim
```

For Zsh:

```bash
echo 'export EDITOR=vim' >> ~/.zshrc
source ~/.zshrc
```

For login shells, especially on macOS or server logins, variables may belong in:

```bash
~/.profile
~/.bash_profile
~/.zprofile
```

The exact file depends on shell and login mode.

### Parent and Child Processes

Every running program is a process.

Your shell is a process. When you run a command from the shell, that command usually runs as a **child process** of the shell.

Example:

```bash
python3 script.py
```

Usually means:

```text
shell process
└── python3 process
```

The shell is the parent. `python3` is the child.

The child receives a **copy** of the parent’s environment.

#### Concrete Example: Parent Gives Environment to Child

Run this in the shell:

```bash
export COLOR=blue
python3 -c 'import os; print("Child sees COLOR =", os.environ.get("COLOR"))'
```

Example output:

```bash
Child sees COLOR = blue
```

The Python process inherited `COLOR` from the shell.

#### Concrete Example: Child Changes Its Own Environment

Now try this:

```bash
export COLOR=blue

python3 -c 'import os; os.environ["COLOR"] = "red"; print("Child changed COLOR to", os.environ["COLOR"])'

echo "Parent still has COLOR=$COLOR"
```

Example output:

```bash
Child changed COLOR to red
Parent still has COLOR=blue
```

The child changed its own copy. The parent shell did not change.

This is one of the most important rules:

> A child process cannot modify the environment of its parent process.

The environment is copied downward, not shared upward.

#### Fork and Exec

When a Unix-style shell runs an external command, it usually uses two important operations:

1. `fork()`
2. `exec()`

They do different things.

##### `fork()`

`fork()` creates a new child process.

Conceptually, the child starts as a copy of the parent.

That includes:

* variables in memory
* open file descriptors
* current working directory
* environment variables

Modern systems optimize this with copy-on-write, but conceptually it is a copy.

After `fork()`:

```text
parent shell
├── environment: COLOR=blue
└── child process
    └── environment: COLOR=blue
```

The child has its own copy. If the child changes `COLOR`, the parent is not affected.

##### `exec()`

`exec()` does **not** create a new process.

Instead, it replaces the current process image with another program.

That means the same process ID continues, but the program code changes.

Important:

> `exec()` keeps the environment of the current process unless a different environment is explicitly supplied.

So if a child process has:

```bash
COLOR=blue
```

and then calls `exec()` to become `python3`, the new Python program still sees:

```bash
COLOR=blue
```

But that does not mean the parent shell is affected.

#### Normal Shell Command: `fork()` + `exec()`

When you run:

```bash
ls
```

the shell usually does this:

```text
1. shell calls fork()
2. child process is created
3. child calls exec("ls")
4. child becomes ls
5. ls runs
6. ls exits
7. parent shell continues
```

Process tree:

```text
shell
└── ls
```

The important point:

> The shell itself did not become `ls`.
> A child process became `ls`.

That is why changes made by `ls`, Python, Node, Ruby, or any other child process do not affect the parent shell environment.

#### Why “exec Keeps the Same Environment” Can Be Confusing

This sentence is true:

> `exec()` keeps the same environment.

But it means:

> The process that calls `exec()` keeps its own environment while becoming a new program.

It does **not** mean:

> The child can change the parent’s environment.

Example:

```bash
export MODE=dev
python3 -c 'import os; print(os.environ["MODE"])'
```

The shell forks a child. The child execs Python. Python sees `MODE=dev`.

But:

```bash
export MODE=dev
python3 -c 'import os; os.environ["MODE"]="prod"; print(os.environ["MODE"])'
echo "$MODE"
```

Example output:

```bash
prod
dev
```

Python changed its own environment, not the shell’s environment.

#### Running `exec` Directly in the Shell

There is a special case.

If you run:

```bash
exec python3
```

then the shell itself is replaced by Python.

There is no new child shell continuing afterward.

Example:

```bash
export MODE=dev
exec python3 -c 'import os; print(os.environ["MODE"])'
```

Example output:

```bash
dev
```

After Python exits, your shell is gone. The terminal may close or return to the parent terminal program.

So:

```bash
python3
```

usually means:

```text
shell forks child
child execs python3
parent shell remains
```

But:

```bash
exec python3
```

means:

```text
shell execs python3
shell is replaced
no original shell remains
```

#### Fork vs Exec Summary

| Operation      | Creates new process? | Keeps same process ID? | Environment behavior                                          |
| -------------- | -------------------: | ---------------------: | ------------------------------------------------------------- |
| `fork()`       |                  Yes | No, child gets new PID | Child receives copy of parent environment                     |
| `exec()`       |                   No |                    Yes | New program keeps current process environment unless replaced |
| normal command |         Yes, usually |     Child gets new PID | Shell forks; child execs command with copied environment      |
| `exec command` |                   No |                    Yes | Current shell is replaced by command                          |

#### Can a Child Process Change the Parent’s Environment?

No.

This does not work:

```bash
export TOKEN=old

python3 -c 'import os; os.environ["TOKEN"]="new"'

echo "$TOKEN"
```

Example output:

```bash
old
```

The Python process changed only itself.

Another example with a shell script:

Create `change_token.sh`:

```bash
#!/usr/bin/env bash
export TOKEN=new
echo "Inside child script: TOKEN=$TOKEN"
```

Run it:

```bash
chmod +x change_token.sh

export TOKEN=old
./change_token.sh
echo "Back in parent shell: TOKEN=$TOKEN"
```

Example output:

```bash
Inside child script: TOKEN=new
Back in parent shell: TOKEN=old
```

Why?

Because running `./change_token.sh` starts a child process.

The child process can change its own environment, but not the parent shell’s environment.

#### When Can a Script Change the Current Shell?

A script can change your current shell only if you **source** it.

Sourcing means the file is executed inside the current shell process instead of in a child process.

Create `change_token.sh`:

```bash
export TOKEN=new
echo "Inside sourced script: TOKEN=$TOKEN"
```

Run it with `source`:

```bash
export TOKEN=old
source ./change_token.sh
echo "Back in same shell: TOKEN=$TOKEN"
```

Example output:

```bash
Inside sourced script: TOKEN=new
Back in same shell: TOKEN=new
```

The shorthand for `source` is `.`:

```bash
. ./change_token.sh
```

So:

| Command            | Runs in child process? | Can modify current shell variables? |
| ------------------ | ---------------------: | ----------------------------------: |
| `./script.sh`      |                    Yes |                                  No |
| `bash script.sh`   |                    Yes |                                  No |
| `source script.sh` |                     No |                                 Yes |
| `. script.sh`      |                     No |                                 Yes |

This is why tools that modify your shell environment often tell you to use `source`.

For example:

```bash
source venv/bin/activate
```

A Python virtual environment activation script must modify your current shell’s `PATH`, so it has to be sourced.

If you ran it as a normal script:

```bash
./venv/bin/activate
```

it would modify only a child process and then exit, leaving your shell unchanged.

### Subshells

A subshell is a child shell process.

Parentheses create a subshell:

```bash
COLOR=blue

(
  COLOR=red
  echo "Inside subshell: COLOR=$COLOR"
)

echo "Outside subshell: COLOR=$COLOR"
```

Example output:

```bash
Inside subshell: COLOR=red
Outside subshell: COLOR=blue
```

The assignment inside the subshell does not affect the parent shell.

By contrast, braces run in the current shell:

```bash
COLOR=blue

{
  COLOR=red
  echo "Inside block: COLOR=$COLOR"
}

echo "Outside block: COLOR=$COLOR"
```

Example output:

```bash
Inside block: COLOR=red
Outside block: COLOR=red
```

So:

| Syntax          | Process behavior      | Parent affected? |
| --------------- | --------------------- | ---------------: |
| `( commands )`  | runs in subshell      |               No |
| `{ commands; }` | runs in current shell |              Yes |

Remember the required spacing and semicolon with braces:

```bash
{ commands; }
```

not:

```bash
{commands}
```

### Builtins vs External Commands

Some commands are shell builtins. They run inside the shell process itself.

Examples:

```bash
cd
export
unset
readonly
alias
set
source
```

These can change the current shell.

For example:

```bash
cd /tmp
```

changes the current shell’s working directory.

If `cd` were an external child process, it would be useless, because the child would change its directory and then exit, leaving the parent shell unchanged.

External commands, such as:

```bash
ls
python3
grep
awk
node
ruby
```

usually run in child processes.

They inherit environment variables, but cannot modify the parent shell.

### Common Environment Variables

#### `HISTSIZE`

The number of commands your shell remembers is controlled by `HISTSIZE`.

```bash
echo "$HISTSIZE"
```

Example output:

```bash
1000
```

Here, the shell keeps the last 1,000 commands in memory.

You can increase it:

```bash
export HISTSIZE=2000
```

If you set it to `0`, command history may be disabled for the current session:

```bash
export HISTSIZE=0
```

A related variable is `HISTFILESIZE`, which controls how many lines are saved to the history file.

Example:

```bash
echo "$HISTFILESIZE"
```

Example output:

```bash
2000
```

#### `HOME`

`HOME` stores your home directory.

```bash
echo "$HOME"
```

Example output:

```bash
/home/ahmad
```

Many commands use this to find user-specific files.

For example:

```bash
cp config.json "$HOME/.config/myapp/"
```

The tilde shortcut also usually expands using the home directory:

```bash
cd ~
```

If `HOME` points to a nonexistent path, you may see errors in containers, minimal environments, or incorrectly configured users.

#### `PWD`

`PWD` stores the current working directory.

```bash
echo "$PWD"
```

Example output:

```bash
/home/ahmad/projects/env_test
```

The shell updates `PWD` when you use `cd`.

Example:

```bash
cd /tmp
echo "$PWD"
```

Example output:

```bash
/tmp
```

If your directory path involves symbolic links, `PWD` usually shows the logical path.

Example:

```bash
pwd
```

may show:

```bash
/home/ahmad/link_to_project
```

while:

```bash
pwd -P
```

may show the physical path:

```bash
/mnt/data/projects/real_project
```

#### `OLDPWD`

`OLDPWD` stores the previous working directory.

Example:

```bash
pwd
cd /tmp
echo "$OLDPWD"
```

Example output:

```bash
/home/ahmad/projects/env_test
```

You can jump back using:

```bash
cd -
```

Example output:

```bash
/home/ahmad/projects/env_test
```

#### `HOSTNAME`

`HOSTNAME` identifies the current machine.

```bash
echo "$HOSTNAME"
```

Example output:

```bash
ahmad-laptop
```

This is useful in logs and backups:

```bash
tar -czf "$(date +%F)-$HOSTNAME-backup.tar.gz" "$HOME/projects"
```

Example filename:

```bash
2026-05-03-ahmad-laptop-backup.tar.gz
```

In containers or cloud machines, the hostname may be a generated ID.

#### `PATH`

`PATH` is one of the most important environment variables.

It is a colon-separated list of directories where the shell searches for executable commands.

```bash
echo "$PATH"
```

Example output:

```bash
/usr/local/bin:/usr/bin:/bin:/home/ahmad/bin
```

When you type:

```bash
python3
```

the shell searches each directory in `PATH` from left to right.

You can see which executable is found:

```bash
which python3
```

Example output:

```bash
/usr/bin/python3
```

or:

```bash
command -v python3
```

Example output:

```bash
/usr/bin/python3
```

To append a directory:

```bash
export PATH="$PATH:/opt/tools/bin"
```

To make your custom scripts override system binaries, prepend the directory:

```bash
export PATH="$HOME/custom/bin:$PATH"
```

Prepending is powerful but risky. If `$HOME/custom/bin` contains a script named `ls`, then typing `ls` may run your custom script instead of `/bin/ls`.

You can inspect command resolution with:

```bash
type ls
```

Example output:

```bash
ls is /usr/bin/ls
```

#### `LANG`

`LANG` controls locale settings such as language, character encoding, sorting behavior, and formatting.

```bash
echo "$LANG"
```

Example output:

```bash
en_US.UTF-8
```

A common safe value is:

```bash
export LANG=en_US.UTF-8
```

If locale variables are misconfigured, programs may warn about unsupported locales or handle Unicode incorrectly.

#### `EDITOR`

`EDITOR` tells command-line tools which editor to open.

```bash
export EDITOR=vim
```

Programs such as `git commit`, `crontab -e`, and some CLI tools may use it.

Example:

```bash
git config --global core.editor "$EDITOR"
```

### Changing Variables

#### Current Shell Only

To set a variable in the current shell:

```bash
DATABASE_URL='postgres://user:pass@localhost/db'
echo "$DATABASE_URL"
```

Example output:

```bash
postgres://user:pass@localhost/db
```

This is a shell variable. Child processes will not inherit it unless you export it.

```bash
python3 -c 'import os; print(os.environ.get("DATABASE_URL"))'
```

Example output:

```bash
None
```

Now export it:

```bash
export DATABASE_URL
python3 -c 'import os; print(os.environ.get("DATABASE_URL"))'
```

Example output:

```bash
postgres://user:pass@localhost/db
```

You can also set and export in one line:

```bash
export DATABASE_URL='postgres://user:pass@localhost/db'
```

#### One Command Only

You can set an environment variable for only one command:

```bash
DEBUG=1 python3 -c 'import os; print(os.environ.get("DEBUG"))'
```

Example output:

```bash
1
```

Afterward:

```bash
echo "$DEBUG"
```

Example output:

```bash
```

This is useful for temporary configuration:

```bash
NODE_ENV=production npm start
```

or:

```bash
AWS_PROFILE=dev terraform plan
```

#### Permanent Updates

For permanent updates, add the export statement to a startup file.

Bash:

```bash
echo 'export EDITOR=vim' >> ~/.bashrc
source ~/.bashrc
```

Zsh:

```bash
echo 'export EDITOR=vim' >> ~/.zshrc
source ~/.zshrc
```

Then verify:

```bash
echo "$EDITOR"
```

Example output:

```bash
vim
```

### Operations on Variables

#### Removing Variables

Use `unset` to remove a shell or environment variable from the current shell.

```bash
export API_KEY=abc123
echo "$API_KEY"
```

Example output:

```bash
abc123
```

Now unset it:

```bash
unset API_KEY
echo "$API_KEY"
```

Example output:

```bash
```

If the variable was exported, `unset` also removes it from the environment of future child processes.

#### Making Variables Read-Only

Once you have set a variable that should not change, mark it as read-only:

```bash
readonly max_retries=5
```

Now reassignment fails:

```bash
max_retries=3
```

Example output:

```bash
bash: max_retries: readonly variable
```

Unsetting also fails:

```bash
unset max_retries
```

Example output:

```bash
bash: unset: max_retries: cannot unset: readonly variable
```

This is useful for constants in scripts:

```bash
readonly CONFIG_DIR="$HOME/.config/myapp"
readonly MAX_RETRIES=5
```

#### Enforcing Defined Variables

Referencing an unset variable normally expands to an empty string.

Example:

```bash
echo "Hello $username"
```

If `username` is unset, output is:

```bash
Hello 
```

That can hide bugs.

Use:

```bash
set -u
```

or:

```bash
set -o nounset
```

Now referencing an unset variable causes an error.

Example script:

```bash
#!/usr/bin/env bash
set -u

echo "Count is $count"
```

If `count` is not set, Bash exits with an error like:

```bash
bash: count: unbound variable
```

You can also require a variable explicitly:

```bash
: "${API_KEY:?API_KEY is required}"
```

If `API_KEY` is unset or empty, the script stops with an error.

Example:

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${API_KEY:?API_KEY is required}"

echo "Using API key..."
```

#### Customizing Your Prompt with `PS1`

Your shell prompt is controlled by the `PS1` variable.

Example:

```bash
PS1="\u@\h:\w\$ "
```

Your prompt may look like:

```bash
ahmad@machine:/home/ahmad$
```

Common escape sequences:

| Escape sequence | Meaning                                 |
| --------------- | --------------------------------------- |
| `\u`            | Current username                        |
| `\h`            | Hostname up to the first dot            |
| `\H`            | Full hostname                           |
| `\w`            | Current working directory               |
| `\W`            | Basename of current working directory   |
| `\$`            | `#` if root, otherwise `$`              |
| `\n`            | Newline                                 |
| `\t`            | Current time in 24-hour HH:MM:SS format |

Example with a newline:

```bash
PS1="\u@\h:\w\n\$ "
```

Prompt:

```bash
ahmad@machine:/home/ahmad/projects
$ 
```

`PS1` is usually a shell variable used by the interactive shell itself. It does not usually need to be exported.

#### Word Splitting and `IFS`

`IFS` stands for **Internal Field Separator**.

It controls how Bash splits unquoted variable expansions into words.

By default, `IFS` contains:

* space
* tab
* newline

Example:

```bash
list="alpha beta gamma"

for item in $list; do
  echo "$item"
done
```

Example output:

```bash
alpha
beta
gamma
```

The shell split `$list` on spaces because `$list` was unquoted.

If you quote it:

```bash
list="alpha beta gamma"

for item in "$list"; do
  echo "$item"
done
```

Example output:

```bash
alpha beta gamma
```

Quoted expansions are not split.

#### Splitting on Commas

You can temporarily set `IFS` to split comma-separated data.

```bash
data="red,green,blue"

IFS=',' read -r first second third <<< "$data"

echo "$first"
echo "$second"
echo "$third"
```

Example output:

```bash
red
green
blue
```

Another example:

```bash
data="red,green,blue"
old_ifs=$IFS
IFS=','

for color in $data; do
  echo "$color"
done

IFS=$old_ifs
```

Example output:

```bash
red
green
blue
```

Be careful changing global `IFS`. It can break scripts in surprising ways.

Prefer local or one-command usage where possible:

```bash
IFS=',' read -r a b c <<< "$data"
```

#### Empty `IFS`

Setting `IFS` to an empty value disables word splitting for unquoted expansions.

```bash
list="a b c"
IFS=

for item in $list; do
  echo "$item"
done
```

Example output:

```bash
a b c
```

This can be useful in rare cases, but it can also break loops that expect normal splitting.

#### Listing Shell Definitions

Use `set` to inspect shell variables, functions, and shell state:

```bash
set
```

Example output:

```bash
BASH=/usr/bin/bash
BASHOPTS=checkwinsize:cmdhist:complete_fullquote:expand_aliases:extglob:extquote
HOME=/home/ahmad
HOSTNAME=ahmad-laptop
IFS=$' \t\n'
PATH=/usr/local/bin:/usr/bin:/bin
...
```

`set` shows more than `printenv`.

| Command      | Shows                                                            |
| ------------ | ---------------------------------------------------------------- |
| `printenv`   | Environment variables                                            |
| `env`        | Environment variables, or runs command with modified environment |
| `set`        | Shell variables, environment variables, functions, shell options |
| `declare -p` | Shell variables in reusable Bash syntax                          |
| `export -p`  | Exported variables                                               |

Example:

```bash
declare -p HOME
```

Example output:

```bash
declare -x HOME="/home/ahmad"
```

The `-x` means exported.

## `env`: Running Commands with Modified Environments

The `env` command can run a program with a modified environment.

Example:

```bash
env MODE=test python3 -c 'import os; print(os.environ["MODE"])'
```

Example output:

```bash
test
```

You can also start with an empty environment using `env -i`:

```bash
env -i python3 -c 'import os; print(os.environ)'
```

Example output:

```bash
environ({})
```

A more realistic example:

```bash
env -i PATH=/usr/bin:/bin HOME="$HOME" python3 -c 'import os; print(os.environ)'
```

This runs Python with only the variables you explicitly provide.

This is useful for debugging scripts that accidentally depend on your personal shell environment.

#### Safe Script Defaults

When writing shell scripts intended to run reliably, it is common to start with:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

Meaning:

| Option        | Meaning                                                  |
| ------------- | -------------------------------------------------------- |
| `-e`          | Exit immediately if a command fails                      |
| `-u`          | Treat unset variables as errors                          |
| `-o pipefail` | Make pipelines fail if any command in the pipeline fails |

Example:

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${INPUT_FILE:?INPUT_FILE is required}"

grep "ERROR" "$INPUT_FILE" | sort | uniq
```

Without `pipefail`, this pipeline:

```bash
grep "ERROR" missing.txt | sort
```

might appear successful because `sort` succeeded, even though `grep` failed.

With `pipefail`, the whole pipeline fails.

### Practical Debugging Examples

#### Check Whether a Variable Is Exported

```bash
MY_VAR=hello
export EXPORTED_VAR=world

printenv MY_VAR
printenv EXPORTED_VAR
```

Example output:

```bash
world
```

`MY_VAR` does not appear because it is not exported.

You can also check with Python:

```bash
MY_VAR=hello
export EXPORTED_VAR=world

python3 -c 'import os; print("MY_VAR =", os.environ.get("MY_VAR")); print("EXPORTED_VAR =", os.environ.get("EXPORTED_VAR"))'
```

Example output:

```bash
MY_VAR = None
EXPORTED_VAR = world
```

#### Prove That a Child Cannot Change the Parent

```bash
export LEVEL=parent

python3 -c '
import os
print("Before change in child:", os.environ.get("LEVEL"))
os.environ["LEVEL"] = "child"
print("After change in child:", os.environ.get("LEVEL"))
'

echo "Back in parent: LEVEL=$LEVEL"
```

Example output:

```bash
Before change in child: parent
After change in child: child
Back in parent: LEVEL=parent
```

### Prove That Sourcing Changes the Current Shell

Create `set_level.sh`:

```bash
LEVEL=sourced
export LEVEL
```

Run normally:

```bash
export LEVEL=parent
bash set_level.sh
echo "$LEVEL"
```

Example output:

```bash
parent
```

Now source it:

```bash
source set_level.sh
echo "$LEVEL"
```

Example output:

```bash
sourced
```

#### Prove That Different Terminals Do Not Share Environment Changes

Terminal 1:

```bash
export DEMO=terminal_one
echo "$DEMO"
```

Example output:

```bash
terminal_one
```

Terminal 2:

```bash
echo "$DEMO"
```

Example output:

```bash
```

They are separate shell processes.

### Environment Variables and Python Virtual Environments

Python virtual environments are often described as “isolated Python environments,” but it is important to understand what they really do.

A Python virtual environment does **not** create a new operating-system-level container. It does not fully isolate your machine, your filesystem, your users, or your processes.

Instead, a virtual environment mainly changes which Python interpreter and Python packages your shell uses.

The most important mechanism is environment-variable and shell-variable modification.

### What a Python Virtual Environment Contains

When you create a virtual environment:

```bash
python3 -m venv .venv
```

Python creates a directory like this:

```text
.venv/
├── bin/
│   ├── activate
│   ├── python
│   ├── python3
│   └── pip
├── lib/
│   └── python3.x/
│       └── site-packages/
└── pyvenv.cfg
```

On Windows, the layout is slightly different:

```text
.venv/
├── Scripts/
│   ├── activate
│   ├── python.exe
│   └── pip.exe
├── Lib/
│   └── site-packages/
└── pyvenv.cfg
```

The parts are:

| Part                                | Meaning                                                |
| ----------------------------------- | ------------------------------------------------------ |
| `.venv/bin/python`                  | Python interpreter used inside the virtual environment |
| `.venv/bin/pip`                     | Pip associated with that environment                   |
| `.venv/lib/python3.x/site-packages` | Packages installed into that environment               |
| `.venv/bin/activate`                | Shell script that modifies your current shell          |
| `pyvenv.cfg`                        | Metadata telling Python where the venv came from       |

#### Creating a Virtual Environment Does Not Activate It

This command:

```bash
python3 -m venv .venv
```

only creates the `.venv` directory.

It does **not** change your current shell.

After creating it, this may still point to the system Python:

```bash
which python
```

Example output:

```bash
/usr/bin/python
```

or:

```bash
which python3
```

Example output:

```bash
/usr/bin/python3
```

To use the virtual environment conveniently, you usually activate it.

#### Activating a Virtual Environment

On Linux/macOS with Bash or Zsh:

```bash
source .venv/bin/activate
```

or equivalently:

```bash
. .venv/bin/activate
```

After activation:

```bash
which python
```

Example output:

```bash
/home/ahmad/project/.venv/bin/python
```

And:

```bash
which pip
```

Example output:

```bash
/home/ahmad/project/.venv/bin/pip
```

Your prompt may also change:

```text
(.venv) ahmad@machine:~/project$
```

That prompt change is only cosmetic, but it helps you see that the venv is active.

#### Why Activation Must Be Sourced

This is the most important part.

The activation script changes your **current shell environment**.

That is why you run:

```bash
source .venv/bin/activate
```

not:

```bash
./.venv/bin/activate
```

If you run it as a normal script:

```bash
./.venv/bin/activate
```

it runs in a child process.

That child process may modify its own environment, but then it exits. Your parent shell stays unchanged.

This is the same rule as before:

> A child process cannot modify the environment of its parent process.

So activation must be sourced because sourcing executes the file inside the current shell process.

### What `activate` Actually Changes

Activation mostly does four things:

1. Sets `VIRTUAL_ENV`
2. Modifies `PATH`
3. Stores the old `PATH`
4. Changes the shell prompt

A simplified activation script looks like this:

```bash
VIRTUAL_ENV="/home/ahmad/project/.venv"
export VIRTUAL_ENV

_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH

_OLD_VIRTUAL_PS1="$PS1"
PS1="(.venv) $PS1"
```

After activation:

```bash
echo "$VIRTUAL_ENV"
```

Example output:

```bash
/home/ahmad/project/.venv
```

And:

```bash
echo "$PATH"
```

Example output:

```bash
/home/ahmad/project/.venv/bin:/usr/local/bin:/usr/bin:/bin
```

The important change is that the venv’s `bin` directory is placed at the **front** of `PATH`.

Before activation:

```bash
PATH=/usr/local/bin:/usr/bin:/bin
```

After activation:

```bash
PATH=/home/ahmad/project/.venv/bin:/usr/local/bin:/usr/bin:/bin
```

So when you type:

```bash
python
```

the shell searches:

```text
/home/ahmad/project/.venv/bin
/usr/local/bin
/usr/bin
/bin
```

It finds:

```text
/home/ahmad/project/.venv/bin/python
```

before the system Python. That is the main trick.

#### Activation Does Not Magically Change Python Globally

Activation does not replace `/usr/bin/python`. It does not uninstall system packages. It does not rewrite your operating system.It only changes your current shell so that commands like:

```bash
python
pip
pytest
django-admin
black
ruff
mypy
```

resolve first to executables inside:

```bash
.venv/bin/
```

You can verify this:

```bash
which python
which pip
```

Example output:

```bash
/home/ahmad/project/.venv/bin/python
/home/ahmad/project/.venv/bin/pip
```

But the system Python still exists:

```bash
/usr/bin/python3 --version
```

Example output:

```bash
Python 3.11.6
```

### `pip install` Inside a Virtual Environment

After activation:

```bash
source .venv/bin/activate
pip install requests
```

`pip` resolves to:

```bash
.venv/bin/pip
```

So packages are installed into:

```text
.venv/lib/python3.x/site-packages/
```

You can check:

```bash
python -c 'import requests; print(requests.__file__)'
```

Example output:

```text
/home/ahmad/project/.venv/lib/python3.11/site-packages/requests/__init__.py
```

That means the package is installed in the virtual environment, not globally.

#### Concrete Example

Suppose your project directory is:

```bash
/home/ahmad/demo
```

Create a venv:

```bash
cd /home/ahmad/demo
python3 -m venv .venv
```

Before activation:

```bash
which python
```

Example output:

```bash
/usr/bin/python
```

Activate:

```bash
source .venv/bin/activate
```

Now:

```bash
echo "$VIRTUAL_ENV"
```

Example output:

```bash
/home/ahmad/demo/.venv
```

And:

```bash
which python
```

Example output:

```bash
/home/ahmad/demo/.venv/bin/python
```

Install a package:

```bash
pip install requests
```

Check where it went:

```bash
python -c 'import requests; print(requests.__file__)'
```

Example output:

```bash
/home/ahmad/demo/.venv/lib/python3.11/site-packages/requests/__init__.py
```

Deactivate:

```bash
deactivate
```

Now:

```bash
which python
```

Example output:

```bash
/usr/bin/python
```

So activation temporarily changes command lookup. Deactivation restores the old shell state.

#### What `deactivate` Does

When you activate a venv, the activation script usually saves old values:

```bash
_OLD_VIRTUAL_PATH="$PATH"
_OLD_VIRTUAL_PS1="$PS1"
```

When you run:

```bash
deactivate
```

it restores them.

Conceptually:

```bash
PATH="$_OLD_VIRTUAL_PATH"
PS1="$_OLD_VIRTUAL_PS1"
unset VIRTUAL_ENV
unset _OLD_VIRTUAL_PATH
unset _OLD_VIRTUAL_PS1
```

After deactivation:

```bash
echo "$VIRTUAL_ENV"
```

Example output:

```bash
```

And:

```bash
which python
```

Example output:

```bash
/usr/bin/python
```

`deactivate` works because activation defines a shell function named `deactivate` in your current shell.

That function would not exist if you ran the activation script as a normal child process.

### Why `python -m pip` Is Often Safer Than `pip`

Inside a venv, this usually works:

```bash
pip install flask
```

But this is often safer:

```bash
python -m pip install flask
```

Why?

Because it guarantees that `pip` belongs to the exact `python` interpreter you are using.

Example:

```bash
which python
```

Output:

```bash
/home/ahmad/demo/.venv/bin/python
```

Then:

```bash
python -m pip install flask
```

installs Flask into the environment used by:

```bash
/home/ahmad/demo/.venv/bin/python
```

This avoids mistakes where `pip` and `python` accidentally point to different installations.

#### You Can Use a Venv Without Activating It

Activation is convenient, but not required.

You can directly call the venv’s Python:

```bash
./.venv/bin/python script.py
```

or:

```bash
./.venv/bin/python -m pip install requests
```

This works even if the venv is not activated.

Why?

Because you explicitly chose the interpreter:

```bash
./.venv/bin/python
```

So the shell does not need to find `python` through `PATH`.

This is useful in scripts, cron jobs, systemd services, and CI pipelines.

Example:

```bash
/home/ahmad/demo/.venv/bin/python /home/ahmad/demo/app.py
```

That is often more reliable than relying on activation.

#### What a Venv Does Not Isolate

A Python virtual environment does **not** isolate everything.

It does not isolate:

| Thing                                                                     |                                        Is it isolated by venv? |
| ------------------------------------------------------------------------- | -------------------------------------------------------------: |
| Python packages                                                           |                                                     Mostly yes |
| Python interpreter command lookup                                         |                                            Yes, through `PATH` |
| System libraries                                                          |                                                             No |
| Filesystem                                                                |                                                             No |
| Network access                                                            |                                                             No |
| Users and permissions                                                     |                                                             No |
| Environment variables like `HOME`, `USER`, `PATH` except modified entries |                                                             No |
| Running processes                                                         |                                                             No |
| OS packages installed by apt/dnf/brew                                     |                                                             No |
| Non-Python tools                                                          | No, unless installed into `.venv/bin` and found through `PATH` |

For real OS-level isolation, use tools like containers, virtual machines, or sandboxing mechanisms.

A venv is mainly for Python dependency isolation.

#### Venv Activation as Environment Manipulation

So when people say:

```bash
source .venv/bin/activate
```

they are really saying:

> Modify my current shell so that this project’s Python and Python-installed command-line tools come first.

The activation script does not enter a magical Python mode.

It mainly changes:

```bash
PATH
VIRTUAL_ENV
PS1
```

and defines:

```bash
deactivate
```

This is why these commands work after activation:

```bash
python
pip
pytest
black
ruff
mypy
```

They are found inside:

```bash
.venv/bin/
```

because that directory is now first in `PATH`.

### Container Build, Credentials, and Environment Variables

Containers use environment variables heavily, but you need to separate three different moments:

1. **Image build time**
2. **Container runtime**
3. **Application process runtime**

These are related, but they are not the same.

A common mistake is to think:

> “If I set an environment variable during `docker build`, my running container will automatically and safely have it.”

Sometimes it will. Sometimes it will not. And sometimes it will leak secrets into the image.

### Build Time vs Runtime

#### Build Time

Build time happens when you run:

```bash
docker build -t myapp .
```

During build time, Docker executes instructions in your `Dockerfile`.

Example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

The `RUN` commands execute while the image is being built.

For example:

```dockerfile
RUN echo "Installing dependencies"
```

runs during:

```bash
docker build -t myapp .
```

not when the container starts.

#### Runtime

Runtime happens when you start a container from an image:

```bash
docker run myapp
```

At runtime, Docker creates a container process and starts the command from `CMD` or `ENTRYPOINT`.

Example:

```dockerfile
CMD ["python", "app.py"]
```

means that when you run:

```bash
docker run myapp
```

Docker starts roughly:

```bash
python app.py
```

inside the container.

#### Environment Variables at Runtime

The most common way to pass configuration into a container is with `docker run -e`.

Example:

```bash
docker run -e APP_ENV=production myapp
```

Inside the container, the application can read:

```python
import os

print(os.environ.get("APP_ENV"))
```

Example output:

```text
production
```

You can pass multiple variables:

```bash
docker run \
  -e APP_ENV=production \
  -e LOG_LEVEL=info \
  -e DATABASE_URL='postgres://user:pass@db:5432/app' \
  myapp
```

Inside Python:

```python
import os

app_env = os.environ.get("APP_ENV")
log_level = os.environ.get("LOG_LEVEL")
database_url = os.environ.get("DATABASE_URL")

print(app_env)
print(log_level)
print(database_url)
```

Example output:

```text
production
info
postgres://user:pass@db:5432/app
```

These variables are part of the environment of the main process inside the container.

If that process starts child processes, those children inherit the environment too.

#### Runtime Environment Variables Flow to Child Processes

Suppose your image runs this Python app:

```python
# app.py
import os
import subprocess

print("Parent APP_ENV:", os.environ.get("APP_ENV"))

subprocess.run([
    "python",
    "-c",
    "import os; print('Child APP_ENV:', os.environ.get('APP_ENV'))"
])
```

Run the container:

```bash
docker run -e APP_ENV=production myapp
```

Example output:

```text
Parent APP_ENV: production
Child APP_ENV: production
```

The child Python process inherited the environment from the parent Python process.

But if the child changes the environment, the parent does not change.

Example:

```python
# app.py
import os
import subprocess

os.environ["APP_ENV"] = "parent"

subprocess.run([
    "python",
    "-c",
    "import os; os.environ['APP_ENV']='child'; print('Child APP_ENV:', os.environ['APP_ENV'])"
])

print("Parent APP_ENV:", os.environ["APP_ENV"])
```

Example output:

```text
Child APP_ENV: child
Parent APP_ENV: parent
```

Same rule as normal Unix processes:

> Environment variables are inherited downward.
> They do not propagate upward from child to parent.

#### `ENV` in a Dockerfile

Dockerfile `ENV` sets an environment variable in the image.

Example:

```dockerfile
FROM python:3.12-slim

ENV APP_ENV=production
ENV LOG_LEVEL=info

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
```

Then in `app.py`:

```python
import os

print(os.environ.get("APP_ENV"))
print(os.environ.get("LOG_LEVEL"))
```

Build and run:

```bash
docker build -t myapp .
docker run myapp
```

Example output:

```text
production
info
```

`ENV` values become default environment variables for containers created from the image.

You can override them at runtime:

```bash
docker run -e APP_ENV=development myapp
```

Then `APP_ENV` is:

```text
development
```

So:

```dockerfile
ENV APP_ENV=production
```

means:

> If the user does not provide another value at runtime, use `APP_ENV=production`.

#### `ARG` in a Dockerfile

Dockerfile `ARG` is for build-time variables.

Example:

```dockerfile
FROM python:3.12-slim

ARG APP_VERSION
RUN echo "Building version: $APP_VERSION"

CMD ["python", "--version"]
```

Build with:

```bash
docker build --build-arg APP_VERSION=1.2.3 -t myapp .
```

During the build, Docker can use:

```bash
$APP_VERSION
```

inside Dockerfile instructions after the `ARG` declaration.

But `ARG` is not automatically available at runtime.

Example:

```dockerfile
FROM python:3.12-slim

ARG APP_VERSION

CMD ["python", "-c", "import os; print(os.environ.get('APP_VERSION'))"]
```

Build:

```bash
docker build --build-arg APP_VERSION=1.2.3 -t myapp .
```

Run:

```bash
docker run myapp
```

Example output:

```text
None
```

Why?

Because `ARG` is build-time only unless you explicitly copy it into `ENV`.

### Copying `ARG` into `ENV`

You can convert a build-time argument into a runtime environment variable:

```dockerfile
FROM python:3.12-slim

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

CMD ["python", "-c", "import os; print(os.environ.get('APP_VERSION'))"]
```

Build:

```bash
docker build --build-arg APP_VERSION=1.2.3 -t myapp .
```

Run:

```bash
docker run myapp
```

Example output:

```text
1.2.3
```

But be careful:

> Anything put into `ENV` becomes part of the image configuration and can be inspected later.

This is usually fine for non-secret values like versions:

```dockerfile
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION
```

But it is dangerous for secrets.

#### Do Not Put Secrets in `ENV` During Build

Bad example:

```dockerfile
FROM python:3.12-slim

ENV AWS_ACCESS_KEY_ID=AKIA...
ENV AWS_SECRET_ACCESS_KEY=supersecret

RUN python build_script.py
```

This bakes secrets into the image metadata/layers.

Anyone with access to the image may be able to inspect them.

For example:

```bash
docker inspect myapp
```

may reveal environment variables stored in the image config.

You should also avoid:

```dockerfile
ARG AWS_SECRET_ACCESS_KEY
RUN echo "$AWS_SECRET_ACCESS_KEY"
```

and:

```bash
docker build --build-arg AWS_SECRET_ACCESS_KEY=supersecret -t myapp .
```

Even though `ARG` is build-time, it can still leak through:

* build logs
* image history
* cached layers
* package manager config files
* files created during build
* shell history or CI logs

So the rule is:

> Do not use Dockerfile `ARG` or `ENV` for secrets unless you fully understand where they may be recorded.

#### Build Secrets: Safer Build-Time Credentials

Sometimes you need credentials during build.

For example:

* installing private Python packages
* downloading private source files
* authenticating to a private package registry
* cloning a private repository

Do not do this:

```dockerfile
ARG PIP_TOKEN
RUN pip install private-package --extra-index-url "https://token:$PIP_TOKEN@example.com/simple"
```

The token may leak into build history or logs.

A safer BuildKit-style pattern is to use a build secret.

Example Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1.7

FROM python:3.12-slim

WORKDIR /app

RUN --mount=type=secret,id=pip_token \
    PIP_TOKEN="$(cat /run/secrets/pip_token)" && \
    pip install private-package \
      --extra-index-url "https://token:${PIP_TOKEN}@example.com/simple"
```

Build:

```bash
DOCKER_BUILDKIT=1 docker build \
  --secret id=pip_token,env=PIP_TOKEN \
  -t myapp .
```

With:

```bash
export PIP_TOKEN=supersecret
```

The secret is mounted temporarily during that `RUN` instruction at:

```text
/run/secrets/pip_token
```

It is not meant to be persisted in the final image.

Still be careful not to echo it, write it into files, or include it in generated configuration.

Bad:

```dockerfile
RUN --mount=type=secret,id=pip_token \
    cat /run/secrets/pip_token > /app/token.txt
```

That copies the secret into the image.

Good:

```dockerfile
RUN --mount=type=secret,id=pip_token \
    PIP_TOKEN="$(cat /run/secrets/pip_token)" && \
    use-token-temporarily
```

#### Runtime Secrets

For runtime secrets, pass them at container start time instead of baking them into the image.

Example:

```bash
docker run \
  -e DATABASE_URL='postgres://user:pass@db:5432/app' \
  -e API_KEY='secret-value' \
  myapp
```

Inside Python:

```python
import os

database_url = os.environ["DATABASE_URL"]
api_key = os.environ["API_KEY"]
```

This is common and convenient.

However, environment variables are not perfect secret storage.

They can sometimes be exposed through:

* process inspection
* container inspection
* crash dumps
* application logs
* debug pages
* accidental `printenv`
* shell history
* orchestrator metadata

For stronger secret management, use the secret mechanism provided by your platform.

Examples:

* Docker secrets
* Kubernetes Secrets
* cloud secret managers
* mounted secret files
* CI/CD secret stores

#### `--env-file`

Instead of passing many `-e` options, you can use an env file.

Create `.env`:

```env
APP_ENV=production
LOG_LEVEL=info
DATABASE_URL=postgres://user:pass@db:5432/app
```

Run:

```bash
docker run --env-file .env myapp
```

Inside Python:

```python
import os

print(os.environ.get("APP_ENV"))
print(os.environ.get("LOG_LEVEL"))
print(os.environ.get("DATABASE_URL"))
```

Example output:

```text
production
info
postgres://user:pass@db:5432/app
```

Important:

> An env file is not automatically secret-safe.

If `.env` contains credentials, protect it:

```bash
chmod 600 .env
```

and do not commit it:

```bash
echo ".env" >> .gitignore
```

#### Docker Compose Environment Variables

With Compose, you can pass runtime environment variables like this:

```yaml
services:
  app:
    image: myapp
    environment:
      APP_ENV: production
      LOG_LEVEL: info
      DATABASE_URL: postgres://user:pass@db:5432/app
```

Or:

```yaml
services:
  app:
    image: myapp
    env_file:
      - .env
```

Then:

```bash
docker compose up
```

The variables are injected into the container at runtime.

Inside the app:

```python
import os

print(os.environ.get("APP_ENV"))
```

Example output:

```text
production
```

#### Compose `.env` vs Container `env_file`

This is a frequent source of confusion.

Compose has two different concepts:

1. `.env` file used by Compose for variable substitution
2. `env_file:` used to pass variables into the container

They are not the same thing.

#### Compose `.env` for Substitution

Suppose you have a `.env` file:

```env
APP_IMAGE=myapp:latest
HOST_PORT=8080
```

And `compose.yaml`:

```yaml
services:
  app:
    image: ${APP_IMAGE}
    ports:
      - "${HOST_PORT}:8000"
```

Compose uses `.env` to substitute values before creating containers.

This affects the Compose file.

It does not automatically mean every variable in `.env` is injected into the container environment.

#### `env_file:` for Container Environment

To inject variables into the container, use:

```yaml
services:
  app:
    image: myapp
    env_file:
      - .env
```

Now variables from `.env` become environment variables inside the container.

So:

```yaml
services:
  app:
    image: ${APP_IMAGE}
```

uses `.env` for Compose substitution.

But:

```yaml
services:
  app:
    env_file:
      - .env
```

passes variables into the container.

#### Build Args in Compose

Compose can also pass build arguments.

```yaml
services:
  app:
    build:
      context: .
      args:
        APP_VERSION: "1.2.3"
```

Dockerfile:

```dockerfile
FROM python:3.12-slim

ARG APP_VERSION
RUN echo "Building version $APP_VERSION"
```

This makes `APP_VERSION` available during image build.

But it does not automatically exist at runtime.

To preserve it at runtime:

```dockerfile
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION
```

Again, this is okay for non-secrets like versions, commit SHAs, or build metadata.

Do not use this pattern for credentials.

#### Multi-Stage Builds and Secrets

Multi-stage builds can reduce accidental secret leakage, but they are not magic.

Example:

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app

RUN --mount=type=secret,id=pip_token \
    PIP_TOKEN="$(cat /run/secrets/pip_token)" && \
    pip wheel private-package \
      --extra-index-url "https://token:${PIP_TOKEN}@example.com/simple" \
      -w /wheels

FROM python:3.12-slim

COPY --from=builder /wheels /wheels
RUN pip install /wheels/*

CMD ["python", "--version"]
```

The final image does not include the whole builder filesystem, only what you copy.

But if you copy secret-containing files from the builder stage, they still leak.

Bad:

```dockerfile
COPY --from=builder /root/.config/pip/pip.conf /root/.config/pip/pip.conf
```

Good:

```dockerfile
COPY --from=builder /wheels /wheels
```

Also avoid writing secrets to files in the first place.

### Runtime Environment Variables Override Dockerfile `ENV`

Dockerfile:

```dockerfile
FROM python:3.12-slim

ENV APP_ENV=production

CMD ["python", "-c", "import os; print(os.environ['APP_ENV'])"]
```

Build:

```bash
docker build -t myapp .
```

Run normally:

```bash
docker run myapp
```

Example output:

```text
production
```

Override at runtime:

```bash
docker run -e APP_ENV=development myapp
```

Example output:

```text
development
```

So precedence is roughly:

```text
runtime -e / env_file / orchestrator env
overrides
Dockerfile ENV default
```

#### Environment Variables and Image Layers

Docker images are built in layers.

Each Dockerfile instruction may create metadata or filesystem changes.

Example:

```dockerfile
FROM python:3.12-slim

ENV API_KEY=supersecret
```

Even if you later do:

```dockerfile
ENV API_KEY=
```

the secret may still exist in image history or earlier metadata.

Similarly:

```dockerfile
RUN echo "supersecret" > /tmp/secret.txt
RUN rm /tmp/secret.txt
```

can still be dangerous because the earlier layer may contain the file.

Do not rely on deleting secrets later in the Dockerfile.

The safer rule:

> Never put secrets into image layers in the first place.

#### Example: Bad Container Secret Pattern

Bad Dockerfile:

```dockerfile
FROM python:3.12-slim

ARG GITHUB_TOKEN

RUN git clone https://$GITHUB_TOKEN@github.com/example/private-repo.git /app

WORKDIR /app

CMD ["python", "app.py"]
```

Build:

```bash
docker build \
  --build-arg GITHUB_TOKEN=ghp_secret \
  -t myapp .
```

Problems:

* token may appear in build logs
* token may appear in shell history
* token may appear in image metadata/history
* token may be cached in layers
* private repository metadata may remain in the image

Better:

```dockerfile
# syntax=docker/dockerfile:1.7

FROM python:3.12-slim

WORKDIR /app

RUN --mount=type=secret,id=github_token \
    GITHUB_TOKEN="$(cat /run/secrets/github_token)" && \
    git clone https://x-access-token:${GITHUB_TOKEN}@github.com/example/private-repo.git .
```

Build:

```bash
export GITHUB_TOKEN=ghp_secret

DOCKER_BUILDKIT=1 docker build \
  --secret id=github_token,env=GITHUB_TOKEN \
  -t myapp .
```

Even better, for many workflows:

* clone source code outside the Docker build using CI credentials
* pass the source directory as build context
* do not make Docker responsible for fetching private source

#### Example: Python App Reading Runtime Configuration

`app.py`:

```python
import os
import sys

required = ["DATABASE_URL", "SECRET_KEY"]

missing = [name for name in required if not os.environ.get(name)]

if missing:
    print(f"Missing required environment variables: {', '.join(missing)}", file=sys.stderr)
    sys.exit(1)

database_url = os.environ["DATABASE_URL"]
secret_key = os.environ["SECRET_KEY"]

print("App configured successfully")
print("DATABASE_URL exists:", bool(database_url))
print("SECRET_KEY exists:", bool(secret_key))
```

Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

Build:

```bash
docker build -t env-demo .
```

Run without env vars:

```bash
docker run env-demo
```

Example output:

```text
Missing required environment variables: DATABASE_URL, SECRET_KEY
```

Run with env vars:

```bash
docker run \
  -e DATABASE_URL='postgres://user:pass@db:5432/app' \
  -e SECRET_KEY='supersecret' \
  env-demo
```

Example output:

```text
App configured successfully
DATABASE_URL exists: True
SECRET_KEY exists: True
```

This is the standard pattern:

> Build the image once.
> Configure it differently at runtime using environment variables.

#### Example: Build-Time Version, Runtime Secrets

A good split:

* Build-time: app version, commit SHA, build date
* Runtime: database password, API tokens, secret keys

Dockerfile:

```dockerfile
FROM python:3.12-slim

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
```

`app.py`:

```python
import os

print("App version:", os.environ.get("APP_VERSION"))
print("Runtime environment:", os.environ.get("APP_ENV"))
print("Has database URL:", bool(os.environ.get("DATABASE_URL")))
```

Build:

```bash
docker build \
  --build-arg APP_VERSION=1.2.3 \
  -t myapp:1.2.3 .
```

Run:

```bash
docker run \
  -e APP_ENV=production \
  -e DATABASE_URL='postgres://user:pass@db:5432/app' \
  myapp:1.2.3
```

Example output:

```text
App version: 1.2.3
Runtime environment: production
Has database URL: True
```

This is a healthy pattern because `APP_VERSION` is not secret, while `DATABASE_URL` is provided at runtime.

#### Containers and `.env` Files in Python Apps

Many Python apps use `python-dotenv` to load a `.env` file:

```python
from dotenv import load_dotenv
import os

load_dotenv()

print(os.environ.get("DATABASE_URL"))
```

This is common in local development.

But inside containers, there are two different approaches:

##### Approach 1: Docker injects environment variables

```bash
docker run --env-file .env myapp
```

Then Python reads from `os.environ`.

No need for `python-dotenv` inside the container.

##### Approach 2: App reads `.env` from the filesystem

Dockerfile:

```dockerfile
COPY .env /app/.env
```

Python:

```python
from dotenv import load_dotenv
load_dotenv()
```

This is usually worse for secrets because the `.env` file becomes part of the image if copied during build.

Avoid:

```dockerfile
COPY .env .
```

Better:

```dockerfile
COPY . .
```

with `.dockerignore` containing:

```text
.env
.git
__pycache__
.venv
```

Then pass variables at runtime:

```bash
docker run --env-file .env myapp
```

#### `.dockerignore` and Secret Protection

Your build context is everything Docker can see during build.

If your project contains:

```text
.env
.aws/
.ssh/
.venv/
.git/
```

and you run:

```bash
docker build -t myapp .
```

Docker may send those files to the Docker daemon as part of the build context unless excluded.

Use `.dockerignore`.

Example `.dockerignore`:

```text
.env
.env.*
!.env.example

.git
.venv
__pycache__
*.pyc

.aws
.ssh
id_rsa
id_ed25519
```

This helps prevent accidental secret exposure.

Important:

> `.dockerignore` does not protect secrets already copied into the image by Dockerfile instructions.
> It only keeps files out of the build context.

#### Inspecting Container Environment

To see environment variables in a running container:

```bash
docker exec container_name printenv
```

Example:

```bash
docker exec myapp-container printenv APP_ENV
```

To inspect image default environment variables:

```bash
docker image inspect myapp
```

or:

```bash
docker inspect myapp
```

You may see Dockerfile `ENV` values in the image configuration.

For a running container:

```bash
docker inspect container_name
```

This can also reveal runtime environment variables.

That is another reason not to treat environment variables as perfect secret storage.

#### Kubernetes Environment Variables

In Kubernetes, containers also receive environment variables at runtime.

Example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: app
          image: myapp:1.2.3
          env:
            - name: APP_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
```

Inside Python:

```python
import os

print(os.environ.get("APP_ENV"))
print(bool(os.environ.get("DATABASE_URL")))
```

The values are injected into the process environment when the container starts.

A Kubernetes Secret is better than hardcoding secrets in the image, but environment-variable secrets can still be exposed to processes with sufficient permissions.

Many production systems prefer mounting secrets as files.

Example:

```yaml
volumeMounts:
  - name: secret-volume
    mountPath: "/run/secrets"
    readOnly: true
volumes:
  - name: secret-volume
    secret:
      secretName: myapp-secrets
```

Then your app reads:

```python
from pathlib import Path

database_url = Path("/run/secrets/database-url").read_text().strip()
```

#### CI/CD Credentials and Docker Builds

CI systems often provide secrets as environment variables.

Example:

```bash
GITHUB_TOKEN
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
PIP_INDEX_URL
NPM_TOKEN
```

Be careful when using them in Docker builds.

Bad:

```bash
docker build \
  --build-arg AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
  -t myapp .
```

Better for build-time secret needs:

```bash
DOCKER_BUILDKIT=1 docker build \
  --secret id=aws_secret_access_key,env=AWS_SECRET_ACCESS_KEY \
  -t myapp .
```

Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1.7

FROM python:3.12-slim

RUN --mount=type=secret,id=aws_secret_access_key \
    AWS_SECRET_ACCESS_KEY="$(cat /run/secrets/aws_secret_access_key)" && \
    some-build-command
```

Even with BuildKit secrets:

* do not print the secret
* do not write it into files copied into final image
* do not include it in generated config
* do not put it into `ENV`
* do not copy secret-containing cache directories

#### Common Bad Patterns

#### Bad: Secrets in Dockerfile

```dockerfile
ENV SECRET_KEY=supersecret
```

Problem: baked into image metadata.

#### Bad: Secrets as Build Args

```dockerfile
ARG SECRET_KEY
RUN echo "$SECRET_KEY"
```

Problem: may leak through history, logs, cache, or generated files.

##### Bad: Copying `.env` into Image

```dockerfile
COPY .env /app/.env
```

Problem: secret file becomes part of image.

##### Bad: Printing Environment

```dockerfile
RUN printenv
```

or:

```python
print(os.environ)
```

Problem: secrets may appear in logs.

##### Bad: Installing Private Packages with Token in URL

```dockerfile
RUN pip install \
  --extra-index-url "https://user:token@example.com/simple" \
  private-package
```

Problem: token may appear in logs or build metadata.

#### Safer Patterns

##### Good: Runtime Environment Variables for Configuration

```bash
docker run \
  -e APP_ENV=production \
  -e DATABASE_URL="$DATABASE_URL" \
  myapp
```
##### Good: Build Args for Non-Secrets

```bash
docker build \
  --build-arg APP_VERSION=1.2.3 \
  -t myapp:1.2.3 .
```

Dockerfile:

```dockerfile
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION
```

##### Good: BuildKit Secrets for Build-Time Credentials

```bash
DOCKER_BUILDKIT=1 docker build \
  --secret id=pip_token,env=PIP_TOKEN \
  -t myapp .
```

Dockerfile:

```dockerfile
RUN --mount=type=secret,id=pip_token \
    PIP_TOKEN="$(cat /run/secrets/pip_token)" && \
    pip install private-package
```

##### Good: `.dockerignore`

```text
.env
.env.*
!.env.example
.git
.venv
.aws
.ssh
```

##### Good: Runtime Secret Files

```bash
docker run \
  --mount type=bind,src="$PWD/secrets",dst=/run/secrets,readonly \
  myapp
```

Python:

```python
from pathlib import Path

secret_key = Path("/run/secrets/secret_key").read_text().strip()
```

#### Practical Decision Table

| Need                                        | Best mechanism                                 |
| ------------------------------------------- | ---------------------------------------------- |
| App mode like `production` or `development` | Runtime env var                                |
| Log level                                   | Runtime env var                                |
| Public app version                          | Build arg copied to `ENV`                      |
| Git commit SHA                              | Build arg copied to `ENV`                      |
| Database password                           | Runtime secret, env var, or mounted secret     |
| API token needed while app runs             | Runtime secret                                 |
| Token needed only during build              | BuildKit secret                                |
| Private package install during build        | BuildKit secret                                |
| Local development config                    | `.env` file, not committed                     |
| Compose variable substitution               | Compose `.env`                                 |
| Container environment from file             | Compose `env_file:` or `docker run --env-file` |
| Prevent accidental build context leaks      | `.dockerignore`                                |

### Challenges

1. Create a shell variable and then try to read it from a Python child process. Export the variable and try again. Explain the difference between a shell variable and an environment variable.
2. Export an environment variable in one terminal, then open another terminal and try to read it there. Explain why environment variables do not automatically persist between separate terminals.
3. Write a script that changes an environment variable. Run it normally, then run it with `source`. Explain why only the sourced version changes the current shell.
4. Use Python or another child process to modify an inherited environment variable. After the child exits, check the value in the parent shell. Explain why the parent was not affected.
5. Compare `( VAR=value; echo "$VAR" )` with `{ VAR=value; echo "$VAR"; }`. Explain the difference between a subshell and a current-shell block.
6. Use `printenv`, `env`, `set`, `declare -p`, and `export -p` to inspect variables. Compare which commands show only environment variables and which show shell variables too.
7. Modify `PATH` to include a custom directory containing a small executable script. Run the script from another directory and explain how command lookup uses `PATH`.
8. Create and activate a Python virtual environment. Check `which python`, `which pip`, `echo "$PATH"`, and `echo "$VIRTUAL_ENV"` before and after activation. Explain what activation actually changes.
9. Try running a virtual environment’s `activate` script normally instead of sourcing it. Explain why the current shell is not affected.
10. Run a command with a temporary environment variable, such as `DEBUG=1 python3 app.py`, then check whether `DEBUG` still exists afterward. Explain command-scoped environment variables.
11. Use `env -i` to start a command with an almost empty environment. Add back only selected variables like `PATH` and `HOME`. Explain why many programs depend on environment variables.
12. Write a small Dockerfile using both `ARG` and `ENV`. Build the image with `--build-arg`, run a container, and explain which values are available at build time versus runtime.
13. Run a container with `docker run -e APP_ENV=production ...` and read the value inside the application. Explain how runtime environment variables are injected into the container process.
14. Override a Dockerfile `ENV` value using `docker run -e`. Explain the precedence between image defaults and runtime environment variables.
15. Create a `.env` file and use it with `docker run --env-file` or Docker Compose `env_file`. Explain the difference between using `.env` for Compose substitution and passing variables into the container.
16. Demonstrate why secrets should not be baked into a Docker image using `ENV` or `ARG`. Explain safer alternatives such as runtime secrets, mounted secret files, or BuildKit secrets.
17. Add `.env`, `.venv`, `.git`, `.ssh`, and `.aws` to `.dockerignore`. Explain how `.dockerignore` helps prevent accidental secret or dependency leakage during image builds.
18. Use a Python script inside a container to start a child process. Show that the child inherits runtime environment variables from the parent process.
19. Store a script counter in a file rather than relying only on an environment variable. Explain why environment variables are not a good mechanism for persistent state.
20. Set a variable as read-only with `readonly`, then try to change and unset it. Explain when read-only variables are useful in scripts.
