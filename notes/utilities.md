## Taking Screenshots

*Scrot* is a small program used for taking screenshots directly from the termianl.

On Debian based system, you can install it in the following way:

    apt install scrot

Minimal example:

    scrot screenshot.png

Some more options:

    scrot -b -d 3 screenshot.png -e 'mv $f ~/Desktop/'

* The -b option instructs the program to include the window borders in the screenshot.
* The -d option specifies a 3 second delay.
* The command `-e 'mv $f ~/Pictures/'` instructs the utility to save the screenshot to the *~/Pictures* directory. 

## Recording screen

*Vokoscreen* is perfect for recording screen with webcam capture.

On Debian based system, you can install it in the following way:

    apt install vokoscreen
    
![Screenshot from 2022-09-21 11-15-03](https://user-images.githubusercontent.com/37275728/191465681-8b4915ad-b8a5-4a69-b05b-d3b25b5e2d95.png)

To start the app, you can simply type:

    vokoscreenNG

## Preparing a bootable stick

*USBImager* can be used to prepare a bootable stick with a Linux image.

![Screenshot from 2022-09-06 22-47-32](https://user-images.githubusercontent.com/37275728/188735068-290204a3-e986-49e7-be72-3caf4fa95644.png)
