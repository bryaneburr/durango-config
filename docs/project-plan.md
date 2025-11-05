# Durango Specification

Durango provides a reusable configuration subsystem built on Pydantic Settings. This document tracks implementation phases and major milestones.

## Phase 1 — Foundations (Planned)

- [x] Scaffold project structure, tooling, and documentation skeleton.
- [x] Define core interfaces (`DurangoSettings`, `ConfigManager`, source contracts).
- [x] Establish automated workflows (CI, pre-commit, docs build).

## Phase 2 — Source Implementations (Planned)

- [x] Implement file loader with YAML/JSON/TOML support.
- [x] Implement environment loader for `<IDENTIFIER>__SECTION__KEY` precedence.
- [x] Implement override loader and merge strategies.
- [x] Validate precedence pipeline with unit and integration tests.

## Phase 3 — Lifecycle & Extensibility (Planned)

- [x] Add callback/observer system for reload events.
- [ ] Document extension points for custom sources and merges.
- [ ] Harden error types and JSON-friendly payloads.

## Phase 4 — Documentation & Release (Planned)

- [ ] Complete user guide and API reference.
- [ ] Publish preview builds to TestPyPI, verify install across Python 3.9–3.12.
- [ ] Tag `v0.1.0` and release to PyPI.

Progress is recorded in `notes/STATUS.md`. Update this specification as milestones advance or scope changes.
