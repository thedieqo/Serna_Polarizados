import importlib
import sys
import types
import unittest
from unittest.mock import patch, sentinel

from sqlalchemy.engine import URL


class SessionBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_config = types.ModuleType("app.core.config")
        cls.fake_config.settings = cls._settings()
        cls.modules_patch = patch.dict(
            sys.modules, {"app.core.config": cls.fake_config}
        )
        cls.modules_patch.start()
        cls.engine_patch = patch("sqlalchemy.create_engine")
        cls.create_engine = cls.engine_patch.start()
        cls.create_engine.return_value = sentinel.engine
        sys.modules.pop("app.db.session", None)
        cls.session_module = importlib.import_module("app.db.session")
        cls.addClassCleanup(sys.modules.pop, "app.db.session", None)
        cls.addClassCleanup(cls.engine_patch.stop)
        cls.addClassCleanup(cls.modules_patch.stop)

    def setUp(self):
        self.session_module = self.__class__.session_module
        self.create_engine = self.__class__.create_engine
        self.session_module.settings = self._settings()
        self.create_engine.reset_mock()

    @staticmethod
    def _settings(**overrides):
        values = {
            "DATABASE_URL": "postgresql://verify:verify@db.internal.test:5432/verify",
            "POSTGRES_USER": None,
            "POSTGRES_PASSWORD": None,
            "POSTGRES_HOST": None,
            "POSTGRES_PORT": None,
            "POSTGRES_DB": None,
        }
        values.update(overrides)
        return types.SimpleNamespace(**values)

    def _build_with(self, **overrides):
        self.session_module.settings = self._settings(**overrides)
        self.create_engine.reset_mock()
        return self.session_module._build_engine(), self.create_engine.call_args

    def test_url_connection_parameters_are_preserved(self):
        dsn = (
            "postgres://verify:p%2Fss%3Aword@db.internal.test:5432/verify"
            "?sslmode=require&sslrootcert=%2Ftmp%2Ffake-ca.pem"
            "&application_name=verify"
        )
        engine, call = self._build_with(DATABASE_URL=dsn)
        self.assertIs(engine, sentinel.engine)
        built_url = call.args[0]
        self.assertIsInstance(built_url, URL)
        self.assertEqual(built_url.drivername, "postgresql")
        self.assertEqual(built_url.query["sslmode"], "require")
        self.assertEqual(built_url.query["sslrootcert"], "/tmp/fake-ca.pem")
        self.assertEqual(built_url.query["application_name"], "verify")
        self.assertEqual(call.kwargs, {"pool_pre_ping": True})

    def test_escaped_credentials_are_decoded(self):
        dsn = (
            "postgresql://user%40domain:p%2Fss%3Aword%23x"
            "@db.internal.test:5432/verify?sslmode=require"
        )
        _, call = self._build_with(DATABASE_URL=dsn)
        built_url = call.args[0]
        self.assertEqual(built_url.username, "user@domain")
        self.assertEqual(built_url.password, "p/ss:word#x")
        self.assertEqual(built_url.host, "db.internal.test")
        self.assertEqual(built_url.query["sslmode"], "require")

    def test_component_configuration_remains_supported(self):
        _, call = self._build_with(
            DATABASE_URL="not-a-url",
            POSTGRES_USER="component_user",
            POSTGRES_PASSWORD="component_pass",
            POSTGRES_HOST="db.components.test",
            POSTGRES_PORT=5433,
            POSTGRES_DB="component_db",
        )
        built_url = call.args[0]
        self.assertIsInstance(built_url, URL)
        self.assertEqual(built_url.drivername, "postgresql")
        self.assertEqual(built_url.username, "component_user")
        self.assertEqual(built_url.password, "component_pass")
        self.assertEqual(built_url.host, "db.components.test")
        self.assertEqual(built_url.port, 5433)
        self.assertEqual(built_url.database, "component_db")
        self.assertEqual(dict(built_url.query), {})

    def test_no_real_connection_is_created(self):
        with patch("psycopg2.connect") as dbapi_connect:
            _, call = self._build_with()
        dbapi_connect.assert_not_called()
        self.assertIsInstance(call.args[0], URL)
        self.create_engine.assert_called_once()

    def test_malformed_url_error_does_not_expose_credentials(self):
        with self.assertRaises(RuntimeError) as caught:
            self._build_with(
                DATABASE_URL=(
                    "postgresql://verify:p%2Fss%3Aword%23x"
                    "@db.internal.test:notaport/verify"
                )
            )
        self.assertIsNone(caught.exception.__cause__)
        self.assertNotIn("p/ss:word#x", str(caught.exception))
        self.assertNotIn("p%2Fss%3Aword%23x", str(caught.exception))
        self.assertNotIn("verify", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
