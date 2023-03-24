from api.utils.database import db
from api.utils.serializer_deserializer import ma

class GPU(db.Model):
    __tablename__="CPUS"

    id=db.Column("index",db.Integer,primary_key=True,autoincrement=True)
    bellek_boyutu=db.Column("Bellek Boyutu(GB)",db.Float, nullable=True)
    uretici=db.Column("İşlemci Üreticisi",db.String,nullable=True)
    ekran_karti_modeli=db.Column("Ekran Kartı Modeli",db.String,nullable=True)
    uri=db.Column("uri",db.String ,nullable=True)
    urun_adi=db.Column("Ürün Adı",db.String ,nullable=True)
    en_dusuk_fiyat=db.Column("En Düşük Fiyat",db.Float ,nullable=True)
    medyan_fiyat=db.Column("Medyan Fiyat",db.Float ,nullable=True)
    ekran_karti_skoru=db.Column("Ekran Kartı Skoru",db.Float ,nullable=True)
    cluster_label=db.Column("Cluster Label",db.Integer ,nullable=True)
    cosine_similar=db.Column("Cosine Similar",db.Integer ,nullable=True)
    first_nn=db.Column("1.NearestNeighbor",db.Integer ,nullable=True)
    second_nn=db.Column("2.NearestNeighbor",db.Integer ,nullable=True)

    def __init__(self,bellek_boyutu,uretici,ekran_karti_modeli,uri,urun_adi,en_dusuk_fiyat,medyan_fiyat,ekran_karti_skoru
        ,cluster_label,cosine_similar,first_nn,second_nn,id=None):
        self.id=id
        self.bellek_boyutu =bellek_boyutu
        self.uretici =uretici
        self.ekran_karti_modeli =ekran_karti_modeli
        self.uri =uri
        self.urun_adi =urun_adi
        self.en_dusuk_fiyat =en_dusuk_fiyat
        self.medyan_fiyat =medyan_fiyat
        self.ekran_karti_skoru =ekran_karti_skoru
        self.cluster_label =cluster_label
        self.cosine_similar =cosine_similar
        self.first_nn =first_nn
        self.second_nn =second_nn
    
class GPUSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=GPU