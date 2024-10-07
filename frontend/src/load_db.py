import os
from sqlalchemy import create_engine, text, Column, Integer, String, ForeignKey, DECIMAL, Date, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

# Load the MySQL root password from environment variables
mysql_root_password = os.getenv('MYSQL_ROOT_PASSWORD', 'default_root_pass')  # Fallback in case the env variable isn't set
# You can set it up by doing: export MYSQL_ROOT_PASSWORD=your_secure_password

config = {'host': 'localhost',
          'database_name': 'hr',
          'user': 'root',
          'password': mysql_root_password}

engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}', echo=True)
# engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}', echo=True)

with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config['database_name']}"))

Base = declarative_base()

# Empresa model
class Empresa(Base):
    __tablename__ = 'Empresa'
    id = Column(Integer, primary_key=True)
    rut = Column(String(20))
    nombre = Column(String(100))
    direccion = Column(String(255))
    telefono = Column(String(20))
    giro = Column(String(100))

# Colaborador model
class Colaborador(Base):
    __tablename__ = 'Colaborador'
    id = Column(Integer, primary_key=True)
    rut = Column(String(20))
    nombre = Column(String(50))
    apellido = Column(String(50))
    fecha_nacimiento = Column(Date)
    fecha_ingreso = Column(Date)
    telefono = Column(String(20))
    salario = Column(DECIMAL(10, 2))
    nacionalidad = Column(String(50))
    contratos = relationship('Contrato', back_populates='colaborador')
    vacaciones = relationship('Vacaciones', back_populates='colaborador')
    evaluaciones = relationship('Evaluacion', back_populates='colaborador')
    capacitaciones = relationship('Capacitacion', back_populates='colaborador')
    remuneraciones = relationship('Remuneracion', back_populates='colaborador')
    cargos = relationship('Cargo', secondary='ColaboradorCargo', back_populates='colaboradores')

# Cargo model
class Cargo(Base):
    __tablename__ = 'Cargo'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    colaboradores = relationship('Colaborador', secondary='ColaboradorCargo', back_populates='cargos')

# ColaboradorCargo association table (Many-to-Many relationship between Colaborador and Cargo)
class ColaboradorCargo(Base):
    __tablename__ = 'ColaboradorCargo'
    colaborador_id = Column(Integer, ForeignKey('Colaborador.id'), primary_key=True)
    cargo_id = Column(Integer, ForeignKey('Cargo.id'), primary_key=True)
    
# AFP model
class AFP(Base):
    __tablename__ = 'AFP'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    comision_porcentaje = Column(DECIMAL(5, 2))
    remuneraciones = relationship('Remuneracion', back_populates='afp')

# Departamento model
class Departamento(Base):
    __tablename__ = 'Departamento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    contratos = relationship('Contrato', back_populates='departamento')

# Vacaciones model
class Vacaciones(Base):
    __tablename__ = 'Vacaciones'
    id = Column(Integer, primary_key=True)
    colaborador_id = Column(Integer, ForeignKey('Colaborador.id'))
    fecha_inicio = Column(Date)
    fecha_termino = Column(Date)
    dias_tomados = Column(Integer) # Days taken in the period above 
    dias_acumulados = Column(Integer) # Acumulated after the vacation period above
    colaborador_antiguo = Column(Boolean) #If 1 then it's an employee that has worked for 15 years (20 days assigned instead of 15)
    colaborador = relationship('Colaborador', back_populates='vacaciones')

# Evaluacion model
class Evaluacion(Base):
    __tablename__ = 'Evaluacion'
    id = Column(Integer, primary_key=True)
    colaborador_id = Column(Integer, ForeignKey('Colaborador.id'))
    fecha_evaluacion = Column(Date)
    evaluador = Column(String(100))
    factor_evaluacion = Column(DECIMAL(5, 2))
    calificacion = Column(String(50))  # Bueno, regular, malo/deficiente
    comentarios = Column(Text)
    colaborador = relationship('Colaborador', back_populates='evaluaciones')

