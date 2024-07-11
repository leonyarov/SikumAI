from sqlalchemy.orm import sessionmaker

from database import Prompt, db
from sqlalchemy import create_engine

def save_prompt(prompt, result):
    p = Prompt(prompt=prompt, response=result)
    try:
        db.session.add(p)
        db.session.commit()
    except:
        engine = create_engine('sqlite:///instance/database.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(p)
        session.commit()



def get_prompt(prompt):
    try:
        p = Prompt.query.filter_by(prompt=prompt).first()
    except:
        engine = create_engine('sqlite:///instance/database.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        p = session.query(Prompt).filter_by(prompt=prompt).first()
    return p
