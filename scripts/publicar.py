#!/usr/bin/env python3
"""
Publica o primeiro recurso da fila.json na seção correspondente do README.md.

Roda todo dia via .github/workflows/publicar-diario.yml. Se a fila estiver
vazia, não muda nada (nenhum commit falso) e o workflow abre uma issue
lembrando de reabastecer.

Formato de cada item da fila:
  { "secao": "...", "nome": "...", "url": "https://...", "descricao": "..." }

Uso local: python scripts/publicar.py
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
FILA = ROOT / "fila.json"


def gh_output(**kwargs):
    """Expõe valores para os passos seguintes do workflow."""
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            for k, v in kwargs.items():
                f.write(f"{k}={v}\n")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    fila = json.loads(FILA.read_text(encoding="utf-8")) if FILA.exists() else []
    if not fila:
        print("FILA_VAZIA — nada a publicar hoje.")
        gh_output(nome="", vazia="1")
        return

    item = fila.pop(0)
    secao, nome = item["secao"], item["nome"]
    url, desc = item["url"], item["descricao"].rstrip(".")

    texto = README.read_text(encoding="utf-8")
    marcador = f"## {secao}\n"
    inicio = texto.find(marcador)
    if inicio == -1:
        raise SystemExit(f"erro: seção '{secao}' não existe no README — corrija a fila.json")

    # fim da seção = próximo título ou separador
    candidatos = [p for p in (texto.find("\n## ", inicio + len(marcador)),
                              texto.find("\n---", inicio + len(marcador))) if p != -1]
    fim = min(candidatos) if candidatos else len(texto)
    while texto[fim - 1] == "\n":
        fim -= 1

    entrada = f"\n- [{nome}]({url}) — {desc}."
    README.write_text(texto[:fim] + entrada + texto[fim:], encoding="utf-8")
    FILA.write_text(json.dumps(fila, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    restam = len(fila)
    print(f"PUBLICADO: {nome} (seção {secao}) — restam {restam} na fila")
    gh_output(nome=nome, vazia="1" if restam == 0 else "0")
    if restam <= 2:
        print(f"AVISO: só {restam} item(ns) na fila — hora de reabastecer!")


if __name__ == "__main__":
    main()
