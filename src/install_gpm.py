import os
import sys
import subprocess

cur_dir = os.path.dirname(os.path.realpath(__file__))
command = 'python -m PyInstaller --distpath ' + cur_dir + ' --clean --noconfirm --onefile --console --name "gpm"  "' + cur_dir + '\\main.py"'

os.system(command)

