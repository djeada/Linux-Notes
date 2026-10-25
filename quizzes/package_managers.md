# Package Managers Quiz

Notes: [Package Managers](../notes/package_managers.md)

Check your understanding of APT, dpkg, YUM/DNF, RPM, repositories and installing software from tarballs.

#### Q. Which package management system do Debian, Ubuntu and their derivatives use?

* [ ] YUM
* [x] APT
* [ ] Pacman
* [ ] DNF

> **Explanation:** Debian-based systems use APT (Advanced Package Tool) on top of `dpkg`. YUM and DNF belong to the Red Hat family, and Pacman is Arch Linux's package manager.

#### Q. Which tool is the standard package manager on current Fedora and RHEL-family systems?

* [ ] APT
* [ ] dpkg
* [ ] zypper
* [x] DNF

> **Explanation:** DNF replaced YUM on Fedora and RHEL 8+, where `yum` is kept only as a link to `dnf`. zypper belongs to openSUSE, and APT and dpkg to Debian.

#### Q. What does `apt update` do?

* [ ] Downloads and installs the newest versions of all installed packages
* [x] Refreshes the package lists from the configured repositories, installing nothing
* [ ] Updates the `apt` program itself to its newest release
* [ ] Removes packages that are no longer needed by anything

> **Explanation:** `apt update` refreshes the local index of available packages and versions. Installing newer versions is the job of `apt upgrade`, which should run after the index is current.

#### Q. `apt upgrade` reports that one package was "kept back" because its new version needs another installed package removed. Which command performs that upgrade?

* [ ] `apt update`
* [ ] `apt install --reinstall`
* [x] `apt full-upgrade`
* [ ] `apt autoremove`

> **Explanation:** `apt upgrade` may install new dependencies but never removes installed packages, so it skips such upgrades. `apt full-upgrade` is allowed to remove packages when that is needed to upgrade the system as a whole.

#### Q. Which command installs the package `nginx` from the configured APT repositories?

* [ ] `apt get nginx`
* [x] `apt install nginx`
* [ ] `apt add nginx`
* [ ] `apt download nginx`

> **Explanation:** `apt install` resolves and installs the package with its dependencies. `apt download` only fetches the `.deb` file into the current directory, and `apt get` is not a subcommand.

#### Q. You downloaded `package.deb` and want to install it while letting APT fetch any missing dependencies. Which command does that?

* [x] `apt install ./package.deb`
* [ ] `dpkg -i package.deb`
* [ ] `apt download package.deb`
* [ ] `apt-cache show package.deb`

> **Explanation:** Given a path (note the `./`), `apt install` installs the local file and pulls dependencies from the repositories. `dpkg -i` installs the file but does not resolve dependencies.

#### Q. `dpkg -i cowsay.deb` ends with "dependency problems - leaving unconfigured". Which command installs the missing dependencies and finishes configuring the package?

* [ ] `dpkg --configure -a`
* [x] `apt-get install -f`
* [ ] `apt-get clean`
* [ ] `dpkg -r cowsay`

> **Explanation:** `dpkg` unpacks the package but cannot fetch dependencies, so it stays half-installed (`iU`). `apt-get install -f` (fix broken) downloads what is missing and completes configuration; `dpkg --configure -a` alone would fail again for the same reason.

#### Q. Which command uninstalls a package but keeps its system-wide configuration files?

* [x] `apt remove package`
* [ ] `apt purge package`
* [ ] `apt autoremove package`
* [ ] `apt clean package`

> **Explanation:** `apt remove` deletes the program files and leaves configuration in `/etc`, so a reinstall picks it up again. `apt purge` removes the configuration files too.

#### Q. After `apt remove cron`, `dpkg -l cron` shows the status `rc`. What does that mean?

* [ ] The package is installed, and its configuration files are up to date
* [ ] The package is marked for reinstallation the next time APT runs
* [ ] The package and all its configuration files were removed completely
* [x] The package is removed, but its configuration files are still on disk

> **Explanation:** The first letter is the desired state (`r`emove) and the second the actual state (`c`onfig-files only). `apt purge cron` deletes those leftovers even after a plain remove; files in home directories are never touched.

#### Q. What does `apt autoremove` do?

* [x] Removes packages that were installed as dependencies and are no longer needed
* [ ] Removes packages whose installation failed or left them broken
* [ ] Deletes downloaded `.deb` files from the cache in `/var/cache/apt`
* [ ] Removes configuration files left behind by removed packages

> **Explanation:** When nothing depends on an automatically installed package any more, `autoremove` uninstalls it to free space. Cleaning the download cache is `apt clean`.

