activate_this = '/home/Envs/ncb_p3/bin/activate_this.py'
exec(open("/home/Envs/ncb_p3/bin/activate_this.py").read(), {'__file__': "/home/Envs/ncb_p3/bin/activate_this.py"})

# import sys

# sys.path.append('/var/www/NCB_Cleaner')

from ConfRoomCleaner import CRCleaner

confroomcleaner('scheduled')
