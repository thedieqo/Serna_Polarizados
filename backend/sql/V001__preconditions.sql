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
