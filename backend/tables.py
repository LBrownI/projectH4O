import os
from sqlalchemy import create_engine, text, Column, Integer, String, ForeignKey, DECIMAL, Date, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

# Load the MySQL root password from environment variables
mysql_root_password = os.getenv('MYSQL_ROOT_PASSWORD', 'default_root_pass')  # Fallback in case the env variable isn't set
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
    orden = Column(String(50))
    familia = Column(String(50))

    descriptions = relationship('PlantDescription', back_populates='plants', uselist=False)
    cares = relationship('PlantCare', back_populates='plants')


class PlantType(Base):
    __tablename__ = 'PlantType'
    id = Column(Integer, primary_key=True)
    habito = Column(String(100), nullable=False)
    descripcion = Column(Text)

    descriptions = relationship('PlantDescription', back_populates='types')


class PlantDescription(Base):
    __tablename__ = 'PlantDescription'
    id = Column(Integer, primary_key=True)
    planta_id = Column(Integer, ForeignKey('Plant.id', ondelete='CASCADE'))  # Corrected to Plant.id
    origen_nativo = Column(String(255))
    descripcion = Column(Text)
    tipo_id = Column(Integer, ForeignKey('PlantType.id', ondelete='SET NULL'))  # Corrected to PlantType.id

    plants = relationship('Plant', back_populates='descriptions')
    types = relationship('PlantType', back_populates='descriptions')  # Corrected to PlantType


class PlantCare(Base):
    __tablename__ = 'PlantCare'
    id = Column(Integer, primary_key=True)
    planta_id = Column(Integer, ForeignKey('Plant.id', ondelete='CASCADE'))  # Corrected to Plant.id
    temp_ideal = Column(String(20))
    luz = Column(String(50))
    humedad = Column(String(20))
    riego = Column(String(255))
    ph = Column(String(255))
    abonado = Column(Text)
    tiempo_crecimiento = Column(String(50))
    tipo_tierra = Column(String(255))
    plantacion = Column(String(50))
    transplante = Column(String(50))
    estacion_siembra = Column(String(50))
    estacion_recoleccion = Column(String(50))

    plants = relationship('Plant', back_populates='cares')


class PlantDisease(Base):
    __tablename__ = 'PlantDisease'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    sintomas = Column(Text)
    tratamiento = Column(Text)
    prevencion = Column(Text)


Base.metadata.create_all(engine)

