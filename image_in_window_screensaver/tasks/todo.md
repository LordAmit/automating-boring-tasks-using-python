# Todo: image_in_window_screensaver

Spec: ../SPEC.md (status: draft, awaiting approval)

## Decided, not yet implemented

- [ ] Task: `file_walker.walk` default `dir_path=None`, resolve `argh.get_path()` inside the function (spec Q4)
  - Acceptance: importing `file_walker` no longer parses argv; tests do not need to patch `sys.argv` before import
  - Verify: test command in SPEC.md exits 0
  - Files: file_walker.py, tests/test_file_walker.py
- [ ] Task: build the mode path with `os.path.join` in `walk` (spec Q5)
  - Acceptance: `--path ~/Pictures/x` (no trailing slash) works with `1` and `2`
  - Verify: run viewer with and without trailing slash, press `1`
  - Files: file_walker.py
- [ ] Task: drop direct `PySide2` imports from `main_window.py` (spec Q7)
  - Acceptance: only `qtpy` imports remain; app starts
  - Verify: run viewer
  - Files: main_window.py
- [ ] Task: write co-located `SPEC-compress-images.md` for `compress_images.py` (spec Q8)
  - Acceptance: spec covers objective, commands, ImageMagick dependency, boundaries
  - Verify: review
  - Files: SPEC-compress-images.md

## To decide

- [ ] Decide: stay on PySide2 with Python 3.11, or migrate to PySide6 (spec Q6)
  - Acceptance: decision recorded in SPEC.md Tech Stack
  - Files: SPEC.md, requirements.txt

## Features

- [x] Task: `?` shows the keymap overlay, `Esc` hides it (SPEC.md "Feature: keymap overlay")
  - Acceptance: see spec section criteria 1 to 4
  - Verify: run viewer, press `?` in windowed and fullscreen mode, press `Esc`; manual check pending
  - Files: image_widget.py, readme.md
- [x] Task: delay toast on `=`, `-`, `+`, `_`, `t`, `y`, and play state on `p` (SPEC.md "Feature: delay toast")
  - Acceptance: see spec section criteria 1 to 4
  - Verify: run viewer, tap `=` five times fast, confirm one toast, hidden 2 s after last tap; manual check pending
  - Files: image_widget.py, readme.md
