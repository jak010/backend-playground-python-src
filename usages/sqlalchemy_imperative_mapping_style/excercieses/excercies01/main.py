from usages.sqlalchemy_imperative_mapping_style.config.sa_models import Member
from usages.sqlalchemy_imperative_mapping_style.config.start_mappers import start_mapper

from usages.sqlalchemy_imperative_mapping_style.config.client import get_session

def get_member():

    s = get_session()
    print(s.query(Member).all())
    s.commit()
    s.close()



if __name__ == '__main__':
    start_mapper()

    get_member()