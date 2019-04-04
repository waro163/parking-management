import os
from app import create_app,db
from app.models import User,Role,Order,ParkingS
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
#manager.add_command('shell',Shell(make_context=make_shell_context()))
#manager.add_command('db',MigrateCommand)

# with app.app_context() as app_context:
#     app_context.push()
#     db.create_all()
# app.run(host='0.0.0.0', port=8081)

if __name__ == '__main__':
    # manager.run()
    app = create_app('default')
    with app.app_context() as app_context:
        app_context.push()
        db.create_all()
        Role.insert_roles()
    app.run(host='0.0.0.0', port=8081)