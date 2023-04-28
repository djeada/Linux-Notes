## Package Managers

Debian and Ubuntu are popular Linux distributions for home users. These distributions and their derivatives use the Advanced Package Tool (`APT`). Other distributions use alternative package managers, like `DNF`, `YUM`, `Pacman`, which have unique functionalities and syntax.

Be cautious with package managers as they install software and dependencies and may affect your system's configuration.

## Installing from Tarballs

Tarballs allow software installation on Linux without package managers. The process involves three steps:

1. Extract

Navigate to the tarball directory and run:

```
tar -zxvf path_to_tar.tar.gz
cd path_to_tar
```

2. Compile

Use the standard Linux compilation tool, `make`:

```
make
```

If a config file with dependencies exists, run it before compiling.

3. Install

Use `make install` if available, or manually copy the executable to `usr/local/bin`:

```
make install
```

Automatic updates aren't available for apps installed this way.

## Installing and Updating Software Packages with APT

`apt-get` and `aptitude` are older versions of `apt`. Use `apt` instead.

Update your repositories with `apt update`. This command lists package versions without updating the software:

```bash
apt update
```

`apt upgrade` updates all installed packages to their latest versions:

```bash
apt upgrade
```

To install a package, use:

```bash
apt install httpd
```

To install a local .deb file, use:

```bash
apt install /path/to/package/name.deb
```

To confirm successful installation, use:

```bash
apt show httpd
```

## Installing and Updating Software Packages with YUM

Unlike `apt`, `yum` doesn't require repository updates before installing apps.

To check for updates, use:

```bash
yum check-update
```

To update all packages, use:

```bash
yum update
```

To update a specific package, use:

```bash
yum update httpd
```

To search packages by name, use:

```bash
yum search apache
```

To install a package with YUM, use:

```bash
yum install httpd
```

To display package info with YUM, use:

```bash
yum info httpd
```

To display all installed packages, use:

```bash
yum list installed
```

To remove a package, use:

```bash
yum remove httpd
```

To clean cache, use:

```bash
yum clean all
```

## Installing and Updating Software Packages with RPM

To download an rpm package, use:

```bash
wget http://some_website/sample_file.rpm
```

To install from rpm, use:

```bash
rpm -ivh sample_file.rpm
```

To list all packages, use:

```bash
rpm -qa
```

To list specific package, use:

```bash
rpm -qa nano
```

To display documentation, use:

```bash
rpm -qd nano
```

To remove a package, use:

```bash
rpm -e nano
```

## Managing APT Repositories
APT repositories are defined in `/etc/apt/sources.list` or files in `/etc/apt/sources.list.d/` on Debian-based distributions.

add-apt-repository adds or deletes APT repositories in `/etc/apt/sources.list`. Install it with:

```bash
apt update
apt install software-properties-common
```

To install Wine on a Debian-based system, follow these steps:

Get the repository key and install it:

```bash
wget -nc https://dl.winehq.org/wine-builds/winehq.key
gpg -o /etc/apt/trusted.gpg.d/winehq.key.gpg --dearmor winehq.key
```

Add the repository:

```bash
add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ focal main'
```

Update the package database:

```bash
apt update
```

Install `Wine`:

```bash
sudo apt install --install-recommends winehq-stable
```

Verify the installation with:

```bash
wine --version
```

## Managing YUM Repositories

Configuration files for repos are located at `/etc/yum.repos.d`.

To display enabled repositories list, use:

```bash
yum repolist all
```

To add a repo, use:

```bash
yum-config-manager --add-repo=[URL]
```

To enable a repo, use:

```bash
yum-config-manager --enable [repo_id]
```

To disable a repo, use:

```bash
yum-config-manager --disable [repo_id]
```

### Repository Description

A repository is a collection of software packages managed by package managers. Components include:

- Label: a unique identifier.
- Name: the repository name.
- Mirrorlist: a list of mirrors with repository copies.
- Base URL: the URL for repository RPM packages.
- GPG check: indicates if GPG integrity checks are needed.

Common labels categorize repositories as:

- Base: essential applications with full support.
- Updates: package updates.
- Optional: unsupported open-source software.
- Supplemental: unsupported proprietary packages.
- Extras: additional unsupported packages.

## Challenges

1. Use your preferred package manager to search, install, and uninstall the 0ad app. Update repositories if needed.
2. Define a package manager and explain its purpose.
3. Describe YUM and the software it can install.
4. Explain APT and its differences from YUM.
5. Define a tarball and its relation to package managers.
6. Explain using package managers to install software from specific repositories or specific package versions.
7. Describe using package managers to update or upgrade installed packages.
8. Explain using package managers to remove or uninstall packages.
9. List common options or commands for package managers like YUM or APT.
10. Explain using package managers to search for available packages or find information about installed packages.
11. Discuss potential challenges or drawbacks of using package managers and how to address them.
