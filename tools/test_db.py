import sys
sys.path.append('/home/vagrant/personal/new_simi')

from sqlalchemy import create_engine
from core.models.subjects import *
from core.models.base import install_model

engine = create_engine('mysql://root:@localhost/simi', convert_unicode=True, echo=True)
install_model(engine)
