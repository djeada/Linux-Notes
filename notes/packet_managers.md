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

To display package info, use:

```bash
yum info httpd
```

To install a package, use:

```bash
yum install httpd
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
