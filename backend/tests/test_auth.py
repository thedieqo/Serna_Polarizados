import asyncio
import time
from dataclasses import dataclass
from unittest import TestCase
from unittest.mock import patch

import jwt
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi import HTTPException

from app.core.auth import (
    auth_ready,
    get_current_identity,
    require_admin_identity,
    require_write_access,
    write_enabled,
)
from app.core.config import Settings
from app.core.token_verifier import (
    SupabaseTokenVerifier,
    TokenVerificationError,
    VerifiedIdentity,
)
from app.main import app


SUPABASE_URL = "https://example.supabase.co"
ADMIN_EMAILS = "admin.1@example.com,admin.2@example.com"


def configured_settings(**overrides):
    values = {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_PUBLISHABLE_KEY": "sb_publishable_test_only",
        "SUPABASE_VERIFY_MODE": "jwks",
        "ADMIN_EMAILS": ADMIN_EMAILS,
        "REGISTRO_WRITE_ENABLED": False,
    }
    values.update(overrides)
    return Settings(**values)


class FakeVerifier:
    def __init__(self, identity=None, error=None):
        self.identity = identity
        self.error = error

    def verify(self, token: str):
        if self.error:
            raise self.error
        return self.identity


@dataclass
class FakeSigningKey:
    key: object


class AuthDependencyTests(TestCase):
    def setUp(self):
        self.settings = configured_settings()
        self.admin = VerifiedIdentity(
            email="admin.1@example.com",
            email_verified=True,
            subject="user-test",
            role="authenticated",
        )

    def test_auth_ready_requires_url_publishable_key_and_admins(self):
        self.assertTrue(auth_ready(self.settings))
        self.assertFalse(auth_ready(configured_settings(ADMIN_EMAILS="")))
        self.assertFalse(auth_ready(configured_settings(SUPABASE_PUBLISHABLE_KEY=None)))
        self.assertFalse(write_enabled(self.settings))

    def test_write_access_permanece_cerrado(self):
        with self.assertRaises(HTTPException) as contexto:
            asyncio.run(require_write_access(self.settings))
        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(
            contexto.exception.detail["code"], "ESCRITURA_NO_HABILITADA"
        )

    def test_sesion_ausente(self):
        with self.assertRaises(HTTPException) as contexto:
            asyncio.run(
                get_current_identity(
                    authorization=None, verifier=FakeVerifier(), settings=self.settings
                )
            )
        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(
            contexto.exception.detail["code"], "AUTENTICACION_REQUERIDA"
        )

    def test_sesion_ausente_sin_configuracion_devuelve_401(self):
        sin_configurar = configured_settings(SUPABASE_URL=None)
        with self.assertRaises(HTTPException) as contexto:
            asyncio.run(
                get_current_identity(
                    authorization=None, verifier=None, settings=sin_configurar
                )
            )
        self.assertEqual(contexto.exception.status_code, 401)

    def test_token_presente_sin_configuracion_devuelve_503(self):
        sin_configurar = configured_settings(SUPABASE_URL=None)
        with self.assertRaises(HTTPException) as contexto:
            asyncio.run(
                get_current_identity(
                    authorization="Bearer token-local", verifier=None, settings=sin_configurar
                )
            )
        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(
            contexto.exception.detail["code"], "AUTENTICACION_NO_CONFIGURADA"
        )

    def test_token_invalido(self):
        error = TokenVerificationError("TOKEN_INVALIDO", "Token de sesión inválido")
        with self.assertRaises(HTTPException) as contexto:
            asyncio.run(
                get_current_identity(
                    authorization="Bearer token-invalido",
                    verifier=FakeVerifier(error=error),
                    settings=self.settings,
                )
            )
        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(contexto.exception.detail["code"], "TOKEN_INVALIDO")

    def test_token_expirado(self):
        error = TokenVerificationError("TOKEN_EXPIRADO", "La sesión ha expirado")
        with self.assertRaises(HTTPException) as contexto:
            asyncio.run(
                get_current_identity(
                    authorization="Bearer token-expirado",
                    verifier=FakeVerifier(error=error),
                    settings=self.settings,
                )
            )
        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(contexto.exception.detail["code"], "TOKEN_EXPIRADO")

    def test_administrador_permitido(self):
        resultado = asyncio.run(
            require_admin_identity(identity=self.admin, settings=self.settings)
        )
        self.assertEqual(resultado, "admin.1@example.com")

    def test_segundo_administrador_permitido(self):
        identidad = VerifiedIdentity(
            email="admin.2@example.com",
            email_verified=True,
            subject="user-test-2",
            role="authenticated",
        )
        resultado = asyncio.run(
            require_admin_identity(identity=identidad, settings=self.settings)
        )
        self.assertEqual(resultado, "admin.2@example.com")

    def test_correo_no_verificado(self):
        identidad = VerifiedIdentity(
            email="admin.1@example.com",
            email_verified=False,
            subject="user-test",
            role="authenticated",
        )
        with self.assertRaises(HTTPException) as contexto:
            asyncio.run(
                require_admin_identity(identity=identidad, settings=self.settings)
            )
        self.assertEqual(contexto.exception.status_code, 403)
        self.assertEqual(contexto.exception.detail["code"], "CORREO_NO_VERIFICADO")

    def test_usuario_no_autorizado(self):
        identidad = VerifiedIdentity(
            email="otro@example.com",
            email_verified=True,
            subject="user-test-3",
            role="authenticated",
        )
        with self.assertRaises(HTTPException) as contexto:
            asyncio.run(
                require_admin_identity(identity=identidad, settings=self.settings)
            )
        self.assertEqual(contexto.exception.status_code, 403)
        self.assertEqual(contexto.exception.detail["code"], "USUARIO_NO_AUTORIZADO")


