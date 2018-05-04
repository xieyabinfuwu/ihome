# -*- coding: utf-8 -*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from ihome_main import create_app, db
from ihome_main.models import * # User, Area, House, Facility, HouseImage, Order, house_facility

app=create_app("development")
migrate=Migrate(app,db)
manager = Manager(app)

def make_shell_context():
    return dict(app=app,db=db,User=User,Area=Area,House=House,Facility=Facility,
                HouseImage=HouseImage,Order=Order,house_facility=house_facility)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manager.run()