#### Q. Which command deletes all downloaded package files from the local APT cache to free disk space?

* [ ] `apt autoremove`
* [ ] `apt purge`
* [x] `apt clean`
* [ ] `apt update`

> **Explanation:** `apt clean` empties the cache of `.deb` files in `/var/cache/apt/archives`. `apt autoclean` removes only files that can no longer be downloaded, and `autoremove` uninstalls packages.

#### Q. `apt show apache2` prints a full description of the package. What does this prove?

* [ ] That `apache2` is installed and its service is currently running
* [ ] That `apache2` is installed, although its service may be stopped
* [ ] That `apache2` was installed on this system at some point in the past
* [x] Only that the package exists in the repository metadata, installed or not

> **Explanation:** `apt show` describes packages from repository data. Check local installation with `dpkg-query -W -f='${Status}\n' apache2`, which prints `install ok installed` for installed packages.

#### Q. Which command searches the APT package lists for packages related to `nginx`?

* [x] `apt search nginx`
* [ ] `apt find nginx`
* [ ] `apt locate nginx`
* [ ] `apt query nginx`

> **Explanation:** `apt search` matches names and descriptions in the package index. Searching needs no root privileges, unlike installing or removing.

#### Q. Why do scripts usually call `apt-get` and `apt-cache` instead of `apt`?

* [ ] `apt` is not installed by default on Debian or Ubuntu server images
* [ ] `apt-get` resolves dependencies automatically, while `apt` installs only named packages
* [x] `apt` is designed for interactive use, while `apt-get` keeps a stable interface for scripts
* [ ] `apt-get` is faster because it skips repository signature checks

> **Explanation:** `apt` adds progress bars and friendlier output and may change between releases; piping it prints "apt does not have a stable CLI interface". `apt-get` and `apt-cache` prioritize backward compatibility, so automation should use them.

#### Q. Which command lists the packages installed on a Debian-based system?

* [ ] `apt list --upgradable`
* [ ] `apt-cache search .`
* [x] `dpkg -l`
* [ ] `apt show --all`

> **Explanation:** `dpkg -l` prints every package known to dpkg with its status (`ii` means installed). `apt list --installed` is another option; `--upgradable` only shows packages with pending updates.

#### Q. Which command fetches the `.deb` file of a package into the current directory without installing it?

* [ ] `apt get package`
* [ ] `apt fetch package`
* [ ] `apt save package`
* [x] `apt download package`

> **Explanation:** `apt download` saves the package file locally, which is useful for offline installation or inspection. It does not download dependencies.

#### Q. Where are APT repositories configured?

* [ ] `/etc/yum.repos.d/`
* [ ] `/var/lib/apt/lists/` and the index files cached inside it
* [x] `/etc/apt/sources.list` and files in `/etc/apt/sources.list.d/`
* [ ] `/etc/apt/apt.conf` and files in `/etc/apt/apt.conf.d/`

> **Explanation:** Repository entries live in `sources.list` and in `sources.list.d/` (Ubuntu 24.04 uses `sources.list.d/ubuntu.sources`). `/var/lib/apt/lists/` holds the downloaded index files, and `/etc/yum.repos.d/` is for YUM/DNF.

#### Q. Which command adds a repository, such as a PPA, on Ubuntu?

* [x] `add-apt-repository ppa:user/repo`
* [ ] `apt add-repo ppa:user/repo`
* [ ] `apt-key add ppa:user/repo`
* [ ] `apt source ppa:user/repo`

> **Explanation:** `add-apt-repository` (from `software-properties-common`) writes the entry into `/etc/apt/sources.list.d/` and, on current Ubuntu, refreshes the package lists itself unless given `-n`.

#### Q. What is a PPA on Ubuntu?

* [ ] A Primary Package Archive maintained by Canonical
* [x] A Personal Package Archive that publishes packages outside the official repositories
* [ ] A Private Package Archive that requires a subscription
* [ ] A Preferred Package Archive chosen automatically for speed

> **Explanation:** PPAs let individuals or teams distribute packages through Launchpad. Because they are third-party, only add PPAs you trust.

#### Q. Why does a modern APT source entry include `[signed-by=/etc/apt/keyrings/winehq.gpg]`?

* [ ] It encrypts the packages downloaded from that repository with the key
* [ ] It tells APT to skip signature checks because the repository is trusted
* [ ] It speeds up downloads by caching the key instead of fetching it each time
* [x] It restricts trust in that key to this repository instead of trusting it for all repositories

> **Explanation:** Scoping a third-party signing key with `signed-by` means it can only vouch for packages from that one source, limiting the damage if the key or repository is compromised.

