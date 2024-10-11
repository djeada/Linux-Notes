## Dynamic Window Manager (DWM)

The Dynamic Window Manager (DWM) is a minimal, lightweight, and highly efficient tiling window manager designed to help you manage application windows in a clean and distraction-free manner. Instead of overlapping windows as seen in traditional window managers, DWM organizes windows in a tiled layout, making it easy to see and navigate multiple applications simultaneously. DWM is based on the X Window System, making it suitable for use on Unix-like operating systems.

DWM stands out for its extreme simplicity and high customization capability. It is part of the suckless software philosophy, which emphasizes clarity, simplicity, and resource efficiency. 

![dwm](https://user-images.githubusercontent.com/37275728/189493108-20a94d0c-24fd-4b35-8b78-527a350abc0c.png)

Here's how DWM looks in action. Each window takes a portion of the screen, allowing for easy multitasking.

### Installation

Installation of DWM is straightforward. If you're on a Debian-based system such as Ubuntu or Mint, you can install DWM and its related suckless-tools packages using the following command in your terminal:

```bash
sudo apt install dwm suckless-tools
```

The suckless-tools package contains additional utilities developed by the suckless community, including dmenu, a fast and lightweight dynamic menu for X, and slock, a simple screen locker utility.

After installation, you can choose DWM as your window manager from the login screen.

Remember that DWM is highly customizable, but changes typically require modifying the source code and recompiling. So if you're up for some tinkering, you can clone the DWM source code from the suckless website, make changes to suit your needs, and then build and install your custom version of DWM.

### Usage

- After installing DWM, interaction is mainly through keyboard shortcuts, making it quicker and more efficient than using a mouse in a tiling window manager environment.
- Opening a new terminal can be done by pressing `Shift + Alt + Enter`, which typically launches the `st` terminal or `xterm` if `st` isn't installed.
- To move focus between different windows, you use `Alt + j` and `Alt + k`, which cycle through the windows in the currently visible tag.
- Promoting a window from the stack to the master area or vice versa is done by pressing `Alt + Enter`.
- Closing the currently focused window can be achieved by either clicking the close button or typing `exit` and pressing `Enter` in terminal windows.
- DWM uses a concept called tags, similar to virtual desktops or workspaces, and switching views to another tag is done by pressing `Alt + [tag number]`, with tag numbers ranging from 1 to 9.
- To quit DWM, you press `Shift + Alt + q`, which will close the window manager and return you to your display manager or console.
- Moving a window to another tag involves focusing on the window and then pressing `Shift + Alt + [tag number]`.
- Toggling a window between tiled and floating modes is done by focusing on it and pressing `Alt + t`. This shortcut can also be used to revert the window back to the tiled layout.
- Toggling a window to full-screen mode within the current layout is done by pressing `Alt + m`, which switches to the monocle layout, making the focused window occupy the entire screen. This is particularly useful when you want to focus on a single window.
- Resizing a floating window can be accomplished by holding `Alt`, then right-clicking and dragging the window.
- Moving a floating window similarly requires holding `Alt` and then left-clicking and dragging the window.
- Launching an application launcher like `dmenu` can be done by pressing `Alt + p`, allowing you to start applications by typing their name, making for a quick and efficient workflow.
- Cycling through different layouts (e.g., tiling, floating, monocle) is done by pressing `Alt + Space`. This is useful when you want to experiment with different ways of arranging your windows.
- Viewing all windows across all tags simultaneously can be achieved by pressing `Alt + 0`. This allows you to quickly access any open window without switching tags.
- Moving a window to the scratchpad (a hidden, floating workspace) is done by pressing `Shift + Alt + s`. This is useful for keeping a window handy without cluttering your main workspace.
- Switching between the last used tags is quickly done by pressing `Alt + Tab`, allowing for fast toggling between workspaces.
- Focusing on the master area window directly can be done by pressing `Alt + l`. This is handy when you want to quickly shift your attention to the main application you're working on.
- Adjusting the master area size can be done dynamically by holding `Alt` and pressing `h` or `l`. This allows you to give more screen space to the master window or the stack area as needed.
- Restarting DWM without logging out is possible by pressing `Shift + Alt + r`, which reloads DWM with any new configurations applied, making it easier to test changes without disrupting your session.
- Taking a screenshot can be done by integrating tools like `scrot` or `maim` and binding them to a key combination in your `config.h`. For example, `Alt + Shift + s` could be used to take a screenshot of your current screen.
- Adjusting gaps between windows (if you've patched DWM with gaps support) can be done with custom keybindings, allowing you to increase or decrease spacing dynamically, tailoring your workspace to your visual preferences.
- Killing a non-responsive window can be done by focusing on it and pressing `Shift + Alt + c`, force-closing the application without needing to open a task manager.
- Checking the system status (like CPU usage, memory, or battery) can be enhanced by adding a custom status bar script to DWM, providing real-time system information directly on your screen.
- Locking your screen for security can be done by setting up a keybinding like `Alt + Shift + l` to launch a screen locker like `slock`, ensuring your system is protected when you step away.
- Navigating between monitors in a multi-monitor setup is done by pressing `Alt + Shift + [arrow key]`, allowing you to quickly move focus or windows across different screens.

### Configuration

Unlike other window managers that use configuration files, DWM is customized by directly modifying its source code and then recompiling it. This approach provides a lot of flexibility and control over DWM's behavior and appearance. The main configuration is located in the `config.h` file, which can be found in the DWM source code directory.

Follow these steps to customize DWM to your preferences:

#### Download the DWM Source Code

You can clone the source code from the official suckless git repository using the following command:

```bash
git clone https://git.suckless.org/dwm
```

#### Navigate to the `dwm` Directory and Create a `config.h` File

The `config.def.h` file contains the default settings. To customize DWM, you should first copy `config.def.h` to `config.h`. Then, you can edit the `config.h` file with your preferred text editor (e.g., nano, vim, emacs). Here's how to do that:

```bash
cd dwm
cp config.def.h config.h
nano config.h
```

#### Customize the `config.h` File

In the `config.h` file, you can change various settings according to your preferences. For example, you can modify key bindings, set custom colors, define the status bar's appearance, and select the default font. 

**Changing the Border Configuration:**

I. Within `config.h`, locate the section where the border settings are defined. It typically looks like this:

```c
static const unsigned int borderpx  = 1;        /* border pixel of windows */
```

`borderpx` controls the width of the border around each window. The default value is usually `1` pixel.

II. To increase or decrease the border width, change the value of `borderpx`. For example, to set the border width to 2 pixels, change the line to:

```c
static const unsigned int borderpx  = 2;
```

If you want to remove the border entirely, you can set `borderpx` to `0`:

```c
static const unsigned int borderpx  = 0;
```

III. The border color for both focused and unfocused windows is defined in the color scheme section of `config.h`. Look for the following lines:

```c
static const char col_gray1[]       = "#222222";
static const char col_gray2[]       = "#444444";
static const char col_gray3[]       = "#bbbbbb";
static const char col_gray4[]       = "#eeeeee";
static const char col_cyan[]        = "#005577";
static const char *colors[][3]      = {
   /*               fg         bg         border   */
   [SchemeNorm] = { col_gray3, col_gray1, col_gray2 },
   [SchemeSel]  = { col_gray4, col_cyan,  col_cyan  },
};
```

Here, `col_cyan` is used for the border of the focused window, and `col_gray2` is used for the unfocused windows. To change the border color, replace the hex color code with your preferred color. For example, to change the focused window border to red:

```c
static const char col_red[]         = "#ff0000";
static const char *colors[][3]      = {

   /*               fg         bg         border   */

   [SchemeNorm] = { col_gray3, col_gray1, col_gray2 },

   [SchemeSel]  = { col_gray4, col_red,   col_red   },

};
```

IV. After adjusting the border settings and any other customizations, save your changes and exit the text editor.

#### Compile and Install the Modified DWM

After modifying the `config.h` file, you need to compile the DWM source code and install the new binary:

```bash
sudo make clean install
```

This command will clean up any previous builds and compile your customized version of DWM.

#### Apply the Changes

To apply your changes, you need to restart DWM. You can do this by logging out and logging back in, or by restarting your X session. Once you log back in, the updated DWM with your new border settings and other customizations should be in effect.

### Further Resources

- If you are seeking additional information about configuring and using DWM, the official DWM Tutorial provided by the suckless community is an excellent starting point. It offers a comprehensive walkthrough of basic DWM usage and configuration, available at [https://dwm.suckless.org/tutorial/](https://dwm.suckless.org/tutorial/).
- For a more in-depth understanding of DWM and its functionalities, the DWM man page is an invaluable resource. You can access it in your terminal by running the command `man dwm`.
- The DWM Config Archive is a collection of user-submitted `config.h` files, serving as a treasure trove of interesting and varied configurations. Exploring these files can provide new ideas for your own DWM setup or even a ready-to-use configuration that suits your needs. Visit the archive at [https://dwm.suckless.org/customisation/](https://dwm.suckless.org/customisation/).
