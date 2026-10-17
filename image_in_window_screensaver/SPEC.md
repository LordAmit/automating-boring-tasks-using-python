# Spec: image_in_window_screensaver (No Nonsense Image Viewer / Screensaver)

Status: DRAFT, awaiting approval. Spec lives next to the code it describes
(co-located spec pattern). Plan and task list for this module go in
`image_in_window_screensaver/tasks/plan.md` and
`image_in_window_screensaver/tasks/todo.md`, not at the repository root.

## Objective

A keyboard-driven image viewer and slideshow for macOS, built on Qt via
`qtpy`. The single user is the repository owner. It points at a root folder
that holds `landscape/` and `portrait/` subfolders, loads every image under
them into memory as a list of paths, and lets the user step, shuffle, sort,
filter, trash, bookmark and reveal images with single keys. A timer advances
the slideshow at a user-adjustable interval.

This spec is the baseline for an existing, working tool. Its first job is to
state what the tool is supposed to do today so that later changes have
acceptance criteria. Known gaps between the readme and the code are listed
under Open Questions, not silently fixed.

### User stories

- As the owner, I start the viewer on a folder and it shows a random image,
  then advances automatically every 300 seconds by default.
- As the owner, I control everything from the keyboard without a toolbar.
- As the owner, I can filter to landscape or portrait only, sort by date,
  reverse, and return to the image where the shuffle started.
- As the owner, I can set a home image with `--start_image`. Filtering with
  `1` or `2` jumps back to it. `b` and `0` are a separate bookmark pair for
  recovering my place.
- As the owner, I can send the current image to Trash (recoverable) and open
  its folder in Finder.

## Tech Stack

- Python 3.11 (PySide2 5.15.x has no wheels for 3.12+; the machine's default
  `python3` is 3.14, so a pinned venv is required)
- `qtpy` 2.2.0 over `PySide2` 5.15.2.1 (all widget code imports `qtpy`,
  except `main_window.py` which still imports `PySide2` directly)
- `Send2Trash` 1.8.0 for recoverable delete
- `unittest` from the standard library for tests
- `compress_images.py` shells out to ImageMagick `convert` and `mv`

Pinned versions are in `requirements.txt`.

## Commands

All commands run from `image_in_window_screensaver/`. There is no venv in the
tree today; create one first. None of these were executed while writing this
spec because Qt is not installed on this machine yet.

```sh
# one-time setup
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt

# run
.venv/bin/python main_window.py --path ~/Pictures/somefolder/ [--start_image <file>] [--ignore word1,word2]

# tests (headless Qt)
QT_QPA_PLATFORM=offscreen .venv/bin/python -m unittest discover -s tests -t . -v

# compress oversized images (requires ImageMagick)
.venv/bin/python compress_images.py --path <folder>/landscape/ --backup <backup_folder>/
```

There is no build step and no configured linter. `runme.sh` and
`compressme.sh` hardcode `/Users/amitseal/...` paths that do not exist on this
machine; treat them as personal launchers, not as the documented commands.

## Project Structure

```
image_in_window_screensaver/
  SPEC.md                 -> this file (co-located spec)
  tasks/                  -> plan.md and todo.md once the spec is approved
  main_window.py          -> entry point; creates QApplication and ImageWidget
  image_widget.py         -> ImageWidget: list state, key handling, timer, display
  file_walker.py          -> walk(): collects image paths, filters, sorts
  argument_handler.py     -> argparse wrapper with lazy module-level cache
  bad_practise_global.py  -> mutable module globals: pause bounds, autoplay, shuffle
  custom_log.py           -> thin logging.debug wrapper
  compress_images.py      -> companion CLI: compress + back up images over 5 MB
  main_level_widget.py    -> fully commented out, unused
  top_level_widget.py     -> fully commented out, unused
  tests/                  -> unittest cases; one module per source module
  readme.md               -> user-facing docs and the keyboard map
```

## Code Style

Modules are flat, functions and attributes are `snake_case`, private widget
state is prefixed with an underscore, and logging goes through the
`custom_log` alias `l`. Type hints are used on signatures. New code follows
the existing pattern:

```python
def image_next(self, step: int = 1) -> None:
    l.log("next")
    self._current_index += step
    if self._current_index >= len(self._all_images):
        self._current_index = 0
    self._set_image(self._current_index)
```

Conventions to keep:

- Import Qt through `qtpy`, never `PySide2` directly, so the binding can be
  swapped without touching widget code.
- Keyboard bindings live only in `ImageWidget.keyReleaseEvent`; the readme
  Shortcuts table must match it one for one.
