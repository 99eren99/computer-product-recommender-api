from api.utils.database import db
from api.utils.serializer_deserializer import ma

class CPU(db.Model):
    __tablename__="CPUS"

    id=db.Column("index",db.Integer,primary_key=True,autoincrement=True)
    islemci=db.Column("İşlemci",db.String, nullable=True)
    islemci_serisi=db.Column("İşlemci Serisi",db.String,nullable=True)
    islemci_modeli=db.Column("İşlemci Modeli",db.String,nullable=True)
    jenerasyon=db.Column("Jenerasyon",db.String,nullable=True)
    arttirilmis_frekans=db.Column("Arttırılmış Frekans(GHz)",db.Float,nullable=True)
    cekirdek_sayisi=db.Column("Çekirdek",db.Float,nullable=True)
    temel_frekans=db.Column("Temel Frekans(GHz)",db.Float,nullable=True)
    uri=db.Column("uri",db.String ,nullable=True)
    urun_adi=db.Column("Ürün Adı",db.String ,nullable=True)
    en_dusuk_fiyat=db.Column("En Düşük Fiyat",db.Float ,nullable=True)
    medyan_fiyat=db.Column("Medyan Fiyat",db.Float ,nullable=True)
    islemci_skoru=db.Column("İşlemci Skoru",db.Float ,nullable=True)
    cluster_label=db.Column("Cluster Label",db.Integer ,nullable=True)
    cosine_similar=db.Column("Cosine Similar",db.Integer ,nullable=True)
    first_nn=db.Column("1.NearestNeighbor",db.Integer ,nullable=True)
    second_nn=db.Column("2.NearestNeighbor",db.Integer ,nullable=True)

    def __init__(self,islemci,islemci_serisi,islemci_modeli,jenerasyon,arttirilmis_frekans,cekirdek_sayisi,temel_frekans,
        uri,urun_adi,en_dusuk_fiyat,medyan_fiyat,islemci_skoru,cluster_label,cosine_similar,first_nn,second_nn,id=None):
        self.id=id
        self.islemci =islemci
        self.islemci_serisi =islemci_serisi
        self.islemci_modeli =islemci_modeli
        self.jenerasyon =jenerasyon
        self.arttirilmis_frekans =arttirilmis_frekans
        self.cekirdek_sayisi =cekirdek_sayisi
        self.temel_frekans =temel_frekans
        self.uri =uri
        self.urun_adi =urun_adi
        self.en_dusuk_fiyat =en_dusuk_fiyat
        self.medyan_fiyat =medyan_fiyat
        self.islemci_skoru =islemci_skoru
        self.cluster_label =cluster_label
        self.cosine_similar =cosine_similar
        self.first_nn =first_nn
        self.second_nn =second_nn
    
class CPUSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=CPU