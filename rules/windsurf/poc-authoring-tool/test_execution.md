---
trigger: model_decision
description: Test execution instructions. Always use when running tests.
globs: 
---

* **Command**: Execute `uv run pytest` from the appropriate directory. Do not use plain `pytest` or other test runners.
* **Constraint**: NEVER run tests from the repository root.
* **CWD Logic**: Locate the nearest ancestor directory containing `pyproject.toml` relative to the file being edited.
* *Example*: `backend_ml/src/gateways/artefact.py` → CWD: `.../poc-authoring-tool/backend_ml`
* *Example*: `libs/inference/inference/compiler.py` → CWD: `.../poc-authoring-tool/libs/inference`
* **Safety**: If no `pyproject.toml` is found in the path hierarchy, abort and request the correct project root from the user.
