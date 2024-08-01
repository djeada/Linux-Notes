## Dynamic Window Manager (DWM)

The Dynamic Window Manager (DWM) is a minimal, lightweight, and highly efficient tiling window manager designed to help you manage application windows in a clean and distraction-free manner. Instead of overlapping windows as seen in traditional window managers, DWM organizes windows in a tiled layout, making it easy to see and navigate multiple applications simultaneously. DWM is based on the X Window System, making it suitable for use on Unix-like operating systems.

DWM stands out for its extreme simplicity and high customization capability. It is part of the suckless software philosophy, which emphasizes clarity, simplicity, and resource efficiency. 

![dwm](https://user-images.githubusercontent.com/37275728/189493108-20a94d0c-24fd-4b35-8b78-527a350abc0c.png)

Here's how DWM looks in action. Each window takes a portion of the screen, allowing for easy multitasking.

## Installation

Installation of DWM is straightforward. If you're on a Debian-based system such as Ubuntu or Mint, you can install DWM and its related suckless-tools packages using the following command in your terminal:

```bash
sudo apt install dwm suckless-tools
```

The suckless-tools package contains additional utilities developed by the suckless community, including dmenu, a fast and lightweight dynamic menu for X, and slock, a simple screen locker utility.

After installation, you can choose DWM as your window manager from the login screen.

Remember that DWM is highly customizable, but changes typically require modifying the source code and recompiling. So if you're up for some tinkering, you can clone the DWM source code from the suckless website, make changes to suit your needs, and then build and install your custom version of DWM.

## Usage

- After installing DWM, interaction is mainly through keyboard shortcuts, making it quicker and more efficient than using a mouse in a tiling window manager environment.
- Opening a new terminal can be done by pressing `Shift + Alt + Enter`, which typically launches the `st` terminal or `xterm` if `st` isn't installed.
- To move focus between different windows, you use `Alt + j` and `Alt + k`, which cycle through the windows in the currently visible tag.
- Promoting a window from the stack to the master area or vice versa is done by pressing `Alt + Enter`.
- Closing the currently focused window can be achieved by either clicking the close button or typing `exit` and pressing `Enter` in terminal windows.
- DWM uses a concept called tags, similar to virtual desktops or workspaces, and switching views to another tag is done by pressing `Alt + [tag number]`, with tag numbers ranging from 1 to 9.
- To quit DWM, you press `Shift + Alt + q`, which will close the window manager and return you to your display manager or console.
- Moving a window to another tag involves focusing on the window and then pressing `Shift + Alt + [tag number]`.
- Toggling a window between tiled and floating modes is done by focusing on it and pressing `Alt + t`. This shortcut can also be used to revert the window back to the tiled layout.
- Resizing a floating window can be accomplished by holding `Alt`, then right-clicking and dragging the window.
- Moving a floating window similarly requires holding `Alt` and then left-clicking and dragging the window.
- One of the key features of DWM is its customizability. If you are comfortable with C programming, you can modify `config.h`, recompile, and reinstall DWM to change key bindings and other settings to suit your preferences.

## Configuration

Unlike other window managers that use configuration files, DWM is customized by directly modifying its source code and then recompiling it. This approach provides a lot of flexibility and control over DWM's behavior and appearance. The main configuration is located in the `config.h` file, which can be found in the DWM source code directory.

Follow these steps to customize DWM to your preferences:

I. Download the DWM source code

You can clone the source code from the official suckless git repository using the following command:

```bash
git clone https://git.suckless.org/dwm
```

II. Navigate to the dwm directory and create a config.h file

The config.def.h file contains the default settings. To customize DWM, you should first copy config.def.h to config.h. Then, you can edit the config.h file with your preferred text editor (e.g., nano, vim, emacs). Here's how to do that:

```bash
cd dwm
cp config.def.h config.h
nano config.h
```

III. Customize the config.h file

In the config.h file, you can change various settings according to your preferences. For example, you can modify key bindings, set custom colors, define the status bar's appearance, and select the default font. Save your changes and exit the text editor when you're finished.

IV. Compile and install the modified DWM

After modifying the config.h file, you need to compile the DWM source code and install the new binary:

```bash
sudo make clean install
```

V. Apply the changes

Log out and log back in, or restart your X session to apply the changes. The updated DWM should now be in effect.

## Further Resources

- If you are seeking additional information about configuring and using DWM, the official DWM Tutorial provided by the suckless community is an excellent starting point. It offers a comprehensive walkthrough of basic DWM usage and configuration, available at [https://dwm.suckless.org/tutorial/](https://dwm.suckless.org/tutorial/).
- For a more in-depth understanding of DWM and its functionalities, the DWM man page is an invaluable resource. You can access it in your terminal by running the command `man dwm`.
- The DWM Config Archive is a collection of user-submitted `config.h` files, serving as a treasure trove of interesting and varied configurations. Exploring these files can provide new ideas for your own DWM setup or even a ready-to-use configuration that suits your needs. Visit the archive at [https://dwm.suckless.org/customisation/](https://dwm.suckless.org/customisation/).