# Capacitacion model
class Capacitacion(Base):
    __tablename__ = 'Capacitacion'
    id = Column(Integer, primary_key=True)
    colaborador_id = Column(Integer, ForeignKey('Colaborador.id'))
    fecha_capacitacion = Column(Date)
    curso = Column(String(100))
    calificacion = Column(DECIMAL(5, 2))
    institucion = Column(String(100))
    comentarios = Column(Text)
    colaborador = relationship('Colaborador', back_populates='capacitaciones')

# Remuneracion (extended) model
class Remuneracion(Base):
    __tablename__ = 'Remuneracion'
    id = Column(Integer, primary_key=True)
    colaborador_id = Column(Integer, ForeignKey('Colaborador.id'))
    afp_id = Column(Integer, ForeignKey('AFP.id'))
    plan_salud_id = Column(Integer, ForeignKey('PlanDeSalud.id'))
    monto_bruto = Column(DECIMAL(10, 2))
    impuesto = Column(DECIMAL(5, 2))
    deducciones = Column(DECIMAL(10, 2))
    bonus = Column(DECIMAL(10, 2))
    aporte_bienestar = Column(DECIMAL(10, 2))
    monto_liquido = Column(DECIMAL(10, 2))
    colaborador = relationship('Colaborador', back_populates='remuneraciones')
    afp = relationship('AFP', back_populates='remuneraciones')
    plan_salud = relationship('PlanDeSalud', back_populates='remuneraciones')
    bonuses = relationship("Bonus", back_populates="remuneracion")

class PlanDeSalud(Base):
    __tablename__ = 'PlanDeSalud'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    tipo = Column(String(50))
    fonasa = relationship('Fonasa', back_populates='plan_salud')
    isapre = relationship('Isapre', back_populates='plan_salud')
    remuneraciones = relationship('Remuneracion', back_populates='plan_salud')

# PlanDeSalud extension for Fonasa and Isapre
class Fonasa(Base):
    __tablename__ = 'Fonasa'
    id = Column(Integer, primary_key=True)
    plan_salud_id = Column(Integer, ForeignKey('PlanDeSalud.id'))
    descuento = Column(DECIMAL(10, 2))  # Different from Isapre's discount
    plan_salud = relationship('PlanDeSalud', back_populates='fonasa')

class Isapre(Base):
    __tablename__ = 'Isapre'
    id = Column(Integer, primary_key=True)
    plan_salud_id = Column(Integer, ForeignKey('PlanDeSalud.id'))
    descuento = Column(DECIMAL(10, 2))  # Different from Fonasa's discount
    plan_salud = relationship('PlanDeSalud', back_populates='isapre')

class Bonus(Base):
    __tablename__ = 'Bonus'
    id = Column(Integer, primary_key=True)
    remuneracion_id = Column(Integer, ForeignKey('Remuneracion.id'))
    aporte = Column(DECIMAL(10, 2))  # Help for the employee for a discount in money
    beneficio = Column(DECIMAL(10, 2)) # Help for the employee as a monetary aid
    remuneracion = relationship("Remuneracion", back_populates="bonuses")

class Contrato(Base):
    __tablename__ = 'Contrato'
    id = Column(Integer, primary_key=True)
    colaborador_id = Column(Integer, ForeignKey('Colaborador.id'))
    tipo_contrato = Column(String(50))  # contrata, suplencia, reemplazo, planta
    fecha_inicio = Column(Date)
    fecha_termino = Column(Date)
    escalafon = Column(String(50))  # auxiliar, administrativo, tecnico, profesional, directivo
    departamento_id = Column(Integer, ForeignKey('Departamento.id'))  # Dpto/unidad asignado
    fecha_registro = Column(Date)
    colaborador = relationship('Colaborador', back_populates='contratos')
    departamento = relationship('Departamento', back_populates='contratos')

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Method to set hashed password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Method to check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Create the tables in the database
Base.metadata.create_all(engine)


# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Insert data into Empresa table
empresa_data = [
    {'id': 1, 'rut': '76.123.456-7', 'nombre': 'TechCorp', 'direccion': '123 Main Street', 'telefono': '555-0100', 'giro': 'Technology'},
    {'id': 2, 'rut': '78.234.567-8', 'nombre': 'HealthSolutions', 'direccion': '456 Oak Avenue', 'telefono': '555-0200', 'giro': 'Healthcare'}
]

