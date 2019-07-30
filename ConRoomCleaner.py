# -*- coding: utf-8 -*-
"""
CONF ROOMS CLEANER MODULE
@author: maximrollet
"""

import os
import sys
import glob
from datetime import datetime, timedelta
import requests
import json
import logging
from sqlalchemy import *
from sqlalchemy.orm import *
from config.def_config import *

base_path = os.path.dirname(os.path.abspath(__file__))
m_path = '/media/conference'

logger = logging.getLogger(__name__)


class CRCleaner:

    def __init__(self, _type):
        self._type = _type

    def confroomclean(self):
        # CHECKER PART
        """
        logging.info("Cleaner started")
        if _type == 'persistent':
            table = 'type_persistent'  # type: str
        elif _type == 'recurring':
            table = 'type_recurring'
        elif _type == 'scheduled':
            table = 'type_scheduled'
        else:
            warnmess = "Wrong conference type '{}'".format(_type)
            logging.warning(warnmess)
            return {"result": False, "reason": "Wrong type of conference - '{}''".format(_type)}, 400
        """
        ttype = [('persistent', 'type_persistent'), ('scheduled', 'type_scheduled'), ('recurring', 'type_recurring')]
        table_type = ''
        stamptime = datetime.now()  # stamp of time for comparing
        resconflist = []  # list for check results of conferences

        try:
            for i in ttype:
                if i[0] == self._type:
                    table_type = i[1]  # table type for further checks
        except IOError:
            errormsg = "Wrong type of conference  room '{}' was sent!".format(self._type)
            logging.error(errormsg)

        logging.info("mysql queries")

        if table_type == 'type_scheduled':  # For scheduled type of conferences
            querysql = """SELECT a.rid, a.vcb_id, a.room_id, b.start_date, b.duration
                          FROM conf_room AS a LEFT JOIN {} AS b ON b.rid = a.rid
                          WHERE a.type = '{}'""".format(table_type, self._type)
            row = session.execute(text(querysql)).fetchall()
            result = [dict(item) for item in row]
            if result:  # obtaining maximum storage time from ethalon table
                querysql = "SELECT value FROM confmisc WHERE attribute = 'maxstoretime'"
                row = session.execute(text(querysql)).fetchall()
                result = [dict(item) for item in row]
                b = int(result[1][0]['value'])
                maxstoretime = timedelta(days=b)
                for d in result[1]:
                    d['duration'] = int(d['duration'])
                    d['end_date'] = (d['start_date'] + timedelta(minutes=d['duration'])) + maxstoretime
                    if d['end_date'] < stamptime:
                        resconflist.append(d)  # forming result list
        elif table_type == 'type_persistent' or 'type_recurring':
            querysql = """SELECT a.rid, a.vcb_id, a.room_id, b.end_date
                          FROM conf_room AS a LEFT JOIN {} AS b ON b.rid = a.rid
                          WHERE a.type = '{}'""".format(table_type, self._type)
            row = session.execute(text(querysql)).fetchall()
            rqw = [dict(item) for item in row]
            if rqw[1]:  # obtining maximum storage time from ethalone table
                querysql = "SELECT value FROM confmisc WHERE attribute = 'maxstoretime'"
                row = session.execute(text(querysql)).fetchall()
                result = [dict(item) for item in row]
                b = int(result[1][0]['value'])
                maxstoretime = timedelta(days=b)
                for d in rqw[1]:  # add maximum storage time
                    d['end_date'] = (d['end_date'] + maxstoretime)
                    if d['end_date'] < stamptime:  # Comparing with current timestamp
                        resconflist.append(d)  # forming result list
        else:
            errmsg = "Couldn't obtain data for this conference type - '{}'".format(self._type)
            logging.error(errmsg)
            # return {"result": False, "reason": "Couldn't obtain data for this conference type - '{}''".format(
            #    self._type)}, 400

        # CLEANER part
        flist = []  # temporary files lists
        masklist = []  # file mask list
        filelist = []  # file for deletion list
        ploadlist = []  # payload list

        # Preparation for deletion of records from DB
        infmsg = "Preparation for deletion of the conf room info from DB"
        logging.info(infmsg)
        for d in resconflist:
            mask = '{}_*.*'.format(d['room_id'])
            pl = {'vcb_id': d['vcb_id'], 'room_id': d['room_id'], 'type': self._type, 'rid': d['rid']}
            masklist.append(mask)
            ploadlist.append(pl)

        headers = {'content-type': 'application/json'}  # Necessary for sending JSON body
        # removing records from DB via API
        for i in ploadlist:
            # url = "http://100.127.2.12:8191/ncb/deleteConfRoom/{}".format(i['rid'])
            url = "http://100.127.2.12:8191/ncb/deleteConfRoom"
            payload = i
            response = requests.delete(url, data=json.dumps(payload), headers=headers)
            fpath = '{}/{}/{}'.format(m_path, i['vcb_id'], 'records')  # forming path for further removing of files
            flist.append(fpath)
            logging.info(response)

        # removing appropriate record files
        logging.info("Removing appropriate record files for conf room")
        pathlist = list(set(flist))  # result pathlist with removed duplicate values
        try:
            for path in pathlist:
                os.chdir(path)
                for mask in masklist:
                    l = glob.glob(mask)
                    filelist.extend(l)  # list with files found by mask
        except IOError:
            logging.error("Files not found in the directory: Check path existance!")
        try:
            for path in pathlist:
                os.chdir(path)
                for file in filelist:
                    os.unlink(file)
        except IOError:
            logging.error("Files not found in the directory!")
