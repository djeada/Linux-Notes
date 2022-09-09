## Package managers

Debian and Ubuntu are arguably the most well-known Linux distributions (at least for the home users). Those two distros (and their derivatives) use <code>APT</code> (Advanced Package Tool). Other distributions use alternative package managers, such as <code>DNF</code> <code>YUM</code>, <code>Pacman</code>, and so on. You will be unable to use the apt command on the machines using those distros. Those other package managers have their own functionalities and syntax, which may differ significantly from that of <code>APT</code>.

Be cautious, as package managers frequently not only install software with all of its dependencies, but also interfere with your system's configuration!

## Installing from tarballs

You may install software directly from the tarball on your Linux machine, without using a package manager.
This procedure consists of three steps: 

1. Extract

Go to the directory that contains your tarball and run the following commands: 

```bash
tar -zxvf path_to_tar.tar.gz
cd path_to_tar
```

2. Compile

<code>Make</code> is the standard Linux compilation tool: 

```bash
make
```

There may also be a <code>config</code> file with dependencies that must be installed before this application can be compiled. In this case run the config file first.

3. Install

If a <code>make install</code> is available, use: 

```bash
make install
```

If not, copy the executable manully to <code>usr/local/bin</code>:

```bash
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
2. Install MongoDB from their official repositories.
