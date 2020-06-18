
def init_db(db,User):
    from .models.user import User,Roles,user_roles
    db.drop_all()
    db.create_all()
    cust = Roles(role='customer')
    admin =Roles(role='admin')
    role1 = Roles(role='role1')
    tom = User(name='tom',email='tom@your-tom.com',active=True,source='local')
    tom.set_password('')
    db.session.add(admin)
    tom.roles.append(admin)
    db.session.add(cust)
    db.session.add(tom)
    db.session.commit()       

def update_db(db,User):
    from .models.user import User,Roles,user_roles

    cust = Roles.query.filter_by(role='customer').first()
    admin =Roles.query.filter_by(role='admin').first()
    role1 = Roles(role='role1')
    db.session.add(role1)
    tom = User.query.get(1)
    tom.roles.clear()
    tom.roles.append(cust)
    #db.session.add(cust)
    #db.session.add(tom)
    db.session.commit()       
