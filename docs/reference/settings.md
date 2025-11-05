# Settings Models

`DurangoSettings` extends `pydantic_settings.BaseSettings` with a few defaults that make layering easier.

```python
from durango import DurangoSettings


class SearchSettings(DurangoSettings):
    default_limit: int = 20
    auto_enable: bool = True
    embedding_function: str = "text-embedding-3-small"
```

## Features

- **Google-style docstrings**: document models/classes/functions for downstream automation.
- **Immutable option**: opt into `model_config = ConfigDict(frozen=True)` to prevent accidental writes.
- **Nested structures**: combine dataclasses and Pydantic models to model complex configurations.
- **Custom env parsing**: automatically convert environment names like `APP__SEARCH__DEFAULT_LIMIT`.

## Tips

- Group related fields into sub-models for clarity (e.g., `SearchSettings`, `DatabaseSettings`).
- Provide sensible defaults so CLI tools can run without config files.
- For secret values, pair with your preferred secret storage (Durango does not persist them).

See `durango/settings.py` for reusable mixins and advice on structuring models.
