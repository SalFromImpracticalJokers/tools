_____


_____
CASPER_1.0_interact.py -->

this is a python built encryption tool (casper stands for cryptographic auto symetrical procedural encryption routine) (yes I made that up) that uses (minmum) 128 bit auto generated keys made based of a string input. the size of an input is rounded up to the next multiple of 128 bits for encryption and an appropriate length key is generated for it. Multiple XOR operations take place with the data and the key as well as with the 'defualt' variable which you can change when using this to make your encryption more unique from others with the program. Multiple ciphers are also applied to the plain text such as ceaser, substitution, reversals, and representation changes.

This encryption is pretty good but if you actually want to make this secure, when you use it, make sure to replace 'defualt', 'sub' and 'characters' with your own version in the same format (you can achieve this by just doing random.shuffle() on them and then copypasting the output back into the code as the new variable). maybe also change the order the XOR's occur for further safety.

If someone thinks they can crack this algorithm (im sure you can), try tell me what this says:

=y8!.:d!%yNyN:YY=OOy:%=:.~yOO%~y-:!OH!%O.~8!::=~-~H%v~.~v:yO8:yYdNOY~!vYd~8:~!%Y~O-N-N~N!~vNv:vy=Y8::y{N8~=y=YyN!yNNOOONH%:~:y!~

anyways, have fun!

_____
Screw_Edge_v2.py -->

This is a simple scipt i made that sees when windows opens something on Edge, closes it, and opens it in Chrome instead.
This could easily be reconfigured to monitor and replace any two browsers but if you want you can request from me.

Requires: pygetwindow (pip)

_____
chat_msg.exe/chat_msg.pyw -->

This is just a messanger i made from a 'firebase' realtime database that i made for free, it has end to end encryption (using CASPER) and allows for the creation of chats with different names and passwords. if you actually want to customise this or see the code, use the python file, but you will have to then put in your own details for the firebase as you cant have mine :)
Do this by making a free firebase real time databse, then putting the content of the json you can download from firebase, and the link to the database, in the specified locations in the python scipt (in the __init__ function  of the GUI class).

(python file) requires: firebase_admin

_____
image_hider.py -->

This is a very basic script i made that takes a path to a image file (openable in pygame, which is most), and a message. It then manipulates the RGB values of the pixels starting from the top left and hides the message in the image, then outputing a new image.

Note: this does not account for the width of the image, if your message has more characters than the image has pixels in width, it will break (but that would be a pretty long message). A certain level of resolution is also needed but most should be fine. Lasltly, if you want it to be more secure to attackers, replace the 'alpha' list at the top with your own list in a random order.

Requires: Pygame (pip)

____
video_cleaner.py -->

This is a script that takes a video file, and then attempts to remove duplicate frames and then outputs a more smooth video file. It is slow to run so dont use massive videos and it also removes sound. Overall, not the best program in the world but a good proof of concept. feel free to mess around with it.

Requires: opencv-python, numpy, scikit-image (pip)

_____
wifi_scanner.py -->

This is a linux command line tool that uses 'iw' (a linux package that should be preinstalled but can be installed) to list all the different wifi's your wifi receiver is picking up in a table, showing ssid, frequency, strength, and quality. the table is in strenght order and is constantly refreshing with pipelining. This is a useful tool for setting up your home wifi as you can walk around and check what frequencies/channels to avoid based on how many wifi's around you (decrease interferance and packet loss). Also may be useful for network SECURITY (NO USING THIS FOR HACKING OK).

requires: Linux + iw, keyboard (sudo pip, you dont need to have this but it allows you to pause it with spacebar)

any issues please check the '-h'/'--help' messages ('sudo python3 wifi_scanner.py -h')
