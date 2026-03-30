## Changelog

# Version 0.1.3 (2026-03-30)

- Added a minimal runnable sample table at `examples/minimal_otu.txt`.
- Added one-command verification script `scripts/verify_minimal_pipeline.sh` for import + run + visualize smoke testing.
- Updated README with quick-start verification instructions.

# Version 0.1.2 (2026-03-30)

- Added unit tests for LEfSe command-prefix resolution and subprocess error handling helpers.
- Added troubleshooting section in README for Python 2.7 / command-prefix runtime issues.

# Version 0.1.1 (2026-03-30)

- Added `command_prefix` support for method/visualizer so LEfSe can run from a separate Python 2.7 environment.
- Added `Q2_LEFSE_COMMAND_PREFIX` environment-variable fallback.
- Updated README with Python 2.7 compatibility guidance and examples.

# Version 0.1.0 (2026-03-30)

- Replaced HUMAnN3 scaffold code with real LEfSe execution workflow.
- Added robust subprocess error handling for LEfSe CLI calls.
- Implemented `OTUTable` format validation.
- Registered semantic type/format mappings for `OTUTable`.
- Added QIIME 2 method (`run`) and visualizer (`visualize`) for LEfSe.
- Fixed package metadata (`setup.py`) to use `q2-lefse` module paths.
- Refreshed README with actual plugin usage.

# Version 0.0.3 (2016-10-3)

- Initial scaffold.
