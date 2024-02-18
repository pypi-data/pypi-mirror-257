from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class DarklyThemeHook(ThemeHook):
    """
    Bootswatch Darkly Theme
    https://bootswatch.com/darkly/
    """

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Darkly",
            "Flatly in night mode!",
            css=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.2.3/darkly/bootstrap.min.css",
                "integrity": "sha512-YRcmztDXzJQCCBk2YUiEAY+r74gu/c9UULMPTeLsAp/Tw5eXiGkYMPC4tc4Kp1jx/V9xjEOCVpBe4r6Lx6n5dA=="
            }],
            js=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
                "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ=="
            }, {
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.3/js/bootstrap.min.js",
                "integrity": "sha512-1/RvZTcCDEUjY/CypiMz+iqqtaoQfAITmNSJY17Myp4Ms5mdxPS5UV7iOfdZoxcGhzFbOm6sntTKJppjvuhg4g=="
            }],
            header_padding="4.5em"
        )


@hooks.register('theme_hook')
def register_darkly_hook():
    return DarklyThemeHook()
