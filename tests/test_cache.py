import pytest

from markdown_field.cache import clear_cache, get_field_config, register_field


@pytest.fixture(autouse=True)
def clear_cache_before_each_test():
    yield
    clear_cache()


class TestCache:
    def test_register_and_get_field_config(self):
        key = register_field(
            extensions=["toc"], extension_configs={"toc": {"depth": 2}}
        )
        config = get_field_config(key)

        assert config is not None
        assert config["extensions"] == ["toc"]
        assert config["extension_configs"] == {"toc": {"depth": 2}}

    def test_get_nonexistent_key_returns_none(self):
        config = get_field_config("nonexistent-key")
        assert config is None

    def test_clear_cache(self):
        key = register_field(extensions=["toc"], extension_configs={})
        assert get_field_config(key) is not None

        clear_cache()
        assert get_field_config(key) is None
