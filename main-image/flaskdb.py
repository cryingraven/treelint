from app import manager,db
import config
import controller
import model
if __name__ == '__main__':
    db.create_all()
    manager.run()