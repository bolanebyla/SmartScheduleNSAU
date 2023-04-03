from smart_schedule_nsau.adapters.cli import create_cli

from .alembic_runner import run_cmd as alembic_run_cmd

cli = create_cli(alembic_run_cmd)
