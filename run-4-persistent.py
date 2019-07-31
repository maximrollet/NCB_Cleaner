import os
import sys

activate_this = '/home/Envs/ncb_p3/bin/activate_this.py'
exec(open("/home/Envs/ncb_p3/bin/activate_this.py").read(), {'__file__': "/home/Envs/ncb_p3/bin/activate_this.py"})

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append('/var/www/NCB_Cleaner')

from ConRoomCleaner import *

RunCleaner = CRCleaner("persistent")
RunCleaner.confroomclean()


