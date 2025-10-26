from __future__ import annotations

from typing import Dict

from app.models.entities import AdvertiserType


def validate_advertiser_payload(payload: Dict[str, str]) -> None:
    advertiser_type = payload.get("advertiser_type")
    document_status = payload.get("document_status")
    metadata = payload.get("metadata", {})

    if not advertiser_type:
        raise ValueError("advertiser_type é obrigatório")

    try:
        adv_type = AdvertiserType(advertiser_type)
    except ValueError as exc:
        raise ValueError("Tipo de anunciante inválido") from exc

    if document_status != "active":
        raise ValueError("Documento deve estar com status ativo")

    if adv_type is AdvertiserType.BROKER:
        creci = metadata.get("creci")
        if not creci:
            raise ValueError("CRECI obrigatório para corretores")
    elif adv_type is AdvertiserType.AGENCY:
        cnpj = metadata.get("cnpj")
        if not cnpj:
            raise ValueError("CNPJ obrigatório para imobiliárias")
    elif adv_type is AdvertiserType.DEVELOPER:
        cnpj = metadata.get("cnpj")
        if not cnpj:
            raise ValueError("CNPJ obrigatório para incorporadoras")
        if not metadata.get("portfolio_url"):
            raise ValueError("portfolio_url obrigatório para incorporadoras")

