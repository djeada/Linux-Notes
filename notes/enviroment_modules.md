## Environment Modules

Environment Modules is a utility that provides dynamic modification of a user's environment via modulefiles. Each modulefile contains the information needed to configure the shell for an application. This tool helps users manage the environment settings, such as `PATH` and `LD_LIBRARY_PATH`, for different software versions, allowing easy switching between different versions or loading/unloading applications as required.

This is particularly useful in high-performance computing (HPC) environments, which often have many software packages installed. Manually managing these environments can be cumbersome and error-prone, and indiscriminate use of all packages could cause conflicts or compatibility issues. With Environment Modules, users can load only what they need for a particular task, reducing the potential for conflicts.

## Installing Environment Modules

The installation of Environment Modules depends on the type of Linux system you're using. Here's how you can install it on Debian-based and CentOS systems:

* **Debian-based systems (such as Ubuntu):** Use the following command to install Environment Modules:

```bash
sudo apt install environment-modules
```

* **CentOS (or other RHEL-based distributions):** Use the following command to install Environment Modules:

```bash
sudo yum install environment-modules
```

After installing Environment Modules, you might need to log out and log back in (or source your shell's configuration file) for the changes to take effect. After that, you can start using the module command to load, unload, and switch between different environments.

## Working with Environment Module Files

Environment module files, usually stored in the `/etc/modulefiles` directory or a location specified by the `MODULEPATH` environment variable, dictate how the shell environment should be modified for each software package. These files, named `modulefile`, are read and managed by the `module` command.

The structure of a modulefile directory usually reflects the software and its versions. For instance, for a software named "my_app" with version "1.0", the modulefile could be located at `/etc/modulefiles/my_app/1.0`.

Here's how you can create a directory for a specific application's modulefiles and a modulefile for a specific version of the application:

1. Create a directory for your application's modulefiles:

```bash
sudo mkdir /etc/modulefiles/my_app
```

2. Create a modulefile for a specific version of the application:

```bash
sudo touch /etc/modulefiles/my_app/1.0
```

3. Edit the modulefile: Open the created modulefile in a text editor:

```bash
sudo nano /etc/modulefiles/my_app/1.0
```

The modulefile should contain environment settings needed for the software. Here's a basic example:

```bash
#%Module 1.0
##
##  This is a sample modulefile for environment modules.
##

proc ModulesHelp { } {
    puts stderr "\tThis is a sample modulefile for environment modules."
}

module-whatis "This is a sample modulefile for environment modules."

prepend-path PATH /path/to/my/app/
prepend-path LD_LIBRARY_PATH /path/to/my/app/lib
conflict my_app
```

In this example:

- The `module-whatis` command provides a short description of the module.
- The `prepend-path` commands add the specified paths to the PATH and LD_LIBRARY_PATH environment variables, respectively.
- The `conflict` command ensures that no other versions of "my_app" are loaded when this module is loaded.

Remember to replace /path/to/my/app/ with the actual installation path of your application. After saving the modulefile, you can load it using the module `load my_app/1.0` command.

## Usage

The `module` command is your primary interface for interacting with Environment Modules. It provides various sub-commands to load, unload, and list modules, among other tasks.

Here are some of the most commonly used `module` sub-commands:

- **`module load [module_name]`:** This command loads the specified module, making the software available in your shell environment. If multiple versions of a software package are available, you can specify the version as well, e.g., `module load my_app/1.0`.

- **`module unload [module_name]`:** This command unloads the specified module, removing its environment settings from your shell. Like the `load` command, you can specify the version to unload.

- **`module avail`:** This command lists all available modules. If you want to find available versions of a specific application, you can pass the application name as an argument, e.g., `module avail my_app`.

- **`module list`:** This command lists all currently loaded modules. This can be helpful to see which software packages and versions are active in your current environment.

- **`module purge`:** This command unloads all currently loaded modules. Be careful when using this command, as it could potentially disrupt your working environment by removing all loaded software.

You should use the `module` command to interact with Environment Modules, as this tool ensures that all environment changes are correctly and consistently applied. Manual editing of module files should be avoided unless you are defining a new module or modifying the behavior of an existing one.

## Example: Switching Between Python Versions

Environment Modules is especially useful when you need to switch between different versions of the same software. For example, you may need to switch between Python 2.7 and Python 3.8 for different projects. The steps below illustrate how you can use Environment Modules to handle this task.

1. Create a directory for Python modulefiles

```bash
sudo mkdir /etc/modulefiles/python
```

2. Create and configure a modulefile for Python 2.7:

```bash
sudo touch /etc/modulefiles/python/2.7
sudo nano /etc/modulefiles/python/2.7
```

3. In the opened nano editor, add the necessary lines to the modulefile (adjust prepend-path lines based on your system's Python 2.7 location).

```bash
#%Module 1.0
##
##  Module for the Python 2.7 programming language.
##

module-whatis "Module for Python 2.7"

prepend-path PATH /usr/local/python2.7/bin
prepend-path LD_LIBRARY_PATH /usr/local/python2.7/lib
conflict python
```

4. Create and configure a modulefile for Python 3.8:

```bash
sudo touch /etc/modulefiles/python/3.8
sudo nano /etc/modulefiles/python/3.8
```

Similarly, add the necessary lines to this modulefile (adjust prepend-path lines based on your system's Python 3.8 location).

```bash
#%Module 1.0
##
##  Module for the Python 3.8 programming language.
##

module-whatis "Module for Python 3.8"

prepend-path PATH /usr/local/python3.8/bin
prepend-path LD_LIBRARY_PATH /usr/local/python3.8/lib
conflict python
```

5. Switch between the Python versions: Now you can use the module command to load and unload the different versions of Python as needed. For instance, if you want to use Python 2.7, use:

```bash
module load python/2.7
```

And when you need Python 3.8, first unload the Python 2.7 module and then load Python 3.8:

```bash
module unload python/2.7
module load python/3.8
```

These commands modify your shell environment to set the appropriate version of Python as the default. You can verify the active Python version using the `python --version` command.


## Challenges: Exploring Environment Modules

1. Install environment modules on your system, using the appropriate command for your operating system (e.g., `apt install environment-modules` for Debian-based systems, `yum install environment-modules` for CentOS, etc.).
2. Create a directory in `/etc/modulefiles` for a new application. For example, create a directory for Python by executing `sudo mkdir /etc/modulefiles/python`.
3. Choose a specific version of the application you'd like to manage using environment modules. Create a modulefile for this version within the application directory you created. For instance, create a modulefile for Python 3.8 with `sudo touch /etc/modulefiles/python/3.8`.
4. Edit the modulefile you just created and configure it appropriately. Remember to use the `prepend-path` directive to add the application's bin and lib directories to the `PATH` and `LD_LIBRARY_PATH` environment variables respectively. Make sure to include the `conflict` directive to prevent simultaneous loading of conflicting versions of the application.
5. Use the `module` command to load the application version from the modulefile you created. Verify that the module is loaded correctly by checking the output of `module list` and the application's version (e.g., `python --version`).
6. Use the `module unload` command to unload the application module you loaded in the previous step. Verify that the module is unloaded by running `module list` and checking the application's version again.
7. Use the `module avail` command to list all the available modules on your system. Do you see the module file you created?
8. Finally, unload all the loaded modules using the `module purge` command. Ensure that no modules are loaded afterwards by running `module list`.
