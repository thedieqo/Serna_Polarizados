DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'clientes'
    ) THEN
        RAISE EXCEPTION 'Falta la tabla public.clientes';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'vehiculos'
    ) THEN
        RAISE EXCEPTION 'Falta la tabla public.vehiculos';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'instalaciones'
    ) THEN
        RAISE EXCEPTION 'Falta la tabla public.instalaciones';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_indexes
        WHERE schemaname = 'public'
          AND tablename = 'clientes'
          AND indexdef ILIKE '%UNIQUE%'
          AND indexdef LIKE '%(documento)%'
    ) THEN
        RAISE EXCEPTION 'Falta restricción única en public.clientes.documento';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_indexes
        WHERE schemaname = 'public'
          AND tablename = 'vehiculos'
          AND indexdef ILIKE '%UNIQUE%'
          AND indexdef LIKE '%(placa)%'
    ) THEN
        RAISE EXCEPTION 'Falta restricción única en public.vehiculos.placa';
    END IF;
END $$;

ALTER TABLE public.clientes ADD COLUMN IF NOT EXISTS telefono text;
ALTER TABLE public.clientes ADD COLUMN IF NOT EXISTS email text;
ALTER TABLE public.vehiculos ADD COLUMN IF NOT EXISTS marca text;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS tipo_factura text;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'instalaciones_tipo_factura_check'
    ) THEN
        ALTER TABLE public.instalaciones
        ADD CONSTRAINT instalaciones_tipo_factura_check
        CHECK (tipo_factura IN ('normal', 'electronica'));
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS public.catalogo_tecnologias_polarizado (
    id text PRIMARY KEY,
    label text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.catalogo_opacidades_polarizado (
    id text PRIMARY KEY,
    label text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.catalogo_instaladores (
    id text PRIMARY KEY,
    label text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.catalogo_tipos_factura (
    id text PRIMARY KEY,
    label text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.catalogo_vidrios_polarizado (
    id text PRIMARY KEY,
    label text NOT NULL,
    paneles text[] NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS public.instalacion_detalles (
    id bigserial PRIMARY KEY,
    instalacion_id integer NOT NULL REFERENCES public.instalaciones(id) ON DELETE CASCADE,
    vidrio_id text NOT NULL REFERENCES public.catalogo_vidrios_polarizado(id),
    panel text,
    tecnologia_id text NOT NULL REFERENCES public.catalogo_tecnologias_polarizado(id),
    opacidad_id text NOT NULL REFERENCES public.catalogo_opacidades_polarizado(id),
    instalador_id text NOT NULL REFERENCES public.catalogo_instaladores(id),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT instalacion_detalles_vidrio_panel_check CHECK (
        (vidrio_id = 'sunroof_doble' AND panel IN ('delantero', 'trasero'))
        OR (vidrio_id <> 'sunroof_doble' AND panel IS NULL)
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS instalacion_detalles_vidrio_panel_uniq
ON public.instalacion_detalles (
    instalacion_id,
    vidrio_id,
    COALESCE(panel, 'unico')
);

INSERT INTO public.catalogo_tecnologias_polarizado (id, label) VALUES
    ('high_definition_premium', 'High Definition Premium'),
    ('ultra_hd', 'Ultra HD'),
    ('color_stable', 'Color Stable'),
    ('ceramic_ir', 'Ceramic IR')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.catalogo_opacidades_polarizado (id, label) VALUES
    ('5', '5 %'),
    ('20', '20 %'),
    ('35', '35 %')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.catalogo_instaladores (id, label) VALUES
    ('daniel_mira', 'Daniel Mira'),
    ('joseth_mora', 'Joseth Mora')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.catalogo_tipos_factura (id, label) VALUES
    ('normal', 'Normal'),
    ('electronica', 'Electrónica')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.catalogo_vidrios_polarizado (id, label, paneles) VALUES
    ('parabrisas', 'Parabrisas', '{}'),
    ('laterales_delanteros', 'Laterales delanteros', '{}'),
    ('laterales_traseros', 'Laterales traseros', '{}'),
    ('luneta', 'Luneta', '{}'),
    ('sunroof_simple', 'Techo solar simple', '{}'),
    ('sunroof_doble', 'Techo solar doble', ARRAY['delantero', 'trasero'])
ON CONFLICT (id) DO NOTHING;
