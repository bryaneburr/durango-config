# Durango

<img src="images/durango_logo.png" height="200" style="height: 200px" />

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
- Project plan: `notes/SPEC.md`
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

## License

Durango is available under the MIT License. See `LICENSE` for details.