- Image list state (`_all_images`, `_current_index`, `_shuffle_start_index`)
  is owned by `ImageWidget`; `file_walker` is stateless apart from
  `current_mode`.
- No `print` for diagnostics; use `l.log`.

## Testing Strategy

- Framework: standard library `unittest`, discovered from `tests/`.
- Run headless with `QT_QPA_PLATFORM=offscreen`; a `QApplication` is created
  once per test class in `setUpClass`.
- Pure logic (index wrap-around, sort, filter, ignore-word matching, timer
  bounds) gets unit tests with no filesystem beyond `tmp_path`-style temp
  dirs created in the test.
- Widget behavior is tested by constructing `ImageWidget` against a temp
  folder of tiny generated images and sending `QKeyEvent`s, not by manual
  clicking.
- Coverage target: every public method on `ImageWidget` and every branch of
  `file_walker.walk` has at least one test. No numeric threshold is enforced.
- Test modules are named after the module under test. The existing
  `tests/test_file_walker.py` actually tests `ImageWidget` and should be
  renamed as part of the first task.

## Boundaries

- Always: run the test command above before committing; keep readme
  Shortcuts in sync with `keyReleaseEvent`; use `send2trash`, never
  `os.remove`, for user images; create temp folders for tests instead of
  touching `~/Pictures`.
- Ask first: swapping PySide2 for PySide6; adding or removing a dependency;
  changing any existing key binding; changing default pause, autoplay or
  shuffle settings; deleting the two commented-out widget files.
- Never: run `compress_images.py` or any delete path against a real photo
  folder during development; commit a venv or personal absolute paths; remove
  a failing test to get green.

## Success Criteria (baseline)

1. A fresh clone plus the setup commands above yields a venv where the test
   command exits 0.
2. `main_window.py --path <folder>` on a folder containing `landscape/` and
   `portrait/` with jpg, jpeg, png and bmp files opens a window showing one
   image, with the window title containing the image path.
3. Every key in the readme Shortcuts table performs the described action, and
   every handled key in `keyReleaseEvent` appears in the readme.
4. Next and previous wrap at both ends without raising `IndexError` for a
   list of length 1, 2 and 50.
5. `Delete` moves the file to Trash, removes it from the list, and shows the
   next image; the app does not crash when the last remaining image is
   deleted.
6. Pause interval never leaves the range `[least_pause_secs,
   max_pause_secs]` regardless of key sequence.
7. Filtering with `1` or `2` reloads the filtered list and jumps to the home
   image given by `--start_image`. If no home image was given, or it is not
   in the filtered set, the first image of the filtered list is shown.
8. Pressing `3` reloads the unfiltered list, keeps the on-screen image if it
   is still present, and clears the active filter so a later `d` or `e` sort
   applies to all images.

## Feature: keymap overlay (approved 2026-10-17)

Pressing `?` shows the keyboard shortcut list as an overlay panel drawn
inside the viewer window, on top of the image. `Esc` hides it.

Acceptance criteria:

1. `?` shows the overlay in both windowed and fullscreen mode; `Esc` hides it.
2. The slideshow keeps advancing underneath, and every other key keeps
   working while the overlay is visible.
3. The overlay text is a hand-maintained string in `image_widget.py` and
   matches the readme Shortcuts table one for one.
4. The overlay resizes with the window.

Out of scope: pausing the slideshow, a separate draggable window, mouse
interaction with the overlay, `?` toggling itself closed, readme generation.

## Open Questions

Discrepancies found while reading the code. Each needs a decision before it
becomes a task.

1. Resolved 2026-10-17: key `3` now reloads the unfiltered list and clears
   the filter mode (see success criterion 8).
2. Resolved 2026-10-17: `0` documented in readme Shortcuts next to `b`.
3. Resolved 2026-10-17: `--start_image` is a home image, and `1` and `2`
   jumping to it is intended. No code change (see success criterion 7).
4. Decided 2026-10-17, deferred to tasks/todo.md: move the `dir_path`
   default to `None` and resolve it inside `walk`.
5. Decided 2026-10-17, in tasks/todo.md: switch to `os.path.join`.
6. Deferred 2026-10-17 to tasks/todo.md: decide PySide2 on 3.11 vs
   PySide6. Until then the Tech Stack section stands.
7. Decided 2026-10-17, in tasks/todo.md: drop the direct `PySide2` imports
   in `main_window.py`.
8. Resolved 2026-10-17: `compress_images.py` is out of scope for this spec
   and gets its own co-located `SPEC-compress-images.md` (in tasks/todo.md).
