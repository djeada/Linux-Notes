## Package managers

Debian and Ubuntu are arguably the most well-known Linux distributions (at least for the home users). Those two distros (and their derivatives) use Advanced Package Tool (`APT`). Other distributions use alternative package managers, such as `DNF`, `YUM`, `Pacman`, and so on. You will be unable to use the apt command on the machines using those distros. These other package managers have their own functionalities and syntax, which may differ significantly from that of `APT`.

Be cautious when using package managers, as they frequently not only install software with all of its dependencies, but also interfere with your system's configuration.


## Installing from tarballs

You may install software directly from the tarball on your Linux machine, without using a package manager. This process consists of three steps:

1. Extract

Go to the directory that contains your tarball and run the following commands:

```
tar -zxvf path_to_tar.tar.gz
cd path_to_tar
```

2. Compile

Make is the standard Linux compilation tool:

```
make
```

There may also be a config file with dependencies that must be installed before this application can be compiled. In this case, run the config file first.

3. Install

If a make install is available, use:

```
make install
```

If not, copy the executable manully to usr/local/bin:

```
mv exe_name usr/local/bin/exe_name
```

There is no mechanism to automatically update apps that have been installed in this manner.

## Install and update software packages from APT repo

<code>apt-get</code> and <code>aptitude</code> are older versions of <code>apt</code>. That means that you should not use them!

In general, you should obtain a list of the most recent versions of accessible packages from your update repository before you begin installing new applications. 
To update your repos, use <code>apt update</code>. Executing this command will display a list of possible package versions, but no real software will be updated>:

```bash
apt update
```

<code>apt upgrade</code>, on the other hand, may use this information to update all installed packages to their most recent versions:

```bash
apt upgrade
```

To install a package, use:

```bash
apt install httpd
```

If you have a local *.deb* file on your machine, you may use apt to install as well:

```bash
apt install /path/to/package/name.deb
```

You can use the following commands to ensure that a package has been successfully installed (and that you have installed what you believe you have installed):

```bash
apt show httpd
```

## Install and update software packages from YUM repo

In contrast to <code>apt</code>, there is no two-step process. It is not necessary to update the repositories before installing apps with <code>yum</code>.

To check for update, use:

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

## Install and update software packages from RPM repo

To download a rpm package, use:

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
The apt software repositories are defined in the /etc/apt/sources.list file or in different files in the /etc/apt/sources.list.d/ directory on Ubuntu and all other Debian-based distributions. 

<code>add-apt-repository</code> is a Python script that adds an APT repository to /etc/apt/sources.list. The command can also be used to delete a previously added repository.

To install it, follow these steps: 

```bash
apt update
apt install software-properties-common
```

Assume we want to install wine on our Debian-based system. We must take the following steps:

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

Finally install wine:

```bash
sudo apt install --install-recommends winehq-stable
```

Verify that the installation was successful by running the following command: 

```bash
wine --version
```

## Managing YUM Repositories

Configuration file for repos is located at: /etc/yum.repos.d

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

### Description of the repository:

* label - the label used as an identifier in the repository file 
* name - the name of the repository 
* mirrorlist - a link to information about mirror servers for this server
* baseurl - the base url to which the rpm packages should be found.
* gpgcheck - set to 1 if a gpg integrity check on the packages is required. 

### Labels for repositories:

* base - the base repository including all essential Red Hat applications. Packages with full support.
* updates - a repository containing just updates.
* optional - open source software that Red Hat does not support.
* supplemental - proprietary packages that Red Hat does not support.
* extras - additional packages that Red Hat does not support. 

## Challenges

1. Using your preferred package manager, look for the 0ad app. It's possible that you'll need to update the repositories first. Install the app if the search was successful. Try out the app. Using the same package manager, uninstall it. 
1. What is a package manager and why is it useful?
1. How does YUM work and what types of software can it be used to install?
1. What is APT and how does it differ from YUM?
1. What is a tarball and how is it used in relation to package managers?
1. How can you use a package manager to install software from a specific repository or to install a specific version of a package?
1. How can you use a package manager to update or upgrade installed packages?
1. How can you use a package manager to remove or uninstall packages?
1. What are some common options or commands used with package managers such as YUM or APT?
1. How can you use a package manager to search for available packages or to find information about installed packages?
1. What are some potential challenges or drawbacks to using a package manager, and how can these be addressed?
