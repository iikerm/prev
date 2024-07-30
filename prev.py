import sys
import os

scriptPath = "Replace this with the folder where you will store the script"
ls_format = "lsd"   # Replace this with 'ls' if you dont have the 'lsd' utility installed

bold_code = "\033[1m"
uline_code = "\033[4m"
end_style_code = "\033[0m"

def formatAsError(text: str):
    text = "\033[91m" + text + end_style_code
    return text

def listDirs(dirToList=os.getcwd()):
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
args = args[1:]     # Excludes the provided file name from the list of arguments

if not os.path.exists(fname):
    print(formatAsError(" | Given file does not exist (" + f"\033[97m'{fname}'{end_style_code}" + formatAsError(")")))
    raise SystemExit

if os.path.isdir(fname):
    listDirs(fname)
    raise SystemExit

ext = fname.split(".")[-1]      # Obtains file extension if possible

with open(scriptPath + "imgTypes.txt", "r") as imgTypesFile:
    imgTypes = (imgTypesFile.read()).split("\n")

# print(f"\n·  {fname}")
# Uncomment last line for the program to print the name of the file that will be opened

if ext != fname and imgTypes.__contains__(ext):
    """
    This part will open images provided using the icat kitten(extension) 
    for kitty terminal emulator.
    Requires both kitty terminal emulator and imagemagick terminal plugin
    """

    linespace = 10
    border = 5
    tWin_width = 152    # Width in characters of my current terminal window

    os.system("clear")
    print("\n"*int(border/2 - 1))   # Takes the border of the image with respect to the window edges into account

    for i in range(0, int(linespace)+border+1):         # '‾'  '_'
        print(" "*int(tWin_width/2 - linespace*2), end="")

        if i==0:
            print("_"*(linespace*4+2))
        elif i == int(linespace)+border:
            print("‾"*(linespace*4+2))
        else:
            print("|" + " "*int(linespace*4) + "|")
    
    os.system(f"kitty +kitten icat --align=center --scale-up --place={int(linespace*4)}x{linespace}@{int(tWin_width/2 - linespace*2 +1)}x{border} {' '.join(args)} {fname}")
    listDirs()

elif ext == "pdf":
    os.system(f"evince {fname} {' '.join(args)}")       # &> /dev/null 
else:
    catOutput = os.popen(f"cat {fname} -n {' '.join(args)}")
    try:
        print(catOutput.read())
    except UnicodeDecodeError:
        print(formatAsError("| Unsupported file type given"))

