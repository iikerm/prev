import sys
import os
import datetime as dt       # To convert modification & creation date timestamps into normal dates

scriptPath = "/home/iker/.scripts/prev/"
ls_format = "lsd"   # Replace this with 'ls' if you dont have the 'lsd' utility installed

bold_code = "\033[1m"
uline_code = "\033[4m"
end_style_code = "\033[0m"

validArguments = {"help1": "-h", "help2": "--help",
                  "clear_imgs1": "-ci", "clear_imgs2": "--clear-images", 
                  "show_lines1": "-l=", "show_lines2": "--show-lines=",
                  "see_from1": "-p=", "see_from2": "--see-from="}

helpText = f"""\t{bold_code}{uline_code}Prev tool help:{end_style_code}

        {bold_code}Usage:{end_style_code}

        Write prev <path_to_file_or_dir> <argument(s)> in order to preview a file.
        If no path is provided, it will preview the current directory
        
        {bold_code}Arguments:{end_style_code}

        -ci             \t--clear-images            \t This will erase from the window any images that have been previously rendered

        -h              \t--help                    \t It will display this page

        {bold_code}Extra arguments that can be used with text files:{end_style_code}

        -p=<pos>        \t--see-from=<pos>          \t Determines from which line position will the text file be read. Default is 1.

        -l=<line_amount>\t--show-lines=<line_amount>\t Determines the amount of lines that will be displayed from a 
                                                    \t\t given line onwards. Any negative value will mean that the 
                                                    \t\t file will be output entirely. Default is -1.

    """

def formatAsError(text: str):
    text = "\033[91m" + text + end_style_code
    return text

def listDirs(dirToList=os.getcwd(), spaces=12):
    print("\n"*spaces)
    if dirToList != os.getcwd():
        dirToList = dirToList.replace(os.getcwd(), ".")
        # This if can be removed if you want the absolute path to always be displayed
        # Made so that paths being displayed are not as long

    print(f"\n{uline_code}󱞊    {bold_code}{dirToList}{end_style_code}")       # 󱞊 is the nerdfonts icon for a folder with an eye
    os.system(f"{ls_format} {dirToList} --group-dirs=first")

def checkInt(toCheck: str, errorText: str):
    try:
        toCheck = int(toCheck)
    except ValueError:
        print(errorText)
        raise SystemExit
        # Done so that the program doesn't crash later on by trying to compare a string to an integer
    
    return toCheck


if len(sys.argv) <= 1:
    # print(formatAsError(" | Invalid syntax, please include options"))
    # Uncomment the line above 
    listDirs()
    raise SystemExit


args = sys.argv[1:]     # '1:' excludes the script name
# print(f"Argument list: {args}")

fname = args[0]
count = 1
if fname.__contains__("'"):
    """ 
    This for loop ensures that the user can introduce file names separated by spaces
    by using the '' to delimit what is the actual file name
    """
    for elem in args:
        count += 1

        fname += " " + elem
        if elem.__contains__("'"):
            break


args = args[count:]     # Excludes the provided file name from the list of arguments

# Checks some arguments that can be passed without a file name / directory being provided
if fname.__contains__(validArguments["clear_imgs1"]) or fname.__contains__(validArguments["clear_imgs2"]):
    os.system("kitty +kitten icat --clear")
    print("Images cleared successfully")
    raise SystemExit

elif fname.__contains__(validArguments["help1"]) or fname.__contains__(validArguments["help2"]):
    print(helpText)
    raise SystemExit


# Checks if the file exists
if not os.path.exists(fname):
    print(formatAsError(" | Given file does not exist (" + f"\033[97m'{fname}'{end_style_code}" + formatAsError(")")))
    raise SystemExit

# Displays an 'ls' type command result if the given name is a directory
if os.path.isdir(fname):
    listDirs(os.path.abspath(fname))    # The absolute path of the given directory will be displayed
    raise SystemExit

if fname.__contains__("."):
    ext = fname.split(".")[-1]      # Obtains file extension if possible
