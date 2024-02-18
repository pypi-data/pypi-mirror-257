from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


CSS_STATICS = [{
    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.2/css/bootstrap.min.css",
    "integrity": "sha512-b2QcS5SsA8tZodcDtGRELiGv5SaKSk1vDHDaQRda0htPYWZ6046lr3kJ5bAAQdpV2mmA/4v0wQF9MyU6/pDIAg=="
}]

JS_STATICS = [{
    "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
    "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ=="
}, {
    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.2/js/bootstrap.min.js",
    "integrity": "sha512-WW8/jxkELe2CAiE4LvQfwm1rajOS8PHasCCx+knHG0gBHt8EXxS6T6tJRTGuDQVnluuAvMxWF4j8SNFDKceLFg=="
}]


class BootstrapThemeHook(ThemeHook):
    """
    Bootstrap in all its glory!
    https://getbootstrap.com/
    """

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Bootstrap",
            "Powerful, extensible, and feature-packed frontend toolkit.",
            css=CSS_STATICS,
            js=JS_STATICS,
            header_padding="3.5em"
        )


class BootstrapDarkThemeHook(ThemeHook):
    """
    Bootstrap in all its glory!, but _dark_
    https://getbootstrap.com/
    """

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Bootstrap Dark",
            "Powerful, extensible, and feature-packed frontend toolkit.",
            css=CSS_STATICS,
            js=JS_STATICS,
            html_tags="data-bs-theme=dark",
            header_padding="3.5em"
        )


@hooks.register('theme_hook')
def register_bootstrap_dark_hook():
    return BootstrapDarkThemeHook()


@hooks.register('theme_hook')
def register_bootstrap_hook():
    return BootstrapThemeHook()
