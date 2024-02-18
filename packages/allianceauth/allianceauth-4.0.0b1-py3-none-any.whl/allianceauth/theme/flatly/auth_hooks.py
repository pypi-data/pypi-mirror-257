from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class FlatlyThemeHook(ThemeHook):
    """
    Bootswatch Flatly Theme
    https://bootswatch.com/flatly/
    """

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Flatly",
            "Flat and modern!",
            css=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.2/flatly/bootstrap.min.css",
                "integrity": "sha512-rx+BMEjKes84XHg1erhvtq7Mqxm/lm6w4WMoCtDAaTMtUzT5iK5hNTu8mc2+yPNSldAX5hheN/ZhtNQjjYy5nA=="
            }],
            js=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
                "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ=="
            }, {
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.2/js/bootstrap.min.js",
                "integrity": "sha512-WW8/jxkELe2CAiE4LvQfwm1rajOS8PHasCCx+knHG0gBHt8EXxS6T6tJRTGuDQVnluuAvMxWF4j8SNFDKceLFg=="
            }],
            header_padding="4.5em"
        )


@hooks.register('theme_hook')
def register_flatly_hook():
    return FlatlyThemeHook()
