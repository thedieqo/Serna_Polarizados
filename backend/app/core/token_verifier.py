import json
import logging
import time
from dataclasses import dataclass
from functools import lru_cache
from types import SimpleNamespace
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import jwt
from fastapi import Depends
from jwt import PyJWKClient

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


class TokenVerificationError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 401):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


@dataclass(frozen=True)
class VerifiedIdentity:
    email: str
    email_verified: bool
    subject: str
    role: str | None = None


_ALLOWED_ALGORITHMS = frozenset({"ES256", "ES384", "ES512", "RS256", "RS384", "RS512", "EdDSA"})


class SupabaseTokenVerifier:
    def __init__(self, settings: Settings):
        self.base_url = (settings.SUPABASE_URL or "").rstrip("/")
        self.publishable_key = settings.SUPABASE_PUBLISHABLE_KEY
        self.issuer = settings.SUPABASE_JWT_ISSUER or f"{self.base_url}/auth/v1"
        self.audience = settings.SUPABASE_JWT_AUDIENCE or "authenticated"
        self.mode = (settings.SUPABASE_VERIFY_MODE or "jwks").strip().lower()
        self.jwks_url = settings.SUPABASE_JWKS_URL or f"{self.base_url}/auth/v1/.well-known/jwks.json"
        self._jwks_client = (
            PyJWKClient(self.jwks_url, cache_keys=True, lifespan=600)
            if self.mode == "jwks" and self.jwks_url.startswith(("http://", "https://"))
            else None
        )

    def verify(self, token: str) -> VerifiedIdentity:
        if not self.base_url:
            raise TokenVerificationError(
                "AUTH_CONFIG_INCOMPLETA", "La autenticación no está configurada", 503
            )
        if self.mode == "jwks":
            return self._verify_with_jwks(token)
        if self.mode == "auth_server":
            return self._verify_with_auth_server(token)
        raise TokenVerificationError(
            "MODO_VERIFICACION_INVALIDO", "El modo de verificación no es válido", 503
        )

    def _fetch_user_profile(self, token: str) -> dict[str, Any]:
        if not self.publishable_key:
            raise TokenVerificationError(
                "AUTH_CONFIG_INCOMPLETA", "La autenticación no está configurada", 503
            )
        request = Request(
            f"{self.base_url}/auth/v1/user",
            headers={
                "apikey": self.publishable_key,
                "Authorization": f"Bearer {token}",
            },
        )
        try:
            with urlopen(request, timeout=5) as response:
                user_payload = json.load(response)
        except HTTPError as exc:
            if exc.code in (401, 403):
                raise TokenVerificationError("TOKEN_INVALIDO", "Token de sesión inválido") from exc
            raise TokenVerificationError("AUTH_NO_DISPONIBLE", "No fue posible validar la sesión", 503) from exc
        except (URLError, TimeoutError, ValueError) as exc:
            raise TokenVerificationError("AUTH_NO_DISPONIBLE", "No fue posible validar la sesión", 503) from exc
        if not isinstance(user_payload, dict):
            raise TokenVerificationError("TOKEN_INVALIDO", "Token de sesión inválido")
        return user_payload

    def _verify_with_jwks(self, token: str) -> VerifiedIdentity:
        if self._jwks_client is None:
            raise TokenVerificationError(
                "AUTH_CONFIG_INCOMPLETA", "La autenticación no está configurada", 503
            )
        try:
            header = jwt.get_unverified_header(token)
        except Exception as exc:
            raise TokenVerificationError("TOKEN_INVALIDO", "Token de sesión inválido") from exc

        algorithm = header.get("alg")
        key_id = header.get("kid")
        if algorithm not in _ALLOWED_ALGORITHMS:
            raise TokenVerificationError("ALGORITMO_NO_PERMITIDO", "Token de sesión inválido")
        if not key_id:
            raise TokenVerificationError("CLAVE_NO_IDENTIFICADA", "Token de sesión inválido")

        try:
            signing_key = self._jwks_client.get_signing_key(key_id).key
        except Exception as exc:
            raise TokenVerificationError("CLAVE_NO_DISPONIBLE", "No fue posible validar la sesión", 503) from exc

        try:
            claims = jwt.decode(
                token,
                signing_key,
                algorithms=[algorithm],
                audience=self.audience,
                issuer=self.issuer,
                options={
                    "require": ["exp", "iss", "aud", "sub", "role", "email"]
                },
            )
        except Exception as exc:
            missing_claim = getattr(exc, "claim", None)
            logger.warning(
                "token_rejected category=TOKEN_INVALIDO reason=JWT_DECODE detail=%s",
                missing_claim or exc.__class__.__name__,
            )
            raise TokenVerificationError("TOKEN_INVALIDO", "Token de sesión inválido") from exc

        user_profile = self._fetch_user_profile(token)
        claims["email"] = user_profile.get("email") or claims.get("email")
        return self._identity_from_claims(claims, user_profile)

    def _verify_with_auth_server(self, token: str) -> VerifiedIdentity:
        if not self.publishable_key:
            raise TokenVerificationError(
                "AUTH_CONFIG_INCOMPLETA", "La autenticación no está configurada", 503
            )

        user_payload = self._fetch_user_profile(token)

        try:
            claims = jwt.decode(
                token,
                options={
                    "verify_signature": False,
                    "verify_exp": False,
                    "verify_aud": False,
                    "verify_iss": False,
                },
            )
        except Exception as exc:
            raise TokenVerificationError("TOKEN_INVALIDO", "Token de sesión inválido") from exc

        if claims.get("iss") != self.issuer or not self._audience_matches(claims.get("aud")):
            raise TokenVerificationError("TOKEN_INVALIDO", "Token de sesión inválido")
        if not claims.get("exp") or int(claims["exp"]) <= time.time():
            raise TokenVerificationError("TOKEN_EXPIRADO", "La sesión ha expirado")

        claims["email"] = user_payload.get("email") or claims.get("email")
        claims["role"] = user_payload.get("role") or claims.get("role")
        return self._identity_from_claims(claims, user_payload)

    def _audience_matches(self, audience: Any) -> bool:
        if isinstance(audience, str):
            return audience == self.audience
        if isinstance(audience, (list, tuple, set)):
            return self.audience in audience
        return False

    def _identity_from_claims(
        self, claims: dict[str, Any], user_profile: dict[str, Any] | None = None
    ) -> VerifiedIdentity:
        email = claims.get("email")
        subject = claims.get("sub")
        if (
            not isinstance(email, str)
            or not email.strip()
            or not isinstance(subject, str)
            or not subject
            or claims.get("role") != "authenticated"
        ):
            raise TokenVerificationError("TOKEN_INVALIDO", "Token de sesión inválido")
        confirmed_at = None
        if user_profile:
            confirmed_at = user_profile.get("email_confirmed_at") or user_profile.get("confirmed_at")
        return VerifiedIdentity(
            email=email.strip().lower(),
            email_verified=bool(confirmed_at),
            subject=subject,
            role=claims.get("role"),
        )


