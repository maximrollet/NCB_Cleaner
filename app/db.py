import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc, text
from config.config import config_by_name

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])

session = scoped_session(sessionmaker(bind=engine))

logger = logging.getLogger(__name__)


class NCBdb():

    def ncb_getQuery(self, querySQL):
        try:
            row = self.session.execute(text(querySQL)).fetchall()
            result = [dict(item) for item in row]
            return True, result
        except exc.ProgrammingError as er:
            logger.critical('ERROR: ProgrammingError in Conference DB. Call to support immediately - %s' % (er))
            return False, er
        except exc.InternalError as er:
            logger.critical('ERROR: InternallError in Conference DB. Call to support immediately - %s' % (er))
            return False, er
        except exc.SQLAlchemyError as er:
            logger.critical('ERROR: Can not get a data from Conference DB. Call to support immediately - %s' % (er))
            return False, er

        # if more than one rows are retrieved - it gets first row from the list as a dictionary
    def listdicttodict(self, listdict):

        return listdict[1][0] if listdict[1][0] else []

    # def getGlobalMediaPath(self):
    #    if not os.path.exists(self.conferenceMediaStoragePath):  # check it out whether it exist
    #        return None  # if it doesn't - return None
    #    else:
    #       return self.conferenceMediaStoragePath  # otherwise return the path
