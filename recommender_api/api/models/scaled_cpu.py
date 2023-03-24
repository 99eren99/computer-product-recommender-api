from api.utils.database import db
from api.utils.serializer_deserializer import ma

class ScaledCPU(db.Model):
    __tablename__="CPUS"

    id=db.Column("index",db.Integer,primary_key=True,autoincrement=True)
    arttirilmis_frekans=db.Column("Arttırılmış Frekans(GHz)",db.Float,nullable=True)
    cekirdek_sayisi=db.Column("Çekirdek",db.Float,nullable=True)
    temel_frekans=db.Column("Temel Frekans(GHz)",db.Float,nullable=True)
    medyan_fiyat=db.Column("Medyan Fiyat",db.Float ,nullable=True)
    islemci_skoru=db.Column("İşlemci Skoru",db.Float ,nullable=True)

    def __init__(self,arttirilmis_frekans,cekirdek_sayisi,temel_frekans,medyan_fiyat,islemci_skoru,id=None):
        self.id=id
        self.arttirilmis_frekans =arttirilmis_frekans
        self.cekirdek_sayisi =cekirdek_sayisi
        self.temel_frekans =temel_frekans
        self.medyan_fiyat =medyan_fiyat
        self.islemci_skoru =islemci_skoru
    
class ScaledCPUSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ScaledCPU