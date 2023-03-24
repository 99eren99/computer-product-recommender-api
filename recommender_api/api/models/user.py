from api.utils.database import db
from api.utils.serializer_deserializer import ma


class User(db.Model):
    __tablename__="USERS"

    user_name=db.Column("User Name",db.String,primary_key=True)
    password=db.Column("Password",db.String ,nullable=False)
    email=db.Column("Email",db.String ,nullable=False)
    verification_status=db.Column("Email Verificated",db.Bool ,nullable=False)

    def __init__(self,user_name,password,email,verification_status):
        self.id=id
        self.user_name =user_name
        self.password =password
        self.email =email
        self.verification_status=verification_status

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=User