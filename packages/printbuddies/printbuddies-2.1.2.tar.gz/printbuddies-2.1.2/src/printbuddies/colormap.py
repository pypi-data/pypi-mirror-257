from dataclasses import dataclass
from typing import Iterator


@dataclass
class Tag:
    """Reduce the size of f-strings when using `rich`.
    >>> from rich import print
    >>> p = Tag("pale_turquoise4")
    >>> c = Tag("cornflower_blue")
    >>> print(f"{p}This{p.o} {c}is{c.o} {p}a{p.o} {c}string")
    >>> same as
    >>> print("[pale_turquoise4]This[/pale_turquoise4] [cornflower_blue]is[/cornflower_blue] [pale_turquoise4]a[/pale_turquoise4] [cornflower_blue]string")
    """

    name: str

    def __str__(self) -> str:
        return f"[{self.name}]"

    @property
    def o(self) -> str:
        """Closing tag for this tag."""
        return f"[/{self.name}]"

    @property
    def off(self) -> str:
        """Closing tag for this tag."""
        return self.o


class ColorMap:
    """Color map for the rich colors at https://rich.readthedocs.io/en/stable/appendix/colors.html

    See color options conveniently with your IDE's autocomplete.

    Each color has two `Tag` properties: one using the full name and one using an abbreviation.

    `ColorMap.aquamarine1` and `ColorMap.a1` return equivalent `Tag` instances.

    >>> from rich import print
    >>> 'To alternate colors, instead of doing this:'
    >>> print("[aquamarine1]This [light_pink4]is [aquamarine]a [light_pink4]string")
    >>> 'You can do:'
    >>> c = ColorMap()
    >>> print(f"{c.a1}This {c.lp4}is {c.a1}a {c.lp4}string")"""

    @property
    def _tag_list(self) -> list[Tag]:
        tags = [
            getattr(self, obj)
            for obj in dir(self)
            if not obj.startswith("_") and isinstance(getattr(self, obj), Tag)
        ]
        return sorted(tags, key=lambda t: t.name)

    def __len__(self) -> int:
        return len(self._tag_list)

    def __iter__(self) -> Iterator[Tag]:
        for toggle in self._tag_list:
            yield toggle

    def __getitem__(self, key: int) -> Tag:
        return self._tag_list[key]

    @property
    def aquamarine1(self) -> Tag:
        """abbreviation: `a1`"""
        return Tag("aquamarine1")

    @property
    def a1(self) -> Tag:
        """aquamarine1"""
        return self.aquamarine1

    @property
    def aquamarine3(self) -> Tag:
        """abbreviation: `a3`"""
        return Tag("aquamarine3")

    @property
    def a3(self) -> Tag:
        """aquamarine3"""
        return self.aquamarine3

    @property
    def black(self) -> Tag:
        """abbreviation: `bl`"""
        return Tag("black")

    @property
    def bl(self) -> Tag:
        """black"""
        return self.black

    @property
    def blue(self) -> Tag:
        """abbreviation: `b`"""
        return Tag("blue")

    @property
    def b(self) -> Tag:
        """blue"""
        return self.blue

    @property
    def blue1(self) -> Tag:
        """abbreviation: `b1`"""
        return Tag("blue1")

    @property
    def b1(self) -> Tag:
        """blue1"""
        return self.blue1

    @property
    def blue3(self) -> Tag:
        """abbreviation: `b3`"""
        return Tag("blue3")

    @property
    def b3(self) -> Tag:
        """blue3"""
        return self.blue3

    @property
    def blue_violet(self) -> Tag:
        """abbreviation: `bv`"""
        return Tag("blue_violet")

    @property
    def bv(self) -> Tag:
        """blue_violet"""
        return self.blue_violet

    @property
    def bright_black(self) -> Tag:
        """abbreviation: `brbl`"""
        return Tag("bright_black")

    @property
    def brbl(self) -> Tag:
        """bright_black"""
        return self.bright_black

    @property
    def bright_blue(self) -> Tag:
        """abbreviation: `bb`"""
        return Tag("bright_blue")

    @property
    def bb(self) -> Tag:
        """bright_blue"""
        return self.bright_blue

    @property
    def bright_cyan(self) -> Tag:
        """abbreviation: `bc`"""
        return Tag("bright_cyan")

    @property
    def bc(self) -> Tag:
        """bright_cyan"""
        return self.bright_cyan

    @property
    def bright_green(self) -> Tag:
        """abbreviation: `bg`"""
        return Tag("bright_green")

    @property
    def bg(self) -> Tag:
        """bright_green"""
        return self.bright_green

    @property
    def bright_magenta(self) -> Tag:
        """abbreviation: `bm`"""
        return Tag("bright_magenta")

    @property
    def bm(self) -> Tag:
        """bright_magenta"""
        return self.bright_magenta

    @property
    def bright_red(self) -> Tag:
        """abbreviation: `br`"""
        return Tag("bright_red")

    @property
    def br(self) -> Tag:
        """bright_red"""
        return self.bright_red

    @property
    def bright_white(self) -> Tag:
        """abbreviation: `bw`"""
        return Tag("bright_white")

    @property
    def bw(self) -> Tag:
        """bright_white"""
        return self.bright_white

    @property
    def bright_yellow(self) -> Tag:
        """abbreviation: `by`"""
        return Tag("bright_yellow")

    @property
    def by(self) -> Tag:
        """bright_yellow"""
        return self.bright_yellow

    @property
    def cadet_blue(self) -> Tag:
        """abbreviation: `cb`"""
        return Tag("cadet_blue")

    @property
    def cb(self) -> Tag:
        """cadet_blue"""
        return self.cadet_blue

    @property
    def chartreuse1(self) -> Tag:
        """abbreviation: `ch1`"""
        return Tag("chartreuse1")

    @property
    def ch1(self) -> Tag:
        """chartreuse1"""
        return self.chartreuse1

    @property
    def chartreuse2(self) -> Tag:
        """abbreviation: `ch2`"""
        return Tag("chartreuse2")

    @property
    def ch2(self) -> Tag:
        """chartreuse2"""
        return self.chartreuse2

    @property
    def chartreuse3(self) -> Tag:
        """abbreviation: `ch3`"""
        return Tag("chartreuse3")

    @property
    def ch3(self) -> Tag:
        """chartreuse3"""
        return self.chartreuse3

    @property
    def chartreuse4(self) -> Tag:
        """abbreviation: `ch4`"""
        return Tag("chartreuse4")

    @property
    def ch4(self) -> Tag:
        """chartreuse4"""
        return self.chartreuse4

    @property
    def cornflower_blue(self) -> Tag:
        """abbreviation: `cobl`"""
        return Tag("cornflower_blue")

    @property
    def cobl(self) -> Tag:
        """cornflower_blue"""
        return self.cornflower_blue

    @property
    def cornsilk1(self) -> Tag:
        """abbreviation: `co1`"""
        return Tag("cornsilk1")

    @property
    def co1(self) -> Tag:
        """cornsilk1"""
        return self.cornsilk1

    @property
    def cyan(self) -> Tag:
        """abbreviation: `c`"""
        return Tag("cyan")

    @property
    def c(self) -> Tag:
        """cyan"""
        return self.cyan

    @property
    def cyan1(self) -> Tag:
        """abbreviation: `c1`"""
        return Tag("cyan1")

    @property
    def c1(self) -> Tag:
        """cyan1"""
        return self.cyan1

    @property
    def cyan2(self) -> Tag:
        """abbreviation: `c2`"""
        return Tag("cyan2")

    @property
    def c2(self) -> Tag:
        """cyan2"""
        return self.cyan2

    @property
    def cyan3(self) -> Tag:
        """abbreviation: `c3`"""
        return Tag("cyan3")

    @property
    def c3(self) -> Tag:
        """cyan3"""
        return self.cyan3

    @property
    def dark_blue(self) -> Tag:
        """abbreviation: `db`"""
        return Tag("dark_blue")

    @property
    def db(self) -> Tag:
        """dark_blue"""
        return self.dark_blue

    @property
    def dark_cyan(self) -> Tag:
        """abbreviation: `dc`"""
        return Tag("dark_cyan")

    @property
    def dc(self) -> Tag:
        """dark_cyan"""
        return self.dark_cyan

    @property
    def dark_goldenrod(self) -> Tag:
        """abbreviation: `dg`"""
        return Tag("dark_goldenrod")

    @property
    def dg(self) -> Tag:
        """dark_goldenrod"""
        return self.dark_goldenrod

    @property
    def dark_green(self) -> Tag:
        """abbreviation: `dagr`"""
        return Tag("dark_green")

    @property
    def dagr(self) -> Tag:
        """dark_green"""
        return self.dark_green

    @property
    def dark_khaki(self) -> Tag:
        """abbreviation: `dk`"""
        return Tag("dark_khaki")

    @property
    def dk(self) -> Tag:
        """dark_khaki"""
        return self.dark_khaki

    @property
    def dark_magenta(self) -> Tag:
        """abbreviation: `dm`"""
        return Tag("dark_magenta")

    @property
    def dm(self) -> Tag:
        """dark_magenta"""
        return self.dark_magenta

    @property
    def dark_olive_green1(self) -> Tag:
        """abbreviation: `dog1`"""
        return Tag("dark_olive_green1")

    @property
    def dog1(self) -> Tag:
        """dark_olive_green1"""
        return self.dark_olive_green1

    @property
    def dark_olive_green2(self) -> Tag:
        """abbreviation: `dog2`"""
        return Tag("dark_olive_green2")

    @property
    def dog2(self) -> Tag:
        """dark_olive_green2"""
        return self.dark_olive_green2

    @property
    def dark_olive_green3(self) -> Tag:
        """abbreviation: `dog3`"""
        return Tag("dark_olive_green3")

    @property
    def dog3(self) -> Tag:
        """dark_olive_green3"""
        return self.dark_olive_green3

    @property
    def dark_orange(self) -> Tag:
        """abbreviation: `do`"""
        return Tag("dark_orange")

    @property
    def do(self) -> Tag:
        """dark_orange"""
        return self.dark_orange

    @property
    def dark_orange3(self) -> Tag:
        """abbreviation: `do3`"""
        return Tag("dark_orange3")

    @property
    def do3(self) -> Tag:
        """dark_orange3"""
        return self.dark_orange3

    @property
    def dark_red(self) -> Tag:
        """abbreviation: `dr`"""
        return Tag("dark_red")

    @property
    def dr(self) -> Tag:
        """dark_red"""
        return self.dark_red

    @property
    def dark_sea_green(self) -> Tag:
        """abbreviation: `dsg`"""
        return Tag("dark_sea_green")

    @property
    def dsg(self) -> Tag:
        """dark_sea_green"""
        return self.dark_sea_green

    @property
    def dark_sea_green1(self) -> Tag:
        """abbreviation: `dsg1`"""
        return Tag("dark_sea_green1")

    @property
    def dsg1(self) -> Tag:
        """dark_sea_green1"""
        return self.dark_sea_green1

    @property
    def dark_sea_green2(self) -> Tag:
        """abbreviation: `dsg2`"""
        return Tag("dark_sea_green2")

    @property
    def dsg2(self) -> Tag:
        """dark_sea_green2"""
        return self.dark_sea_green2

    @property
    def dark_sea_green3(self) -> Tag:
        """abbreviation: `dsg3`"""
        return Tag("dark_sea_green3")

    @property
    def dsg3(self) -> Tag:
        """dark_sea_green3"""
        return self.dark_sea_green3

    @property
    def dark_sea_green4(self) -> Tag:
        """abbreviation: `dsg4`"""
        return Tag("dark_sea_green4")

    @property
    def dsg4(self) -> Tag:
        """dark_sea_green4"""
        return self.dark_sea_green4

    @property
    def dark_slate_gray1(self) -> Tag:
        """abbreviation: `daslgr1`"""
        return Tag("dark_slate_gray1")

    @property
    def daslgr1(self) -> Tag:
        """dark_slate_gray1"""
        return self.dark_slate_gray1

    @property
    def dark_slate_gray2(self) -> Tag:
        """abbreviation: `daslgr2`"""
        return Tag("dark_slate_gray2")

    @property
    def daslgr2(self) -> Tag:
        """dark_slate_gray2"""
        return self.dark_slate_gray2

    @property
    def dark_slate_gray3(self) -> Tag:
        """abbreviation: `daslgr3`"""
        return Tag("dark_slate_gray3")

    @property
    def daslgr3(self) -> Tag:
        """dark_slate_gray3"""
        return self.dark_slate_gray3

    @property
    def dark_turquoise(self) -> Tag:
        """abbreviation: `dt`"""
        return Tag("dark_turquoise")

    @property
    def dt(self) -> Tag:
        """dark_turquoise"""
        return self.dark_turquoise

    @property
    def dark_violet(self) -> Tag:
        """abbreviation: `dv`"""
        return Tag("dark_violet")

    @property
    def dv(self) -> Tag:
        """dark_violet"""
        return self.dark_violet

    @property
    def deep_pink1(self) -> Tag:
        """abbreviation: `dp1`"""
        return Tag("deep_pink1")

    @property
    def dp1(self) -> Tag:
        """deep_pink1"""
        return self.deep_pink1

    @property
    def deep_pink2(self) -> Tag:
        """abbreviation: `dp2`"""
        return Tag("deep_pink2")

    @property
    def dp2(self) -> Tag:
        """deep_pink2"""
        return self.deep_pink2

    @property
    def deep_pink3(self) -> Tag:
        """abbreviation: `dp3`"""
        return Tag("deep_pink3")

    @property
    def dp3(self) -> Tag:
        """deep_pink3"""
        return self.deep_pink3

    @property
    def deep_pink4(self) -> Tag:
        """abbreviation: `dp4`"""
        return Tag("deep_pink4")

    @property
    def dp4(self) -> Tag:
        """deep_pink4"""
        return self.deep_pink4

    @property
    def deep_sky_blue1(self) -> Tag:
        """abbreviation: `dsb1`"""
        return Tag("deep_sky_blue1")

    @property
    def dsb1(self) -> Tag:
        """deep_sky_blue1"""
        return self.deep_sky_blue1

    @property
    def deep_sky_blue2(self) -> Tag:
        """abbreviation: `dsb2`"""
        return Tag("deep_sky_blue2")

    @property
    def dsb2(self) -> Tag:
        """deep_sky_blue2"""
        return self.deep_sky_blue2

    @property
    def deep_sky_blue3(self) -> Tag:
        """abbreviation: `dsb3`"""
        return Tag("deep_sky_blue3")

    @property
    def dsb3(self) -> Tag:
        """deep_sky_blue3"""
        return self.deep_sky_blue3

    @property
    def deep_sky_blue4(self) -> Tag:
        """abbreviation: `dsb4`"""
        return Tag("deep_sky_blue4")

    @property
    def dsb4(self) -> Tag:
        """deep_sky_blue4"""
        return self.deep_sky_blue4

    @property
    def dodger_blue1(self) -> Tag:
        """abbreviation: `db1`"""
        return Tag("dodger_blue1")

    @property
    def db1(self) -> Tag:
        """dodger_blue1"""
        return self.dodger_blue1

    @property
    def dodger_blue2(self) -> Tag:
        """abbreviation: `db2`"""
        return Tag("dodger_blue2")

    @property
    def db2(self) -> Tag:
        """dodger_blue2"""
        return self.dodger_blue2

    @property
    def dodger_blue3(self) -> Tag:
        """abbreviation: `db3`"""
        return Tag("dodger_blue3")

    @property
    def db3(self) -> Tag:
        """dodger_blue3"""
        return self.dodger_blue3

    @property
    def gold1(self) -> Tag:
        """abbreviation: `go1`"""
        return Tag("gold1")

    @property
    def go1(self) -> Tag:
        """gold1"""
        return self.gold1

    @property
    def gold3(self) -> Tag:
        """abbreviation: `go3`"""
        return Tag("gold3")

    @property
    def go3(self) -> Tag:
        """gold3"""
        return self.gold3

    @property
    def green(self) -> Tag:
        """abbreviation: `g`"""
        return Tag("green")

    @property
    def g(self) -> Tag:
        """green"""
        return self.green

    @property
    def green1(self) -> Tag:
        """abbreviation: `g1`"""
        return Tag("green1")

    @property
    def g1(self) -> Tag:
        """green1"""
        return self.green1

    @property
    def green3(self) -> Tag:
        """abbreviation: `g3`"""
        return Tag("green3")

    @property
    def g3(self) -> Tag:
        """green3"""
        return self.green3

    @property
    def green4(self) -> Tag:
        """abbreviation: `g4`"""
        return Tag("green4")

    @property
    def g4(self) -> Tag:
        """green4"""
        return self.green4

    @property
    def green_yellow(self) -> Tag:
        """abbreviation: `gy`"""
        return Tag("green_yellow")

    @property
    def gy(self) -> Tag:
        """green_yellow"""
        return self.green_yellow

    @property
    def grey0(self) -> Tag:
        """abbreviation: `grey0`"""
        return Tag("grey0")

    @property
    def grey100(self) -> Tag:
        """abbreviation: `grey100`"""
        return Tag("grey100")

    @property
    def grey11(self) -> Tag:
        """abbreviation: `grey11`"""
        return Tag("grey11")

    @property
    def grey15(self) -> Tag:
        """abbreviation: `grey15`"""
        return Tag("grey15")

    @property
    def grey19(self) -> Tag:
        """abbreviation: `grey19`"""
        return Tag("grey19")

    @property
    def grey23(self) -> Tag:
        """abbreviation: `grey23`"""
        return Tag("grey23")

    @property
    def grey27(self) -> Tag:
        """abbreviation: `grey27`"""
        return Tag("grey27")

    @property
    def grey3(self) -> Tag:
        """abbreviation: `grey3`"""
        return Tag("grey3")

    @property
    def grey30(self) -> Tag:
        """abbreviation: `grey30`"""
        return Tag("grey30")

    @property
    def grey35(self) -> Tag:
        """abbreviation: `grey35`"""
        return Tag("grey35")

    @property
    def grey37(self) -> Tag:
        """abbreviation: `grey37`"""
        return Tag("grey37")

    @property
    def grey39(self) -> Tag:
        """abbreviation: `grey39`"""
        return Tag("grey39")

    @property
    def grey42(self) -> Tag:
        """abbreviation: `grey42`"""
        return Tag("grey42")

    @property
    def grey46(self) -> Tag:
        """abbreviation: `grey46`"""
        return Tag("grey46")

    @property
    def grey50(self) -> Tag:
        """abbreviation: `grey50`"""
        return Tag("grey50")

    @property
    def grey53(self) -> Tag:
        """abbreviation: `grey53`"""
        return Tag("grey53")

    @property
    def grey54(self) -> Tag:
        """abbreviation: `grey54`"""
        return Tag("grey54")

    @property
    def grey58(self) -> Tag:
        """abbreviation: `grey58`"""
        return Tag("grey58")

    @property
    def grey62(self) -> Tag:
        """abbreviation: `grey62`"""
        return Tag("grey62")

    @property
    def grey63(self) -> Tag:
        """abbreviation: `grey63`"""
        return Tag("grey63")

    @property
    def grey66(self) -> Tag:
        """abbreviation: `grey66`"""
        return Tag("grey66")

    @property
    def grey69(self) -> Tag:
        """abbreviation: `grey69`"""
        return Tag("grey69")

    @property
    def grey7(self) -> Tag:
        """abbreviation: `grey7`"""
        return Tag("grey7")

    @property
    def grey70(self) -> Tag:
        """abbreviation: `grey70`"""
        return Tag("grey70")

    @property
    def grey74(self) -> Tag:
        """abbreviation: `grey74`"""
        return Tag("grey74")

    @property
    def grey78(self) -> Tag:
        """abbreviation: `grey78`"""
        return Tag("grey78")

    @property
    def grey82(self) -> Tag:
        """abbreviation: `grey82`"""
        return Tag("grey82")

    @property
    def grey84(self) -> Tag:
        """abbreviation: `grey84`"""
        return Tag("grey84")

    @property
    def grey85(self) -> Tag:
        """abbreviation: `grey85`"""
        return Tag("grey85")

    @property
    def grey89(self) -> Tag:
        """abbreviation: `grey89`"""
        return Tag("grey89")

    @property
    def grey93(self) -> Tag:
        """abbreviation: `grey93`"""
        return Tag("grey93")

    @property
    def honeydew2(self) -> Tag:
        """abbreviation: `ho2`"""
        return Tag("honeydew2")

    @property
    def ho2(self) -> Tag:
        """honeydew2"""
        return self.honeydew2

    @property
    def hot_pink(self) -> Tag:
        """abbreviation: `hp`"""
        return Tag("hot_pink")

    @property
    def hp(self) -> Tag:
        """hot_pink"""
        return self.hot_pink

    @property
    def hot_pink2(self) -> Tag:
        """abbreviation: `hp2`"""
        return Tag("hot_pink2")

    @property
    def hp2(self) -> Tag:
        """hot_pink2"""
        return self.hot_pink2

    @property
    def hot_pink3(self) -> Tag:
        """abbreviation: `hp3`"""
        return Tag("hot_pink3")

    @property
    def hp3(self) -> Tag:
        """hot_pink3"""
        return self.hot_pink3

    @property
    def indian_red(self) -> Tag:
        """abbreviation: `ir`"""
        return Tag("indian_red")

    @property
    def ir(self) -> Tag:
        """indian_red"""
        return self.indian_red

    @property
    def indian_red1(self) -> Tag:
        """abbreviation: `ir1`"""
        return Tag("indian_red1")

    @property
    def ir1(self) -> Tag:
        """indian_red1"""
        return self.indian_red1

    @property
    def khaki1(self) -> Tag:
        """abbreviation: `k1`"""
        return Tag("khaki1")

    @property
    def k1(self) -> Tag:
        """khaki1"""
        return self.khaki1

    @property
    def khaki3(self) -> Tag:
        """abbreviation: `k3`"""
        return Tag("khaki3")

    @property
    def k3(self) -> Tag:
        """khaki3"""
        return self.khaki3

    @property
    def light_coral(self) -> Tag:
        """abbreviation: `lc`"""
        return Tag("light_coral")

    @property
    def lc(self) -> Tag:
        """light_coral"""
        return self.light_coral

    @property
    def light_cyan1(self) -> Tag:
        """abbreviation: `lc1`"""
        return Tag("light_cyan1")

    @property
    def lc1(self) -> Tag:
        """light_cyan1"""
        return self.light_cyan1

    @property
    def light_cyan3(self) -> Tag:
        """abbreviation: `lc3`"""
        return Tag("light_cyan3")

    @property
    def lc3(self) -> Tag:
        """light_cyan3"""
        return self.light_cyan3

    @property
    def light_goldenrod1(self) -> Tag:
        """abbreviation: `lg1`"""
        return Tag("light_goldenrod1")

    @property
    def lg1(self) -> Tag:
        """light_goldenrod1"""
        return self.light_goldenrod1

    @property
    def light_goldenrod2(self) -> Tag:
        """abbreviation: `lg2`"""
        return Tag("light_goldenrod2")

    @property
    def lg2(self) -> Tag:
        """light_goldenrod2"""
        return self.light_goldenrod2

    @property
    def light_goldenrod3(self) -> Tag:
        """abbreviation: `lg3`"""
        return Tag("light_goldenrod3")

    @property
    def lg3(self) -> Tag:
        """light_goldenrod3"""
        return self.light_goldenrod3

    @property
    def light_green(self) -> Tag:
        """abbreviation: `lg`"""
        return Tag("light_green")

    @property
    def lg(self) -> Tag:
        """light_green"""
        return self.light_green

    @property
    def light_pink1(self) -> Tag:
        """abbreviation: `lp1`"""
        return Tag("light_pink1")

    @property
    def lp1(self) -> Tag:
        """light_pink1"""
        return self.light_pink1

    @property
    def light_pink3(self) -> Tag:
        """abbreviation: `lp3`"""
        return Tag("light_pink3")

    @property
    def lp3(self) -> Tag:
        """light_pink3"""
        return self.light_pink3

    @property
    def light_pink4(self) -> Tag:
        """abbreviation: `lp4`"""
        return Tag("light_pink4")

    @property
    def lp4(self) -> Tag:
        """light_pink4"""
        return self.light_pink4

    @property
    def light_salmon1(self) -> Tag:
        """abbreviation: `ls1`"""
        return Tag("light_salmon1")

    @property
    def ls1(self) -> Tag:
        """light_salmon1"""
        return self.light_salmon1

    @property
    def light_salmon3(self) -> Tag:
        """abbreviation: `ls3`"""
        return Tag("light_salmon3")

    @property
    def ls3(self) -> Tag:
        """light_salmon3"""
        return self.light_salmon3

    @property
    def light_sea_green(self) -> Tag:
        """abbreviation: `lsg`"""
        return Tag("light_sea_green")

    @property
    def lsg(self) -> Tag:
        """light_sea_green"""
        return self.light_sea_green

    @property
    def light_sky_blue1(self) -> Tag:
        """abbreviation: `lsb1`"""
        return Tag("light_sky_blue1")

    @property
    def lsb1(self) -> Tag:
        """light_sky_blue1"""
        return self.light_sky_blue1

    @property
    def light_sky_blue3(self) -> Tag:
        """abbreviation: `lsb3`"""
        return Tag("light_sky_blue3")

    @property
    def lsb3(self) -> Tag:
        """light_sky_blue3"""
        return self.light_sky_blue3

    @property
    def light_slate_blue(self) -> Tag:
        """abbreviation: `lsb`"""
        return Tag("light_slate_blue")

    @property
    def lsb(self) -> Tag:
        """light_slate_blue"""
        return self.light_slate_blue

    @property
    def light_slate_grey(self) -> Tag:
        """abbreviation: `lislgr`"""
        return Tag("light_slate_grey")

    @property
    def lislgr(self) -> Tag:
        """light_slate_grey"""
        return self.light_slate_grey

    @property
    def light_steel_blue(self) -> Tag:
        """abbreviation: `listbl`"""
        return Tag("light_steel_blue")

    @property
    def listbl(self) -> Tag:
        """light_steel_blue"""
        return self.light_steel_blue

    @property
    def light_steel_blue1(self) -> Tag:
        """abbreviation: `listbl1`"""
        return Tag("light_steel_blue1")

    @property
    def listbl1(self) -> Tag:
        """light_steel_blue1"""
        return self.light_steel_blue1

    @property
    def light_steel_blue3(self) -> Tag:
        """abbreviation: `listbl3`"""
        return Tag("light_steel_blue3")

    @property
    def listbl3(self) -> Tag:
        """light_steel_blue3"""
        return self.light_steel_blue3

    @property
    def light_yellow3(self) -> Tag:
        """abbreviation: `ly3`"""
        return Tag("light_yellow3")

    @property
    def ly3(self) -> Tag:
        """light_yellow3"""
        return self.light_yellow3

    @property
    def magenta(self) -> Tag:
        """abbreviation: `m`"""
        return Tag("magenta")

    @property
    def m(self) -> Tag:
        """magenta"""
        return self.magenta

    @property
    def magenta1(self) -> Tag:
        """abbreviation: `m1`"""
        return Tag("magenta1")

    @property
    def m1(self) -> Tag:
        """magenta1"""
        return self.magenta1

    @property
    def magenta2(self) -> Tag:
        """abbreviation: `m2`"""
        return Tag("magenta2")

    @property
    def m2(self) -> Tag:
        """magenta2"""
        return self.magenta2

    @property
    def magenta3(self) -> Tag:
        """abbreviation: `m3`"""
        return Tag("magenta3")

    @property
    def m3(self) -> Tag:
        """magenta3"""
        return self.magenta3

    @property
    def medium_orchid(self) -> Tag:
        """abbreviation: `mo`"""
        return Tag("medium_orchid")

    @property
    def mo(self) -> Tag:
        """medium_orchid"""
        return self.medium_orchid

    @property
    def medium_orchid1(self) -> Tag:
        """abbreviation: `mo1`"""
        return Tag("medium_orchid1")

    @property
    def mo1(self) -> Tag:
        """medium_orchid1"""
        return self.medium_orchid1

    @property
    def medium_orchid3(self) -> Tag:
        """abbreviation: `mo3`"""
        return Tag("medium_orchid3")

    @property
    def mo3(self) -> Tag:
        """medium_orchid3"""
        return self.medium_orchid3

    @property
    def medium_purple(self) -> Tag:
        """abbreviation: `mp`"""
        return Tag("medium_purple")

    @property
    def mp(self) -> Tag:
        """medium_purple"""
        return self.medium_purple

    @property
    def medium_purple1(self) -> Tag:
        """abbreviation: `mp1`"""
        return Tag("medium_purple1")

    @property
    def mp1(self) -> Tag:
        """medium_purple1"""
        return self.medium_purple1

    @property
    def medium_purple2(self) -> Tag:
        """abbreviation: `mp2`"""
        return Tag("medium_purple2")

    @property
    def mp2(self) -> Tag:
        """medium_purple2"""
        return self.medium_purple2

    @property
    def medium_purple3(self) -> Tag:
        """abbreviation: `mp3`"""
        return Tag("medium_purple3")

    @property
    def mp3(self) -> Tag:
        """medium_purple3"""
        return self.medium_purple3

    @property
    def medium_purple4(self) -> Tag:
        """abbreviation: `mp4`"""
        return Tag("medium_purple4")

    @property
    def mp4(self) -> Tag:
        """medium_purple4"""
        return self.medium_purple4

    @property
    def medium_spring_green(self) -> Tag:
        """abbreviation: `msg`"""
        return Tag("medium_spring_green")

    @property
    def msg(self) -> Tag:
        """medium_spring_green"""
        return self.medium_spring_green

    @property
    def medium_turquoise(self) -> Tag:
        """abbreviation: `mt`"""
        return Tag("medium_turquoise")

    @property
    def mt(self) -> Tag:
        """medium_turquoise"""
        return self.medium_turquoise

    @property
    def medium_violet_red(self) -> Tag:
        """abbreviation: `mvr`"""
        return Tag("medium_violet_red")

    @property
    def mvr(self) -> Tag:
        """medium_violet_red"""
        return self.medium_violet_red

    @property
    def misty_rose1(self) -> Tag:
        """abbreviation: `mr1`"""
        return Tag("misty_rose1")

    @property
    def mr1(self) -> Tag:
        """misty_rose1"""
        return self.misty_rose1

    @property
    def misty_rose3(self) -> Tag:
        """abbreviation: `mr3`"""
        return Tag("misty_rose3")

    @property
    def mr3(self) -> Tag:
        """misty_rose3"""
        return self.misty_rose3

    @property
    def navajo_white1(self) -> Tag:
        """abbreviation: `nw1`"""
        return Tag("navajo_white1")

    @property
    def nw1(self) -> Tag:
        """navajo_white1"""
        return self.navajo_white1

    @property
    def navajo_white3(self) -> Tag:
        """abbreviation: `nw3`"""
        return Tag("navajo_white3")

    @property
    def nw3(self) -> Tag:
        """navajo_white3"""
        return self.navajo_white3

    @property
    def navy_blue(self) -> Tag:
        """abbreviation: `nb`"""
        return Tag("navy_blue")

    @property
    def nb(self) -> Tag:
        """navy_blue"""
        return self.navy_blue

    @property
    def orange1(self) -> Tag:
        """abbreviation: `o1`"""
        return Tag("orange1")

    @property
    def o1(self) -> Tag:
        """orange1"""
        return self.orange1

    @property
    def orange3(self) -> Tag:
        """abbreviation: `o3`"""
        return Tag("orange3")

    @property
    def o3(self) -> Tag:
        """orange3"""
        return self.orange3

    @property
    def orange4(self) -> Tag:
        """abbreviation: `o4`"""
        return Tag("orange4")

    @property
    def o4(self) -> Tag:
        """orange4"""
        return self.orange4

    @property
    def orange_red1(self) -> Tag:
        """abbreviation: `orre1`"""
        return Tag("orange_red1")

    @property
    def orre1(self) -> Tag:
        """orange_red1"""
        return self.orange_red1

    @property
    def orchid(self) -> Tag:
        """abbreviation: `or_`"""
        return Tag("orchid")

    @property
    def or_(self) -> Tag:
        """orchid"""
        return self.orchid

    @property
    def orchid1(self) -> Tag:
        """abbreviation: `or1`"""
        return Tag("orchid1")

    @property
    def or1(self) -> Tag:
        """orchid1"""
        return self.orchid1

    @property
    def orchid2(self) -> Tag:
        """abbreviation: `or2`"""
        return Tag("orchid2")

    @property
    def or2(self) -> Tag:
        """orchid2"""
        return self.orchid2

    @property
    def pale_green1(self) -> Tag:
        """abbreviation: `pg1`"""
        return Tag("pale_green1")

    @property
    def pg1(self) -> Tag:
        """pale_green1"""
        return self.pale_green1

    @property
    def pale_green3(self) -> Tag:
        """abbreviation: `pg3`"""
        return Tag("pale_green3")

    @property
    def pg3(self) -> Tag:
        """pale_green3"""
        return self.pale_green3

    @property
    def pale_turquoise1(self) -> Tag:
        """abbreviation: `pt1`"""
        return Tag("pale_turquoise1")

    @property
    def pt1(self) -> Tag:
        """pale_turquoise1"""
        return self.pale_turquoise1

    @property
    def pale_turquoise4(self) -> Tag:
        """abbreviation: `pt4`"""
        return Tag("pale_turquoise4")

    @property
    def pt4(self) -> Tag:
        """pale_turquoise4"""
        return self.pale_turquoise4

    @property
    def pale_violet_red1(self) -> Tag:
        """abbreviation: `pvr1`"""
        return Tag("pale_violet_red1")

    @property
    def pvr1(self) -> Tag:
        """pale_violet_red1"""
        return self.pale_violet_red1

    @property
    def pink1(self) -> Tag:
        """abbreviation: `p1`"""
        return Tag("pink1")

    @property
    def p1(self) -> Tag:
        """pink1"""
        return self.pink1

    @property
    def pink3(self) -> Tag:
        """abbreviation: `p3`"""
        return Tag("pink3")

    @property
    def p3(self) -> Tag:
        """pink3"""
        return self.pink3

    @property
    def plum1(self) -> Tag:
        """abbreviation: `pl1`"""
        return Tag("plum1")

    @property
    def pl1(self) -> Tag:
        """plum1"""
        return self.plum1

    @property
    def plum2(self) -> Tag:
        """abbreviation: `pl2`"""
        return Tag("plum2")

    @property
    def pl2(self) -> Tag:
        """plum2"""
        return self.plum2

    @property
    def plum3(self) -> Tag:
        """abbreviation: `pl3`"""
        return Tag("plum3")

    @property
    def pl3(self) -> Tag:
        """plum3"""
        return self.plum3

    @property
    def plum4(self) -> Tag:
        """abbreviation: `pl4`"""
        return Tag("plum4")

    @property
    def pl4(self) -> Tag:
        """plum4"""
        return self.plum4

    @property
    def purple(self) -> Tag:
        """abbreviation: `pu`"""
        return Tag("purple")

    @property
    def pu(self) -> Tag:
        """purple"""
        return self.purple

    @property
    def purple3(self) -> Tag:
        """abbreviation: `pu3`"""
        return Tag("purple3")

    @property
    def pu3(self) -> Tag:
        """purple3"""
        return self.purple3

    @property
    def purple4(self) -> Tag:
        """abbreviation: `pu4`"""
        return Tag("purple4")

    @property
    def pu4(self) -> Tag:
        """purple4"""
        return self.purple4

    @property
    def red(self) -> Tag:
        """abbreviation: `r`"""
        return Tag("red")

    @property
    def r(self) -> Tag:
        """red"""
        return self.red

    @property
    def red1(self) -> Tag:
        """abbreviation: `r1`"""
        return Tag("red1")

    @property
    def r1(self) -> Tag:
        """red1"""
        return self.red1

    @property
    def red3(self) -> Tag:
        """abbreviation: `r3`"""
        return Tag("red3")

    @property
    def r3(self) -> Tag:
        """red3"""
        return self.red3

    @property
    def rosy_brown(self) -> Tag:
        """abbreviation: `rb`"""
        return Tag("rosy_brown")

    @property
    def rb(self) -> Tag:
        """rosy_brown"""
        return self.rosy_brown

    @property
    def royal_blue1(self) -> Tag:
        """abbreviation: `rb1`"""
        return Tag("royal_blue1")

    @property
    def rb1(self) -> Tag:
        """royal_blue1"""
        return self.royal_blue1

    @property
    def salmon1(self) -> Tag:
        """abbreviation: `s1`"""
        return Tag("salmon1")

    @property
    def s1(self) -> Tag:
        """salmon1"""
        return self.salmon1

    @property
    def sandy_brown(self) -> Tag:
        """abbreviation: `sb`"""
        return Tag("sandy_brown")

    @property
    def sb(self) -> Tag:
        """sandy_brown"""
        return self.sandy_brown

    @property
    def sea_green1(self) -> Tag:
        """abbreviation: `sg1`"""
        return Tag("sea_green1")

    @property
    def sg1(self) -> Tag:
        """sea_green1"""
        return self.sea_green1

    @property
    def sea_green2(self) -> Tag:
        """abbreviation: `sg2`"""
        return Tag("sea_green2")

    @property
    def sg2(self) -> Tag:
        """sea_green2"""
        return self.sea_green2

    @property
    def sea_green3(self) -> Tag:
        """abbreviation: `sg3`"""
        return Tag("sea_green3")

    @property
    def sg3(self) -> Tag:
        """sea_green3"""
        return self.sea_green3

    @property
    def sky_blue1(self) -> Tag:
        """abbreviation: `sb1`"""
        return Tag("sky_blue1")

    @property
    def sb1(self) -> Tag:
        """sky_blue1"""
        return self.sky_blue1

    @property
    def sky_blue2(self) -> Tag:
        """abbreviation: `sb2`"""
        return Tag("sky_blue2")

    @property
    def sb2(self) -> Tag:
        """sky_blue2"""
        return self.sky_blue2

    @property
    def sky_blue3(self) -> Tag:
        """abbreviation: `sb3`"""
        return Tag("sky_blue3")

    @property
    def sb3(self) -> Tag:
        """sky_blue3"""
        return self.sky_blue3

    @property
    def slate_blue1(self) -> Tag:
        """abbreviation: `slbl1`"""
        return Tag("slate_blue1")

    @property
    def slbl1(self) -> Tag:
        """slate_blue1"""
        return self.slate_blue1

    @property
    def slate_blue3(self) -> Tag:
        """abbreviation: `slbl3`"""
        return Tag("slate_blue3")

    @property
    def slbl3(self) -> Tag:
        """slate_blue3"""
        return self.slate_blue3

    @property
    def spring_green1(self) -> Tag:
        """abbreviation: `spgr1`"""
        return Tag("spring_green1")

    @property
    def spgr1(self) -> Tag:
        """spring_green1"""
        return self.spring_green1

    @property
    def spring_green2(self) -> Tag:
        """abbreviation: `spgr2`"""
        return Tag("spring_green2")

    @property
    def spgr2(self) -> Tag:
        """spring_green2"""
        return self.spring_green2

    @property
    def spring_green3(self) -> Tag:
        """abbreviation: `spgr3`"""
        return Tag("spring_green3")

    @property
    def spgr3(self) -> Tag:
        """spring_green3"""
        return self.spring_green3

    @property
    def spring_green4(self) -> Tag:
        """abbreviation: `spgr4`"""
        return Tag("spring_green4")

    @property
    def spgr4(self) -> Tag:
        """spring_green4"""
        return self.spring_green4

    @property
    def steel_blue(self) -> Tag:
        """abbreviation: `stbl`"""
        return Tag("steel_blue")

    @property
    def stbl(self) -> Tag:
        """steel_blue"""
        return self.steel_blue

    @property
    def steel_blue1(self) -> Tag:
        """abbreviation: `stbl1`"""
        return Tag("steel_blue1")

    @property
    def stbl1(self) -> Tag:
        """steel_blue1"""
        return self.steel_blue1

    @property
    def steel_blue3(self) -> Tag:
        """abbreviation: `stbl3`"""
        return Tag("steel_blue3")

    @property
    def stbl3(self) -> Tag:
        """steel_blue3"""
        return self.steel_blue3

    @property
    def tan(self) -> Tag:
        """abbreviation: `ta`"""
        return Tag("tan")

    @property
    def ta(self) -> Tag:
        """tan"""
        return self.tan

    @property
    def thistle1(self) -> Tag:
        """abbreviation: `th1`"""
        return Tag("thistle1")

    @property
    def th1(self) -> Tag:
        """thistle1"""
        return self.thistle1

    @property
    def thistle3(self) -> Tag:
        """abbreviation: `th3`"""
        return Tag("thistle3")

    @property
    def th3(self) -> Tag:
        """thistle3"""
        return self.thistle3

    @property
    def turquoise2(self) -> Tag:
        """abbreviation: `t2`"""
        return Tag("turquoise2")

    @property
    def t2(self) -> Tag:
        """turquoise2"""
        return self.turquoise2

    @property
    def turquoise4(self) -> Tag:
        """abbreviation: `t4`"""
        return Tag("turquoise4")

    @property
    def t4(self) -> Tag:
        """turquoise4"""
        return self.turquoise4

    @property
    def violet(self) -> Tag:
        """abbreviation: `v`"""
        return Tag("violet")

    @property
    def v(self) -> Tag:
        """violet"""
        return self.violet

    @property
    def wheat1(self) -> Tag:
        """abbreviation: `wh1`"""
        return Tag("wheat1")

    @property
    def wh1(self) -> Tag:
        """wheat1"""
        return self.wheat1

    @property
    def wheat4(self) -> Tag:
        """abbreviation: `wh4`"""
        return Tag("wheat4")

    @property
    def wh4(self) -> Tag:
        """wheat4"""
        return self.wheat4

    @property
    def white(self) -> Tag:
        """abbreviation: `w`"""
        return Tag("white")

    @property
    def w(self) -> Tag:
        """white"""
        return self.white

    @property
    def yellow(self) -> Tag:
        """abbreviation: `y`"""
        return Tag("yellow")

    @property
    def y(self) -> Tag:
        """yellow"""
        return self.yellow

    @property
    def yellow1(self) -> Tag:
        """abbreviation: `y1`"""
        return Tag("yellow1")

    @property
    def y1(self) -> Tag:
        """yellow1"""
        return self.yellow1

    @property
    def yellow2(self) -> Tag:
        """abbreviation: `y2`"""
        return Tag("yellow2")

    @property
    def y2(self) -> Tag:
        """yellow2"""
        return self.yellow2

    @property
    def yellow3(self) -> Tag:
        """abbreviation: `y3`"""
        return Tag("yellow3")

    @property
    def y3(self) -> Tag:
        """yellow3"""
        return self.yellow3

    @property
    def yellow4(self) -> Tag:
        """abbreviation: `y4`"""
        return Tag("yellow4")

    @property
    def y4(self) -> Tag:
        """yellow4"""
        return self.yellow4
