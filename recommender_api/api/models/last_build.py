from api.utils.database import db
from api.utils.serializer_deserializer import ma


class LastBuild(db.Model):
    __tablename__="LastBuild"

    build_number=db.Column("BuildNumber",db.String,primary_key=True)

    def __init__(self,build_number=None):
        self.build_number=build_number

class LastBuildSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=LastBuild