for data in empresa_data:
    empresa = Empresa(**data)
    session.add(empresa)
session.commit()

# Insert data into Colaborador table
colaborador_data = [
    {'id': 1, 'rut': '12.345.678-9', 'nombre': 'John', 'apellido': 'Smith', 'fecha_nacimiento': date(1980, 5, 12), 'fecha_ingreso': date(2020, 1, 15), 'telefono': '555-2345', 'salario': 2000.00, 'nacionalidad': 'Chilean'},
    {'id': 2, 'rut': '12.345.678-1', 'nombre': 'Mary', 'apellido': 'Johnson', 'fecha_nacimiento': date(1985, 9, 22), 'fecha_ingreso': date(2019, 3, 10), 'telefono': '555-6789', 'salario': 2500.00, 'nacionalidad': 'Chilean'},
    {'id': 3, 'rut': '13.345.678-2', 'nombre': 'Carlos', 'apellido': 'Williams', 'fecha_nacimiento': date(1990, 7, 18), 'fecha_ingreso': date(2021, 6, 5), 'telefono': '555-9102', 'salario': 1800.00, 'nacionalidad': 'Chilean'},
    {'id': 4, 'rut': '14.345.678-3', 'nombre': 'Anna', 'apellido': 'Brown', 'fecha_nacimiento': date(1992, 11, 2), 'fecha_ingreso': date(2018, 9, 25), 'telefono': '555-1124', 'salario': 2300.00, 'nacionalidad': 'Chilean'},
    {'id': 5, 'rut': '18.145.678-4', 'nombre': 'Louis', 'apellido': 'Davis', 'fecha_nacimiento': date(1995, 2, 15), 'fecha_ingreso': date(2022, 2, 1), 'telefono': '555-1416', 'salario': 2100.00, 'nacionalidad': 'Chilean'},
    {'id': 6, 'rut': '16.245.678-5', 'nombre': 'Laura', 'apellido': 'Miller', 'fecha_nacimiento': date(1997, 6, 25), 'fecha_ingreso': date(2020, 8, 14), 'telefono': '555-1718', 'salario': 2400.00, 'nacionalidad': 'Chilean'},
    {'id': 7, 'rut': '16.645.678-6', 'nombre': 'Robert', 'apellido': 'Wilson', 'fecha_nacimiento': date(1987, 4, 8), 'fecha_ingreso': date(2017, 10, 12), 'telefono': '555-1920', 'salario': 2200.00, 'nacionalidad': 'Chilean'},
    {'id': 8, 'rut': '12.945.678-7', 'nombre': 'Fernanda', 'apellido': 'Taylor', 'fecha_nacimiento': date(1988, 1, 3), 'fecha_ingreso': date(2021, 4, 8), 'telefono': '555-2021', 'salario': 2700.00, 'nacionalidad': 'Chilean'},
    {'id': 9, 'rut': '14.745.678-8', 'nombre': 'George', 'apellido': 'Anderson', 'fecha_nacimiento': date(1986, 12, 20), 'fecha_ingreso': date(2020, 3, 14), 'telefono': '555-2223', 'salario': 2600.00, 'nacionalidad': 'Chilean'},
    {'id': 10, 'rut': '10.345.678-K', 'nombre': 'Claudia', 'apellido': 'Thomas', 'fecha_nacimiento': date(1983, 10, 30), 'fecha_ingreso': date(2016, 7, 3), 'telefono': '555-2324', 'salario': 1900.00, 'nacionalidad': 'Chilean'},
    {'id': 11, 'rut': '12.987.654-3', 'nombre': 'Jean', 'apellido': 'Baptiste', 'fecha_nacimiento': date(1990, 3, 18), 'fecha_ingreso': date(2021, 7, 12), 'telefono': '555-3456', 'salario': 2100.00, 'nacionalidad': 'Haitian'}
]


for data in colaborador_data:
    colaborador = Colaborador(**data)
    session.add(colaborador)
session.commit()

