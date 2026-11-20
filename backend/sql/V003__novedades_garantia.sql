DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'instalaciones'
    ) THEN
        RAISE EXCEPTION 'Falta la tabla public.instalaciones';
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS public.instalacion_novedades (
    id bigserial PRIMARY KEY,
    instalacion_id integer NOT NULL REFERENCES public.instalaciones(id) ON DELETE CASCADE,
    fecha_atencion timestamptz NOT NULL,
    motivo text NOT NULL,
    descripcion text NOT NULL,
    registrado_por text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS instalacion_novedades_instalacion_fecha_idx
ON public.instalacion_novedades (instalacion_id, fecha_atencion DESC);