#### Q. What is the purpose of GPG signatures in package management?

* [ ] To compress packages so they download faster from mirrors
* [x] To verify that packages are authentic and have not been tampered with
* [ ] To encrypt package contents so mirrors cannot read them
* [ ] To record which package version is installed on each system

> **Explanation:** The package manager checks each package or repository index against a trusted signing key. A failed check means the data did not come from the expected source or was modified.

#### Q. In a YUM/DNF `.repo` file, what does `gpgcheck=1` do?

* [ ] Enables the repository
* [ ] Downloads the repository's GPG key automatically
* [x] Makes YUM/DNF verify the GPG signature of packages from that repository
* [ ] Encrypts connections to the mirror

> **Explanation:** With `gpgcheck=1`, packages whose signatures do not verify are refused. Enabling a repository is controlled separately with `enabled=1`, and the key location with `gpgkey=`.

#### Q. A server has this file. You run `dnf install mytool`, and `mytool` exists only in this repository. What happens?

```text
# /etc/yum.repos.d/internal.repo
[internal]
name=Internal tools
baseurl=https://repo.example.com/el9/
enabled=0
gpgcheck=1
```

* [ ] DNF installs `mytool` but skips the signature check
* [x] DNF reports that no package `mytool` is available, because the repository is disabled
* [ ] DNF enables the repository permanently and installs `mytool`
* [ ] DNF downloads `mytool` from a mirror list instead of `baseurl`

> **Explanation:** `enabled=0` hides the repository from normal commands. `dnf --enablerepo=internal install mytool` uses it once, and `gpgcheck=1` still applies to the downloaded package.

#### Q. A nightly script runs `dnf check-update` and alerts on any non-zero exit status. It alerts almost every night, though nothing is broken. Why?

* [ ] `check-update` needs root and fails for normal users
* [ ] `check-update` exits 1 whenever the metadata cache is refreshed
* [ ] `check-update` installs updates and exits non-zero when a reboot is needed
* [x] `check-update` exits 100 when updates are available, 0 when there are none and 1 on error

> **Explanation:** `dnf check-update` (and `yum check-update`) only lists pending updates. Exit status 100 means "updates available", so scripts should treat 100 separately from real errors.

#### Q. Which YUM command updates every installed package?

* [x] `yum update`
* [ ] `yum check-update`
* [ ] `yum refresh`
* [ ] `yum install --all`

> **Explanation:** `yum update` with no package names upgrades everything; naming a package, as in `yum update httpd`, limits it. On DNF the usual spelling is `dnf upgrade`, and `update` is accepted as an alias.

#### Q. How does refreshing package metadata on YUM/DNF differ from APT?

* [ ] YUM/DNF never cache metadata and query the repository on every command
* [x] YUM/DNF refresh expired metadata automatically, while APT needs an explicit `apt update`
* [ ] YUM/DNF require running `yum update` before every install, like APT
* [ ] YUM/DNF download every package in the repository ahead of time

> **Explanation:** YUM and DNF keep a metadata cache and refresh it when it is older than `metadata_expire`. With APT you normally run `apt update` yourself before installing or upgrading.

#### Q. On Rocky Linux 9 you need the command `semanage`, but it is not installed. Which command tells you which package provides it?

* [ ] `dnf search semanage`
* [ ] `rpm -qf /usr/sbin/semanage`
* [x] `dnf provides /usr/sbin/semanage`
* [ ] `dnf info semanage`

> **Explanation:** `dnf provides` searches repository file lists and reports `policycoreutils-python-utils`. `rpm -qf` only works for files that are already installed, and `dnf search` matches names and summaries, not file paths.

#### Q. Which package name do you install to get the Apache web server on Fedora/RHEL, compared with Debian/Ubuntu?

* [ ] `apache2` on Fedora/RHEL and `httpd` on Debian/Ubuntu
* [ ] `apache` on both
* [ ] `httpd` on both
* [x] `httpd` on Fedora/RHEL and `apache2` on Debian/Ubuntu

> **Explanation:** Package and service names differ between distribution families, so `dnf install httpd` and `apt install apache2` install the same software. Search first when you are unsure.

#### Q. Which YUM command shows detailed information such as version, size and description for the package `httpd`?

* [x] `yum info httpd`
* [ ] `yum show httpd`
* [ ] `yum describe httpd`
* [ ] `yum about httpd`

> **Explanation:** `yum info` (or `dnf info`) displays metadata for an installed or available package. On APT systems the equivalent is `apt show`.

#### Q. Which command lists all installed packages using YUM?

* [ ] `yum show installed`
* [x] `yum list installed`
* [ ] `yum installed`
* [ ] `yum query --installed`

