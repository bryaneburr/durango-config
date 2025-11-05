# Durango Documentation

Durango layers configuration defaults, files, environment variables, and runtime overrides to produce validated Pydantic Settings. Use it when you need predictable precedence across CLI tools, background services, and automation pipelines.

## Why Durango?

- **Deterministic precedence** across multiple sources.
- **Format flexibility** including YAML, JSON, and TOML without additional boilerplate.
- **Typed settings** so consumers receive rich validation errors.
- **Reload & callbacks** for long-running processes that react to configuration changes.
- **Extensibility** to plug in additional sources or merge strategies.

## Getting Started

Install Durango with uv:

```bash
uv add durango
```

Create a settings model:

```python
from durango import ConfigManager, DurangoSettings


class ApiSettings(DurangoSettings):
    api_url: str
    token: str


manager = ConfigManager(
    settings_type=ApiSettings,
    identifier="MYAPP",
    default_file="~/.config/myapp/config.yaml",
)

settings = manager.load()
```

### Configuration Layers

1. **Defaults** from the settings model.
2. **Configuration file** supplied via `default_file` or the `config_path` argument.
3. **Environment variables** using `<IDENTIFIER>__SECTION__KEY` names.
4. **User overrides** provided programmatically (dict or keyword arguments).

Later layers win over earlier ones. The resulting model is cached until you call `reload()` or change overrides.

Explore the reference section for a deeper dive into each component.
