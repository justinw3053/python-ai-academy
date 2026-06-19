import pytest
import os
import json
from backend.content_engine import parse_notebook, get_lesson_content

@pytest.fixture
def mock_notebook(tmp_path):
    # Create a mock .ipynb file
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": ["# Lesson 1\n", "Welcome to the station."]
            },
            {
                "cell_type": "code",
                "source": [
                    "x = 5\n",
                    "# === AUTOMATED CHECK ===\n",
                    "assert x == 5\n"
                ]
            }
        ]
    }
    file_path = tmp_path / "mock_lesson.ipynb"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(notebook_content, f)
    return file_path

def test_parse_notebook(mock_notebook):
    content = parse_notebook(str(mock_notebook))
    
    assert content["title"] == "Lesson 1"
    assert "Welcome to the station." in content["markdown"]
    
    # Check that code and assertions are split correctly
    assert len(content["exercises"]) == 1
    exercise = content["exercises"][0]
    assert "x = 5" in exercise["starter_code"]
    assert "assert x == 5" in exercise["assertions"]
    assert "AUTOMATED CHECK" not in exercise["starter_code"]
