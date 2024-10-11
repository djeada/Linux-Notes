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

#### Installing Environment Modules from Source

If the Environment Modules package is not available through your operating system’s package manager, or if you require a specific version, you can install it directly from the source. This approach provides greater flexibility, particularly if you want to install a newer or custom version.

I. **Download the Latest Version:**

First, download the source code from the official Environment Modules repository on SourceForge. The following example uses `wget` to fetch version 4.7.1, but be sure to replace the URL with the latest version if needed:

```bash
wget https://sourceforge.net/projects/modules/files/Modules/modules-4.7.1/modules-4.7.1.tar.gz
tar -xzf modules-4.7.1.tar.gz
cd modules-4.7.1
```

- `wget` is a command-line tool used to download files from the internet.
- The `tar -xzf` command extracts the downloaded `.tar.gz` archive, unzipping it into a directory named `modules-4.7.1`.
- `cd modules-4.7.1` changes to this directory, where the source code is located, preparing for the installation steps.

II. **Configure and Install:**

After extracting the source, you’ll need to configure the build settings and then compile and install the software:

```bash
./configure --prefix=/usr/local/modules
make
sudo make install
```

- `./configure --prefix=/usr/local/modules` initiates the configuration process and specifies the installation prefix. By setting the `--prefix` option, you control where the software will be installed; in this case, `/usr/local/modules`. You can customize this path as needed.
- `make` compiles the source code, creating the binaries that will be installed. This step may take a few minutes depending on your system.
- `sudo make install` installs the compiled software to the specified prefix directory. This command requires `sudo` because it installs files in system directories that need root privileges.

III. **Configure Shell Initialization:**

To make the `module` command available in your shell, you need to add a line to your shell initialization file. This line loads the Environment Modules system each time you open a new shell session:

```bash
echo "source /usr/local/modules/init/bash" >> ~/.bashrc
```

- This command appends the `source` line to your `~/.bashrc` file, ensuring the modules system is initialized whenever you start a new shell.
- Adjust `bash` in the path if you use a different shell, such as `zsh` or `tcsh`. For example, if you use `zsh`, the line would be: `source /usr/local/modules/init/zsh`.

To apply these changes immediately, either log out and back in or reload your shell configuration:

```bash
source ~/.bashrc
```

This command applies the new configuration without requiring a logout, so you can start using Environment Modules right away. Now you should be able to run the `module` command and manage software modules as needed.

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

To organize your modulefiles, it’s a good practice to create a directory structure that reflects the software you’re managing. This makes it easier to maintain and locate modulefiles as your collection grows.

I. **Create a Directory for Your Application:**

Use the following command to create a new directory for your application within the standard modulefile path:

```bash
sudo mkdir -p /usr/share/modules/modulefiles/my_app
```

- The `-p` flag tells `mkdir` to create the parent directories if they do not already exist, which helps avoid errors if any intermediate directories are missing.
- Replace `my_app` with the name of your application, making the modulefile directory structure more organized.

II. **Set Appropriate Permissions:**

To ensure that users can access the modulefiles, set the correct permissions on the new directory:

```bash
sudo chmod 755 /usr/share/modules/modulefiles/my_app
```

- The `755` permission setting allows the owner to read, write, and execute files in the directory, while others can read and execute files. This is usually suitable for shared module directories, as it allows others to access the files but not modify them.

#### Writing a Modulefile for a Specific Version

A modulefile is a simple script that configures the environment for a particular software version. By setting paths and environment variables, a modulefile helps users load the necessary settings for your application without modifying their shell configuration files.

I. **Create the Modulefile:**

To create a modulefile, use a text editor to open a new file with the version number you want to manage:

```bash
sudo nano /usr/share/modules/modulefiles/my_app/1.0
```

- This command creates a file named `1.0` inside the `my_app` directory, representing version 1.0 of your application.
- You can replace `1.0` with any version number, following this naming convention for each version of the software you want to manage with modules.

II. **Edit the Modulefile:**

Here’s an example modulefile for `my_app` version 1.0. The file contains commands that configure the environment whenever the module is loaded.

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

