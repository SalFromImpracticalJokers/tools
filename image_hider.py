import os
import pygame

os.chdir(os.path.dirname(os.path.realpath(__file__)))

pygame.init()

alpha = [" ", "e", "a", "r", "i", "o", "t", "n", "s", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "p", "q", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", "!", "?", "(", ")", "-", "/", "'", ":", ";", '"', "+", "=", "*", "<", ">", "%", "^", "&", "£", "$", "@", "#", "~", "_"]

def hid():
    os.system("cls")
    name = input("Enter image name to hide data in: ")
    os.system("cls")
    data = input("Enter the message you want to hide: ")
    os.system("cls")
    newname = input("Enter the new name: ")
    os.system("cls")
    try:
        mimage = pygame.image.load(name)
    except:
        os.system("cls")
        input("No file found\n")
        main()
    try:
        pixel = pygame.PixelArray(mimage)
        length = len(data)
        x = 0
        color = mimage.unmap_rgb(pixel[x, 0])
        colourb = mimage.unmap_rgb(pixel[0, 1])
        colourb = str(colourb)
        colourb = colourb[:colourb.index(",")]
        colourb = colourb[1:]
        colourb = int(colourb)
        length = colourb + length
        if length > 255:
            length = length - 255
        color = pygame.Color(color)
        color = str(color)
        color = color[:len(color)-1]
        colors = color.split(", ")
        colors.pop(0)
        for i in colors:
            tempe = int(i)
            tempi = colors.index(i)
            colors.pop(tempi)
            colors.insert(tempi, tempe)
        c1 = colors[0]
        c2 = colors[1]
        c3 = colors[2]
        change = length - colourb
        pixel[x, 0] = pygame.Color(c1, c2, length)
        for i in data:
            x += 1
            add = alpha.index(i)
            add = colourb + add
            if add > 255:
                add = add - 255
            pixel[x, 0] = pygame.Color(c1, c2, add)

        mimage = pixel.make_surface()
        pygame.image.save(mimage, newname)
        os.system("cls")
        input("Data hidden\n")
    except:
        input("Error: likely file name\n")
    main()

def fin():
    os.system("cls")
    name = input("Enter image name with hidden data in: ")
    try:
        mimage = pygame.image.load(name)
    except:
        os.system("cls")
        input("No file found\n")
        main()
    try:
        pixel = pygame.PixelArray(mimage)
        lengthp = mimage.unmap_rgb(pixel[0, 0])
        lengthl = str(lengthp).split(", ")
        length = lengthl[2]
        length = int(length)
        basep = mimage.unmap_rgb(pixel[0, 1])
        basel = str(basep).split(", ")
        base = basel[0]
        base = base.replace("(", "")
        base = int(base)
        length = length - base
        if length < 0:
            length = 255 + length
        letters = []
        for i in range(1, length + 1):
            lengthp = mimage.unmap_rgb(pixel[i, 0])
            lengthl = str(lengthp).split(", ")
            length = str(lengthl[2])
            length = int(length)
            length = length - base
            if length < 0:
                length = 255 + length
            letters.append(alpha[length])
        os.system("cls")
        letterst = ""
        for i in letters:
            letterst = letterst + i
        letters = letterst
        if letters == "":
            lengthp = mimage.unmap_rgb(pixel[0, 0])
            lengthl = str(lengthp).split(", ")
            length = lengthl[0]
            length = length.replace("(", "")
            length = int(length)
            basep = mimage.unmap_rgb(pixel[0, 1])
            basel = str(basep).split(", ")
            base = basel[0]
            base = base.replace("(", "")
            base = int(base)
            length = length - base
            if length < 0:
                length = 255 + length
            letters = []
            for i in range(1, length + 1):
                lengthp = mimage.unmap_rgb(pixel[i, 0])
                lengthl = str(lengthp).split(", ")
                length = str(lengthl[0])
                length = length.replace("(", "")
                length = int(length)
                length = length - base
                if length < 0:
                    length = 255 + length
                letters.append(alpha[length])
            os.system("cls")
            letterst = ""
            for i in letters:
                letterst = letterst + i
            letters = letterst
        input(f"Message: {letters}")
    except:
        input("Error: likely file name\n")
    main()

def main():
    while True:
        os.system("cls")
        com = input("Hide or unpack (1/2): ")
        if com == "1" or com == "2":
            break
        else:
            os.system("cls")
            input("Invalid input")
    if com == "1":
        hid()
    else:
        fin()
        
main()