# Insert data into AFP table
afp_data = [
    {'id': 1, 'nombre': 'AFP Capital', 'comision_porcentaje': 1.44},
    {'id': 2, 'nombre': 'AFP Cuprum', 'comision_porcentaje': 1.44},
    {'id': 3, 'nombre': 'AFP Habitat', 'comision_porcentaje': 1.27},
    {'id': 4, 'nombre': 'AFP Modelo', 'comision_porcentaje': 0.58},
    {'id': 5, 'nombre': 'AFP Planvital', 'comision_porcentaje': 1.16},
    {'id': 6, 'nombre': 'AFP Provida', 'comision_porcentaje': 1.45},
    {'id': 7, 'nombre': 'AFP Uno', 'comision_porcentaje': 0.49}
]

for data in afp_data:
    afp = AFP(**data)
    session.add(afp)
session.commit()


# Insert data into Cargo table
cargo_data = [
    {'id': 1, 'nombre': 'Software Engineer', 'descripcion': 'Develops and maintains software applications.'},
    {'id': 2, 'nombre': 'HR Specialist', 'descripcion': 'Handles employee relations and recruitment.'},
    {'id': 3, 'nombre': 'Project Manager', 'descripcion': 'Leads and manages project execution.'},
    {'id': 4, 'nombre': 'System Administrator', 'descripcion': 'Manages IT systems and infrastructure.'},
    {'id': 5, 'nombre': 'Marketing Analyst', 'descripcion': 'Analyzes marketing data and trends.'}
]

for data in cargo_data:
    cargo = Cargo(**data)
    session.add(cargo)
session.commit()

colaborador_cargo_data = [
    {'colaborador_id': 1, 'cargo_id': 1},  # John -> Software Engineer
    {'colaborador_id': 2, 'cargo_id': 2},  # Mary -> HR Specialist
    {'colaborador_id': 3, 'cargo_id': 1},  # Carlos -> Software Engineer
    {'colaborador_id': 4, 'cargo_id': 2},  # Anna -> HR Specialist
    {'colaborador_id': 5, 'cargo_id': 3},  # Louis -> Project Manager
    {'colaborador_id': 6, 'cargo_id': 4},  # Laura -> System Administrator
    {'colaborador_id': 7, 'cargo_id': 4},  # Robert -> System Administrator
    {'colaborador_id': 8, 'cargo_id': 5},  # Fernanda -> Marketing Analyst
    {'colaborador_id': 9, 'cargo_id': 5},  # George -> Marketing Analyst
    {'colaborador_id': 10, 'cargo_id': 3},  # Claudia -> Project Manager
    {'colaborador_id': 11, 'cargo_id': 1}   # Jean -> Software Engineer
]

for data in colaborador_cargo_data:
    colcargo = ColaboradorCargo(**data)
    session.add(colcargo)
session.commit()

# Insert data into Departamento table
departamento_data = [
    {'id': 1, 'nombre': 'IT Department'},
    {'id': 2, 'nombre': 'HR Department'},
    {'id': 3, 'nombre': 'Finance Department'},
    {'id': 4, 'nombre': 'Marketing Department'}
]

for data in departamento_data:
    departamento = Departamento(**data)
    session.add(departamento)
session.commit()

# Insert data into PlanDeSalud, Fonasa, and Isapre tables
plan_salud_data = [
    {'id': 1, 'nombre': 'Fonasa Plan A', 'tipo': 'Fonasa'},
    {'id': 2, 'nombre': 'Fonasa Plan B', 'tipo': 'Fonasa'},
    {'id': 3, 'nombre': 'Isapre Plan 1', 'tipo': 'Isapre'},
    {'id': 4, 'nombre': 'Isapre Plan 2', 'tipo': 'Isapre'}
]

for data in plan_salud_data:
    plan_salud = PlanDeSalud(**data)
    session.add(plan_salud)
session.commit()

fonasa_data = [
    {'id': 1, 'plan_salud_id': 1, 'descuento': 7.00},
    {'id': 2, 'plan_salud_id': 2, 'descuento': 7.00}
]

for data in fonasa_data:
    fonasa = Fonasa(**data)
    session.add(fonasa)
session.commit()

isapre_data = [
    {'id': 1, 'plan_salud_id': 3, 'descuento': 10.00},
    {'id': 2, 'plan_salud_id': 4, 'descuento': 12.00}
]

