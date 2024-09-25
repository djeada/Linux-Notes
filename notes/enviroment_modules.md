## Environment Modules

Environment Modules is a powerful and flexible tool that enables dynamic modification of a user's environment via modulefiles. Each modulefile contains the information necessary to configure the shell for a specific application or version, allowing users to seamlessly switch between different software environments. This utility is essential in complex computing environments, such as high-performance computing (HPC) clusters, where managing multiple software packages and versions can be challenging.

Environment Modules simplifies this process by handling environment variables like `PATH`, `LD_LIBRARY_PATH`, and others, ensuring that users can load and unload applications as needed without conflicts or compatibility issues. It promotes efficient use of system resources and enhances productivity by providing a consistent and user-friendly interface for environment management.

Main idea:

- Load and unload software environments on-the-fly.
- Easily switch between different versions of software packages.
- Automatically detect and prevent conflicts between incompatible modules.
- Define complex environment setups using Tcl scripting within modulefiles.

### Installing Environment Modules

The installation process for Environment Modules varies depending on your Linux distribution. Below are the instructions for different systems:

#### Debian-based Systems (e.g., Ubuntu)

Update the package list and install Environment Modules:

```bash
sudo apt update
sudo apt install environment-modules
```

#### Red Hat-based Systems (e.g., CentOS, RHEL, Fedora)

Use `yum` or `dnf` to install Environment Modules:

```bash
# For CentOS/RHEL
sudo yum install environment-modules

# For Fedora
sudo dnf install environment-modules
```

#### SUSE-based Systems (e.g., openSUSE)

Install using `zypper`:

```bash
sudo zypper install environment-modules
```

#### Installing from Source

If a package is not available for your distribution or you need a specific version, you can install Environment Modules from source:

I. **Download the Latest Version:**

```bash
wget https://sourceforge.net/projects/modules/files/Modules/modules-4.7.1/modules-4.7.1.tar.gz
tar -xzf modules-4.7.1.tar.gz
cd modules-4.7.1
```

II. **Configure and Install:**

```bash
./configure --prefix=/usr/local/modules
make
sudo make install
```

III. **Configure Shell Initialization:**

Add the following line to your shell initialization file (e.g., `~/.bashrc`):

```bash
source /usr/local/modules/init/bash
```

Replace `bash` with your shell if different (e.g., `zsh`, `tcsh`).

After installation, you may need to log out and log back in or source your shell's configuration file:

```bash
source ~/.bashrc
```

### Working with Environment Module Files

Modulefiles are scripts written in the Tcl language that define how to modify the environment for a specific application. They are typically stored in directories specified by the `MODULEPATH` environment variable, such as `/usr/share/modules/modulefiles` or `/etc/modulefiles`.

#### Example Modulefile Directory

Here's an example of what a directory tree structure might look like for a collection of modulefiles organized for various applications and versions. Each application has its own subdirectory, and within that, modulefiles for specific versions are stored. Additionally, a `.version` file or symbolic link might be present to specify the default version.

```
/etc/modulefiles
├── python
│   ├── 2.7
│   ├── 3.6
│   ├── 3.8
│   └── .version
├── gcc
│   ├── 8.4.0
│   ├── 9.3.0
│   └── 10.2.0
├── my_app
│   ├── 1.0
│   ├── 2.1
│   ├── 2.2
│   └── default -> 2.1
├── cuda
│   ├── 10.1
│   ├── 11.0
│   └── .version
├── openmpi
│   ├── 3.1.4
│   ├── 4.0.5
│   └── 4.1.0
└── cmake
    ├── 3.17
    ├── 3.18
    └── .version
```

This structure provides organization and makes it easy to manage multiple versions of different software using Environment Modules. Each application has its own directory under `/etc/modulefiles`, and within those directories, version-specific modulefiles are stored.

#### Creating Modulefile Directories

I. **Create a Directory for Your Application:**

```bash
sudo mkdir -p /usr/share/modules/modulefiles/my_app
```

