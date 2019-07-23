import os
import logging
from sqlalchemy import *
from sqlalchemy.orm import *
from config.def_config import *

logger = logging.getLogger(__name__)

conn = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'], echo=True)
Session = sessionmaker(bind=conn)
session = Session()


# class NCBdb(LocalConfig):
class NCBdb(LocalConfig):

    def ncb_getQuery(self, sqlquery):
        try:
            row = self.session.execute(text(sqlquery)).fetchall()
            result = [dict(item) for item in row]
            return True, result
        except exc.ProgrammingError as er:
            logger.critical('ERROR: ProgrammingError in Conference DB. Call to support immediately - %s' % (er))
            return False, er
        except exc.InternalError as er:
            logger.critical('ERROR: InternalError in Conference DB. Call to support immediately - %s' % (er))
            return False, er
        except exc.SQLAlchemyError as er:
            logger.critical('ERROR: Can not get a data from Conference DB. Call to support immediately - %s' % (er))
            return False, er

        # if more than one rows are retrieved - it gets first row from the list as a dictionary
    def listdicttodict(self, listdict):

        return listdict[1][0] if listdict[1][0] else []

