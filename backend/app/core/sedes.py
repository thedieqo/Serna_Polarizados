"""Catálogo cerrado: nunca aceptar nombres de esquema enviados por el cliente."""
SEDES = {'el-carmen': {'nombre': 'El Carmen (Ibagué)', 'correo': None, 'schema': 'public'}, 'mirolindo': {'nombre': 'Mirolindo (Ibagué)', 'correo': None, 'schema': 'sede_mirolindo'}, 'usaquen': {'nombre': 'Usaquén (Bogotá)', 'correo': 'usaquensp@gmail.com', 'schema': 'sede_usaquen'}, '1ra-de-mayo': {'nombre': '1ra de Mayo (Bogotá)', 'correo': '1rademayosp@gmail.com', 'schema': 'sede_1ra_de_mayo'}, 'ciudad-montes': {'nombre': 'Ciudad Montes (Bogotá)', 'correo': 'ciudadmontessp@gmail.com', 'schema': 'sede_ciudad_montes'}, 'prado-veraniego': {'nombre': 'Prado Veraniego (Bogotá)', 'correo': 'pradoveraniegosp@gmail.com', 'schema': 'sede_prado_veraniego'}, 'cali': {'nombre': 'Cali (Cali)', 'correo': 'calisp@gmail.com', 'schema': 'sede_cali'}, 'pereira': {'nombre': 'Pereira (Pereira)', 'correo': 'pereirasp@gmail.com', 'schema': 'sede_pereira'}, 'bucaramanga': {'nombre': 'Bucaramanga (Bucaramanga)', 'correo': 'bucaramangasp@gmail.com', 'schema': 'sede_bucaramanga'}, 'tunja': {'nombre': 'Tunja (Tunja)', 'correo': 'tunjasp@gmail.com', 'schema': 'sede_tunja'}, 'pasto': {'nombre': 'Pasto (Pasto)', 'correo': 'pastosp@gmail.com', 'schema': 'sede_pasto'}}

SEDES.update({'7-de-agosto': {'nombre':'7 de Agosto (Bogotá)','correo':'','schema':'sede_7_de_agosto'}, 'porvenir': {'nombre':'Porvenir (Villavicencio)','correo':'','schema':'sede_porvenir'}, 'santo-tomas': {'nombre':'Santo Tomás (Villavicencio)','correo':'','schema':'sede_santo_tomas'}})

CORREO_EL_CARMEN = 'sernapolarizadosibague.1@gmail.com'

def permitidas(email, settings):
    email = email.strip().lower()
    if email == CORREO_EL_CARMEN:
        return ['el-carmen'] if email in settings.admin_emails else []
    return [k for k,v in SEDES.items() if (email in settings.admin_emails if v['correo'] is None else email == v['correo'])]