II. **Set Appropriate Permissions:**

```bash
sudo chmod 755 /usr/share/modules/modulefiles/my_app
```

#### Writing a Modulefile for a Specific Version

I. **Create the Modulefile:**

```bash
sudo nano /usr/share/modules/modulefiles/my_app/1.0
```

II. **Edit the Modulefile:**

Here's an example modulefile for "my_app" version 1.0:

```tcl
#%Module1.0#####################################################################
##
## my_app modulefile
##

proc ModulesHelp { } {
   puts stderr "This module loads my_app version 1.0"
}

module-whatis "Loads my_app version 1.0"

# Set the installation prefix
set root /opt/my_app/1.0

# Modify environment variables
prepend-path PATH $root/bin
prepend-path LD_LIBRARY_PATH $root/lib
prepend-path MANPATH $root/share/man

# Set custom environment variables
setenv MY_APP_HOME $root

# Handle conflicts with other versions
conflict my_app
```

**Explanation:**

- `proc ModulesHelp { }`: Defines the help message displayed with `module help my_app/1.0`.
- `module-whatis`: Provides a brief description shown by `module whatis my_app/1.0`.
- `set root`: Sets a variable for the installation directory of the application.
- `prepend-path`: Adds directories to environment variables.
- `setenv`: Sets a custom environment variable.
- `conflict`: Prevents loading multiple versions of "my_app" simultaneously.

III. **Save and Exit:**

Press `Ctrl + O` to save and `Ctrl + X` to exit the editor.

#### Managing the MODULEPATH Variable

To ensure that your modulefiles are found by the `module` command, you may need to update the `MODULEPATH` environment variable.

I. **Add to MODULEPATH Temporarily:**

```bash
module use /usr/share/modules/modulefiles
```

II. **Add to MODULEPATH Permanently:**

Add the above line to your shell initialization file (e.g., `~/.bashrc`).

### Usage

The `module` command is the primary tool for interacting with Environment Modules. Below are common subcommands and examples of how to use them.

#### Loading Modules

I. **Load a Module:**

```bash
module load my_app
```

If multiple versions exist, and no default is set, you may need to specify the version:

```bash
module load my_app/1.0
```

II. **Load Multiple Modules:**

```bash
module load gcc/9.3.0 openmpi/4.0.5 my_app/1.0
```

#### Unloading Modules

I. **Unload a Module:**

```bash
module unload my_app
```

II. **Unload Multiple Modules:**

```bash
module unload gcc openmpi my_app
```

#### Listing Modules

I. **List Loaded Modules:**

```bash
module list
```

II. **List Available Modules:**

```bash
module avail
```

To list modules matching a pattern:

```bash
module avail my_app
```

#### Displaying Module Information

I. **Show Module Details:**

```bash
module show my_app/1.0
```

II. **Get Help for a Module:**

```bash
module help my_app/1.0
```

#### Switching Between Modules

```bash
module switch my_app/1.0 my_app/2.0
```

#### Purging Modules

```bash
module purge
```

Use this command with caution, as it will remove all currently loaded modules.

#### Saving and Restoring Module Sets

I. **Save Current Module Set:**

```bash
module save my_default_modules
```

II. **Restore Module Set:**

```bash
module restore my_default_modules
```

III. **List Saved Module Sets:**

```bash
module savelist
```

### Example: Switching Between Python Versions

Environment Modules is especially useful when you need to switch between different versions of the same software. For example, you may need to switch between Python 2.7 and Python 3.8 for different projects. The steps below illustrate how you can use Environment Modules to handle this task.

#### I. Create a directory for Python modulefiles

First, you need a directory where your Python module files will reside. This is typically located in `/etc/modulefiles/`, but you can adjust the path based on your system’s configuration. Create a directory for Python modulefiles:

```bash
sudo mkdir /etc/modulefiles/python
```

This command creates a directory `/etc/modulefiles/python`, where you'll store the configuration files for different Python versions.