else:
    ext = None

# Loads contents of he file with supported image extensions (or at least the ones that have been tested)
with open(scriptPath + "imgTypes.txt", "r") as imgTypesFile:
    imgTypes = (imgTypesFile.read()).split("\n")

# print(f"\n·  {fname}")
# Uncomment last line for the program to print the name of the file that will be opened


# Starts proccessing given file if it should
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


    # Prints the border for the image
    for i in range(0, int(linespace)+border+1):
        # '‾'  '_' are the characters used for bottom and top of the image frame respectively
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
    os.system(f"kitty +kitten icat --align=center --scale-up --place={int(linespace*4)}x{linespace}@{int(border+2)}x{border} {fname}")
    listDirs()

elif ext == "pdf":
    os.system(f"evince '{fname}' {' '.join(args)}")
    # &> /dev/null can be written after 'evince' so that less GTK warning messages are shown, but it causes permission errors inside some folders
    # This is due to a GTK bug which I could not find a solution for

else:
    catOutput = os.popen(f"cat {fname} -n")
    try:
        fileContent = catOutput.read()
    except UnicodeDecodeError:
        # The 'cat' command will produce "random" characters when trying to open non-text files 
        # (i.e. zip, tgz, binaries etc.) which raise UnicodeDecodeError when printed
        print(formatAsError("| Unable to preview this file type (") + f"\033[97m'{ext}'{end_style_code}" + formatAsError(")"))
        raise SystemExit

    
    
    # This part will only be reached if the text file can be previewed

    # Splits the contents of the file into lines
    fileContent = fileContent.split("\n")
    while fileContent.__contains__(""):
        fileContent.remove("")


    # Checks if the user entered an argument to only see a certain number of lines from the file

    linesToShow = -1        # Default value to show all the lines (any negative number will do the same)
    for arg in args:
        if arg.__contains__(validArguments["show_lines1"]):
            linesToShow = arg.replace(validArguments["show_lines1"], "")
            linesToShow = checkInt(linesToShow, formatAsError("| Invalid number of lines given (") + f"\033[97m'{linesToShow}'{end_style_code}" + formatAsError(")"))
        
        elif arg.__contains__(validArguments["show_lines2"]):
            linesToShow = arg.replace(validArguments["show_lines2"], "")
            linesToShow = checkInt(linesToShow, formatAsError("| Invalid number of lines given (") + f"\033[97m'{linesToShow}'{end_style_code}" + formatAsError(")"))

    startingPos = 1        # Default value to start from the start
    for arg in args:
        if arg.__contains__(validArguments["see_from1"]):
            startingPos = arg.replace(validArguments["see_from1"], "")
            startingPos = checkInt(startingPos, formatAsError("| Invalid position to read from (") + f"\033[97m'{startingPos}'{end_style_code}" + formatAsError(")"))
        
        elif arg.__contains__(validArguments["see_from2"]):
            startingPos = arg.replace(validArguments["see_from2"], "")
            startingPos = checkInt(startingPos, formatAsError("| Invalid position to read from (") + f"\033[97m'{startingPos}'{end_style_code}" + formatAsError(")"))

    print(f"Lines to show: {linesToShow}\nStarting from: {startingPos}")        # DEBUG
    startingPos -= 1    # So the user can deal with line numbers instead of list indices

    if startingPos >= len(fileContent):
        print(formatAsError("| Position to read from is bigger than file length (") + f"\033[97m{startingPos+1}{end_style_code}" + formatAsError(")"))
        raise SystemExit
    elif startingPos < 0:
        print(formatAsError("| Invalid position to read from (") + f"\033[97m{startingPos+1}{end_style_code}" + formatAsError(")"))
        raise SystemExit
    else:
        fileContent = fileContent[startingPos:]

    if linesToShow >= 0:
        count = 0
        while count < linesToShow and count < len(fileContent):
            print(fileContent[count])
            count += 1
    else:
        for line in fileContent:
            print(line)

