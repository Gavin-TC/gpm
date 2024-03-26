import os
import sys
import subprocess

cur_dir = os.path.dirname(os.path.realpath(__file__))
command = 'pyinstaller --noconfirm --onefile --console --name "gpm"  "' + cur_dir + '"'

print(command)
os.system("PAUSE")

os.system(command)

