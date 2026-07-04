#!/usr/bin/env python3
"""
Gera a pauta da semana: os próximos recursos da fila.json com a data em que
cada um será publicado, em formato de issue com checkboxes de produção de
conteúdo (Instagram/YouTube).

O workflow pauta-semanal.yml roda toda segunda e abre a issue — o GitHub
notifica por e-mail/app automaticamente.

Uso: python scripts/pauta.py > pauta.md
"""
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILA = ROOT / "fila.json"

DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    fila = json.loads(FILA.read_text(encoding="utf-8")) if FILA.exists() else []

    # a publicação diária acontece às 12:00 UTC — se ainda não passou,
    # o primeiro item da fila sai hoje; senão, amanhã
    agora = datetime.now(timezone.utc)
    primeiro_dia = date.today() if agora.hour < 12 else date.today() + timedelta(days=1)

    if not fila:
        print("## 📭 Fila vazia\n")
        print("Não há recursos programados — abasteça a `fila.json` para retomar a pauta.")
        return

    semana = fila[:7]
    fim = primeiro_dia + timedelta(days=len(semana) - 1)
    print(f"## 📅 Recursos programados de {primeiro_dia.strftime('%d/%m')} a {fim.strftime('%d/%m')}\n")
    print("Cada recurso abaixo será publicado automaticamente às 9h (Brasília) do dia indicado —")
    print("use como pauta para alinhar vídeos no Instagram e no YouTube. ✔ = conteúdo produzido.\n")

    for i, item in enumerate(semana):
        dia = primeiro_dia + timedelta(days=i)
        nome_dia = DIAS[dia.weekday()]
        print(f"### {nome_dia} · {dia.strftime('%d/%m')} — [{item['nome']}]({item['url']})")
        print(f"_{item['descricao']}._ ({item['secao']})")
        print("- [ ] vídeo Instagram")
        print("- [ ] vídeo YouTube\n")

    if len(fila) <= 7:
        print(f"> ⚠️ Depois desses, a fila {'acaba' if len(fila) < 7 else 'fica no limite'} — ")
        print("> adicione novos recursos em `fila.json` para a próxima semana.")
    else:
        print(f"> 📦 Ainda há {len(fila) - 7} recurso(s) na fila além desta semana.")


if __name__ == "__main__":
    main()
