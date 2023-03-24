from api.utils.database import db
from api.utils.serializer_deserializer import ma


class Notebook(db.Model):
    __tablename__="NOTEBOOKS"

    id=db.Column("index",db.Integer,primary_key=True,autoincrement=True)
    ekran_boyutu=db.Column("Ekran Boyutu(inç)",db.Float, nullable=True)
    isletim_sistemi=db.Column("İşletim Sistemi",db.String,nullable=True)
    ekran_cozunurlugu=db.Column("Ekran Çözünürlüğü",db.String,nullable=True)
    ekran_panel_tipi=db.Column("Ekran Panel Tipi",db.String,nullable=True)
    ekran_cozunurluk_bicimi=db.Column("Ekran Çözünürlük Biçimi",db.String,nullable=True)
    agirlik=db.Column("Ağırlık(kg)",db.Float,nullable=True)
    ram_boyutu=db.Column("Ram(Bellek) Boyutu(GB)",db.Float,nullable=True)
    islemci_modeli=db.Column("İşlemci Modeli",db.String,nullable=True)
    islemci_arttirilmis_frekans=db.Column("İşlemci Arttırılmış Frekans(GHz)",db.Float,nullable=True)
    islemci_cekirdek_sayisi=db.Column("İşlemci Çekirdek Sayısı",db.Float,nullable=True)
    islemci_markasi=db.Column("İşlemci Markası",db.String,nullable=True)
    islemci_temel_frekans=db.Column("İşlemci Temel Frekans(GHz)",db.Float,nullable=True)
    islemci_onbellegi=db.Column("İşlemci Önbelleği(MB)",db.Float,nullable=True)
    ram_turu=db.Column("Ram(Bellek) Türü",db.String,nullable=True)
    ssd_boyutu=db.Column("SSD Boyutu",db.String,nullable=True)
    uri=db.Column("uri",db.String,nullable=True)
    urun_adi=db.Column("Ürün Adı",db.String,nullable=True)
    en_dusuk_fiyat=db.Column("En Düşük Fiyat",db.Float,nullable=True)
    medyan_fiyat=db.Column("Medyan Fiyat",db.Float ,nullable=True)
    ram_frekansi=db.Column("Ram(Bellek) Frekansı(MHz)",db.Float ,nullable=True)
    hdd_boyutu=db.Column("Sabit Disk(HDD) Boyutu",db.String ,nullable=True)
    ekran_karti_bellegi=db.Column("Harici Ekran Kartı Belleği(GB)",db.Float ,nullable=True)
    ekran_karti_modeli=db.Column("Harici Ekran Kartı Modeli",db.String ,nullable=True)
    islemci_skoru=db.Column("İşlemci Skoru",db.Float ,nullable=True)
    ekran_karti_skoru=db.Column("Ekran Kartı Skoru",db.Float ,nullable=True)
    cluster_label=db.Column("Cluster Label",db.Integer ,nullable=True)
    cosine_similar=db.Column("Cosine Similar",db.Integer ,nullable=True)
    first_nn=db.Column("1.NearestNeighbor",db.Integer ,nullable=True)
    second_nn=db.Column("2.NearestNeighbor",db.Integer ,nullable=True)

    def __init__(self,ekran_boyutu,isletim_sistemi,ekran_cozunurlugu,ekran_panel_tipi,ekran_cozunurluk_bicimi,agirlik,ram_boyutu,
        islemci_modeli,islemci_arttirilmis_frekans,islemci_cekirdek_sayisi,islemci_markasi,islemci_temel_frekans,islemci_onbellegi,
        ram_turu,ssd_boyutu,uri,urun_adi,en_dusuk_fiyat,medyan_fiyat,ram_frekansi,hdd_boyutu,ekran_karti_bellegi,ekran_karti_modeli,
        islemci_skoru,ekran_karti_skoru,cluster_label,cosine_similar,first_nn,second_nn,id=None):
        self.id=id
        self.ekran_boyutu =ekran_boyutu
        self.isletim_sistemi =isletim_sistemi
        self.ekran_cozunurlugu =ekran_cozunurlugu
        self.ekran_panel_tipi =ekran_panel_tipi
        self.ekran_cozunurluk_bicimi =ekran_cozunurluk_bicimi
        self.agirlik =agirlik
        self.ram_boyutu =ram_boyutu
        self.islemci_modeli =islemci_modeli
        self.islemci_arttirilmis_frekans =islemci_arttirilmis_frekans
        self.islemci_cekirdek_sayisi =islemci_cekirdek_sayisi
        self.islemci_markasi =islemci_markasi
        self.islemci_temel_frekans =islemci_temel_frekans
        self.islemci_onbellegi =islemci_onbellegi
        self.ram_turu =ram_turu
        self.ssd_boyutu =ssd_boyutu
        self.uri =uri
        self.urun_adi =urun_adi
        self.en_dusuk_fiyat =en_dusuk_fiyat
        self.medyan_fiyat =medyan_fiyat
        self.ram_frekansi =ram_frekansi
        self.hdd_boyutu =hdd_boyutu
        self.ekran_karti_bellegi =ekran_karti_bellegi
        self.ekran_karti_modeli =ekran_karti_modeli
        self.islemci_skoru =islemci_skoru
        self.ekran_karti_skoru =ekran_karti_skoru
        self.cluster_label =cluster_label
        self.cosine_similar =cosine_similar
        self.first_nn =first_nn
        self.second_nn =second_nn

class NotebookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notebook
