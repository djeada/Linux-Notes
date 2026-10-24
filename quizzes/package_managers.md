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

> **Explanation:** DNF replaced YUM on modern Fedora and RHEL, and `yum` is often kept as a compatibility command. zypper belongs to openSUSE, and APT and dpkg to Debian.

#### Q. What does `apt update` do?

* [ ] Upgrades all installed packages to their newest versions
* [x] Downloads fresh package lists from the configured repositories without installing anything
* [ ] Updates the `apt` program itself
* [ ] Removes packages that are no longer needed

> **Explanation:** `apt update` refreshes the local index of available packages and versions. Installing newer versions is the job of `apt upgrade`, which should run after the index is current.

#### Q. Which command upgrades all installed packages to the newest versions in the refreshed package lists?

* [ ] `apt update`
* [ ] `apt install --all`
* [ ] `apt refresh`
* [x] `apt upgrade`

> **Explanation:** `apt upgrade` installs available updates for installed packages. Run `apt update` first so APT knows which versions exist.

#### Q. Which command installs the package `nginx` from the configured APT repositories?

* [ ] `apt get nginx`
* [x] `apt install nginx`
* [ ] `apt add nginx`
* [ ] `apt download nginx`

> **Explanation:** `apt install` resolves and installs the package with its dependencies. `apt download` only fetches the `.deb` file into the current directory, and `apt get` is not a subcommand.

#### Q. You downloaded `package.deb` and want to install it while letting APT fetch any missing dependencies. Which command does that?

* [ ] `dpkg -i package.deb`
* [ ] `apt download package.deb`
* [ ] `apt-cache show package.deb`
* [x] `apt install ./package.deb`

> **Explanation:** Given a path (note the `./`), `apt install` installs the local file and pulls dependencies from the repositories. `dpkg -i` installs the file but does not resolve dependencies.

#### Q. Which low-level tool installs a `.deb` file directly without resolving dependencies?

* [ ] `rpm -ivh`
* [x] `dpkg -i`
* [ ] `apt-cache`
* [ ] `yum localinstall`

> **Explanation:** `dpkg` is the Debian package tool underneath APT. If dependencies are missing it leaves the package unconfigured, which a later `apt install -f` can fix.

#### Q. Which command uninstalls a package but keeps its system-wide configuration files?

* [x] `apt remove package`
* [ ] `apt purge package`
* [ ] `apt autoremove package`
* [ ] `apt clean package`

> **Explanation:** `apt remove` deletes the program files and leaves configuration in `/etc`, so a reinstall picks it up again. `apt purge` removes the configuration files too.

#### Q. Which command uninstalls a package and also deletes its system-wide configuration files?

* [ ] `apt remove package`
* [ ] `apt clean package`
* [x] `apt purge package`
* [ ] `apt autoclean package`

> **Explanation:** `purge` is `remove` plus deleting the package's configuration files. Files in users' home directories are never touched by either command.

#### Q. What does `apt autoremove` do?

* [ ] Removes broken packages
* [ ] Deletes downloaded package files from the cache
* [ ] Removes old configuration files
* [x] Removes packages that were installed as dependencies and are no longer needed

> **Explanation:** When nothing depends on an automatically installed package any more, `autoremove` uninstalls it to free space. Cleaning the download cache is `apt clean`.

#### Q. Which command deletes all downloaded package files from the local APT cache to free disk space?

* [ ] `apt autoremove`
* [ ] `apt purge`
* [x] `apt clean`
* [ ] `apt update`

> **Explanation:** `apt clean` empties the cache of `.deb` files in `/var/cache/apt/archives`. `apt autoclean` removes only files that can no longer be downloaded, and `autoremove` uninstalls packages.

#### Q. `apt show apache2` prints a full description of the package. What does this prove?

* [ ] That `apache2` is installed and running
* [ ] That `apache2` is installed but not running
* [ ] That `apache2` was installed at some point
* [x] Only that the package exists in the repository metadata, installed or not

> **Explanation:** `apt show` describes packages from repository data. Check local installation with `dpkg-query -W -f='${Status}\n' apache2`, which prints `install ok installed` for installed packages.

#### Q. Which command searches the APT package lists for packages related to `nginx`?

* [ ] `apt find nginx`
* [ ] `apt locate nginx`
* [ ] `apt query nginx`
* [x] `apt search nginx`

> **Explanation:** `apt search` matches names and descriptions in the package index. Searching needs no root privileges, unlike installing or removing.

#### Q. Why do scripts usually call `apt-get` and `apt-cache` instead of `apt`?

* [ ] `apt` is not installed on servers
* [ ] `apt-get` resolves dependencies, while `apt` does not
* [x] `apt` is designed for interactive use, while `apt-get` keeps a stable interface for scripts
* [ ] `apt-get` is faster because it skips signature checks

