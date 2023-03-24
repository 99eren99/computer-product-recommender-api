from api.utils.database import db
from api.utils.serializer_deserializer import ma


class ScaledNotebook(db.Model):
    __tablename__="ScaledNOTEBOOKS"

    id=db.Column("index",db.Integer,primary_key=True,autoincrement=True)
    ekran_boyutu=db.Column("Ekran Boyutu(inç)",db.Float, nullable=True)
    agirlik=db.Column("Ağırlık(kg)",db.Float,nullable=True)
    ram_boyutu=db.Column("Ram(Bellek) Boyutu(GB)",db.Float,nullable=True)
    islemci_arttirilmis_frekans=db.Column("İşlemci Arttırılmış Frekans(GHz)",db.Float,nullable=True)
    islemci_cekirdek_sayisi=db.Column("İşlemci Çekirdek Sayısı",db.Float,nullable=True)
    islemci_temel_frekans=db.Column("İşlemci Temel Frekans(GHz)",db.Float,nullable=True)
    islemci_onbellegi=db.Column("İşlemci Önbelleği(MB)",db.Float,nullable=True)
    medyan_fiyat=db.Column("Medyan Fiyat",db.Float ,nullable=True)
    ram_frekansi=db.Column("Ram(Bellek) Frekansı(MHz)",db.Float ,nullable=True)
    ekran_karti_bellegi=db.Column("Harici Ekran Kartı Belleği(GB)",db.Float ,nullable=True)
    islemci_skoru=db.Column("İşlemci Skoru",db.Float ,nullable=True)
    ekran_karti_skoru=db.Column("Ekran Kartı Skoru",db.Float ,nullable=True)

    def __init__(self,ekran_boyutu,agirlik,ram_boyutu,islemci_arttirilmis_frekans,islemci_cekirdek_sayisi,islemci_temel_frekans,
        islemci_onbellegi,medyan_fiyat,ram_frekansi,ekran_karti_bellegi,islemci_skoru,ekran_karti_skoru,id=None):
        self.id=id
        self.ekran_boyutu =ekran_boyutu
        self.agirlik =agirlik
        self.ram_boyutu =ram_boyutu
        self.islemci_arttirilmis_frekans =islemci_arttirilmis_frekans
        self.islemci_cekirdek_sayisi =islemci_cekirdek_sayisi
        self.islemci_temel_frekans =islemci_temel_frekans
        self.islemci_onbellegi =islemci_onbellegi
        self.medyan_fiyat =medyan_fiyat
        self.ram_frekansi =ram_frekansi
        self.ekran_karti_bellegi =ekran_karti_bellegi
        self.islemci_skoru =islemci_skoru
        self.ekran_karti_skoru =ekran_karti_skoru

class ScaledNotebookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScaledNotebook
