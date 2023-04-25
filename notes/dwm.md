## Dynamic Window Manager

Dynamic Window Manager (DWM) is a lightweight, tiling window manager for efficient and effective window management. It's easy to use, customizable, and based on the X Window System.

![dwm](https://user-images.githubusercontent.com/37275728/189493108-20a94d0c-24fd-4b35-8b78-527a350abc0c.png)

## Installation

Install DWM on a Debian-based system with the command:

```bash
apt install dwm suckless-tools
```

This installs DWM and related suckless-tools packages.

## Usage

With DWM installed, use these commands to manage windows:

* Spawn a new terminal: `Shift + Alt + Enter`
* Move between terminals: `Alt + j and Alt + k`
* Change terminal position: `Alt + Enter`
* Close a terminal: `type exit and press Enter`
* Focus on another tag: `Alt + [tag number]`
* Log out: `Shift + Alt + q`
* Move a window to another tag: `Shift + Alt + [tag number]`
* Toggle a window to float or tile: `Alt + t`
* Resize a floating window: `Alt + Right-click + Drag`
* Move a floating window: `Alt + Left-click + Drag`

## Configuration

DWM can be customized by modifying its source code and recompiling it. The configuration is located in the `config.h` file, found in the DWM source code directory.

1. Download DWM source code:

```bash
git clone https://git.suckless.org/dwm
```

2. Change to the dwm directory and edit the `config.h` file:

```bash
cd dwm
cp config.def.h config.h
nano config.h
```

3. Make changes to the config.h file according to your preferences, such as key bindings, colors, and fonts.

4. Compile and install the modified DWM:

```bash
sudo make clean install
```

5. Log out and log back in to apply the changes.

## Refrences

For more information on using DWM, visit the tutorial on the DWM website: https://dwm.suckless.org/tutorial/
