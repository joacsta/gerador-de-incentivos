from __future__ import annotations

from pathlib import Path

from app.constants import SUB_GRUPOS
from core.domain.models import Registro, Categoria


def criar_diretorio(caminho_str: str) -> None:
    caminho = Path(caminho_str)
    caminho.mkdir(parents=True, exist_ok=True)


def nome_diretorio_registro(
    categoria_vinculada: Categoria, registro_principal: Registro
):
    for chave, valor in SUB_GRUPOS.items():
        if registro_principal.tipo_registro in (10, 12):
            return (
                (
                    f"{categoria_vinculada.id_registro}-especial-"
                    f"{categoria_vinculada.nome_categoria}-"
                    f"{
                        chave.strip()
                        .lower()
                        .replace(' ', '-')
                        .replace('(', '')
                        .replace(')', '')
                        .replace('|', '-')
                    }"
                )
                .lower()
                .strip()
            )
        if valor == registro_principal.tipo_participante:
            return (
                (
                    f"{categoria_vinculada.id_registro}-padrao-"
                    f"{categoria_vinculada.nome_categoria}-"
                    f"{
                        chave.strip()
                        .lower()
                        .replace(' ', '-')
                        .replace('(', '')
                        .replace(')', '')
                        .replace('|', '')
                    }"
                )
                .lower()
                .strip()
            )
