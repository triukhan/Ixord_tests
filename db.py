# from sqlalchemy.orm import sessionmaker
#
# from sqlalchemy import create_engine
#
# from sqlalchemy.ext.declarative import declarative_base
#
# from configuration import CONNECTION
#
#
# Model = declarative_base(name='Model')
#
# engine = create_engine(
#    CONNECTION
# )
#
# Session = sessionmaker(
#     engine,
#     autoflush=False,
#     autocommit=False
# )
#
# session = Session()