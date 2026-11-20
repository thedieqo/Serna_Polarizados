DROP INDEX IF EXISTS public.instalacion_detalles_vidrio_panel_uniq;

DROP TABLE IF EXISTS public.instalacion_detalles;
DROP TABLE IF EXISTS public.catalogo_vidrios_polarizado;
DROP TABLE IF EXISTS public.catalogo_tipos_factura;
DROP TABLE IF EXISTS public.catalogo_instaladores;
DROP TABLE IF EXISTS public.catalogo_opacidades_polarizado;
DROP TABLE IF EXISTS public.catalogo_tecnologias_polarizado;

ALTER TABLE public.instalaciones DROP COLUMN IF EXISTS tipo_factura;
ALTER TABLE public.vehiculos DROP COLUMN IF EXISTS marca;
ALTER TABLE public.clientes DROP COLUMN IF EXISTS email;
ALTER TABLE public.clientes DROP COLUMN IF EXISTS telefono;
