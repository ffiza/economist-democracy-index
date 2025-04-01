from colors import Colors


class Config:
    def __init__(self):
        colors = Colors()

        self.region_colors = {
            "North America": colors.PURPLE,
            "Western Europe": colors.PINK,
            "Eastern Europe and Central Asia": colors.ORANGE,
            "Latin America and the Caribbean": colors.GREEN,
            "Asia and Australasia": colors.BLUE,
            "Middle East and North Africa": colors.RED,
            "Sub-Saharan Africa": colors.BROWN,
        }

        self.region_bg_colors = {
            "North America": colors.LIGHT_PURPLE,
            "Western Europe": colors.LIGHT_PINK,
            "Eastern Europe and Central Asia": colors.LIGHT_ORANGE,
            "Latin America and the Caribbean": colors.LIGHT_GREEN,
            "Asia and Australasia": colors.LIGHT_BLUE,
            "Middle East and North Africa": colors.LIGHT_RED,
            "Sub-Saharan Africa": colors.LIGHT_BROWN,
        }
