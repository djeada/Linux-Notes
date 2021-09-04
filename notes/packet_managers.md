<h1>Package managers</h1>

Debian and Ubuntu are arguably the most well-known Linux distributions that use APT (Advanced Package Tool). Other distributions that use alternative package managers, such as DNF, YUM, Pacman, and so on, will be unable to utilize the apt commands at all. These package managers have their own functionalities and syntax, which may differ significantly from that of apt.

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

<h1>Managing Repositories</h1>

Configuration file for repos is located at: /etc/yum.repos.d

To display enabled repo list, use:

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
