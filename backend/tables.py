import os
from sqlalchemy import create_engine, text, Column, Integer, String, ForeignKey, DECIMAL, Date, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

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

    descripcion = relationship('Descripcion', back_populates='planta', uselist=False)
    cuidados = relationship('Cuidados', back_populates='planta')
    enfermedades = relationship('Enfermedades', back_populates='planta')


class PlantType(Base):
    __tablename__ = 'Type'
    id = Column(Integer, primary_key=True)
    nombre_tipo = Column(String(100), nullable=False)
    descripcion = Column(Text)

    descripciones = relationship('Descripcion', back_populates='tipo')


class PlantDescription(Base):
    __tablename__ = 'Description'
    id = Column(Integer, primary_key=True)
    planta_id = Column(Integer, ForeignKey('planta.id', ondelete='CASCADE'))
    origen_nativo = Column(String(255))
    descripcion = Column(Text)
    comestible = Column(Boolean)
    tipo_id = Column(Integer, ForeignKey('tipo.id', ondelete='SET NULL'))

    planta = relationship('Planta', back_populates='descripcion')
    tipo = relationship('Tipo', back_populates='descripciones')


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

    planta = relationship('Planta', back_populates='cuidados')


class PlantDisease(Base):
    __tablename__ = 'PlantDisease'
    id = Column(Integer, primary_key=True)
    planta_id = Column(Integer, ForeignKey('planta.id', ondelete='CASCADE'))
    nombre = Column(String(100))
    descripcion = Column(Text)
    sintomas = Column(Text)
    tratamiento = Column(Text)
    prevencion = Column(Text)

    planta = relationship('Planta', back_populates='enfermedades')

Base.metadata.create_all(engine)
