<h1>Package managers</h1>

Debian and Ubuntu are arguably the most well-known Linux distributions that use APT (Advanced Package Tool). Other distributions that use alternative package managers, such as DNF, YUM, Pacman, and so on, will be unable to utilize the apt commands at all. These package managers have their own functionalities and syntax, which may differ significantly from that of apt.

Be cautious, as package managers frequently not only install software with all of its dependencies, but also interfere with your system's configuration!

<h1>Install and update software packages from APT repo</h1>

In general, you should obtain a list of the most recent versions of accessible packages from your update repository before you begin installing new applications. 
To update your repos, use <i>apt update</i>. Executing this command will display a list of possible package versions, but no real software will be updated>:

```bash
apt update
```

<i>apt upgrade</i>, on the other hand, may use this information to update all installed packages to their most recent versions:

```bash
apt upgrade
```

To install a package, use:

```bash
apt install httpd
```

You can use the following commands to ensure that a package has been successfully installed (and that you have installed what you believe you have installed):

```bash
apt show httpd
```

<h1>Install and update software packages from YUM repo</h1>

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

<h1>Install and update software packages from RPM repo</h1>

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

<h1>Managing APT Repositories</h1>
The apt software repositories are defined in the /etc/apt/sources.list file or in different files in the /etc/apt/sources.list.d/ directory on Ubuntu and all other Debian-based distributions. 

<i>add-apt-repository</i> is a Python script that adds an APT repository to /etc/apt/sources.list. The command can also be used to delete a previously added repository.

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

<h1>Managing YUM Repositories</h1>

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

<h2>Description of the repository:</h2>

* label - the label used as an identifier in the repository file 
* name - the name of the repository 
* mirrorlist - a link to information about mirror servers for this server
* baseurl - the base url to which the rpm packages should be found.
* gpgcheck - set to 1 if a gpg integrity check on the packages is required. 

<h2>Labels for repositories:</h2>

* base - the base repository including all essential Red Hat applications. Packages with full support.
* updates - a repository containing just updates.
* optional - open source software that Red Hat does not support.
* supplemental - proprietary packages that Red Hat does not support.
* extras - additional packages that Red Hat does not support. 

<h1>Challenges</h1>

1. Using your preferred package manager, look for the 0ad app. It's possible that you'll need to update the repositories first. Install the app if the search was successful. Try out the app. Using the same package manager, uninstall it. 
2. Install MongoDB from their official repositories.
