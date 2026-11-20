ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS desglose_precios jsonb;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS tarifas_aplicadas jsonb;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS moneda text;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS precio_estado text;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS precio_total_cop bigint;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'instalaciones_precio_estado_check'
    ) THEN
        ALTER TABLE public.instalaciones
        ADD CONSTRAINT instalaciones_precio_estado_check
        CHECK (precio_estado IN ('definido', 'pendiente'));
    END IF;
END $$;