for data in isapre_data:
    isapre = Isapre(**data)
    session.add(isapre)
session.commit()

# Insert data into Contrato table
contrato_data = [
    {'id': 1, 'colaborador_id': 1, 'tipo_contrato': 'planta', 'fecha_inicio': date(2020, 1, 15), 'fecha_termino': date(2023, 1, 15), 'escalafon': 'profesional', 'departamento_id': 1, 'fecha_registro': date(2020, 1, 15)},
    {'id': 2, 'colaborador_id': 2, 'tipo_contrato': 'contrata', 'fecha_inicio': date(2019, 3, 10), 'fecha_termino': date(2022, 3, 10), 'escalafon': 'administrativo', 'departamento_id': 2, 'fecha_registro': date(2019, 3, 10)},
    {'id': 3, 'colaborador_id': 3, 'tipo_contrato': 'reemplazo', 'fecha_inicio': date(2021, 6, 5), 'fecha_termino': date(2022, 6, 5), 'escalafon': 'tecnico', 'departamento_id': 3, 'fecha_registro': date(2021, 6, 5)},
    {'id': 4, 'colaborador_id': 4, 'tipo_contrato': 'suplencia', 'fecha_inicio': date(2018, 9, 25), 'fecha_termino': date(2021, 9, 25), 'escalafon': 'auxiliar', 'departamento_id': 4, 'fecha_registro': date(2018, 9, 25)},
    {'id': 5, 'colaborador_id': 5, 'tipo_contrato': 'planta', 'fecha_inicio': date(2022, 2, 1), 'fecha_termino': date(2025, 2, 1), 'escalafon': 'directivo', 'departamento_id': 5, 'fecha_registro': date(2022, 2, 1)}
]

for data in contrato_data:
    contrato = Contrato(**data)
    session.add(contrato)
session.commit()

# Insert data into Vacaciones table
vacaciones_data = [
    {'id': 1, 'colaborador_id': 1, 'fecha_inicio': date(2023, 1, 5), 'fecha_termino': date(2023, 1, 20), 'dias_tomados': 15, 'dias_acumulados': 10, 'colaborador_antiguo': False},
    {'id': 2, 'colaborador_id': 2, 'fecha_inicio': date(2023, 6, 1), 'fecha_termino': date(2023, 6, 10), 'dias_tomados': 9, 'dias_acumulados': 5, 'colaborador_antiguo': False},
    {'id': 3, 'colaborador_id': 3, 'fecha_inicio': date(2022, 12, 15), 'fecha_termino': date(2022, 12, 30), 'dias_tomados': 15, 'dias_acumulados': 3, 'colaborador_antiguo': False},
    {'id': 4, 'colaborador_id': 4, 'fecha_inicio': date(2022, 8, 1), 'fecha_termino': date(2022, 8, 15), 'dias_tomados': 14, 'dias_acumulados': 6, 'colaborador_antiguo': True},
    {'id': 5, 'colaborador_id': 5, 'fecha_inicio': date(2023, 2, 10), 'fecha_termino': date(2023, 2, 25), 'dias_tomados': 15, 'dias_acumulados': 8, 'colaborador_antiguo': False}
]

for data in vacaciones_data:
    vacaciones = Vacaciones(**data)
    session.add(vacaciones)
session.commit()

# Insert data into Evaluacion table
evaluacion_data = [
    {'id': 1, 'colaborador_id': 1, 'fecha_evaluacion': date(2023, 5, 15), 'evaluador': 'Supervisor A', 'factor_evaluacion': 4.5, 'calificacion': 'Good', 'comentarios': 'Excellent performance.'},
    {'id': 2, 'colaborador_id': 2, 'fecha_evaluacion': date(2023, 7, 10), 'evaluador': 'Supervisor B', 'factor_evaluacion': 3.8, 'calificacion': 'Fair', 'comentarios': 'Needs to improve teamwork.'},
    {'id': 3, 'colaborador_id': 3, 'fecha_evaluacion': date(2023, 3, 25), 'evaluador': 'Supervisor C', 'factor_evaluacion': 4.0, 'calificacion': 'Good', 'comentarios': 'Generally good performance.'},
    {'id': 4, 'colaborador_id': 4, 'fecha_evaluacion': date(2022, 12, 5), 'evaluador': 'Supervisor A', 'factor_evaluacion': 4.7, 'calificacion': 'Good', 'comentarios': 'Highly recommended for promotions.'},
    {'id': 5, 'colaborador_id': 5, 'fecha_evaluacion': date(2023, 1, 20), 'evaluador': 'Supervisor B', 'factor_evaluacion': 3.5, 'calificacion': 'Fair', 'comentarios': 'Could improve punctuality.'}
]