#### II. Create and configure a modulefile for Python 2.7

Next, create a modulefile for Python 2.7. A modulefile is essentially a script that modifies environment variables like `PATH` and `LD_LIBRARY_PATH` to make the specific Python version available in your environment.

```bash
sudo touch /etc/modulefiles/python/2.7
sudo nano /etc/modulefiles/python/2.7
```

The `touch` command creates an empty file named `2.7`, and `nano` opens it for editing.

#### III. Edit the modulefile for Python 2.7

In the opened `nano` editor, add the necessary lines that define how the environment should be configured when the Python 2.7 module is loaded. Be sure to modify the `prepend-path` lines based on the actual location of Python 2.7 on your system.

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

- `module-whatis` provides a short description of the module.
- `prepend-path PATH` ensures that the directory containing the Python 2.7 binary is placed at the front of your `PATH` environment variable.
- `prepend-path LD_LIBRARY_PATH` adds the directory containing Python 2.7 libraries to `LD_LIBRARY_PATH`.
- `conflict python` ensures that only one Python version is loaded at a time, preventing conflicts.

Save the file and exit `nano` by pressing `CTRL + X`, then `Y`, and `Enter`.

#### IV. Create and configure a modulefile for Python 3.8

Similarly, you need to create a modulefile for Python 3.8:

```bash
sudo touch /etc/modulefiles/python/3.8
sudo nano /etc/modulefiles/python/3.8
```

Then, add the following lines to configure Python 3.8. Again, adjust the `prepend-path` lines based on your system’s Python 3.8 location.

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

This modulefile works similarly to the one for Python 2.7, but it's configured for Python 3.8. The `conflict python` directive ensures that Python 2.7 and Python 3.8 cannot be loaded at the same time.

#### V. Switch between Python versions

Once the modulefiles are created and configured, you can easily switch between the two Python versions using the `module` command.

To load Python 2.7, run:

```bash
module load python/2.7
```

This will modify your shell environment, updating `PATH` and `LD_LIBRARY_PATH` so that Python 2.7 becomes the default.

If you later need to switch to Python 3.8, first unload Python 2.7, then load Python 3.8:

```bash
module unload python/2.7
module load python/3.8
```

Unloading Python 2.7 ensures that no conflicting versions are loaded simultaneously.

#### VI. Verify the active Python version

After switching between Python versions, you can verify which version is active by using the following command:

```bash
python --version
```

This will display the version of Python currently set as default in your environment.

### Best Practices

I. To ensure reproducibility and avoid unexpected behavior, always specify the version when loading modules.

```bash
module load my_app/1.0
```

II. While `module purge` can help reset your environment, it may also unload critical modules. Check which modules are loaded before purging.

III. Include module load commands in scripts or job submission files to ensure the correct environment is set up for your tasks.

IV. Be aware of module conflicts, especially when working with compilers and MPI libraries. The `conflict` command in modulefiles helps prevent incompatible modules from being loaded together.

### Advanced Modulefile Techniques

Environment Modules support Tcl scripting, which allows for advanced features like conditional logic and dynamic behavior. This makes it possible to create more flexible and powerful modulefiles that adapt to the environment in which they are loaded.

#### Conditional Loading Based on Environment

You can use Tcl's scripting features to implement conditional logic within a modulefile. For example, you might want to load specific dependencies only if another module is already loaded.

```tcl
# Check if a specific module is loaded
if { [ is-loaded gcc/9.3.0 ] } {
    # Load dependencies
    module load dependency_module
} else {
    puts stderr "Error: gcc/9.3.0 must be loaded before my_app."
    exit 1
}
```

- `is-loaded gcc/9.3.0`: This checks if the `gcc/9.3.0` module is already loaded in the environment.
- `module load dependency_module`: Loads a required dependency if the condition is true.
- `puts stderr`: Prints an error message to the standard error if the condition is false.
- `exit 1`: Exits with an error code, signaling a failure due to the unmet condition.

This ensures that the required dependencies are in place before loading your application module.