@lru_cache(maxsize=8)
def _cached_verifier(
    base_url: str,
    publishable_key: str | None,
    jwks_url: str,
    issuer: str,
    audience: str,
    mode: str,
) -> SupabaseTokenVerifier:
    fake_settings = SimpleNamespace(
        SUPABASE_URL=base_url,
        SUPABASE_PUBLISHABLE_KEY=publishable_key,
        SUPABASE_JWKS_URL=jwks_url,
        SUPABASE_JWT_ISSUER=issuer,
        SUPABASE_JWT_AUDIENCE=audience,
        SUPABASE_VERIFY_MODE=mode,
    )
    return SupabaseTokenVerifier(fake_settings)


def build_verifier(settings: Settings) -> SupabaseTokenVerifier | None:
    base_url = (settings.SUPABASE_URL or "").rstrip("/")
    if not base_url:
        return None
    return _cached_verifier(
        base_url,
        settings.SUPABASE_PUBLISHABLE_KEY,
        settings.SUPABASE_JWKS_URL or f"{base_url}/auth/v1/.well-known/jwks.json",
        settings.SUPABASE_JWT_ISSUER or f"{base_url}/auth/v1",
        settings.SUPABASE_JWT_AUDIENCE or "authenticated",
        (settings.SUPABASE_VERIFY_MODE or "jwks").strip().lower(),
    )


def get_token_verifier(
    settings: Settings = Depends(get_settings),
) -> SupabaseTokenVerifier | None:
    return build_verifier(settings)
