# Source Provenance and Separation

This folder is the **BidSentry-E / Syntax Squad** technical workstream. It contains only this product's application source, tests and documentation. No other project concept or older presentation package is merged into the active code.

## User-provided originals preserved unchanged

- `references/Proposed_Master_Build_Original.txt` is byte-identical to the user-provided master-build paste.
- `references/Exact_Copies_Bundle.zip` is the original reference ZIP.
- `references/extracted/Exact_Copy_1.txt`, `Exact_Copy_2.md`, `Exact_Copy_3.txt`, and `Exact_Copy_4.txt` are extracted copies for readability. The original ZIP remains untouched.
- `INPUT_HASHES.txt` records SHA-256 hashes of these source inputs.

## Active implementation

- `app/`, `engine.py`, `tests/`, `.env.example`, `requirements.txt` and `scripts/` form the executable implementation and local test suite.
- Technical documents under the root and `docs/` explain implementation behavior, limitations, research, demo and submission sequence.
- The original source files under `references/` are inputs, not executable code and not a promise that all proposed rules were accepted literally.

## Explicit release exclusions

All PPT/PDF presentation decks, slide montages, presentation-building scripts, local database files, cache directories, Python bytecode, `.venv`, and real `.env` files are excluded. The required pitch PPT is supplied separately for initial Unstop upload.

## Live-integration truth

Local tests mock provider responses. No live TinyFish run with the team's key, public GitHub publication, video publication or Unstop submission is claimed in this package.
