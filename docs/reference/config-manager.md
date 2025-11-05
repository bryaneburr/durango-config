# Config Manager

Durango exposes a single entry point—`ConfigManager`—to coordinate configuration sources and provide a ready-to-use settings instance.

```python
from durango import ConfigManager, DurangoSettings


class ServiceSettings(DurangoSettings):
    debug: bool = False
    database_url: str


manager = ConfigManager(
    settings_type=ServiceSettings,
    identifier="SERVICE",
    default_file="~/.config/service/config.yaml",
)

settings = manager.load()
```

## Construction

- `settings_type`: subclass of `DurangoSettings`.
- `identifier`: prefix for environment variables (`SERVICE__DATABASE_URL`).
- `default_file`: path to the preferred config file; supports `~`. When the target file does not exist, Durango writes the model defaults to that location using the detected format.
- `file_formats`: optional override to restrict/extend supported readers.
- `callbacks`: optional mapping of lifecycle hooks (e.g., `"post_load"`) to callables.

## Precedence

Durango starts with the model defaults, then layers each source in order:

1. **Defaults** declared on the `DurangoSettings` subclass.
2. **Config file** resolved from `config_path` or `default_file`.
3. **Environment variables** named `<IDENTIFIER>__SECTION__KEY`.
4. **User overrides** supplied programmatically.

Later sources win. The resolved values are validated and cached until you call `reload()`.

## Methods

### `load(*, config_path=None, overrides=None)`

Load configuration respecting the precedence chain. The result is cached for subsequent calls unless `reload()` is invoked.

### `reload(*, config_path=None)`

Re-run the resolution process and invoke any registered callbacks.

### `register_callback(event, func)`

Attach a new callback for `"post_load"` or `"pre_reload"` events at runtime.

### `override(overrides)`

Replace the current override dictionary. Call `reload()` to apply immediately or `load()` to merge on demand.

### `to_dict()`

Return the current settings as a plain dictionary—handy for logging or JSON payloads.

## Errors

- `ConfigFileError`: raised when the file cannot be read or parsing fails.
- `ConfigValidationError`: wraps Pydantic validation errors with extra context.
- `UnsupportedFormatError`: triggered when a file extension lacks a registered reader.

Durango renders error messages ready for CLI JSON payloads while keeping the original Pydantic error object attached.