> **Explanation:** `yum list installed` prints installed packages with version and source repository. At the RPM level, `rpm -qa` gives a similar list.

#### Q. Which command removes downloaded packages and cached metadata on a YUM system?

* [ ] `yum clear`
* [ ] `yum cache clean`
* [ ] `yum remove --cache`
* [x] `yum clean all`

> **Explanation:** `yum clean all` deletes cached packages and metadata, freeing space and forcing fresh metadata on the next run.

#### Q. Which command reverts the most recent package transaction on a YUM/DNF system?

* [x] `yum history undo last`
* [ ] `yum revert`
* [ ] `yum cancel last`
* [ ] `yum remove --last`

> **Explanation:** `yum history` lists past transactions, and `yum history undo` reverses one; `last` refers to the most recent. `dnf history undo last` works the same, though undo fails if older package versions are no longer available.

#### Q. Where are YUM repository definitions stored?

* [ ] `/etc/apt/sources.list`
* [ ] `/var/cache/yum/`
* [x] `/etc/yum.repos.d/`
* [ ] `/etc/repos.conf`

> **Explanation:** Each `.repo` file in `/etc/yum.repos.d/` defines one or more repositories with a label, name, base URL or mirror list and `gpgcheck` setting. `/var/cache/yum/` only holds cached data.

#### Q. A `.repo` file section contains both `baseurl=` and `mirrorlist=` lines. How do they differ?

* [ ] `baseurl` is used to download packages, while `mirrorlist` only supplies GPG keys
* [x] `baseurl` names one repository location, while `mirrorlist` is a URL returning a list of mirrors
* [ ] `mirrorlist` names a local cache directory, while `baseurl` is the remote server
* [ ] `baseurl` is consulted only for updates, while `mirrorlist` is used for new installs

> **Explanation:** A mirror list lets the client pick a nearby, up-to-date mirror; `baseurl` names one fixed location. Either can locate the repository metadata, and the `[label]` in brackets is the repository ID used by `--enablerepo`.

#### Q. Which command shows all enabled and disabled repositories on a YUM system?

* [ ] `yum repos`
* [ ] `yum list repos`
* [ ] `yum-config-manager --enable`
* [x] `yum repolist all`

> **Explanation:** `yum repolist` shows enabled repositories, and adding `all` includes disabled ones. `dnf repolist all` works the same way.

#### Q. On RHEL or Rocky Linux 9 with `yum-utils` installed, which command adds a new repository from a `.repo` URL?

* [x] `yum-config-manager --add-repo=URL`
* [ ] `yum install --repo=URL`
* [ ] `add-apt-repository URL`
* [ ] `yum repolist --add URL`

> **Explanation:** `yum-config-manager` saves the `.repo` file into `/etc/yum.repos.d/`; `dnf config-manager --add-repo` is the same on DNF 4. `add-apt-repository` is for APT.

#### Q. On Fedora 41 or later, which uses DNF 5, which command adds a repository from a `.repo` file URL?

* [ ] `dnf config-manager --add-repo=URL`
* [x] `dnf config-manager addrepo --from-repofile=URL`
* [ ] `rpm --import URL`
* [ ] `dnf repolist --add URL`

> **Explanation:** DNF 5 turned `config-manager` options into subcommands, and the old `--add-repo` option is rejected as an unknown argument. `rpm --import` only imports a GPG key.

#### Q. Which command permanently disables the repository with ID `epel` on a RHEL 9-family system?

* [ ] `yum remove epel`
* [ ] `yum --enablerepo=epel update`
* [ ] `yum clean epel`
* [x] `yum-config-manager --disable epel`

> **Explanation:** `--disable` sets `enabled=0` in the repository's `.repo` file, so it stays off until re-enabled with `--enable`. For a single command, use `--disablerepo=epel` instead.

#### Q. What does the `--enablerepo=REPO` option do on a `yum` or `dnf` command?

* [ ] Enables the repository permanently by editing its `.repo` file
* [ ] Creates a new repository definition with the given ID
* [ ] Enables every configured repository, including disabled ones
* [x] Enables a disabled repository for that single command only

> **Explanation:** The option affects only the current command, so the `.repo` file keeps the repository disabled. Use `yum-config-manager --enable` for a permanent change.

#### Q. In `rpm -ivh package.rpm`, what do the three letters mean?

* [x] Install, verbose, print hash marks for progress
* [ ] Install, validate signatures, hold the package
* [ ] Show information, print the version, show help
* [ ] Interactive mode, verify files, compute hashes

> **Explanation:** `-i` installs, `-v` prints details and `-h` shows a progress bar of `#` marks. RPM itself does not download dependencies.