class SupabaseVerifierTests(TestCase):
    def setUp(self):
        self.settings = configured_settings()
        self.verifier = SupabaseTokenVerifier(self.settings)
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()

    def _token(self, **claim_overrides):
        ahora = int(time.time())
        claims = {
            "aud": "authenticated",
            "iss": f"{SUPABASE_URL}/auth/v1",
            "sub": "user-local-test",
            "role": "authenticated",
            "email": "admin.1@example.com",
            "iat": ahora,
            "exp": ahora + 300,
        }
        claims.update(claim_overrides)
        return jwt.encode(
            claims,
            self.private_key,
            algorithm="ES256",
            headers={"kid": "test-kid"},
        )

    def _verify(self, token, profile=None):
        profile = profile if profile is not None else {
            "email": "admin.1@example.com",
            "email_confirmed_at": "2026-01-01T00:00:00Z",
            "role": "authenticated",
        }
        with patch.object(
            self.verifier._jwks_client,
            "get_signing_key",
            return_value=FakeSigningKey(self.public_key),
        ), patch.object(
            self.verifier, "_fetch_user_profile", return_value=profile
        ):
            return self.verifier.verify(token)

    def test_verifica_firma_emisor_audiencia_y_expiracion(self):
        identidad = self._verify(self._token())
        self.assertEqual(identidad.email, "admin.1@example.com")
        self.assertTrue(identidad.email_verified)

    def test_token_sin_claim_email_verified_es_aceptado_si_perfil_lo_confirma(self):
        identidad = self._verify(self._token())
        self.assertTrue(identidad.email_verified)

    def test_no_confia_en_claim_email_verified_si_perfil_no_lo_confirma(self):
        identidad = self._verify(
            self._token(email_verified=True),
            profile={
                "email": "admin.1@example.com",
                "email_confirmed_at": None,
                "role": "authenticated",
            },
        )
        self.assertFalse(identidad.email_verified)
        with self.assertRaises(HTTPException) as contexto:
            asyncio.run(
                require_admin_identity(identity=identidad, settings=configured_settings())
            )
        self.assertEqual(contexto.exception.status_code, 403)
        self.assertEqual(contexto.exception.detail["code"], "CORREO_NO_VERIFICADO")

    def test_fallo_del_perfil_de_usuario_devuelve_503(self):
        error = TokenVerificationError("AUTH_NO_DISPONIBLE", "No fue posible validar la sesión", 503)
        with patch.object(
            self.verifier._jwks_client,
            "get_signing_key",
            return_value=FakeSigningKey(self.public_key),
        ), patch.object(
            self.verifier, "_fetch_user_profile", side_effect=error
        ):
            with self.assertRaises(TokenVerificationError) as contexto:
                self.verifier.verify(self._token())
        self.assertEqual(contexto.exception.code, "AUTH_NO_DISPONIBLE")
        self.assertEqual(contexto.exception.status_code, 503)

    def test_rechaza_token_expirado(self):
        with self.assertRaises(TokenVerificationError):
            self._verify(self._token(exp=int(time.time()) - 10))

    def test_rechaza_otro_issuer(self):
        with self.assertRaises(TokenVerificationError):
            self._verify(self._token(iss="https://otro.supabase.co/auth/v1"))

    def test_rechaza_otra_audiencia(self):
        with self.assertRaises(TokenVerificationError):
            self._verify(self._token(aud="service_role"))

    def test_rechaza_algoritmo_no_asimetrico(self):
        token = jwt.encode(
            {"sub": "x"}, "clave-local-de-prueba-sin-uso-real-123456", algorithm="HS256"
        )
        with self.assertRaises(TokenVerificationError) as contexto:
            self.verifier.verify(token)
        self.assertEqual(contexto.exception.code, "ALGORITMO_NO_PERMITIDO")


class RoutingProtectionTests(TestCase):
    def test_rutas_de_negocio_exigen_administrador(self):
        from app.core.auth import require_sede, require_role_access

        business_routes = [
            route
            for route in app.routes
            if getattr(route, "path", "").startswith("/api/v1/")
            and not getattr(route, "path", "").startswith(("/api/v1/auth/", "/api/v1/soporte/", "/api/v1/gerencia/gestion/", "/api/v1/personal/"))
        ]
        self.assertTrue(business_routes)
        for route in business_routes:
            dependencias = [
                dependencia.call for dependencia in route.dependant.dependencies
            ]
            self.assertIn(require_sede, dependencias, route.path)
            self.assertIn(require_role_access, dependencias, route.path)

    def test_salud_no_expone_datos_personales(self):
        health_paths = {
            getattr(route, "path", "")
            for route in app.routes
            if getattr(route, "path", "") in ("/", "/health")
        }
        self.assertEqual(health_paths, {"/", "/health"})


if __name__ == "__main__":
    pass
