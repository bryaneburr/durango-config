# Durango

<img src="https://github.com/bryaneburr/durango-config/raw/main/images/durango_logo.png" height="200" style="height: 200px" />

Durango is a lightweight configuration management toolkit that layers strongly typed settings, configuration files, environment variables, and programmatic overrides using [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/). It is designed for CLI tools and services that need predictable precedence, multi-format config files, and clear error reporting.

## Key Features

- **Config precedence**: defaults → config file → environment variables → user overrides.
- **Format flexibility**: parse YAML, JSON, or TOML files by default with optional extras.
- **Typed settings**: describe your configuration with Pydantic models and receive fully validated objects.
- **Reload aware**: refresh configuration at runtime and hook into lifecycle callbacks.
- **Extensible**: adapt environment prefixes, merge behaviour, and file lookup strategies to fit your application.

## Quick Start

```python
from durango import ConfigManager, DurangoSettings


class AppSettings(DurangoSettings):
    debug: bool = False
    api_url: str


manager = ConfigManager(
    settings_type=AppSettings,
    identifier="MYAPP",
    default_file="~/.config/myapp/settings.yaml",
)

settings = manager.load()
print(settings.api_url)
```

If `~/.config/myapp/settings.yaml` does not exist, Durango will create it and populate it with the model defaults before layering environment variables and runtime overrides.

Environment variables take the form `MYAPP__API_URL=true`. To override a nested section named `database`, use `MYAPP__DATABASE__URL`.

## Documentation

- Docs site (WIP): see `docs/`
- Architecture notes: `ARCH.md`
- Working session notes: `notes/STATUS.md`

## Contributing

Install the development dependencies with [uv](https://github.com/astral-sh/uv):

```bash
uv sync --all-extras --dev
uv run pre-commit install
```

Run the full pre-commit suite before sending a pull request:

```bash
uv run pre-commit run --all-files
```

### Invoke shortcuts

Durango provides [Invoke](https://www.pyinvoke.org/) tasks that mirror our CI checks. After syncing dependencies run:

```bash
uv run invoke --list
```

Frequently used tasks:

- `uv run invoke sync` — refresh local environments (installs `dev` and `docs` extras).
- `uv run invoke ci` — execute Ruff, MyPy, pytest, and MkDocs in one shot.
- `uv run invoke docs-serve` — launch the docs preview server at `http://127.0.0.1:8000`.
- `uv run invoke build` — generate wheel and source distributions (add `--clean` to delete existing artifacts).
- `uv run invoke publish` — upload distributions to PyPI/TestPyPI with `--index-url`, `--skip-existing`, or `--dry-run`.
- `uv run invoke bump-version` — bump semantic versions or preview changes with `--dry-run`.
- `uv run invoke tag-version` — create annotated git tags and optionally push them.
- `uv run invoke release` — combine version bumping, publishing, and tagging into one workflow.

### Publishing

Run a dry run before publishing to confirm the workflow:

```bash
uv run invoke build
uv run invoke publish --index-url https://test.pypi.org/simple/ --skip-existing --dry-run
uv run invoke release --dry-run
```

When you are ready to ship, supply your API token directly (it will appear in the echoed command):

```bash
uv run invoke bump-version --part patch
uv run invoke build --clean
uv run invoke publish --token "$PYPI_API_TOKEN"
uv run invoke tag-version --push
```

Or let the release task orchestrate the steps:

```bash
uv run invoke release --token "$PYPI_API_TOKEN" --push-tag
```

Use `--index-url https://test.pypi.org/simple/` to target TestPyPI, `--skip-existing` to avoid duplicate uploads, and `--dry-run` any time you want to inspect the composed commands without executing them.

## License

Durango is available under the MIT License. See `LICENSE` for details.