#### Q. Which command lists every package installed in the RPM database?

* [ ] `rpm -e`
* [ ] `rpm -ivh`
* [ ] `rpm -qd`
* [x] `rpm -qa`

> **Explanation:** `-q` queries and `-a` means all packages. `rpm -qd` lists a package's documentation files and `rpm -e` erases a package.

#### Q. Which command checks whether the package `nano` is installed using RPM?

* [x] `rpm -q nano`
* [ ] `rpm -e nano`
* [ ] `rpm -ivh nano`
* [ ] `rpm --install nano`

> **Explanation:** `rpm -q nano` prints the installed version, such as `nano-5.6.1-7.el9.x86_64`, or "package nano is not installed" with exit status 1. `rpm -e` would remove it.

#### Q. What does `rpm -qd nano` print?

* [x] The documentation files installed by the `nano` package
* [ ] The packages that `nano` depends on
* [ ] The files `nano` would delete when removed
* [ ] The description text from the `nano` package header

> **Explanation:** In query mode `-d` selects documentation files. Dependencies are shown with `rpm -qR`, the full file list with `rpm -ql` and the description with `rpm -qi`.

#### Q. Which command removes the installed package `nano` with RPM?

* [ ] `rpm -r nano`
* [ ] `rpm -d nano`
* [x] `rpm -e nano`
* [ ] `rpm -x nano`

> **Explanation:** `-e` stands for erase. RPM refuses with "Failed dependencies" if other installed packages need `nano`, because it does not manage dependencies for you.

#### Q. `rpm -ivh tool.rpm` fails with "Failed dependencies". Why would `dnf install ./tool.rpm` succeed?

* [x] DNF resolves the dependencies and installs them from the repositories
* [ ] DNF ignores dependencies, which RPM checks strictly
* [ ] DNF rebuilds the package so that it no longer has dependencies
* [ ] DNF installs the file without verifying its signature or dependencies

> **Explanation:** RPM is a low-level tool that only checks dependencies. High-level managers like YUM and DNF find and install what is missing, which is their main advantage.

#### Q. On Ubuntu, `apt install chrony` lists `systemd-timesyncd` under "The following packages will be REMOVED". Why?

* [ ] APT removes the oldest package whenever disk space is low
* [ ] `chrony` is a newer version of `systemd-timesyncd`
* [x] The two packages declare a conflict, so APT must remove one to install the other
* [ ] APT always removes packages that were installed automatically

> **Explanation:** Packages can declare `Conflicts` or `Breaks`. APT resolves them by proposing removals and asks before proceeding, so read that section carefully before answering yes.

#### Q. What is the main advantage of a package manager over installing software by hand?

* [ ] It always installs the newest upstream release as soon as it is published
* [x] It tracks dependencies and installed files, so software can be updated or removed cleanly
* [ ] It lets any user install software system-wide without root privileges
* [ ] It compiles every program from source for your specific CPU model

> **Explanation:** Packages declare their dependencies, and the manager records which files belong to which package. Manually installed software must be tracked, patched and removed by you.

#### Q. What is the usual order of steps to build and install software from a source tarball?

* [ ] `make install`, then `./configure`, then extract
* [ ] `./configure`, then extract, then `make`
* [x] Extract, run `./configure` if present, `make`, then `make install`
* [ ] Extract, then `make install`, then `make`

> **Explanation:** After `tar -xzf`, `./configure` checks dependencies and prepares the build, `make` compiles and `make install` copies the results into place, by default under `/usr/local`.

#### Q. You build a tarball whose build uses an autoconf `configure` script, but you have no root access. How do you make `make install` put the program in `~/.local`?

* [ ] Run `make install DESTDIR=/usr/local`
* [ ] Run `sudo make install`, which is required for every tarball
* [ ] Copy the tarball into `~/.local` before extracting it
* [x] Run `./configure --prefix=$HOME/.local` before `make` and `make install`

> **Explanation:** `--prefix` sets the install location, which defaults to `/usr/local`, so the binary goes to `~/.local/bin`. Writing under `/usr/local` needs root, and `DESTDIR` only stages files for packaging.

#### Q. What is the main maintenance drawback of software installed from a tarball?

* [ ] It can only be run by root, because it was installed with `make install`
* [ ] It always overwrites files that belong to distribution packages
* [x] It does not receive automatic updates, so you must track security fixes yourself
* [ ] It is deleted the next time the package cache is cleaned

> **Explanation:** The package manager does not know about manually built software, so `apt upgrade` or `dnf upgrade` will never patch it. Installing it under `/usr/local` at least keeps it separate from packaged files.
