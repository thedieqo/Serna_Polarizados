ALTER TABLE public.clientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vehiculos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.instalaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.catalogo_tecnologias_polarizado ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.catalogo_opacidades_polarizado ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.catalogo_instaladores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.catalogo_tipos_factura ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.catalogo_vidrios_polarizado ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.instalacion_detalles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.instalacion_novedades ENABLE ROW LEVEL SECURITY;

REVOKE ALL ON TABLE public.clientes, public.vehiculos, public.instalaciones, public.catalogo_tecnologias_polarizado, public.catalogo_opacidades_polarizado, public.catalogo_instaladores, public.catalogo_tipos_factura, public.catalogo_vidrios_polarizado, public.instalacion_detalles, public.instalacion_novedades FROM anon, authenticated;

REVOKE ALL ON SEQUENCE public.clientes_id_seq, public.vehiculos_id_seq, public.instalaciones_id_seq, public.instalacion_detalles_id_seq, public.instalacion_novedades_id_seq FROM anon, authenticated;

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.clientes, public.vehiculos, public.instalaciones, public.catalogo_tecnologias_polarizado, public.catalogo_opacidades_polarizado, public.catalogo_instaladores, public.catalogo_tipos_factura, public.catalogo_vidrios_polarizado, public.instalacion_detalles, public.instalacion_novedades TO postgres;

GRANT USAGE, SELECT ON SEQUENCE public.clientes_id_seq, public.vehiculos_id_seq, public.instalaciones_id_seq, public.instalacion_detalles_id_seq, public.instalacion_novedades_id_seq TO postgres;

SELECT pg_notify('pgrst', 'reload schema');
