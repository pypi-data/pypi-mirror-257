from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class MateriaThemeHook(ThemeHook):
    """
    Bootswatch Materia Theme
    https://bootswatch.com/materia/
    """

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Materia",
            "Material is the metaphor",
            css=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.2/materia/bootstrap.min.css",
                "integrity": "sha512-4+PCWoNUxEeasuW2ipP8Avsr7X/oS61Kz2CLdwS6ZfHt7jLuzAAcIfPlWLg4aGaDNo0GSmTOmM9biaqnmo6P7g=="
            }],
            js=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
                "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ=="
            }, {
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.2/js/bootstrap.min.js",
                "integrity": "sha512-WW8/jxkELe2CAiE4LvQfwm1rajOS8PHasCCx+knHG0gBHt8EXxS6T6tJRTGuDQVnluuAvMxWF4j8SNFDKceLFg=="
            }],
            header_padding="5.25em"
        )


@hooks.register('theme_hook')
def register_materia_hook():
    return MateriaThemeHook()
