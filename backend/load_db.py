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

# Insert data into Company table
plant_data = [
    {'id': 1, 'nombre_comun': '', 'nombre_cientifico': '', 'reino': '', 'division': '', 'clase': '', 'subclase': '', 'orden': '', 'familia': '', 'subfamilia': '', 'tribu': '', 'subtribu': '', 'genero': '', 'especie': ''},
    {'id': 2, 'nombre_comun': '', 'nombre_cientifico': '', 'reino': '', 'division': '', 'clase': '', 'subclase': '', 'orden': '', 'familia': '', 'subfamilia': '', 'tribu': '', 'subtribu': '', 'genero': '', 'especie': ''}
]

for data in plant_data:
    plant = Plant(**data)
    session.add(plant)
session.commit()

    