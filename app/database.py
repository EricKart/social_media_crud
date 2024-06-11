from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import time



SQLAlCHEMY_DATABASE_URL = 'postgresql://postgres:102030@localhost/fastapi'
engine = create_engine(SQLAlCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
        ##############-------------DataBase Connection--------------------------------
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="102030",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print(
#             "##########_-------------------##########---------Database connection is successful!------------------################"
#         )
#         break
#     except Exception as error:
#         print(
#             "######################------------------########Connection to Database failed!-----------------"
#         )
#         print("Errors: ", error)
#         time.sleep(3)
#     finally:
#         print("Attempt to connect has completed.")