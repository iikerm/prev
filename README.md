# Preview  youR  Elements  Very professionally  (prev)
This is a very simple script made for the kitty terminal emulator that allows you to obtain a preview for certain file types directly inside the terminal

## Currently supported file types:
### Image file types
Because prev uses a terminal utility called `imageMagick`, it theoretically supports the same file types, even though all of them haven't been tested yet  
### Text file types
When prev is not used with an image, pdf or other specific file types, it will assume that it is dealing with a text file and prints its contents using the `cat` command, and therefore it is able to read almost all of the text files it will encounter
### PDFs and other specific file types
Even though the aim of this program is to be able to quickly preview most files that one would usually encounter inside the terminal, due to limitations and ease of use, other file types such as PDFs or videos (not implemented yet), are opened in an external file viewer
> For Ubuntu, this means that PDF files are opened using the `evince` tool, if your system doesn't have it, the pdf preview won't work

## Prerequisites
### Having python installed in your machine
This script has been tested using python version `3.10.12`, but there shouldn't be any problem if using a different version
> For Ubuntu users, write the following command in the Gnome terminal:
> - `$ sudo apt install python3`
### Installing the kitty terminal emulator
The following link is the github repo for the kitty terminal emulator:  
https://github.com/kovidgoyal/kitty  
Inside this repo are the instructions for installing it
> If you are using Ubuntu, you can simply write the following command in the Gnome terminal:
> - `$ sudo apt install kitty`
### Installing imagemagick utility
This utility is used for image previewing and can be easily installed using:
- `$ sudo apt install imagemagick`

## Optional (but recommended) extras
### Creating an alias for it
This will save you from having to write the full command to execute this script every time you want to use it (`$ python3 /path/prev.py <args>`)
1. To create an alias go to your shell config file (`.bashrc` if you haven't changed your shell, or `.<shell_name>rc` if you have)
2. Then go to the end of the file and write:
   - `alias prev='python3 /path_to_script/prev.py'
3. Now you can just type `$ prev` in your terminal and it will work a lot better

### [lsDeluxe](https://github.com/lsd-rs/lsd) utility
This is a utility that will allow you to use the `lsd` command in order to decorate your terminal and add some icons to the otherwise boring `ls` command 
> On Ubuntu, you can use: `$ sudo snap install lsd --devmode`
> The `--devmode` option is not required but it is the only way to be able to use the command inside hidden folders

### Installing a nerdfont icons compatible font for kitty
The nerdfont icons pack is a series of text-based icons that are used in some parts of the prev script, and are also a requirement for the lsDeluxe utility
