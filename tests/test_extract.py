import json
import os
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from extract import load_last_run, save_last_run

# --- Test load_last_run ---

def test_load_last_run_returns_default_when_no_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = load_last_run()
    assert result == "2000-01-01 00:00:00"

def test_load_last_run_reads_existing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    state = {"last_run": "2026-03-13 10:00:00"}
    with open("last_run.json", "w") as f:
        json.dump(state, f)
    result = load_last_run()
    assert result == "2026-03-13 10:00:00"

# --- Test save_last_run ---

def test_save_last_run_writes_correct_timestamp(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_last_run("2026-03-13 15:00:00")
    with open("last_run.json", "r") as f:
        data = json.load(f)
    assert data["last_run"] == "2026-03-13 15:00:00"

def test_save_last_run_overwrites_existing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_last_run("2026-03-13 10:00:00")
    save_last_run("2026-03-13 15:00:00")
    with open("last_run.json", "r") as f:
        data = json.load(f)
    assert data["last_run"] == "2026-03-13 15:00:00"
