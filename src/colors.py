import matplotlib.colors as mcolors


class Colors:
    """
    A class to manage the color palette and color maps of the project.
    """
    def __init__(self):
        self.LINE = "black"
        self.BLACK = "black"
        self.GRAY = "#7f7f7f"
        self.LIGHT_GRAY = "gainsboro"
        self.DARK_GRAY = "#404040"

        self.BLUE = "#1f77b4"
        self.ORANGE = "#ff7f0e"
        self.GREEN = "#2ca02c"
        self.RED = "#d62728"
        self.PURPLE = "#9467bd"
        self.BROWN = "#8c564b"
        self.PINK = "#e377c2"

        self.LIGHT_BLUE = "#d2e3f0"
        self.LIGHT_ORANGE = "#ffe5ce"
        self.LIGHT_GREEN = "#d4ecd4"
        self.LIGHT_RED = "#f6d3d4"
        self.LIGHT_PURPLE = "#e9e0f1"
        self.LIGHT_BROWN = "#e8dddb"
        self.LIGHT_PINK = "#f9e3f2"

        # A custom colormap to use with Matplotlib
        self.colormaps = {
            "RdWtGr": mcolors.LinearSegmentedColormap.from_list(
                        "RdWtGr",
                        [self.RED, "white", self.GREEN],
                        N=8)
        }

        # A custom colorscale to use with Plotly
        colorscale = []
        for i in range(8):
            j = i / 8
            c = mcolors.rgb2hex(self.colormaps["RdWtGr"]((j + j + 1/8) / 2))
            colorscale.append((j, c))
            colorscale.append((j + 1 / 8, c))
        self.colorscales = {
            "RdWtGr": colorscale,
        }

    @staticmethod
    def get_opaque_hex_from_transparency(hex: str, transparency: float) -> str:
        """
        This method take a hex color and a transparency value (between 0 and 1)
        and returns the equivalent opaque color.

        Parameters
        ----------
        hex : str
            The hexadecimal color.
        transparency : float
            The transparency value. Must be between 0 and 1, where 0 is fully
            transparent and 1 is fully opaque.

        Returns
        -------
        str
            The opaque color in hexadecimal format.
        """
        hex = hex.lstrip("#")
        r, g, b = tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
        r = int(255 - transparency * (255 - r))
        g = int(255 - transparency * (255 - g))
        b = int(255 - transparency * (255 - b))
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
