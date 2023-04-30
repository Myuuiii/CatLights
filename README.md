![](https://minio.myuuiii.com/myuuiii/GitHub/CatLights/CatLights-BannerHeader.png)

## What is CatLights

CatLights is a converter that converts `.png` files to `.mid` files. This project is primarily meant for people that want to use this in combination with Ableton Live and a Novation Launchpad. The user can make their light effects in a tool like Aseprite and convert the animations to MIDI files that can then be used as light effects on the Launchpad.

## How to use

- Make sure you have python installed and added to your PATH system variable (this is asked during the installation of Python)
- Download the latest version of the code using the green button at the top. You can download it as a zip.
  - Make sure that you have the `VelocityMap.png` in the folder besides the script. It will not work if this image is in a different location.
- Open a terminal and type `pip install -r requirements.txt` or run the `install_deps.bat` file to install the required dependencies on your computer.

### Single-Folder

To process a single folder to turn into a `.mid` file. Simply drag the folder with your images over the script and let go. By default, the script will ask what the speed should be. You can up this number to increase the speed or lower it to make it slower. After giving that input, a `.mid` file should appear in the location where the source folder is located.

### Multi-Folder

To process multiple folders and turn them into multiple `.mid` files. Select and drag the folders over the script with 'BATCH PROCESS' in the name. When you let go, multiple `.mid` files will be created in the location where the source folders are located.

## Example

First create your animation with the program of your choice, I will be using Aseprite as it is easy to use in my opinion.

![](https://minio.myuuiii.com/myuuiii/GitHub/CatLights/step1.png)

After you have created your animation, export them to a folder as separate `.png` files.

![](https://minio.myuuiii.com/myuuiii/GitHub/CatLights/step2.png)

Go to the parent directory and drag it over the script, then let go.

![](https://minio.myuuiii.com/myuuiii/GitHub/CatLights/step3.gif)

By default, the script asks for a speed, you can just press enter if you want to keep the default speed. Making the number higher increases the playback speed.

![](https://minio.myuuiii.com/myuuiii/GitHub/CatLights/step4.png)

After that, a `.mid` file should appear in the folder where the source files are located.

![](https://minio.myuuiii.com/myuuiii/GitHub/CatLights/step5.gif)

You can now use this `.mid` file as a light effect in software like Ableton Live

## Does it support X

> **Top Lights**: Yes, all the top lights have their own MIDI addresses, you might need to use a plugin like Kaskobi's [LED Setup](https://www.kaskobi.com/led-setup) plugin to enable custom top light colors.

> **Mode Light**: Yes, the mode light is addressed at `NN27`  which should be D#1, you might need to use a plugin like Kaskobi's [LED Setup](https://www.kaskobi.com/led-setup) plugin to enable custom mode light colors.

> **Novation Light**: I'm not really sure, I do not own a MK3 series Launchpad so I have not been able to test this.

## Custom Velocity Map

You can add your own custom velocity map to the software. The default one is shipped with the software and is called `VelocityMap.png`. Currently, you would need to replace the file in order to load in the custom one. I recommend saving the default one, but you can always re-download it from here.

### What is a Velocity Map

A velocity map looks like this: ![velMap](https://minio.myuuiii.com/myuuiii/GitHub/CatLights/velmap.png)

It is split up in 4 columns of 4 pixels wide and 8 pixels high and is read like this: ![velMapGuide](https://minio.myuuiii.com/myuuiii/GitHub/CatLights/velmapread.png)

### Template Velocity Map

I really recommend making these animations and velocity maps with a tool called Aseprite. I have provided the default color palette you can use to make animations as `/Aseprite Files/ColorPalette.aseprite`. The `/Aseprite Files/VelocityMap.aseprite` file is the default velocity map. If you use a custom palette (using a plugin in Ableton for example) you can change the colors of this Velocity Map and Color Palette to your custom palette colors.