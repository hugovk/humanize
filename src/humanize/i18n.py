"""Activate, get and deactivate translations."""
from __future__ import annotations

import gettext as gettext_module
import os.path
from threading import local

try:
    from typing import Annotated, Doc  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import (  # type: ignore[attr-defined,assignment]
        Annotated,
        Doc,
    )

__all__ = ["activate", "deactivate", "decimal_separator", "thousands_separator"]

_TRANSLATIONS: dict[str | None, gettext_module.NullTranslations] = {
    None: gettext_module.NullTranslations()
}
_CURRENT = local()


# Mapping of locale to thousands separator
_THOUSANDS_SEPARATOR = {
    "de_DE": ".",
    "fr_FR": " ",
    "it_IT": ".",
    "pt_BR": ".",
    "hu_HU": " ",
}

# Mapping of locale to decimal separator
_DECIMAL_SEPARATOR = {
    "de_DE": ",",
    "it_IT": ",",
    "pt_BR": ",",
    "hu_HU": ",",
}


def _get_default_locale_path() -> str | None:
    try:
        if __file__ is None:
            return None
        return os.path.join(os.path.dirname(__file__), "locale")
    except NameError:
        return None


def get_translation() -> gettext_module.NullTranslations:
    try:
        return _TRANSLATIONS[_CURRENT.locale]
    except (AttributeError, KeyError):
        return _TRANSLATIONS[None]


def activate(
    locale: Annotated[str, Doc("Language name, e.g. `en_GB`.")],
    path: Annotated[str | None, Doc("Path to search for locales.")] = None,
) -> gettext_module.NullTranslations:
    """Activate internationalisation.

    Set `locale` as current locale. Search for locale in directory `path`.

    Returns:
        dict: Translations.

    Raises:
        Exception: If humanize cannot find the locale folder.
    """
    if path is None:
        path = _get_default_locale_path()

    if path is None:
        msg = (
            "Humanize cannot determinate the default location of the 'locale' folder. "
            "You need to pass the path explicitly."
        )
        raise Exception(msg)
    if locale not in _TRANSLATIONS:
        translation = gettext_module.translation("humanize", path, [locale])
        _TRANSLATIONS[locale] = translation
    _CURRENT.locale = locale
    return _TRANSLATIONS[locale]


def deactivate() -> None:
    """Deactivate internationalisation."""
    _CURRENT.locale = None


def _gettext(message: Annotated[str, Doc("Text to translate.")]) -> str:
    """Get translation.

    Returns:
        str: Translated text.
    """
    return get_translation().gettext(message)


def _pgettext(
    msgctxt: Annotated[str, Doc("Context of the translation.")],
    message: Annotated[str, Doc("Text to translate.")],
) -> str:
    """Fetches a particular translation.

    It works with `msgctxt` .po modifiers and allows duplicate keys with different
    translations.

    Returns:
        str: Translated text.
    """
    return get_translation().pgettext(msgctxt, message)


def _ngettext(
    message: Annotated[str, Doc("Singular text to translate.")],
    plural: Annotated[str, Doc("Plural text to translate.")],
    num: Annotated[
        int,
        Doc(
            "The number (e.g. item count) to determine translation "
            "for the respective grammatical number."
        ),
    ],
) -> str:
    """Plural version of _gettext.

    Returns:
        str: Translated text.
    """
    return get_translation().ngettext(message, plural, num)


def _gettext_noop(
    message: Annotated[str, Doc("Text to translate in the future.")]
) -> str:
    """Mark a string as a translation string without translating it.

    Example usage:
    ```python
    CONSTANTS = [_gettext_noop('first'), _gettext_noop('second')]
    def num_name(n):
        return _gettext(CONSTANTS[n])
    ```

    Returns:
        str: Original text, unchanged.
    """
    return message


def _ngettext_noop(
    singular: Annotated[str, Doc("Singular text to translate in the future.")],
    plural: Annotated[str, Doc("Plural text to translate in the future.")],
) -> tuple[str, str]:
    """Mark two strings as pluralized translations without translating them.

    Example usage:
    ```python
    CONSTANTS = [ngettext_noop('first', 'firsts'), ngettext_noop('second', 'seconds')]
    def num_name(n):
        return _ngettext(*CONSTANTS[n])
    ```

    Returns:
        tuple: Original text, unchanged.
    """
    return singular, plural


def thousands_separator() -> str:
    """Return the thousands separator for a locale, default to comma.

    Returns:
         str: Thousands separator.
    """
    try:
        sep = _THOUSANDS_SEPARATOR[_CURRENT.locale]
    except (AttributeError, KeyError):
        sep = ","
    return sep


def decimal_separator() -> str:
    """Return the decimal separator for a locale, default to dot.

    Returns:
         str: Decimal separator.
    """
    try:
        sep = _DECIMAL_SEPARATOR[_CURRENT.locale]
    except (AttributeError, KeyError):
        sep = "."
    return sep