> **Explanation:** `apt` adds progress bars and friendlier output and may change between releases. `apt-get` and `apt-cache` prioritize backward-compatible behaviour, so automation should use them.

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
* [ ] `/var/lib/apt/lists/`
* [x] `/etc/apt/sources.list` and files in `/etc/apt/sources.list.d/`
* [ ] `/etc/apt/apt.conf` only

> **Explanation:** Repository entries live in `sources.list` and the `sources.list.d/` directory. `/var/lib/apt/lists/` holds the downloaded index files, and `/etc/yum.repos.d/` is for YUM/DNF.

#### Q. Which command adds a repository, such as a PPA, on Ubuntu?

* [ ] `apt add-repo ppa:user/repo`
* [ ] `apt-key add ppa:user/repo`
* [ ] `apt source ppa:user/repo`
* [x] `add-apt-repository ppa:user/repo`

> **Explanation:** `add-apt-repository` writes the repository entry into `/etc/apt/sources.list.d/`. It comes from the `software-properties-common` package; run `apt update` afterwards.

#### Q. What is a PPA on Ubuntu?

* [ ] A Primary Package Archive maintained by Canonical
* [x] A Personal Package Archive that publishes packages outside the official repositories
* [ ] A Private Package Archive that requires a subscription
* [ ] A Preferred Package Archive chosen automatically for speed

> **Explanation:** PPAs let individuals or teams distribute packages through Launchpad. Because they are third-party, only add PPAs you trust.

#### Q. Why does a modern APT source entry include `[signed-by=/etc/apt/keyrings/winehq.gpg]`?

* [ ] It encrypts the downloaded packages
* [ ] It makes APT skip signature checks for that repository
* [ ] It speeds up downloads by caching the key
* [x] It restricts trust in that key to this repository instead of trusting it for all repositories

> **Explanation:** Scoping a third-party signing key with `signed-by` means it can only vouch for packages from that one source, limiting the damage if the key or repository is compromised.

#### Q. What is the purpose of GPG signatures in package management?

* [ ] To compress packages
* [x] To verify that packages are authentic and have not been tampered with
* [ ] To encrypt package contents during download
* [ ] To track package version numbers

> **Explanation:** The package manager checks each package or repository index against a trusted signing key. A failed check means the data did not come from the expected source or was modified.

#### Q. In a YUM `.repo` file, what does `gpgcheck=1` do?

* [ ] Enables the repository
* [ ] Downloads the repository's GPG key automatically
* [x] Makes YUM verify the GPG signature of packages from that repository
* [ ] Encrypts connections to the mirror

> **Explanation:** With `gpgcheck=1`, packages whose signatures do not verify are refused. Enabling a repository is controlled separately with `enabled=1`.

#### Q. Which command lists the available updates for installed packages on a YUM-based system?

* [ ] `yum show updates`
* [ ] `yum pending`
* [ ] `yum history`
* [x] `yum check-update`

> **Explanation:** `yum check-update` (or `dnf check-update`) lists packages with newer versions. An exit status of 100 means updates are available, not that the command failed.

#### Q. Which YUM command updates every installed package?

* [ ] `yum check-update`
* [ ] `yum refresh`
* [ ] `yum install --all`
* [x] `yum update`

> **Explanation:** `yum update` with no package names upgrades everything; naming a package, as in `yum update httpd`, limits it. On DNF the usual spelling is `dnf upgrade`.

#### Q. How does refreshing package metadata on YUM/DNF differ from APT?

* [ ] YUM/DNF never use a metadata cache
* [x] YUM/DNF refresh expired metadata automatically, while APT needs an explicit `apt update`
* [ ] YUM/DNF require `yum update` before every install
* [ ] YUM/DNF download all packages ahead of time

> **Explanation:** YUM and DNF keep a metadata cache and refresh it when it expires. With APT you normally run `apt update` yourself before installing or upgrading.

#### Q. Which command searches YUM repositories for packages matching `apache`?

* [ ] `yum find apache`
* [ ] `yum locate apache`
* [x] `yum search apache`
* [ ] `yum query apache`

> **Explanation:** `yum search` matches package names and summaries. Searching does not require root privileges.

#### Q. Which package name do you install to get the Apache web server on Fedora/RHEL, compared with Debian/Ubuntu?

* [ ] `apache2` on Fedora/RHEL and `httpd` on Debian/Ubuntu
* [ ] `apache` on both
* [ ] `httpd` on both
* [x] `httpd` on Fedora/RHEL and `apache2` on Debian/Ubuntu

> **Explanation:** Package and service names differ between distribution families, so `dnf install httpd` and `apt install apache2` install the same software. Search first when you are unsure.

#### Q. Which YUM command shows detailed information such as version, size and description for the package `httpd`?

* [ ] `yum show httpd`
* [ ] `yum describe httpd`
* [ ] `yum about httpd`
* [x] `yum info httpd`

> **Explanation:** `yum info` displays metadata for an installed or available package. On APT systems the equivalent is `apt show`.

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

