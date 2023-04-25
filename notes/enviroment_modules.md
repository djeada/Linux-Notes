## Introduction to Environment Modules

Environment modules help users manage multiple software versions on a system, allowing easy switching between versions or loading required software only. This is useful on supercomputers with many software packages, where using all at once could cause conflicts or compatibility issues.

## Installing Environment Modules

Install environment modules on a Debian-based system:

```bash
apt install environment-modules
```

To install environment modules on a CentOS system, use the following command:

```bash
yum install environment-modules
```

## Working with Environment Module Files

Environment module files, stored in `/etc/modulefiles`, specify available software versions. These files, named `modulefile`, are managed by the `module` command.

Create a directory for a specific application's modulefiles:

```bash
mkdir /etc/modulefiles/my_app
```

Create a modulefile for a specific application version:

```bash
touch /etc/modulefiles/my_app/version1.0
```

The modulefile should contain:

```
#%Module 1.0
##
##  This is a sample modulefile for environment modules.
##

module-whatis "This is a sample modulefile for environment modules."

prepend-path PATH /path/to/my/app/
prepend-path LD_LIBRARY_PATH /path/to/my/app/lib
conflict my_app
```

## Usage

Commands for interacting with environment modules:

* `module load`: Load a specific application version.
* `module unload`: Unload a specific application version.
* `module avail`: List available versions of a specific application.
* `module list`: List all currently loaded modules.
* `module purge`: Unload all currently loaded modules.

Use the `module` command to interact with environment modules instead of editing module files directly to ensure proper changes.

## Example

Switch between two Python versions, 2.7 and 3.8, with environment modules:

1. Create a directory for Python modulefiles:

```
mkdir /etc/modulefiles/python
```

2. Create a modulefile for Python 2.7:

```
touch /etc/modulefiles/python/2.7
```

3. Add necessary lines to the modulefile (adjust `prepend-path` lines based on your system's Python 2.7 location).

```
#%Module 1.0
##
##  This is a modulefile for the Python 2.7 programming language.
##

module-whatis "This is a modulefile for Python 2.7"

prepend-path PATH /usr/local/python2.7/bin
prepend-path LD_LIBRARY_PATH /usr/local/python2.7/lib
conflict python
```

4. Create a modulefile for Python 3.8:

```
#%Module 1.0
##
##  This is a modulefile for Python 3.8
##

module-whatis "This is a modulefile for Python 3.8"

prepend-path PATH /usr/local/python3.8/bin
prepend-path LD_LIBRARY_PATH /usr/local/python3.8/lib
conflict python
```

5. Now you can use the `module` command to load and unload the different versions of Python as needed. To use Python 2.7, use:

```
module load python/2.7
```

To use Python 3.8, use:

```
module load python/3.8
```

## Challenges

1. Install environment modules on your system.
2. Create a directory in `/etc/modulefiles` for a new application.
3. Create a modulefile for a specific version of the application in the new directory.
4. Use the `module` command to load the application version from the created modulefile.
5. Unload any loaded module.
6. List available modules on the system.
7. Unload all loaded modules.