#### Setting Default Modules

Administrators can set a default module version so that users automatically load the default version of a module if they don’t specify a specific one. This can be done using either a `.version` file or a symbolic link.

I. **Using a `.version` File:**

You can create a `.version` file in the application's modulefile directory to define the default version of the module.

```tcl
#%Module1.0
set ModulesVersion "1.0"
```

The `.version` file ensures consistency by defaulting to a stable version of the software.

II. **Using a Symbolic Link:**

Another method to set the default module version is by using symbolic links. This method involves creating a symbolic link named `default` pointing to the desired version.

```bash
ln -s 1.0 /usr/share/modules/modulefiles/my_app/default
```

- `ln -s 1.0`: Creates a symbolic link named `default` that points to version `1.0`.
- `/usr/share/modules/modulefiles/my_app/default`: Specifies the path where the symbolic link will reside, which is the modulefile directory for `my_app`.

This approach allows for easy switching of default versions by updating the symbolic link to point to a new version.

### Troubleshooting

Even with well-written modulefiles, users may encounter issues when loading or using modules. Here are common issues and their solutions.

I. **Module Not Found:**

If the module you are trying to load is not found, it could be due to the modulefile directory not being included in the `MODULEPATH`. To verify the directories in `MODULEPATH`, run:

```bash
echo $MODULEPATH
```

If the desired directory is not listed, you can add it using the following command:

```bash
module use /path/to/modulefiles
```

Ensure that the correct directory is permanently added if you need it frequently by adding the command to your shell's initialization script (e.g., `.bashrc` or `.bash_profile`).

II. **Environment Variables Not Set:**

If certain environment variables aren’t being set as expected when you load a module, check the modulefile for errors in syntax or incorrect paths. To inspect what a module does when loaded, use the following command:

```bash
module show <module_name>
```

III. **Conflicts with Other Modules:**

Sometimes, multiple loaded modules can conflict with each other, causing unexpected behavior. If this happens, the easiest solution is to unload all currently loaded modules and start fresh:

```bash
module purge
```

After purging, you can selectively load the required modules for your task.

IV. **Module Command Not Found:**

If you receive an error like `module: command not found`, it indicates that the Environment Modules package is either not installed or not set up properly in your shell environment. To resolve this:

1. Ensure that Environment Modules is installed by checking your package manager or manually inspecting the system.
2. Ensure that your shell initialization file (e.g., `.bashrc`, `.bash_profile`) sources the appropriate environment setup script. For example, for bash, you would typically add:

```bash
source /usr/share/modules/init/bash
```

This ensures that the `module` command is available in your shell sessions.

### Challenges

1. Install environment modules on your system, using the appropriate command for your operating system (e.g., `apt install environment-modules` for Debian-based systems, `yum install environment-modules` for CentOS, etc.).
2. Create a directory in `/etc/modulefiles` for a new application. For example, create a directory for Python by executing `sudo mkdir /etc/modulefiles/python`.
3. Choose a specific version of the application you'd like to manage using environment modules. Create a modulefile for this version within the application directory you created. For instance, create a modulefile for Python 3.8 with `sudo touch /etc/modulefiles/python/3.8`.
4. Edit the modulefile you just created and configure it appropriately. Remember to use the `prepend-path` directive to add the application's bin and lib directories to the `PATH` and `LD_LIBRARY_PATH` environment variables respectively. Make sure to include the `conflict` directive to prevent simultaneous loading of conflicting versions of the application.
5. Use the `module` command to load the application version from the modulefile you created. Verify that the module is loaded correctly by checking the output of `module list` and the application's version (e.g., `python --version`).
6. Use the `module unload` command to unload the application module you loaded in the previous step. Verify that the module is unloaded by running `module list` and checking the application's version again.
7. Use the `module avail` command to list all the available modules on your system. Do you see the module file you created?
8. Finally, unload all the loaded modules using the `module purge` command. Ensure that no modules are loaded afterwards by running `module list`.