#### Q. Which YUM command reverts the most recent package transaction?

* [ ] `yum revert`
* [ ] `yum rollback`
* [ ] `yum cancel`
* [x] `yum history undo last`

> **Explanation:** `yum history` lists past transactions, and `yum history undo` reverses one; `last` refers to the most recent. DNF offers the same subcommands.

#### Q. Where are YUM repository definitions stored?

* [ ] `/etc/apt/sources.list`
* [ ] `/var/cache/yum/`
* [x] `/etc/yum.repos.d/`
* [ ] `/etc/repos.conf`

> **Explanation:** Each `.repo` file in `/etc/yum.repos.d/` defines one or more repositories with a label, name, base URL or mirror list and `gpgcheck` setting. `/var/cache/yum/` only holds cached data.

#### Q. Which command shows all enabled and disabled repositories on a YUM system?

* [ ] `yum repos`
* [ ] `yum list repos`
* [ ] `yum-config-manager --enable`
* [x] `yum repolist all`

> **Explanation:** `yum repolist` shows enabled repositories, and adding `all` includes disabled ones. `dnf repolist all` works the same way.

#### Q. Which command adds a new YUM repository from a URL?

* [ ] `yum install --repo=URL`
* [ ] `add-apt-repository URL`
* [ ] `yum repolist --add URL`
* [x] `yum-config-manager --add-repo=URL`

> **Explanation:** `yum-config-manager` (from `yum-utils`) writes a `.repo` file for the URL; on DNF the equivalent is `dnf config-manager --add-repo`. `add-apt-repository` is for APT.

#### Q. Which command permanently disables the repository with ID `epel` on a YUM system?

* [ ] `yum remove epel`
* [ ] `yum --enablerepo=epel update`
* [ ] `yum clean epel`
* [x] `yum-config-manager --disable epel`

> **Explanation:** `--disable` sets `enabled=0` in the repository's `.repo` file, so it stays off until re-enabled with `--enable`.

#### Q. What does the `--enablerepo=REPO` option do on a `yum` or `dnf` command?

* [ ] Permanently enables the repository
* [ ] Creates a new repository
* [ ] Enables every configured repository
* [x] Enables a disabled repository for that single command only

> **Explanation:** The option affects only the current command, so the `.repo` file keeps the repository disabled. Use `yum-config-manager --enable` for a permanent change.

#### Q. In `rpm -ivh package.rpm`, what do the three letters mean?

* [ ] Install, validate, hold
* [ ] Information, version, help
* [ ] Interactive, verify, hash
* [x] Install, verbose, print hash marks for progress

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

> **Explanation:** `rpm -q nano` prints the installed version, or "package nano is not installed". `rpm -e` would remove it.

#### Q. Which command removes the installed package `nano` with RPM?

* [ ] `rpm -r nano`
* [ ] `rpm -d nano`
* [x] `rpm -e nano`
* [ ] `rpm -x nano`

> **Explanation:** `-e` stands for erase. RPM refuses if other installed packages depend on `nano`, because it does not manage dependencies for you.

#### Q. `rpm -ivh tool.rpm` fails with "Failed dependencies". Why would `dnf install ./tool.rpm` succeed?

* [ ] DNF ignores dependencies
* [ ] DNF converts the package to a `.deb`
* [ ] DNF installs the file without verifying it
* [x] DNF resolves the dependencies and installs them from the repositories

> **Explanation:** RPM is a low-level tool that only checks dependencies. High-level managers like YUM and DNF find and install what is missing, which is their main advantage.

#### Q. What is the main advantage of a package manager over installing software by hand?

* [ ] It always installs the newest upstream version
* [x] It resolves dependencies and keeps the software updated with the rest of the system
* [ ] It never requires root privileges
* [ ] It produces smaller programs

> **Explanation:** Packages declare their dependencies, and the manager tracks installed files so it can update or remove them cleanly. Manually installed software must be tracked and patched by you.

#### Q. What is the usual order of steps to build and install software from a source tarball?

* [ ] `make install`, then `./configure`, then extract
* [ ] `./configure`, then extract, then `make`
* [x] Extract, run `./configure` if present, `make`, then `make install`
* [ ] Extract, then `make install`, then `make`

> **Explanation:** After `tar -xzf`, `./configure` checks dependencies and prepares the build, `make` compiles and `make install` copies the results into place, often under `/usr/local`.

#### Q. What is the main maintenance drawback of software installed from a tarball?

* [ ] It cannot be run by regular users
* [ ] It always overwrites files owned by packages
* [x] It does not receive automatic updates, so you must track security fixes yourself
* [ ] It is deleted when the package cache is cleaned

> **Explanation:** The package manager does not know about manually built software, so `apt upgrade` or `dnf upgrade` will never patch it. Installing it under `/usr/local` at least keeps it separate from packaged files.
