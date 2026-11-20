"""Datos exclusivamente ficticios, creados en una SQLite temporal, nunca en Supabase."""
import sys
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'backend'))
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.base import Base
from app.models.cliente import Cliente
from app.models.vehiculo import Vehiculo
from app.models.instalacion import Instalacion


def crear_demo(ruta):
    engine = create_engine('sqlite:///' + str(ruta))
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        cliente = Cliente(nombre='Cliente demostración',documento='DEMO001',contacto='NO REAL')
        db.add(cliente);db.flush()
        vehiculo = Vehiculo(placa='DEM123',marca='Mazda',cliente_id=cliente.id)
        db.add(vehiculo);db.flush()
        zonas=[{'vidrio':v,'tecnologia':'High Definition Premium','opacidad':'20 %'} for v in ['Parabrisas','Laterales delanteros','Laterales traseros','Luneta']]
        asignaciones=[{'vidrio':z['vidrio'],'panel':None,'instalador':'Instalador demo'} for z in zonas]
        db.add(Instalacion(vehiculo_id=vehiculo.id,fecha=datetime.now(timezone.utc),tipo_servicio='polarizado',estado='finalizado',
            zonas=zonas,asignaciones_instaladores=asignaciones,precio_total_cop=900000,tipo_factura='normal',
            desglose_precios={'cobro':{'descuento_cop':100000,'pagado_cop':900000,'saldo_cop':0,'comision_admin_cop':18000,
                'pagos':[{'medio':'transferencia','monto_cop':600000},{'medio':'efectivo','monto_cop':300000}]},
                'mano_obra':[{'instalador_id':'demo','instalador':'Instalador demo','vidrio':z['vidrio'],'panel':None,'valor_cop':25000} for z in zonas]}))
        db.commit()
    engine.dispose()