- **proc ModulesHelp { }**: Defines a function that outputs a help message when the `module help my_app/1.0` command is run. This is useful for providing users with a brief description of what the module does.
- **module-whatis**: This command specifies a one-line summary of the module, displayed when users run `module whatis my_app/1.0`. It helps users quickly identify what this modulefile does.
- **set root**: The `set` command defines a variable (`root`) that points to the installation directory of your application. This makes the modulefile easier to update, as you can adjust the path in one place if needed.
- The **prepend-path** command adds directories to various environment variables by placing a new directory at the beginning of each specified path. For example, it adds `$root/bin` to `PATH`, so the shell can locate the application's executables; `$root/lib` to `LD_LIBRARY_PATH`, enabling the linker to find the application’s libraries; and `$root/share/man` to `MANPATH`, allowing the `man` command to access the application’s manual pages.
- **setenv**: This command defines a custom environment variable `MY_APP_HOME`, which points to the root directory of the application. Users can reference this variable directly, which can be helpful for scripts or commands related to the application.
- **conflict**: This command prevents users from loading multiple versions of `my_app` at the same time. If a user tries to load a second version without first unloading the current one, the module system will display an error message. This ensures that only one version of the application is loaded, avoiding potential conflicts.

III. **Save and Exit:**

After editing the modulefile, save and close the editor:

- Press `Ctrl + O` to save your changes.
- Press `Ctrl + X` to exit `nano`.

### Managing the MODULEPATH Variable

The `MODULEPATH` environment variable tells the `module` command where to look for available modulefiles. By adjusting `MODULEPATH`, you can customize where the module system searches for additional modules, allowing you to access modulefiles that may not be in the default path.

I. **Add to MODULEPATH Temporarily:**

To add a directory to `MODULEPATH` for your current session only, use the `module use` command:

```bash
module use /usr/share/modules/modulefiles
```

This command tells the module system to include `/usr/share/modules/modulefiles` when searching for available modulefiles. However, it only applies to the current terminal session. Once you log out or close the terminal, the addition to `MODULEPATH` is reset.

II. **Add to MODULEPATH Permanently:**

To make the change permanent, add the `module use` line to your shell initialization file, such as `~/.bashrc` (for Bash users). This ensures the path is always added when you open a new terminal:

```bash
echo "module use /usr/share/modules/modulefiles" >> ~/.bashrc
source ~/.bashrc
```

### Usage of the `module` Command

The `module` command provides several subcommands to interact with environment modules. These subcommands allow you to load, unload, list, display, switch, and manage module configurations.

#### Loading Modules

I. **Load a Module:**

To load a module and make its associated software available for use:

```bash
module load my_app
```

This command loads the specified module and updates environment variables such as `PATH`, `LD_LIBRARY_PATH`, or other variables defined by the modulefile. If multiple versions of a module exist and no default is set, you may need to specify the desired version:

```bash
module load my_app/1.0
```

II. **Load Multiple Modules:**

To load multiple modules at once, separate each module name with a space:

```bash
module load gcc/9.3.0 openmpi/4.0.5 my_app/1.0
```

This example loads the GCC compiler, the Open MPI library, and `my_app`. Modules are loaded in the order specified, which can be important if later modules depend on those loaded earlier.

#### Unloading Modules

I. **Unload a Module:**

To remove a module from your environment and reset any associated environment variables:

```bash
module unload my_app
```

This command removes the specified module's changes from the environment, effectively "unloading" it.

II. **Unload Multiple Modules:**

You can also unload multiple modules at once by listing them with spaces:

```bash
module unload gcc openmpi my_app
```

This is useful for clearing several modules without removing all loaded modules.

#### Listing Modules

I. **List Loaded Modules:**

To view a list of all currently loaded modules:

```bash
module list
```

This command displays the names and versions of each module currently loaded into your environment.

II. **List Available Modules:**

To see a list of all modules available for loading, use:

```bash
module avail
```

If you want to filter the results, you can specify part of a module name or a pattern:

```bash
module avail my_app
```

