import os
import sys
import subprocess
import PyInstaller.__main__

def main():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    install_dir = ""
    path_dir = ""

    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        install_dir = "/usr/local/bin/"
        path_dir = install_dir + "/gpm"
    elif sys.platform.startswith('win'):
        install_dir = "C:\\Program Files"
        path_dir = install_dir + "\\gpm"
    else:
        print("[ERROR] OS not supported!")
        os.system("PAUSE")
        return


    print("\n[\u001b[33mWARNING\u001b[0m] PLEASE DO NOT CLOSE THIS WINDOW UNTIL INSTALLATION IS FINISHED!")

    PyInstaller.__main__.run([
        "--distpath", install_dir,
        "--clean",
        "--noconfirm",
        "--console",
        "--name", "gpm",
        os.path.join(cur_dir, "main.py")
    ])

    if sys.platform.startswith('win'):
        print("\n[\u001b[33mWARNING\u001b[0m] If you haven't already, add the following to your PATH environment variable or the program will not work:")
        print("[\u001b[33m" + path_dir + "\u001b[0m] (COPIED TO CLIPBOARD)\n")
        os.system('echo ' + path_dir + '| clip')
        os.system("PAUSE")

main()

