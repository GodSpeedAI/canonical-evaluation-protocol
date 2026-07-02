set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

validate:
    uv run python tools/validate_okf.py
    uv run cep validate all

test:
    uv run pytest

conformance:
    uv run cep conformance anti-collapse

smoke:
    uv run cep run reality-gap-corpus
    uv run cep run authority-corpus
    uv run cep run settlement-corpus
    uv run cep run capability-corpus

all: validate test conformance smoke

# WP-7 (F-11): export real ledger SettlementRecorded rows → scored CEP corpus,
# then enforce the week-over-week ratchet + anti-collapse. Set PG_DSN to the
# ledger Postgres. Humans read reports/ledger/aggregate.json; the job exits
# non-zero on regression or any settlement collapse (§14 hard cap).
reports_dir := "reports/ledger"
ledger-eval PG_DSN="" PREV="":
    mkdir -p {{reports_dir}}
    uv run python -c \
      "from cep.exporters.ledger_postgres import export_settlement_corpus, ratchet_against; \
       import os,sys; \
       r=export_settlement_corpus(os.environ['PG_DSN'], '{{reports_dir}}/current'); \
       sys.exit(ratchet_against('{{reports_dir}}/previous-aggregate.json', r))"
    cp {{reports_dir}}/current/aggregate.json {{reports_dir}}/previous-aggregate.json