This command will show only those modules that match `my_app`.

#### Displaying Module Information

I. **Show Module Details:**

To view detailed information about a specific module, including the environment variables it modifies:

```bash
module show my_app/1.0
```

This command displays the modulefile’s contents and how it affects your environment, helping you understand what it changes when loaded.

II. **Get Help for a Module:**

Some modules include a help message to provide additional usage information. To access this help:

```bash
module help my_app/1.0
```

#### Switching Between Modules

If you want to replace one version of a module with another, you can use `module switch`:

```bash
module switch my_app/1.0 my_app/2.0
```

This command unloads the first module and immediately loads the second, effectively switching between versions.

#### Purging Modules

The `module purge` command removes all loaded modules from your environment:

```bash
module purge
```

This is useful when you need a clean environment but should be used with caution, as it will unload every loaded module, including those you may still need.

#### Saving and Restoring Module Sets

I. **Save Current Module Set:**

To save your current set of loaded modules, use:

```bash
module save my_default_modules
```

This creates a named set of modules that you can reload later, making it easy to return to a specific configuration.

II. **Restore Module Set:**

To reload a saved module set, use:

```bash
module restore my_default_modules
```

This command reloads all the modules saved under the specified name, allowing you to quickly set up your environment.

III. **List Saved Module Sets:**

To view a list of all saved module sets:

```bash
module savelist
```

This displays the names of all saved sets, helping you remember what configurations you’ve saved for later use.

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

1. Install the Environment Modules package on your system using the appropriate package manager command for your operating system (e.g., `apt install environment-modules` for Debian-based systems or `yum install environment-modules` for CentOS). Explain the purpose of Environment Modules and how they simplify the management of software versions on shared systems.
2. Create a directory under `/etc/modulefiles` for a new application. For example, set up a directory for Python by running `sudo mkdir /etc/modulefiles/python`. Discuss why `/etc/modulefiles` is commonly used for storing modulefiles and how it enables centralized module management.
3. Select a specific version of the application you plan to manage with environment modules (e.g., Python 3.8), and create a modulefile for this version in the directory you set up. For instance, use `sudo touch /etc/modulefiles/python/3.8` to create a modulefile. Briefly describe the structure of modulefile directories and the purpose of organizing applications by version.
4. Edit the modulefile for the application version you selected, configuring it to load the necessary environment settings. Use the `prepend-path` directive to add the `bin` and `lib` directories to the `PATH` and `LD_LIBRARY_PATH` environment variables, respectively. Include the `conflict` directive to prevent the loading of incompatible versions simultaneously. Discuss how `prepend-path` and `conflict` ensure smooth version management.
5. Load the application module you created using the `module load` command, and confirm the module is active by checking the output of `module list` and verifying the application’s version (e.g., `python --version`). Explain how the `module load` command modifies the user environment to include the application paths defined in the modulefile.
6. Unload the module you just loaded by using the `module unload` command. Verify that the module has been removed by running `module list` and checking that the application’s paths are no longer in your environment. Discuss why it’s essential to unload modules, especially when switching between different versions.
7. Use the `module avail` command to list all available modules on your system, including the one you created. Explain how the `module avail` command helps users discover available software and manage multiple applications more effectively.
8. Finally, unload all loaded modules using the `module purge` command, and confirm that no modules remain active by checking the output of `module list`. Discuss the utility of `module purge` for resetting the environment and ensuring a clean state before loading other modules.
Here are two additional challenges to complete the list, focusing on advanced modulefile customization and persistent module environments:
9. Add descriptive metadata to the modulefile, such as a brief description, version information, and any necessary dependencies or prerequisites for the application. Use directives like `module-whatis` to provide a summary and `module help` to give users more details when they load the module. Discuss how adding metadata improves module discoverability and provides helpful information for users.
10. Set up a persistent module environment by configuring your shell profile (e.g., `.bashrc` or `.bash_profile`) to automatically load a specific module or set of modules on login. Test this configuration by logging out and back in, then verifying that the module(s) load automatically. Explain the benefits of persistent module environments for frequent users of specific software.
