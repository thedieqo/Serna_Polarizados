import unittest
from audit import revisar

class AuditTests(unittest.TestCase):
    def test_correcto(self):
        self.assertEqual(revisar('SP1',100,{'cobro':{'pagos':[{'monto_cop':100}], 'pagado_cop':100,'comision_admin_cop':2,'saldo_cop':0}}),[])
    def test_detecta_diferencias(self):
        r=revisar('SP1',100,{'cobro':{'pagos':[{'monto_cop':80}], 'pagado_cop':90,'comision_admin_cop':5,'saldo_cop':20}})
        self.assertEqual(len(r),4)
    def test_incompleto(self):
        self.assertEqual(revisar('SP1',None,None)[0]['regla'],'DATOS_INCOMPLETOS')
