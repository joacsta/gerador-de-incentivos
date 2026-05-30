from __future__ import annotations

from pathlib import Path

from app.constants import REDES
from core.domain.models import Campanha, GrupoProduto


def criar_diretorio_campanha(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def criar_diretorio_campanha_dev(base_path: Path, diretorio_nome_campanha: str) -> str:
    caminho_diretorio = base_path / "templates" / diretorio_nome_campanha
    caminho_diretorio.mkdir(parents=True, exist_ok=True)
    return str(caminho_diretorio)


def nome_campanha_diretorio(grupo_produto: GrupoProduto, campanha: Campanha) -> str:
    segmento = next(
        (key for key, value in REDES.items() if value == campanha.tipo_participante),
        "segmento",
    )
    slug_segmento = (
        segmento.strip().lower().replace(" ", "-").replace("(", "").replace(")", "")
    )
    return (
        (
            f"{grupo_produto.id_campanha}-programa-"
            f"{grupo_produto.nome_grupo_produto}-{slug_segmento}"
        )
        .lower()
        .strip()
    )
