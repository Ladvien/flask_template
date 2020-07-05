import os
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dateutil import parser

###########
# DB info
###########

db_address = "localhost"

engine = create_engine(
    os.environ["DATABASE_URL"],
    convert_unicode=True,
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    
    # ADD MODELS HERE. E.g., "from models import CustomerModel"

    Base.metadata.create_all(bind=engine)

def sql_format_date(date):
    try:
        return parser.parse(date).strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass

# Force datatype
def sanitize(variable, type):
    if type == str:
        variable = str(variable)
        variable = prep_text_for_sql(variable)
    elif type == int:
        variable = int(variable)
    elif type == float:
        variable = float(variable)

    return variable


# Remove troublesome SQL characters.
def prep_text_for_sql(text):
    return text.encode("ascii", errors="ignore").decode().replace("→", "->")
