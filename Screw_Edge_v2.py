import os
import subprocess
import pygetwindow as gw
import time

os.system("cls")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def get_name(name):
    os.system('wmic process where name="msedge.exe" call terminate')
    new_name = []
    for i in name:
        if i == "-":
            break
        new_name.append(i)
    new_name.pop(len(new_name) - 1)
    final_name = ""
    for i in new_name:
        final_name = final_name + i
    return final_name

def open_chrome_with_search(search_query, name):
    if search_query != "New tab":
        search_url = f"https://www.google.com/search?q={search_query}"
        subprocess.Popen([chrome_path, search_url])
        windows = gw.getAllTitles()
        for i in range(100):
            try:
                for i in windows:
                    if " - Google Chrome" in i:
                        target_window = gw.getWindowsWithTitle(i)[0]
                        break
            except:
                _=""
        try:
            target_window.activate()
        except:
            _=""
        print("\n", chrome_path, search_url)
        print("Query: ", search_query)
        print("\nEdge successfully fucked\n")
    else:
        os.system('"C:\Program Files\Google\Chrome\Application\chrome.exe"')
    print("")
    print("\nRUNNING...\n")

def main():
    print("\nRUNNING...\n")
    while True:
        programs = gw.getAllTitles()
        for i in programs:
            if "- Microsoft" in i and " Edge" in i and "untitled" not in i.lower():
                name = get_name(i)
                open_chrome_with_search(name, i)
        time.sleep(0.005)

main()
