from __future__ import annotations

from pathlib import Path

from app.constants.enums import SubGrupos
from core.domain.models import Categoria, Registro


def criar_diretorio(caminho: Path) -> None:
    caminho.mkdir(parents=True, exist_ok=True)


def nome_diretorio_registro(
    categoria_vinculada: Categoria, registro_principal: Registro
) -> str:
    sub_grupos = {sg.name: sg.value for sg in SubGrupos}
    for chave, valor in sub_grupos.items():
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

    return (
        f"{categoria_vinculada.id_registro}-padrao-"
        f"{categoria_vinculada.nome_categoria}".lower().strip()
    )
