#!/usr/bin/env python3
"""
Publica o primeiro recurso da fila.json na seção correspondente do README.md,
registra em publicados.json e regenera o feed RSS (feed.xml).

Roda todo dia via .github/workflows/publicar-diario.yml. Se a fila estiver
vazia, não muda nada (nenhum commit falso) e o workflow abre uma issue
lembrando de reabastecer.

Uso:
  python scripts/publicar.py         # publica o próximo da fila
  python scripts/publicar.py feed    # só regenera o feed.xml
"""
import json
import os
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
FILA = ROOT / "fila.json"
PUBLICADOS = ROOT / "publicados.json"
FEED = ROOT / "feed.xml"

REPO_URL = "https://github.com/paulapeclat/awesome-educacao-midiatica"
FEED_URL = "https://raw.githubusercontent.com/paulapeclat/awesome-educacao-midiatica/main/feed.xml"


def gh_output(**kwargs):
    """Expõe valores para os passos seguintes do workflow."""
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            for k, v in kwargs.items():
                f.write(f"{k}={v}\n")


def carregar(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def salvar(path, dados):
    path.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def gerar_feed(publicados):
    """RSS 2.0 com as 20 publicações mais recentes."""
    itens = []
    for p in reversed(publicados[-20:]):
        dt = datetime.fromisoformat(p["data"]).replace(tzinfo=timezone.utc)
        itens.append(f"""    <item>
      <title>{escape(p["nome"])}</title>
      <link>{escape(p["url"])}</link>
      <guid isPermaLink="false">{escape(p["url"])}#{p["data"][:10]}</guid>
      <pubDate>{format_datetime(dt)}</pubDate>
      <category>{escape(p["secao"])}</category>
      <description>{escape(p["descricao"])}.</description>
    </item>""")

    agora = format_datetime(datetime.now(timezone.utc))
    FEED.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Awesome Educação Midiática — recurso do dia</title>
    <link>{REPO_URL}</link>
    <atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>
    <description>Um recurso de educação midiática por dia, curado por Paula Peclat.</description>
    <language>pt-br</language>
    <lastBuildDate>{agora}</lastBuildDate>
{chr(10).join(itens)}
  </channel>
</rss>
""", encoding="utf-8")


def publicar():
    fila = carregar(FILA, [])
    if not fila:
        print("FILA_VAZIA — nada a publicar hoje.")
        gh_output(nome="", url="", descricao="", vazia="1")
        return

    item = fila.pop(0)
    secao, nome = item["secao"], item["nome"]
    url, desc = item["url"], item["descricao"].rstrip(".")

    texto = README.read_text(encoding="utf-8")
    marcador = f"## {secao}\n"
    inicio = texto.find(marcador)
    if inicio == -1:
        raise SystemExit(f"erro: seção '{secao}' não existe no README — corrija a fila.json")

    candidatos = [p for p in (texto.find("\n## ", inicio + len(marcador)),
                              texto.find("\n---", inicio + len(marcador))) if p != -1]
    fim = min(candidatos) if candidatos else len(texto)
    while texto[fim - 1] == "\n":
        fim -= 1

    README.write_text(texto[:fim] + f"\n- [{nome}]({url}) — {desc}." + texto[fim:], encoding="utf-8")
    salvar(FILA, fila)

    publicados = carregar(PUBLICADOS, [])
    publicados.append({
        "nome": nome, "url": url, "descricao": desc, "secao": secao,
        "data": datetime.now(timezone.utc).strftime("%Y-%m-%dT12:00:00"),
    })
    salvar(PUBLICADOS, publicados)
    gerar_feed(publicados)

    restam = len(fila)
    print(f"PUBLICADO: {nome} (seção {secao}) — restam {restam} na fila")
    gh_output(nome=nome, url=url, descricao=desc, vazia="1" if restam == 0 else "0")
    if restam <= 2:
        print(f"AVISO: só {restam} item(ns) na fila — hora de reabastecer!")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) > 1 and sys.argv[1] == "feed":
        gerar_feed(carregar(PUBLICADOS, []))
        print(f"Feed regenerado: {FEED}")
        return
    publicar()


if __name__ == "__main__":
    main()
