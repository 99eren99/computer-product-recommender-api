from api.utils.database import db
from api.utils.serializer_deserializer import ma

class ScaledGPU(db.Model):
    __tablename__="CPUS"

    id=db.Column("index",db.Integer,primary_key=True,autoincrement=True)
    bellek_boyutu=db.Column("Bellek Boyutu(GB)",db.Float, nullable=True)
    medyan_fiyat=db.Column("Medyan Fiyat",db.Float ,nullable=True)
    ekran_karti_skoru=db.Column("Ekran Kartı Skoru",db.Float ,nullable=True)

    def __init__(self,bellek_boyutu,medyan_fiyat,ekran_karti_skoru,id=None):
        self.id=id
        self.bellek_boyutu =bellek_boyutu
        self.medyan_fiyat =medyan_fiyat
        self.ekran_karti_skoru =ekran_karti_skoru
    
class ScaledGPUSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ScaledGPU