for data in evaluacion_data:
    evaluacion = Evaluacion(**data)
    session.add(evaluacion)
session.commit()

# Insert data into Capacitacion table
capacitacion_data = [
    {'id': 1, 'colaborador_id': 1, 'fecha_capacitacion': date(2023, 3, 5), 'curso': 'Advanced Python', 'calificacion': 4.5, 'institucion': 'Tech Academy', 'comentarios': 'Excellent participation.'},
    {'id': 2, 'colaborador_id': 2, 'fecha_capacitacion': date(2023, 4, 15), 'curso': 'Project Management', 'calificacion': 4.0, 'institucion': 'University A', 'comentarios': 'Good grasp of the subject.'},
    {'id': 3, 'colaborador_id': 3, 'fecha_capacitacion': date(2022, 11, 22), 'curso': 'Cybersecurity', 'calificacion': 3.8, 'institucion': 'Tech Institute', 'comentarios': 'Acceptable performance.'},
    {'id': 4, 'colaborador_id': 4, 'fecha_capacitacion': date(2022, 6, 18), 'curso': 'Digital Marketing', 'calificacion': 4.2, 'institucion': 'Online Academy', 'comentarios': 'Good tool mastery.'},
    {'id': 5, 'colaborador_id': 5, 'fecha_capacitacion': date(2023, 1, 10), 'curso': 'Scrum Master', 'calificacion': 3.5, 'institucion': 'Scrum Training', 'comentarios': 'Needs to improve leadership.'}
]

for data in capacitacion_data:
    capacitacion = Capacitacion(**data)
    session.add(capacitacion)
session.commit()

# Insert data into Remuneracion table
remuneracion_data = [
    {'id': 1, 'colaborador_id': 1, 'afp_id': 1, 'plan_salud_id': 1, 'monto_bruto': 2500.00, 'impuesto': 10.0, 'deducciones': 150.00, 'bonus': 200.00, 'aporte_bienestar': 50.00, 'monto_liquido': 2200.00},
    {'id': 2, 'colaborador_id': 2, 'afp_id': 2, 'plan_salud_id': 2, 'monto_bruto': 3000.00, 'impuesto': 12.0, 'deducciones': 200.00, 'bonus': 250.00, 'aporte_bienestar': 60.00, 'monto_liquido': 2650.00},
    {'id': 3, 'colaborador_id': 3, 'afp_id': 3, 'plan_salud_id': 3, 'monto_bruto': 2300.00, 'impuesto': 9.0, 'deducciones': 130.00, 'bonus': 150.00, 'aporte_bienestar': 40.00, 'monto_liquido': 2070.00},
    {'id': 4, 'colaborador_id': 4, 'afp_id': 4, 'plan_salud_id': 1, 'monto_bruto': 2800.00, 'impuesto': 11.0, 'deducciones': 180.00, 'bonus': 300.00, 'aporte_bienestar': 55.00, 'monto_liquido': 2455.00},
    {'id': 5, 'colaborador_id': 5, 'afp_id': 5, 'plan_salud_id': 2, 'monto_bruto': 2700.00, 'impuesto': 10.5, 'deducciones': 170.00, 'bonus': 280.00, 'aporte_bienestar': 50.00, 'monto_liquido': 2390.00}
]

for data in remuneracion_data:
    remuneracion = Remuneracion(**data)
    session.add(remuneracion)
session.commit()


# Insert user and password into User table
new_user = User(username='LBrownI')
new_user.set_password('Ingreso_07')
session.add(new_user)
session.commit()

# Close the session
session.close()
