import sys
import os
import datetime as dt       # To convert modification & creation date timestamps into normal dates

scriptPath = "Replace this with the folder where you will store the script"
ls_format = "lsd"   # Replace this with 'ls' if you dont have the 'lsd' utility installed

bold_code = "\033[1m"
uline_code = "\033[4m"
end_style_code = "\033[0m"

def formatAsError(text: str):
    text = "\033[91m" + text + end_style_code
    return text

def listDirs(dirToList=os.getcwd()):
    if dirToList != os.getcwd():
        dirToList = dirToList.replace(os.getcwd(), ".")
        # This if can be removed if you want the absolute path to always be displayed
        # Made so that paths being displayed are not as long

    print(f"\n󱞊    {bold_code}{dirToList}{end_style_code}\n")       # 󱞊 is the nerdfonts icon for a folder with an eye
    os.system(f"{ls_format} {dirToList} --group-dirs=first")

if len(sys.argv) <= 1:
    # print(formatAsError(" | Invalid syntax, please include a path"))
    # Uncomment the line above 
    listDirs()
    raise SystemExit

args = sys.argv[1:]     # '1:' excludes the script name
# print(f"Argument list: {args}")

fname = args[0]
count = 1
if fname.__contains__("'"):
    for elem in args:
        count += 1

        fname += " " + elem
        if elem.__contains__("'"):
            break

"""This for loop ensures that the user can introduce file names separated by spaces
by using the '' to delimit what is the actual file name"""

args = args[count:]     # Excludes the provided file name from the list of arguments

if not os.path.exists(fname):
    print(formatAsError(" | Given file does not exist (" + f"\033[97m'{fname}'{end_style_code}" + formatAsError(")")))
    raise SystemExit

if os.path.isdir(fname):
    listDirs(os.path.abspath(fname))    # The absolute path of the given path will be displayed
    raise SystemExit

ext = fname.split(".")[-1]      # Obtains file extension if possible

with open(scriptPath + "imgTypes.txt", "r") as imgTypesFile:
    imgTypes = (imgTypesFile.read()).split("\n")

# print(f"\n·  {fname}")
# Uncomment last line for the program to print the name of the file that will be opened

if ext != fname and imgTypes.__contains__(ext):
    file_stats = os.stat(os.getcwd() + "/" + fname)

    try:
        file_ctime = dt.datetime.fromtimestamp(file_stats.st_ctime)
    except NotImplementedError:
        file_ctime = ""

    # NerdFonts icons used:
    #  - Hashtag symbol for file name
    #  - Database symbol for file size
    # 󱇣 - Image edit symbol for modification date
    # 󰙴 - Stars symbol for creation date

    imgData = [f" {bold_code}File name:\t\t{end_style_code}{fname}", 
               f" {bold_code}File size:\t\t{end_style_code}{round((file_stats.st_size)/(1000*1000), 4)} MB", 
               f"󱇣 {bold_code}Modification date:\t{end_style_code}{dt.datetime.fromtimestamp(os.path.getmtime(os.getcwd()+'/'+fname))}", 
               f"󰙴 {bold_code}Creation date:\t{end_style_code}{file_ctime}"]

    """
    This part will open images provided using the icat kitten(extension) 
    for kitty terminal emulator.
    Requires both kitty terminal emulator and imagemagick terminal plugin
    """

    linespace = 10          # Scale at which the image is displayed along with its border
    border = 5              # Space between window edge and image border

    os.system("clear")      # Can be removed, but then the image's border wont be displayed properly

    print("\n"*int(border/2 - 1))   # Takes the border of the image with respect to the window's top edge into account

    """Prints the border for the image"""
    for i in range(0, int(linespace)+border+1):         # '‾'  '_'
        print(" "*int(border+1), end="")

        if i==0:
            print("_"*(linespace*4+2), end="")
        elif i == int(linespace)+border:
            print("‾"*(linespace*4+2), end="")
        else:
            print("|" + " "*int(linespace*4) + "|", end="")

        if i > 2 and (i-3) < len(imgData):
            print(f"\t\t\t {imgData[i-3]}")
        else:
            print("\n", end="")
    
    # Actually displays the image
    os.system(f"kitty +kitten icat --align=center --scale-up --place={int(linespace*4)}x{linespace}@{int(border+2)}x{border} {' '.join(args)} {fname}")
    listDirs()

elif ext == "pdf":
    os.system(f"evince '{fname}' {' '.join(args)}")
    # &> /dev/null can be used so that less GTK warning messages are shown, but it causes permission errors sometimes

else:
    catOutput = os.popen(f"cat {fname} -n {' '.join(args)}")
    try:
        print(catOutput.read())
    except UnicodeDecodeError:
        print(formatAsError("| Unsupported file type given"))

