import os
from sqlalchemy import create_engine, text, Column, Integer, String, ForeignKey, DECIMAL, Date, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Load the MySQL root password from environment variables
mysql_root_password = os.getenv('MYSQL_H4O_PASSWORD', 'default_root_pass')  # Fallback in case the env variable isn't set
# You can set it up by doing: export MYSQL_ROOT_PASSWORD=your_secure_password

config = {
    'host': 'localhost',
    'database_name': 'h4o',
    'user': 'root',
    'password': mysql_root_password
    }

engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}', echo=True)
#engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}', echo=True)

with engine.connect() as connection:
    connection.execute(text("CREATE DATABASE IF NOT EXISTS h4o"))
engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}', echo=True)

Base = declarative_base()

class Plant(Base):
    __tablename__ = 'Plant'
    id = Column(Integer, primary_key=True)
    nombre_comun = Column(String(50))
    nombre_cientifico = Column(String(100), nullable=False)
    reino = Column(String(50))
    division = Column(String(50))
    clase = Column(String(50))
    subclase = Column(String(50))
    orden = Column(String(50))
    familia = Column(String(50))
    subfamilia = Column(String(50))
    tribu = Column(String(50))
    subtribu = Column(String(50))
    genero = Column(String(50))
    especie = Column(String(50))

    descriptions = relationship('Description', back_populates='plants', uselist=False)
    cares = relationship('PlantCare', back_populates='plants')
    plant_diseases = relationship('Enfermedades', back_populates='plants')


class PlantType(Base):
    __tablename__ = 'PlantType'
    id = Column(Integer, primary_key=True)
    nombre_tipo = Column(String(100), nullable=False)
    descripcion = Column(Text)

    descriptions = relationship('Description', back_populates='types')


class PlantDescription(Base):
    __tablename__ = 'PlantDescription'
    id = Column(Integer, primary_key=True)
    planta_id = Column(Integer, ForeignKey('planta.id', ondelete='CASCADE'))
    origen_nativo = Column(String(255))
    descripcion = Column(Text)
    comestible = Column(Boolean)
    tipo_id = Column(Integer, ForeignKey('tipo.id', ondelete='SET NULL'))

    plants = relationship('Plant', back_populates='descriptions')
    types = relationship('Type', back_populates='descriptions')


class PlantCare(Base):
    __tablename__ = 'PlantCare'
    id = Column(Integer, primary_key=True)
    planta_id = Column(Integer, ForeignKey('planta.id', ondelete='CASCADE'))
    temperatura_ideal = Column(String(20))
    luz = Column(String(50))
    humedad = Column(String(20))
    riego = Column(String(255))
    sustrato = Column(String(255))
    abonado = Column(Text)
    tiempo_crecimiento = Column(String(50))
    tipo_tierra = Column(String(255))
    plantacion = Column(String(50))
    repicado = Column(String(50))
    transplante = Column(String(50))
    rusticidad = Column(String(255))
    estacion_siembra = Column(String(50))
    estacion_recoleccion = Column(String(50))

    plants = relationship('Plant', back_populates='cares')


class PlantDisease(Base):
    __tablename__ = 'PlantDisease'
    id = Column(Integer, primary_key=True)
    planta_id = Column(Integer, ForeignKey('planta.id', ondelete='CASCADE'))
    nombre = Column(String(100))
    descripcion = Column(Text)
    sintomas = Column(Text)
    tratamiento = Column(Text)
    prevencion = Column(Text)

    plants = relationship('Plant', back_populates='plant_diseases')

Base.metadata.create_all(engine)


# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Insert data into Plant table
plant_data = [
    {'id': 1, 'nombre_cientifico': 'Pteris berteroana', 'nombre_comun': 'Helecho Pteris', 'reino': 'Plantae', 
     'division': 'Polypodiophyta', 'clase': 'Polypodiopsida', 'orden': 'Polypodiales', 'familia': 'Pteridaceae'},
    {'id': 2, 'nombre_cientifico': 'Allium cepa var. aggregatum', 'nombre_comun': 'Cebolla babosa', 'reino': 'Plantae', 
     'division': 'Angiospermae', 'clase': 'Liliopsida', 'orden': 'Asparagales', 'familia': 'Amaryllidaceae'},
    {'id': 3, 'nombre_cientifico': 'Solanum lycopersicum', 'nombre_comun': 'Tomate', 'reino': 'Plantae', 
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Solanales', 'familia': 'Solanaceae'},
    {'id': 4, 'nombre_cientifico': 'Daucus carota', 'nombre_comun': 'Zanahoria', 'reino': 'Plantae', 
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Apiales', 'familia': 'Apiaceae'},
    {'id': 5, 'nombre_cientifico': 'Brassica olera var. capitata', 'nombre_comun': 'Repollo', 'reino': 'Plantae', 
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Brassicales', 'familia': 'Brassicaceae'},
    {'id': 6, 'nombre_cientifico': 'Sisyrinchium Striatum', 'nombre_comun': 'Huilmo', 'reino': 'Plantae', 
     'division': 'Tracheophyta', 'clase': 'Liliopsida', 'orden': 'Asparagales', 'familia': 'Iridaceae'},
    {'id': 7, 'nombre_cientifico': 'Beta vulgaris', 'nombre_comun': 'Betarraga', 'reino': 'Plantae', 
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Caryophyllales', 'familia': 'Amaranthaceae'},
    {'id': 8, 'nombre_cientifico': 'Cucumis sativus', 'nombre_comun': 'Pepino', 'reino': 'Plantae', 
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Violales', 'familia': 'Cucurbitaceae'},
    {'id': 9, 'nombre_cientifico': 'Zea mays', 'nombre_comun': 'Choclo', 'reino': 'Plantae', 
     'division': 'Magnoliophyta', 'clase': 'Angiosperma', 'orden': 'Poales', 'familia': 'Poaceae'},
    {'id': 10, 'nombre_cientifico': 'Allium sativum', 'nombre_comun': 'Ajo', 'reino': 'Plantae', 
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Asparagales', 'familia': 'Amaryllidaceae'},
    {'id': 11, 'nombre_cientifico': 'Allium ampeloprasum', 'nombre_comun': 'Cebollín (puerro)', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Liliales', 'familia': 'Amaryllidaceae'},
    {'id': 12, 'nombre_cientifico': 'Citrullus lanatus', 'nombre_comun': 'Sandía', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Violales', 'familia': 'Cucurbitaceae'},
    {'id': 13, 'nombre_cientifico': 'Aloe barbadensis (Miller)', 'nombre_comun': 'Aloe vera', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Liliales', 'familia': 'Liliaceae'},
    {'id': 14, 'nombre_cientifico': 'Tulipa', 'nombre_comun': 'Tulipán', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Liliales', 'familia': 'Liliaceae'},
    {'id': 15, 'nombre_cientifico': 'Capsicum annuum', 'nombre_comun': 'Ají', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Solanales', 'familia': 'Solanaceae'},
    {'id': 16, 'nombre_cientifico': 'Prunus persica', 'nombre_comun': 'Durazno', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Rosales', 'familia': 'Rosaceae'},
    {'id': 17, 'nombre_cientifico': 'Pimpinella anisum', 'nombre_comun': 'Anís', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Apiales', 'familia': 'Apiaceae'},
    {'id': 18, 'nombre_cientifico': 'Peumus boldus', 'nombre_comun': 'Boldo', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Laurales', 'familia': 'Monimiaceae'},
    {'id': 19, 'nombre_cientifico': 'Lapageria rosea', 'nombre_comun': 'Copihue', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Liliales', 'familia': 'Philesiaceae'},
    {'id': 20, 'nombre_cientifico': 'Echeveria secunda', 'nombre_comun': 'Conchita', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Saxifragales', 'familia': 'Crassulaceae'},
    {'id': 21, 'nombre_cientifico': 'Aloe vera', 'nombre_comun': 'Aloe vera', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Asparagales', 'familia': 'Asphodelaceae'},
    {'id': 22, 'nombre_cientifico': 'Lophophora williamsii', 'nombre_comun': 'Peyote', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Caryophyllales', 'familia': 'Cactaceae'},
    {'id': 23, 'nombre_cientifico': 'Myosotis', 'nombre_comun': 'Nomeolvides', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Lamiales', 'familia': 'Boraginaceae'},
    {'id': 24, 'nombre_cientifico': 'Rosa eglanteria', 'nombre_comun': 'Rosa mosqueta', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Rosales', 'familia': 'Rosaceae'},
    {'id': 25, 'nombre_cientifico': 'Rhododendron', 'nombre_comun': 'Rododendro', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Ericales', 'familia': 'Ericaceae'},
    {'id': 26, 'nombre_cientifico': 'Aristotelia chilensis', 'nombre_comun': 'Maqui', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Oxalidales', 'familia': 'Elaeocarpaceae'},
    {'id': 27, 'nombre_cientifico': 'Geranium', 'nombre_comun': 'Geranio', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Geraniales', 'familia': 'Geraniaceae'},
    {'id': 28, 'nombre_cientifico': 'Persea americana', 'nombre_comun': 'Palto', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Laurales', 'familia': 'Lauraceae'},
    {'id': 29, 'nombre_cientifico': 'Pyrus communis', 'nombre_comun': 'Peral', 'reino': 'Plantae',
     'division': 'Tracheophyta', 'clase': 'Magnoliopsida', 'orden': 'Rosales', 'familia': 'Rosaceae'},
    {'id': 30, 'nombre_cientifico': 'Malus domestica', 'nombre_comun': 'Manzano', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Rosales', 'familia': 'Rosaceae'},
    {'id': 31, 'nombre_cientifico': 'Rubus idaeus', 'nombre_comun': 'Frambueso', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Rosales', 'familia': 'Rosaceae'},
    {'id': 32, 'nombre_cientifico': 'Vaccinium corymbosum', 'nombre_comun': 'Arándano (azul)', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Ericales', 'familia': 'Ericaceae'},
    {'id': 33, 'nombre_cientifico': 'Solanum tuberosum', 'nombre_comun': 'Papa', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Solanales', 'familia': 'Solanaceae'},
    {'id': 34, 'nombre_cientifico': 'Lactuca sativa', 'nombre_comun': 'Lechuga', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Asterales', 'familia': 'Asteraceae'},
    {'id': 35, 'nombre_cientifico': 'Asparagus officinalis', 'nombre_comun': 'Espárrago', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Asparagales', 'familia': 'Asparagaceae'},
    {'id': 36, 'nombre_cientifico': 'Cynara scolymus', 'nombre_comun': 'Alcachofa', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Asterales', 'familia': 'Asteraceae'},
    {'id': 37, 'nombre_cientifico': 'Bursera graveolens', 'nombre_comun': 'Palo Santo', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Sapindales', 'familia': 'Burseraceae'},
    {'id': 38, 'nombre_cientifico': 'Araucaria araucana', 'nombre_comun': 'Araucaria', 'reino': 'Plantae',
     'division': 'Pinophyta', 'clase': 'Pinopsida', 'orden': 'Araucariales', 'familia': 'Araucariaceae'},
    {'id': 39, 'nombre_cientifico': 'Luma apiculata', 'nombre_comun': 'Arrayán', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Myrtales', 'familia': 'Myrtaceae'},
    {'id': 40, 'nombre_cientifico': 'Fitzroya cupressoides', 'nombre_comun': 'Alerce', 'reino': 'Plantae',
     'division': 'Pinophyta', 'clase': 'Pinopsida', 'orden': 'Pinidae', 'familia': 'Cupressaceae'},
    {'id': 41, 'nombre_cientifico': 'Smilax aspera', 'nombre_comun': 'Zarzaparrilla', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Liliales', 'familia': 'Smilacaceae'},
    {'id': 42, 'nombre_cientifico': 'Berberis congestiflora', 'nombre_comun': 'Calafate', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Ranunculales', 'familia': 'Berberidaceae'},
    {'id': 43, 'nombre_cientifico': 'Gunnera tinctoria', 'nombre_comun': 'Nalca', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Gunnerales', 'familia': 'Gunneraceae'},
    {'id': 44, 'nombre_cientifico': 'Ugni molinae', 'nombre_comun': 'Murtilla', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Myrtales', 'familia': 'Myrtaceae'},
    {'id': 45, 'nombre_cientifico': 'Equisetum arvense', 'nombre_comun': 'Cola de caballo', 'reino': 'Plantae',
     'division': 'Sphenophyta', 'clase': 'Equisetopsida', 'orden': 'Equisetales', 'familia': 'Equisetaceae'},
    {'id': 46, 'nombre_cientifico': 'Cryptocarya alba', 'nombre_comun': 'Peumo', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Laurales', 'familia': 'Lauraceae'},
    {'id': 47, 'nombre_cientifico': 'Mentha', 'nombre_comun': 'Mento', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Lamiales', 'familia': 'Lamiaceae'},
    {'id': 48, 'nombre_cientifico': 'Salvia rosmarinus', 'nombre_comun': 'Romero', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Lamiales', 'familia': 'Lamiaceae'},
    {'id': 49, 'nombre_cientifico': 'Matricaria chamomilla', 'nombre_comun': 'Manzanilla', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Asterales', 'familia': 'Asteraceae'},
    {'id': 50, 'nombre_cientifico': 'Oreganum vulgare', 'nombre_comun': 'Orégano', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Lamiales', 'familia': 'Lamiaceae'},
    {'id': 51, 'nombre_cientifico': 'Vitis vinifera', 'nombre_comun': 'Parra', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Vitales', 'familia': 'Vitaceae'},
    {'id': 52, 'nombre_cientifico': 'Mandevilla laxa', 'nombre_comun': 'Jazmín chileno', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Gentianales', 'familia': 'Apocynaceae'},
    {'id': 53, 'nombre_cientifico': 'Lavandula angustifolia', 'nombre_comun': 'Lavanda', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Lamiales', 'familia': 'Lamiaceae'},
    {'id': 54, 'nombre_cientifico': 'Dianthus caryophyllus', 'nombre_comun': 'Clavel', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Caryophyllales', 'familia': 'Caryophyllaceae'},
    {'id': 55, 'nombre_cientifico': 'Pouteria lucuma', 'nombre_comun': 'Lúcumo', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Ericales', 'familia': 'Sapotaceae'},
    {'id': 56, 'nombre_cientifico': 'Hyacinthus', 'nombre_comun': 'Jacinto', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Asparagales', 'familia': 'Asparagaceae'},
    {'id': 57, 'nombre_cientifico': 'Haworthia', 'nombre_comun': 'Haworthia', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Asparagales', 'familia': 'Asphodelaceae'},
    {'id': 58, 'nombre_cientifico': 'Echinopsis pachanoi', 'nombre_comun': 'Cactus de San Pedro', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Caryophyllales', 'familia': 'Cactaceae'},
    {'id': 59, 'nombre_cientifico': 'Crassula ovata', 'nombre_comun': 'Oreja de Shrek', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Saxifragales', 'familia': 'Crassulaceae'},
    {'id': 60, 'nombre_cientifico': 'Senecio fistulosus', 'nombre_comun': 'Senecio chileno', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Asterales', 'familia': 'Asteraceae'},
    {'id': 61, 'nombre_cientifico': 'Curcuma longa', 'nombre_comun': 'Cúrcuma', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Liliopsida', 'orden': 'Zingiberales', 'familia': 'Zingiberaceae'},
    {'id': 62, 'nombre_cientifico': 'Cuminum cyminum', 'nombre_comun': 'Comino', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Magnoliopsida', 'orden': 'Apiales', 'familia': 'Apiaceae'},
    {'id': 63, 'nombre_cientifico': 'Moringa oleifera', 'nombre_comun': 'Moringa', 'reino': 'Plantae',
     'division': 'Magnoliophyta', 'clase': 'Eudicotyledoneae', 'orden': 'Brassicales', 'familia': 'Moringaceae'}
]

for data in plant_data:
    plant = Plant(**data)
    session.add(plant)
session.commit()

plant_type = [
    {'id': 1, 'habito': 'Arbol', 'descripcion': 'Planta perenne y leñosa que suele tener un tronco único, ramificado en su parte superior, y una altura considerable.'},
    {'id': 2, 'habito': 'Arbusto', 'descripcion': 'Planta leñosa de menor altura que un árbol, con múltiples tallos que emergen desde la base.'},
    {'id': 3, 'habito': 'Hierba', 'descripcion': 'Planta no leñosa con tallos tiernos y flexibles; suele tener ciclos de vida cortos.'},
    {'id': 4, 'habito': 'Liquen', 'descripcion': 'Asociación simbiótica entre un hongo y un alga o cianobacteria, que forma estructuras planas o ramificadas adheridas a superficies.'},
    {'id': 5, 'habito': 'Seta', 'descripcion': 'Estructura reproductiva de ciertos hongos, típicamente con forma de sombrero y pie; no realiza fotosíntesis.'},
    {'id': 6, 'habito': 'Suculenta', 'descripcion': 'Planta con tejidos engrosados capaces de almacenar agua, adaptada a climas áridos y secos.'},
    {'id': 7, 'habito': 'Tuberculo', 'descripcion': 'Órgano subterráneo engrosado que actúa como almacén de nutrientes, comúnmente utilizado como alimento (ej. papa, camote).'},
    {'id': 8, 'habito': 'Enredadera', 'descripcion': 'Planta que se extiende y escala soportes mediante tallos flexibles o zarcillos, adaptada para trepar o cubrir superficies.'},
    {'id': 9, 'habito': 'Epifita', 'descripcion': 'Planta que crece sobre otra planta (como un árbol) pero sin ser parásita; absorbe agua y nutrientes del aire y la lluvia.'},
    {'id': 10, 'habito': 'Acuatica', 'descripcion': 'Planta que crece en ambientes acuáticos, ya sea flotando, sumergida o en suelos húmedos.'},
    {'id': 11, 'habito': 'Palmera', 'descripcion': 'Planta de tipo monocotiledónea, de tronco delgado, sin ramificar, y hojas grandes en su parte superior.'},
    {'id': 12, 'habito': 'Helecho', 'descripcion': 'Planta sin flores ni semillas, que se reproduce mediante esporas; caracterizada por hojas pinnadas o divididas.'},
    {'id': 13, 'habito': 'Parasita', 'descripcion': 'Planta que obtiene sus nutrientes directamente de otras plantas, a las cuales perjudica.'},
    {'id': 14, 'habito': 'Carnivora', 'descripcion': 'Planta que obtiene nutrientes adicionales atrapando y descomponiendo insectos u otros organismos pequeños.'}
]

for data in plant_type:
    type = PlantType(**data)
    session.add(type)
session.commit()

plant_description_data = [
    {'id': 1, 'planta_id': 1, 'origen_nativo': 'Australia', 
     'descripcion': 'Hojas largas, verdes y divididas, que crecen en racimos desde una base central. Prefiere sombra, humedad y luz indirecta, ideal para interiores o jardines sombreados.', 
     'tipo_id': 12},
    {'id': 2, 'planta_id': 2, 'origen_nativo': 'Sudeste Asiático', 
     'descripcion': 'Hojas largas, verdes y cilíndricas que producen un jugo viscoso al cortarse. Su bulbo es pequeño y poco desarrollado, ya que se cultiva principalmente por sus hojas tiernas y comestibles.', 
     'tipo_id': 3},
    {'id': 3, 'planta_id': 3, 'origen_nativo': 'México', 
     'descripcion': 'Planta herbácea o arbustiva que produce frutos carnosos y generalmente rojos cuando maduran. Sus hojas son compuestas, de color verde intenso, y desprenden un aroma característico.', 
     'tipo_id': 3},
    {'id': 4, 'planta_id': 4, 'origen_nativo': 'Asia Central', 
     'descripcion': 'Planta de raíz comestible, alargada y generalmente anaranjada. Sus hojas son verdes, finamente divididas y crecen en forma de roseta.', 
     'tipo_id': 3},
    {'id': 5, 'planta_id': 5, 'origen_nativo': 'Europa', 
     'descripcion': 'Hojas lisas o ligeramente arrugadas que forman una cabeza compacta y redondeada. Sus colores varían entre verde, morado y blanco, según la variedad.', 
     'tipo_id': 3},
    {'id': 6, 'planta_id': 6, 'origen_nativo': 'Argentina y Chile', 
     'descripcion': 'Hojas largas, estrechas y de color verde grisáceo, similares a espadas. Produce tallos erectos con pequeñas flores de color crema o amarillo pálido, dispuestas en racimos.', 
     'tipo_id': 3},
    {'id': 7, 'planta_id': 7, 'origen_nativo': 'Norte de África', 
     'descripcion': 'Hojas grandes y verdes con nervaduras rojizas. Su raíz es carnosa, de color rojo intenso, aunque también existen variedades amarillas o blancas.', 
     'tipo_id': 3},
    {'id': 8, 'planta_id': 8, 'origen_nativo': 'Sudeste Asiático', 
     'descripcion': 'Planta trepadora o rastrera con hojas grandes y lobuladas. Produce frutos alargados y verdes, que tienen una piel suave y una pulpa crujiente y refrescante.', 
     'tipo_id': 8},
    {'id': 9, 'planta_id': 9, 'origen_nativo': 'México', 
     'descripcion': 'Planta de tallo alto y robusto, con hojas largas y lanceoladas. Produce grandes mazorcas que contienen granos amarillos, aunque también existen variedades de otros colores.', 
     'tipo_id': 3},
    {'id': 10, 'planta_id': 10, 'origen_nativo': 'Asia Central', 
     'descripcion': 'Planta bulbosa que forma racimos de dientes rodeados por una capa exterior papirácea. Tiene hojas largas, estrechas y de color verde.', 
     'tipo_id': 7},
    {'id': 11, 'planta_id': 11, 'origen_nativo': 'Europa y Asia Occidental', 
     'descripcion': 'Su bulbo es alargado y su base forma una parte blanca y carnosa. Se caracteriza por un aroma suave y un sabor ligeramente más suave que la cebolla.', 
     'tipo_id': 7},
    {'id': 12, 'planta_id': 12, 'origen_nativo': 'África', 
     'descripcion': 'Planta trepadora que produce frutos grandes, redondos u ovalados, con una cáscara verde y pulpa roja o rosa, con semillas negras. Tiene hojas grandes, profundamente lobuladas, y crece en climas cálidos.', 
     'tipo_id': 8},
    {'id': 13, 'planta_id': 13, 'origen_nativo': 'África', 
     'descripcion': 'Planta suculenta de hojas gruesas, alargadas y carnosas, con bordes dentados. Estas hojas contienen un gel transparente utilizado por sus propiedades medicinales y cosméticas.', 
     'tipo_id': 6},
    {'id': 14, 'planta_id': 14, 'origen_nativo': 'Asia Central', 
     'descripcion': 'Planta bulbosa que produce flores grandes y vistosas, con pétalos de forma ovalada que pueden ser de diversos colores, como rojo, amarillo, blanco, rosa o morado. Sus hojas son largas, estrechas y de color verde.', 
     'tipo_id': 7},
    {'id': 15, 'planta_id': 15, 'origen_nativo': 'México, Centroamérica y Norte de Sudamérica', 
     'descripcion': 'Planta que produce frutos conocidos como pimientos o chiles, los cuales pueden ser dulces o picantes, dependiendo de la variedad. Tiene hojas de color verde y flores pequeñas y blancas.', 
     'tipo_id': 3},
    {'id': 16, 'planta_id': 16, 'origen_nativo': 'China', 
     'descripcion': 'Árbol frutal de tamaño mediano que produce frutos jugosos y dulces, con una piel aterciopelada y carne firme o suave, dependiendo de la variedad. Tiene hojas lanceoladas y de color verde brillante.', 
     'tipo_id': 1},
    {'id': 17, 'planta_id': 17, 'origen_nativo': 'Región mediterránea oriental', 
     'descripcion': 'Planta herbácea anual que crece hasta aproximadamente un metro de altura. Tiene hojas finamente divididas y flores pequeñas de color blanco, agrupadas en umbelas. La planta produce frutos pequeños, llamados aquenios, que son utilizados por su característico sabor dulce y aromático.', 
     'tipo_id': 3},
    {'id': 18, 'planta_id': 18, 'origen_nativo': 'Chile', 
     'descripcion': 'Árbol perenne. Tiene hojas coriáceas, de color verde oscuro, y produce flores pequeñas y amarillas. El boldo crece en suelos bien drenados y prefiere climas mediterráneos.', 
     'tipo_id': 1},
    {'id': 19, 'planta_id': 19, 'origen_nativo': 'Chile', 
     'descripcion': 'Planta trepadora perenne que produce flores grandes, en forma de campana, de color rojo, rosa o blanco. Sus hojas son alargadas, brillantes y de color verde oscuro.', 
     'tipo_id': 8},
    {'id': 20, 'planta_id': 20, 'origen_nativo': 'México', 
     'descripcion': 'Planta suculenta de hojas gruesas y carnosas, dispuestas en forma de roseta. Las hojas son de color verde grisáceo o azul verdoso, y a menudo tienen bordes rojizos.', 
     'tipo_id': 6},
    {'id': 21, 'planta_id': 21, 'origen_nativo': 'Este y Sur de África',
     'descripcion': 'Planta suculenta de hojas gruesas y alargadas, que crecen en forma de roseta. Las hojas son de color verde y tienen bordes dentados. En su interior, contienen un gel transparente conocido por sus propiedades curativas y cosméticas.',
     'tipo_id': 6},
    {'id': 22, 'planta_id': 22, 'origen_nativo': 'México',
     'descripcion': 'Cactus pequeño y sin espinas, caracterizado por su forma redondeada y su color verde-azuloso. Su superficie tiene una serie de tubérculos, que son las prominencias a lo largo de su cuerpo.',
     'tipo_id': 6},
    {'id': 23, 'planta_id': 23, 'origen_nativo': 'Nueva Zelanda',
     'descripcion': 'Planta herbácea que produce pequeñas flores de color azul, aunque también puede encontrarse en tonos rosa o blanco. Sus hojas son de forma ovalada y de color verde claro.',
     'tipo_id': 3},
    {'id': 24, 'planta_id': 24, 'origen_nativo': 'Europa',
     'descripcion': 'Arbusto que produce flores de color rosa pálido a rosado, con pétalos delicados y fragantes. Sus hojas son pinnadas y de color verde oscuro. Esta planta es famosa por sus frutos, llamados escaramujos, que se utilizan por sus propiedades nutritivas y medicinales.',
     'tipo_id': 1},
    {'id': 25, 'planta_id': 25, 'origen_nativo': 'Cordillera del Himalaya',
     'descripcion': 'Pequeño árbol perenne que produce flores grandes y vistosas, generalmente en tonos de rosa, rojo, blanco, morado o púrpura. Sus hojas son alargadas, de color verde oscuro, y pueden tener un aspecto brillante o mate, dependiendo de la variedad.',
     'tipo_id': 1},
    {'id': 26, 'planta_id': 26, 'origen_nativo': 'Chile y Argentina',
     'descripcion': 'Arbusto nativo de Chile. Produce pequeñas flores blancas o rosadas y frutos pequeños de color morado oscuro o negro, que son altamente valorados por sus propiedades antioxidantes. Sus hojas son de color verde brillante y tiene un hábito de crecimiento erecto.',
     'tipo_id': 3},
    {'id': 27, 'planta_id': 27, 'origen_nativo': 'África del Sur',
     'descripcion': 'Planta herbácea. Se caracteriza por sus hojas lobuladas o dentadas y flores que varían en colores como rosa, morado, rojo o blanco. Son apreciadas en jardinería por su resistencia y su capacidad de atraer polinizadores.',
     'tipo_id': 8},
    {'id': 28, 'planta_id': 28, 'origen_nativo': 'Mesoamérica',
     'descripcion': 'Árbol de hoja perenne que produce frutos grandes y comestibles, con una piel gruesa y una pulpa cremosa. Tiene hojas grandes, de color verde brillante. Prefiere climas cálidos y suelos bien drenados, y es cultivado principalmente por su fruto, que es rico en grasas saludables.',
     'tipo_id': 3},
    {'id': 29, 'planta_id': 29, 'origen_nativo': 'Europa oriental y Asia Occidental',
     'descripcion': 'Árbol frutal de tamaño mediano que produce frutos comestibles llamados peras. Tiene hojas de forma ovalada, de color verde, y flores blancas que florecen en primavera. Planta resistente que se cultiva ampliamente por su fruta.',
     'tipo_id': 1},
    {'id': 30, 'planta_id': 30, 'origen_nativo': 'Asia Central',
     'descripcion': 'Árbol frutal que produce frutos llamados manzanas. Tiene hojas ovaladas y de color verde, con flores blancas o rosadas que florecen en primavera. Es cultivado ampliamente por sus frutos, que varían en sabor y textura según la variedad.',
     'tipo_id': 1},
    {'id': 31, 'planta_id': 31, 'origen_nativo': 'Europa',
     'descripcion': 'Arbusto perenne que produce frutos pequeños y rojos, conocidos como frambuesas. Tiene hojas compuestas, de color verde, y tallos cubiertos de espinas. El frambueso es cultivado principalmente por sus frutos comestibles, que son dulces y ácidos a la vez.',
     'tipo_id': 3},
    {'id': 32, 'planta_id': 32, 'origen_nativo': 'América del Norte',
     'descripcion': 'Arbusto que produce pequeños frutos de color azul oscuro, ricos en antioxidantes. Sus hojas son de forma ovalada, de color verde, que cambian a tonos rojizos en otoño. Es cultivado principalmente por sus frutos comestibles, que se utilizan en diversos productos como jugos y mermeladas.',
     'tipo_id': 3},
    {'id': 33, 'planta_id': 33, 'origen_nativo': 'Chile, Bolivia y Perú',
     'descripcion': 'Planta herbácea que produce tubérculos comestibles subterráneos. Sus hojas son de color verde y tiene flores pequeñas, generalmente blancas o moradas. La papa es uno de los cultivos más importantes del mundo debido a su alto valor nutricional y su versatilidad.',
     'tipo_id': 3},
    {'id': 34, 'planta_id': 34, 'origen_nativo': 'Mediterráneo oriental',
     'descripcion': 'Planta anual que produce hojas tiernas y crujientes, de color verde o rojo, según la variedad. Tiene un crecimiento compacto o en forma de roseta. Es cultivada principalmente por sus hojas comestibles, utilizadas en ensaladas y otros platillos.',
     'tipo_id': 3},
    {'id': 35, 'planta_id': 35, 'origen_nativo': 'Irak',
     'descripcion': 'Planta perenne que produce tallos tiernos y comestibles, conocidos como brotes de espárrago. Tiene hojas en forma de escamas finas que forman una estructura parecida a agujas. Se cultiva por sus brotes, que son ricos en nutrientes.',
     'tipo_id': 3},
    {'id': 36, 'planta_id': 36, 'origen_nativo': 'Norte de África y Sur de Europa',
     'descripcion': 'Planta perenne que produce flores grandes, de color morado, agrupadas en un botón espinoso. Sus hojas son grandes, divididas y de color verde grisáceo. Se cultiva principalmente por su capullo comestible, que es una parte de la flor antes de que florezca.',
     'tipo_id': 3},
    {'id': 37, 'planta_id': 37, 'origen_nativo': 'América Central y Sudamérica',
     'descripcion': 'Árbol que produce un aroma característico cuando su madera se quema. Tiene hojas compuestas, de color verde, y corteza de tonalidades grises o marrones. Es famoso por su madera resinosa, utilizada en la elaboración de incienso.',
     'tipo_id': 1},
    {'id': 38, 'planta_id': 38, 'origen_nativo': 'Chile y Argentina',
     'descripcion': 'Árbol perenne de gran tamaño, con hojas en forma de agujas duras y puntiagudas dispuestas en espiral. Su corteza es gruesa y rugosa, y puede alcanzar grandes alturas.',
     'tipo_id': 1},
    {'id': 39, 'planta_id': 39, 'origen_nativo': 'Chile y Argentina',
     'descripcion': 'Árbol perenne que se caracteriza por su corteza lisa de color rojizo o anaranjado, que se desprende en tiras finas. Sus hojas son brillantes, de color verde, y tiene flores pequeñas y blancas. El árbol produce frutos en forma de bayas negras o moradas.',
     'tipo_id': 1},
    {'id': 40, 'planta_id': 40, 'origen_nativo': 'Chile y Argentina',
     'descripcion': 'Árbol perenne de gran tamaño, que puede alcanzar alturas impresionantes. Tiene una corteza gruesa y fibrosa de color rojizo o marrón, y hojas en forma de escamas, dispuestas en espiral. Es famoso por su longevidad.',
     'tipo_id': 1},
    {'id': 41, 'planta_id': 41, 'origen_nativo': 'África, Asia y Europa',
     'descripcion': 'Planta trepadora perenne que tiene tallos flexibles cubiertos de espinas. Sus hojas son grandes, brillantes y de forma ovalada o corazón. Produce flores pequeñas, de color verde o blanco, seguidas por frutos redondos de color negro.',
     'tipo_id': 8},
    {'id': 42, 'planta_id': 42, 'origen_nativo': 'Chile y Argentina',
     'descripcion': 'Arbusto perenne que produce racimos de flores pequeñas, de color amarillo a anaranjado, seguidas por frutos rojos o morados. Sus hojas son de color verde brillante y tienen una forma ovalada. Es conocida por su resistencia y sus propiedades ornamentales.',
     'tipo_id': 3},
    {'id': 43, 'planta_id': 43, 'origen_nativo': 'Chile y Argentina',
     'descripcion': 'Planta perenne de grandes hojas redondas y acorazonadas que pueden medir hasta 2 metros de diámetro. Sus tallos son gruesos y su floración ocurre en racimos de flores pequeñas y verdes. Es una planta ornamental y se utiliza a menudo en paisajismo debido a su tamaño imponente.',
     'tipo_id': 6},
    {'id': 44, 'planta_id': 44, 'origen_nativo': 'Chile',
     'descripcion': 'Arbusto perenne que produce frutos pequeños, comestibles, de color rojo o púrpura. Sus hojas son de color verde brillante y aromáticas, y sus flores son blancas o rosadas. Se cultiva principalmente por sus frutos, que tienen un sabor dulce y ácido.',
     'tipo_id': 3},
    {'id': 45, 'planta_id': 45, 'origen_nativo': 'Europa',
     'descripcion': 'Planta perenne que tiene tallos verdes, delgados y segmentados, que se asemejan a una cola de caballo. No tiene flores, ya que se reproduce mediante esporas. Sus tallos son ricos en sílice y se usan tradicionalmente por sus propiedades medicinales.',
     'tipo_id': 5},
    {'id': 46, 'planta_id': 46, 'origen_nativo': 'Chile',
     'descripcion': 'Árbol perenne que puede alcanzar grandes alturas. Tiene hojas grandes, de color verde brillante y una forma lanceolada. Sus flores son pequeñas y de color amarillo, seguidas por frutos de color negro.',
     'tipo_id': 1},
    {'id': 47, 'planta_id': 47, 'origen_nativo': 'Europa, Asia y África',
     'descripcion': 'Planta perenne que se caracteriza por sus hojas aromáticas de color verde, que tienen un sabor fresco y refrescante. Produce pequeñas flores, generalmente de color morado o blanco. Es comúnmente cultivada por sus propiedades aromáticas y medicinales.',
     'tipo_id': 3},
    {'id': 48, 'planta_id': 48, 'origen_nativo': 'Región mediterránea, norte y sur de África, y Asia occidental',
     'descripcion': 'Arbusto perenne con hojas estrechas y aromáticas de color verde grisáceo. Produce flores pequeñas de color azul, púrpura o blanco. Es ampliamente cultivada por sus propiedades aromáticas, medicinales y culinarias.',
     'tipo_id': 3},
    {'id': 49, 'planta_id': 49, 'origen_nativo': 'Europa, norte de África y Asia occidental',
     'descripcion': 'Planta herbácea anual que produce flores pequeñas, blancas con un centro amarillo. Sus hojas son finamente divididas y de color verde. Es conocida por sus propiedades calmantes y medicinales, especialmente en infusiones.',
     'tipo_id': 6},
    {'id': 50, 'planta_id': 50, 'origen_nativo': 'Región mediterránea',
     'descripcion': 'Planta perenne que produce hojas ovaladas, de color verde grisáceo, con un aroma fuerte y característico. Sus flores son pequeñas, generalmente de color púrpura o rosa. Es apreciada por sus propiedades aromáticas y medicinales.',
     'tipo_id': 3},
    {'id': 51, 'planta_id': 51, 'origen_nativo': 'Europa mediterránea y Asia Central',
     'descripcion': 'Planta trepadora perenne que produce frutos llamados uvas. Sus hojas son grandes, de forma palmeada y de color verde. Es cultivada principalmente por sus uvas, que se utilizan tanto para el consumo fresco como para la producción de vino.',
     'tipo_id': 3},
    {'id': 52, 'planta_id': 52, 'origen_nativo': 'Sur de Ecuador, Perú, Bolivia y el norte de Chile',
     'descripcion': 'Planta trepadora perenne que produce flores grandes, blancas y fragantes, con un centro amarillo. Sus hojas son de color verde brillante y de forma elíptica. Es muy apreciada como planta ornamental debido a su floración abundante.',
     'tipo_id': 3},
    {'id': 53, 'planta_id': 53, 'origen_nativo': 'Región mediterránea',
     'descripcion': 'Planta perenne que produce espigas de flores pequeñas de color violeta, azul o púrpura. Sus hojas son estrechas, de color verde grisáceo, y tienen un aroma distintivo. Es cultivada por sus propiedades aromáticas y medicinales.',
     'tipo_id': 3},
    {'id': 54, 'planta_id': 54, 'origen_nativo': 'Europa y Asia',
     'descripcion': 'Planta herbácea perenne que produce flores grandes y coloridas, que pueden ser rojas, rosas, blancas o moradas, con un aroma dulce. Sus hojas son estrechas y de color verde grisáceo. Es apreciada por su belleza ornamental y su fragancia.',
     'tipo_id': 6},
    {'id': 55, 'planta_id': 55, 'origen_nativo': 'Región andina de Chile, Perú y Ecuador',
     'descripcion': 'Árbol perenne que produce frutos redondeados o elipsoidales, con una pulpa de color amarillo intenso y un sabor dulce y suave. Sus hojas son grandes, de color verde brillante, y su corteza es rugosa. Es cultivada principalmente por sus frutos comestibles, muy apreciados en la gastronomía andina.',
     'tipo_id': 3},
    {'id': 56, 'planta_id': 56, 'origen_nativo': 'Región mediterránea y África meridional',
     'descripcion': 'Planta bulbosa que produce racimos de flores fragantes y coloridas, que pueden ser moradas, rosas, blancas o rojas. Sus hojas son largas, estrechas y de color verde. Es apreciada en jardinería por su floración vibrante y su aroma intenso.',
     'tipo_id': 3},
    {'id': 57, 'planta_id': 57, 'origen_nativo': 'Sudáfrica',
     'descripcion': 'Rosetas de hojas carnosas, que suelen ser de color verde, aunque algunas variedades pueden presentar tonos rojizos o blancos. Las hojas son cortas, gruesas y a menudo tienen marcas o bandas blancas en su superficie. Es una planta resistente que se utiliza principalmente como planta ornamental.',
     'tipo_id': 6},
    {'id': 58, 'planta_id': 58, 'origen_nativo': 'Región andina de Ecuador, Perú y Bolivia',
     'descripcion': 'Cactus columnar que puede crecer varios metros de altura. Tiene tallos gruesos y erectos, con costillas pronunciadas y espinas pequeñas. Sus flores son grandes, de color blanco o verde claro, y suelen abrirse de noche. Es conocido por sus propiedades alucinógenas debido a su contenido de mescalina.',
     'tipo_id': 6},
    {'id': 59, 'planta_id': 59, 'origen_nativo': 'África del Sur',
     'descripcion': 'Suculenta de crecimiento arbustivo. Tiene hojas carnosas y brillantes, de color verde, aunque algunas variedades pueden tener bordes rojizos. Es una planta resistente, apreciada como ornamental por su forma y su facilidad de cuidado.',
     'tipo_id': 6},
    {'id': 60, 'planta_id': 60, 'origen_nativo': 'Chile',
     'descripcion': 'Planta perenne que tiene tallos gruesos y huecos, cubiertos de hojas alargadas de color verde. Produce flores pequeñas de color amarillo. Esta planta se utiliza principalmente en jardines y paisajismo por su aspecto único.',
     'tipo_id': 6},
    {'id': 61, 'planta_id': 61, 'origen_nativo': 'Suroeste de India',
     'descripcion': 'Planta perenne de la familia del jengibre que produce raíces o rizomas de color amarillo anaranjado. Sus hojas son largas y estrechas, y produce flores pequeñas de color amarillo o púrpura. Es cultivada principalmente por su rizoma, que se utiliza como especia y por sus propiedades medicinales.',
     'tipo_id': 4},
    {'id': 62, 'planta_id': 62, 'origen_nativo': 'Región mediterránea',
     'descripcion': 'Planta anual que produce pequeñas flores blancas o rosadas agrupadas en umbelas. Sus hojas son finamente divididas y de color verde. Se cultiva principalmente por sus semillas aromáticas, utilizadas como especia en la cocina.',
     'tipo_id': 4},
    {'id': 63, 'planta_id': 63, 'origen_nativo': 'Norte de India',
     'descripcion': 'Árbol perenne que puede alcanzar varios metros de altura. Tiene hojas compuestas de color verde brillante y produce flores pequeñas de color blanco o crema, seguidas por frutos en forma de vaina. Es cultivada principalmente por sus hojas, semillas y raíces, que tienen múltiples usos medicinales y alimenticios.',
     'tipo_id': 1}
]

# Inserting into the database
for data in plant_description_data:
    plant_description = PlantDescription(**data)
    session.add(plant_description)
session.commit()

plant_care_data = [
    {'id': 1, 'planta_id': 1, 'temp_ideal': '15-30°C', 'luz': 'No soporta exposición directa', 
     'humedad': '>60%', 'riego': 'Por goteo cada 2-3 días en los meses más calurosos, y cada 5-6 días el resto de meses', 
     'ph': '4.7 - 5.2', 'abonado': 'Cada ocho días a una dosis de 0.5g/l, se recomienda guano', 
     'tiempo_crecimiento': '115 días', 'tipo_tierra': 'Ricos en materia orgánica', 
     'plantacion': 'Separadas unos 35-45cm', 'transplante': 'Cada 2 años', 
     'estacion_siembra': 'N/A', 'estacion_recoleccion': 'N/A'},

    {'id': 2, 'planta_id': 2, 'temp_ideal': '14-32°C', 'luz': '10-12 horas', 
     'humedad': '80-85%', 'riego': 'Regadera de lluvia fina hasta altura de 3cm, después regar con tendido, al principio cada 3-4 días y alargarlo paulatinamente hasta 6-8 días', 
     'ph': '6.0 - 7.0', 'abonado': 'Abonos nitrogenados antes de la formación del bulbo', 
     'tiempo_crecimiento': '210 a 300 días', 'tipo_tierra': 'Suelos de 0.5 a 1.5 cm de profundidad, con buen contenido en materia orgánica y textura suelta', 
     'plantacion': '30 cm', 'transplante': 'Cortar raíces a 1-2 cm, cada 4 a 6 meses', 
     'estacion_siembra': 'Agosto-Octubre', 'estacion_recoleccion': 'Abril-Junio'},

    {'id': 3, 'planta_id': 3, 'temp_ideal': '18-27°C', 'luz': 'Mínimo de 6 horas de sol directo', 
     'humedad': '60-80%', 'riego': '2 a 6.6 mil m³/ha de agua', 
     'ph': '6.0 - 6.5', 'abonado': 'Potasio, calcio y guano', 
     'tiempo_crecimiento': '45 a 70 días', 'tipo_tierra': 'Suelo arenoso, suelto y rico en materia orgánica, con una profundidad de 8-10 cm', 
     'plantacion': '40 - 60 cm', 'transplante': 'N/A', 
     'estacion_siembra': 'Diciembre-Mayo', 'estacion_recoleccion': 'Mayo-Diciembre'},

    {'id': 4, 'planta_id': 4, 'temp_ideal': '15-21°C', 'luz': 'No necesitan luz directa', 
     'humedad': '95-100%', 'riego': 'Al principio del periodo vegetativo 1 o 2 veces por semana; aumentar la frecuencia hasta 2 veces al día, luego reducir en sus fases principales', 
     'ph': '6.0 - 6.8', 'abonado': 'Nitrógeno aplicado con un desarrollo de planta de 10 a 15 cm en dos parcialidades. Fósforo y potasio antes de la siembra', 
     'tiempo_crecimiento': '70 a 120 días', 'tipo_tierra': 'Tierra suelta con alto drenaje. Profundidad de 25-30 cm', 
     'plantacion': '25 cm', 'transplante': 'N/A', 
     'estacion_siembra': 'Todos', 'estacion_recoleccion': 'Todos'},

    {'id': 5, 'planta_id': 5, 'temp_ideal': '12-23°C', 'luz': '8 horas de sol', 
     'humedad': 'Aprox. 95%', 'riego': 'Al principio del periodo vegetativo 1 o 2 veces por semana; aumentar la frecuencia hasta 2 veces al día, luego reducir', 
     'ph': '6.0 - 6.8', 'abonado': 'N-P-K', 
     'tiempo_crecimiento': '93 a 128 días', 'tipo_tierra': 'Tierra suelta, en suelos profundos, ricos en nutrientes y bien drenados', 
     'plantacion': '40-70 cm', 'transplante': '18-38 días', 
     'estacion_siembra': 'Julio-Agosto', 'estacion_recoleccion': 'Octubre-Diciembre'},

    {'id': 6, 'planta_id': 6, 'temp_ideal': '20 - 38°C', 'luz': 'Pleno sol', 
     'humedad': '70-80%', 'riego': 'Tolera períodos secos cortos (no más de 1 mes)', 
     'ph': '5.5 - 7.0', 'abonado': 'Humus de lombriz', 
     'tiempo_crecimiento': 'Rápido', 'tipo_tierra': 'Prefiere suelos húmedos y bien drenados', 
     'plantacion': '15 cm unos de otros', 'transplante': 'Primavera-verano', 
     'estacion_siembra': 'N/A', 'estacion_recoleccion': 'Primavera'},

    {'id': 7, 'planta_id': 7, 'temp_ideal': '10 - 24°C', 'luz': '6 a 8 horas al día', 
     'humedad': '90-95%', 'riego': 'Agua constante evitando el encharcamiento', 
     'ph': '6.0 - 7.5', 'abonado': 'Incorporar compost o estiércol bien descompuesto', 
     'tiempo_crecimiento': '50 y 70 días', 'tipo_tierra': 'Suelos profundos, bien drenados, evitando suelos muy ácidos o extremadamente alcalinos', 
     'plantacion': '20 cm unos de otros', 'transplante': 'N/A', 
     'estacion_siembra': 'Todos', 'estacion_recoleccion': 'Todos'},

    {'id': 8, 'planta_id': 8, 'temp_ideal': '21 - 26°C', 'luz': 'Menos de 12 horas de iluminación al día', 
     'humedad': '60-70%', 'riego': 'Agua constante evitando el encharcamiento', 
     'ph': '5.5 - 6.8', 'abonado': 'Macronutrientes: Nitrógeno, fósforo, potasio, magnesio, calcio, azufre. Micronutrientes: Boro, cloro, cobre, manganeso, molibdeno, zinc', 
     'tiempo_crecimiento': '120 y 180 días', 'tipo_tierra': 'Suelos de textura areno-arcillosa y bien drenados. Sembrar a una profundidad de 2.5 a 3.0 cm', 
     'plantacion': 'Entre 15 y 50 cm', 'transplante': '25 días', 
     'estacion_siembra': 'Enero-Mayo', 'estacion_recoleccion': 'Mayo-Octubre'},

    {'id': 9, 'planta_id': 9, 'temp_ideal': '21 - 27°C', 'luz': '8 horas de luz solar', 
     'humedad': '20-26%', 'riego': '50-80 milímetros de agua cada semana', 
     'ph': '6.0 - 7.0', 'abonado': 'Abonos ricos en nitrógeno', 
     'tiempo_crecimiento': '62-93 días', 'tipo_tierra': 'Suelo a 16-18°C, fértiles y bien drenados, profundidad de 3-5 cm', 
     'plantacion': 'Distancia entre los surcos de 50 a 120 cm', 'transplante': 'N/A', 
     'estacion_siembra': 'Septiembre-Noviembre', 'estacion_recoleccion': 'Noviembre-Enero'},

    {'id': 10, 'planta_id': 10, 'temp_ideal': '20 - 38°C', 'luz': '6-8 horas al día de luz solar', 
     'humedad': '60-70%', 'riego': 'Riegos ligeros frecuentes al inicio (cada 2 días); entre los 30 y 90 días, regar cada 4-5 días. Entre los 90 y 120 días, regar cada 7 días aprox.', 
     'ph': '6.0 - 6.5', 'abonado': '140 kg/ha de nitrógeno y 168 kg/ha de fósforo y potasio', 
     'tiempo_crecimiento': '9 y 10 meses', 'tipo_tierra': 'Suelo suelto y bien drenado. No en suelos limosos o arcillosos. Profundidad de 2.5-5 cm en zonas cálidas y 7.5-10 cm en frías', 
     'plantacion': '15 cm entre plantas, con 30 cm entre hileras', 'transplante': 'N/A', 
     'estacion_siembra': 'Septiembre-Marzo', 'estacion_recoleccion': 'Mayo-Agosto'},

    {'id': 11, 'planta_id': 11, 'temp_ideal': '13 - 24°C', 'luz': '3-6 horas al día', 
     'humedad': '90-95%', 'riego': '8 mm/semana en las primeras 6 semanas, luego 40 mm/semana por planta', 
     'ph': '< 6', 'abonado': 'Relación ideal de N:P:K es 1:2:2', 
     'tiempo_crecimiento': '5 meses', 'tipo_tierra': 'Suelos profundos, bien drenados y esponjosos', 
     'plantacion': '15 cm entre plantas, con 30 cm entre hileras', 'transplante': '2 meses', 
     'estacion_siembra': 'Todos', 'estacion_recoleccion': 'Todos'},

    {'id': 12, 'planta_id': 12, 'temp_ideal': '20-25°C', 'luz': '8-10 horas', 
     'humedad': '60-75%', 'riego': '1-3 litros/semana en épocas frías; 4-8 litros diarios en épocas cálidas', 
     'ph': '6.0 - 7.5', 'abonado': 'Estiércol, abonos minerales: potasio, nitrógeno, fósforo, calcio, magnesio', 
     'tiempo_crecimiento': '100-110 días', 'tipo_tierra': 'Profundidad de 2.5 cm; temperatura de 18°C', 
     'plantacion': '70 a 150 cm entre plantas', 'transplante': 'N/A', 
     'estacion_siembra': 'Enero-Mayo', 'estacion_recoleccion': 'Junio-Septiembre'},

    {'id': 13, 'planta_id': 13, 'temp_ideal': '17-27°C', 'luz': '6 horas al día', 
     'humedad': '40-60%', 'riego': 'Solo cuando el sustrato esté seco', 
     'ph': '6.0 - 7.5', 'abonado': 'Primavera y verano, una vez al mes; otras estaciones, eliminar abonado', 
     'tiempo_crecimiento': '2-3 años', 'tipo_tierra': 'Arenoso, con buen drenado', 
     'plantacion': '20-30 cm', 'transplante': 'Cada 2-3 años', 
     'estacion_siembra': 'Marzo-Septiembre', 'estacion_recoleccion': 'Todo el año'},

    {'id': 14, 'planta_id': 14, 'temp_ideal': 'N/A', 'luz': 'N/A', 
     'humedad': 'N/A', 'riego': 'N/A', 
     'ph': 'N/A', 'abonado': 'N/A', 
     'tiempo_crecimiento': 'N/A', 'tipo_tierra': 'Suelos bien drenados', 
     'plantacion': 'N/A', 'transplante': 'N/A', 
     'estacion_siembra': 'Primavera', 'estacion_recoleccion': 'N/A'},  

    {'id': 15, 'planta_id': 15, 'temp_ideal': '18-24°C', 'luz': '6-8 horas de sol directo', 
     'humedad': '60-80%', 'riego': 'Regular, mantener sustrato húmedo pero no encharcado', 
     'ph': '6.0-7.0', 'abonado': 'Abonos equilibrados con mayor énfasis en potasio y fósforo', 
     'tiempo_crecimiento': '90-120 días', 'tipo_tierra': 'Suelos bien drenados y ricos en nutrientes', 
     'plantacion': 'Cada 40-50 cm entre plantas', 'transplante': 'Cada 2-3 años', 
     'estacion_siembra': 'Primavera', 'estacion_recoleccion': 'Finales de verano o principios de otoño'},

    {'id': 16, 'planta_id': 16, 'temp_ideal': '15-28°C', 'luz': '8 horas de sol directo', 
     'humedad': '55-70%', 'riego': 'Riego regular, evitar encharcamiento', 
     'ph': '6.5-7.5', 'abonado': 'Fertilizantes equilibrados, compost orgánico', 
     'tiempo_crecimiento': '80-100 días', 'tipo_tierra': 'Suelos bien drenados y ricos en nutrientes', 
     'plantacion': '30 cm entre plantas', 'transplante': 'Cada 2 años', 
     'estacion_siembra': 'Primavera', 'estacion_recoleccion': 'Verano hasta principios de otoño'}

]

# Inserting into the database
for data in plant_care_data:
    care = PlantCare(**data)
    session.add(care)
session.commit()

plant_disease_data = [
    {'id': 1, 'nombre': 'Plagas', 
     'descripcion': 'Entre estas están: cochinillas, ácaros o pulgones', 
     'sintomas': 'Amarillamiento y caída de hojas, superficie pegajosa por melaza, presencia de insectos en tallo y hojas.', 
     'tratamiento': 'Limpia las hojas con un algodón humedecido en alcohol isopropílico; en casos extremos, usa insecticida.', 
     'prevencion': 'Inspeccionar hojas periódicamente, buena ventilación y evitar exceso de abono.'},
    {'id': 2, 'nombre': 'Podredumbre de raíces', 
     'descripcion': 'Causada por hongos como *Pythium* o *Phytophthora*.', 
     'sintomas': 'Hojas amarillas o marchitas, base blanda o ennegrecida, olor desagradable en el sustrato.', 
     'tratamiento': 'Reduce el riego y asegura un buen drenaje del sustrato; retira las raíces afectadas con herramientas estériles; aplica un fungicida sistémico.', 
     'prevencion': 'Usa un sustrato aireado y bien drenado; evita el exceso de riego y los encharcamientos.'},
    {'id': 3, 'nombre': 'Moho blanco', 
     'descripcion': 'Enfermedad fúngica causada por hongos como *Erysiphe* y *Oidium*.', 
     'sintomas': 'Manchas blancas polvorientas en hojas, tallos y brotes; hojas deformadas y secas.', 
     'tratamiento': 'Retira las partes infectadas; aplica fungicidas específicos a base de azufre.', 
     'prevencion': 'Mejora la ventilación; evita mojar las hojas al regar.'},
    {'id': 4, 'nombre': 'Antracnosis', 
     'descripcion': 'Causada por hongos del género *Colletotrichum*.', 
     'sintomas': 'Manchas oscuras con bordes definidos en hojas y frutos; áreas hundidas y secas en frutos; caída de hojas prematura.', 
     'tratamiento': 'Retira las partes infectadas; usa fungicidas de amplio espectro, como los a base de cobre.', 
     'prevencion': 'Mantén las plantas sanas con fertilización equilibrada; evita el riego por aspersión.'},
    {'id': 5, 'nombre': 'Tizón tardío', 
     'descripcion': 'Causado por el hongo *Phytophthora infestans*, afecta cultivos como papa y tomate.', 
     'sintomas': 'Manchas oscuras e irregulares en hojas y tallos; frutos con manchas marrones y tejidos blandos; colapso rápido de la planta.', 
     'tratamiento': 'Retira las plantas infectadas; usa fungicidas sistémicos específicos.', 
     'prevencion': 'Planta variedades resistentes; practica rotación de cultivos.'},
    {'id': 6, 'nombre': 'Roya', 
     'descripcion': 'Causada por hongos del género *Puccinia*.', 
     'sintomas': 'Pústulas naranjas o rojizas en el envés de las hojas; hojas amarillentas y caída prematura.', 
     'tratamiento': 'Poda y destruye las hojas afectadas; aplica fungicidas específicos.', 
     'prevencion': 'Evita el riego por aspersión; mejora la circulación de aire.'},
    {'id': 7, 'nombre': 'Mildiu', 
     'descripcion': 'Enfermedad fúngica causada por *Plasmopara viticola* y otros.', 
     'sintomas': 'Manchas amarillas en el haz de las hojas; moho grisáceo o blanco en el envés; hojas deformadas y necrosis.', 
     'tratamiento': 'Aplica fungicidas a base de cobre o sistémicos; retira las hojas infectadas.', 
     'prevencion': 'Reduce la humedad ambiental; usa variedades resistentes.'},
    {'id': 8, 'nombre': 'Verticilosis', 
     'descripcion': 'Causada por *Verticillium dahliae* y *Verticillium albo-atrum*.', 
     'sintomas': 'Marchitez en hojas superiores o en un solo lado de la planta; decoloración de los vasos en el tallo; retraso en el crecimiento y muerte gradual.', 
     'tratamiento': 'No existe cura definitiva; elimina plantas infectadas; mejora la salud del suelo con compost o biofungicidas.', 
     'prevencion': 'Planta variedades resistentes; practica rotación de cultivos; evita suelos contaminados.'},
    {'id': 9, 'nombre': 'Fusariosis', 
     'descripcion': 'Causada por especies de *Fusarium*.', 
     'sintomas': 'Marchitez repentina; hojas amarillentas y caída; decoloración marrón en los tejidos internos de tallos o raíces; colapso total en infecciones severas.', 
     'tratamiento': 'No tiene cura; elimina plantas infectadas; aplica fungicidas preventivos si recurrente.', 
     'prevencion': 'Usa suelos esterilizados; planta variedades resistentes; asegura buen drenaje.'},
    {'id': 10, 'nombre': 'Moho negro', 
     'descripcion': 'Causada por el hongo *Diplocarpon rosae*, afecta rosales y otras ornamentales.', 
     'sintomas': 'Manchas negras o marrones oscuras en las hojas; hojas amarillean y caen prematuramente; planta debilitada y menos flores.', 
     'tratamiento': 'Retira y desecha hojas infectadas; aplica fungicidas específicos, preferiblemente a base de cobre o azufre.', 
     'prevencion': 'Rocía preventivamente en épocas de alta humedad; riega directamente en la base; asegura buena circulación de aire; fertiliza regularmente.'}
]

# Inserting into the database
for data in plant_disease_data:
    sickness = PlantDisease(**data)
    session.add(sickness)
session.commit()