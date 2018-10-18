# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2018 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from collections import OrderedDict
from bokeh import palettes
from IPython.core.display import HTML
import colour
import yaml

from chartify._core.options import options


class CustomColors:
    def __init__(self):

        config_filename = options.get_option('config.colors')
        try:
            self.colors = self.from_yaml(config_filename)
        except FileNotFoundError:
            self.colors = {
                (232, 232, 232): 'Light Grey',
                (83, 88, 95): 'Dark Grey',
            }

    def to_yaml(self, filename):
        """Write colors to a yaml file"""
        with open(filename, 'w') as outfile:
            yaml.dump(self.colors, outfile, default_flow_style=False)

    def from_yaml(self, filename):
        """Load colors from yaml file"""
        return yaml.load(open(filename))

    def overwrite_colors(self):
        """Overwrite colors in the colour module with custom colors."""
        if not self.colors:
            return

        for color_rgb, color_name in self.colors.items():
            # Remove color from default names if it already exits.
            color_name = color_name.lower()
            if color_name in list(colour.COLOR_NAME_TO_RGB.keys()):
                delete_color_value = colour.COLOR_NAME_TO_RGB[color_name]
                del colour.RGB_TO_COLOR_NAMES[delete_color_value]
                del colour.COLOR_NAME_TO_RGB[color_name]
            colour.RGB_TO_COLOR_NAMES[color_rgb] = [color_name]

        colour.COLOR_NAME_TO_RGB = dict(
            (name.lower(), rgb)
            for rgb, names in list(colour.RGB_TO_COLOR_NAMES.items())
            for name in names)


# Load custom colors.
CustomColors().overwrite_colors()


class Color(colour.Color):
    DISPLAY_HEIGHT = '20px'
    DISPLAY_WIDTH = '200px'

    def _html(self):
        return """<div style="width: {width};
                        height: {height};
                        background-color: {color};
                        color: {foreground_color};
                        padding: 2px;
                        margin: 2px;
                        display: block;">'{name}',</div>""".format(
            height=self.DISPLAY_HEIGHT,
            width=self.DISPLAY_WIDTH,
            color=self.hex,
            name=self.get_web(),
            foreground_color=self.foreground_color())

    def show(self):
        return HTML(self._html())

    def foreground_color(self):
        return Color('#000000') if self.get_luminance() > 0.4 else Color(
            '#ffffff')

    def linear_gradient(self, finish_color, n=10):
        """Return a gradient list of (n) colors between
        two colors."""
        # Starting and ending colors in RGB form
        s = self.get_rgb()
        f = finish_color.get_rgb()
        # Initilize a list of the output colors with the starting color
        RGB_list = [s]
        # Calcuate a color at each evenly spaced value of t from 1 to n
        for t in range(1, n):
            # Interpolate RGB vector for color at the current value of t
            curr_vector = [(s[j] + (float(t) / (n - 1)) * (f[j] - s[j]))
                           for j in range(3)]
            # Add it to our list of output colors
            RGB_list.append(curr_vector)
        RGB_list = [Color(rgb=r) for r in RGB_list]
        return RGB_list


class ColorPalette:
    def __init__(self, colors, palette_type=None, name=None):
        self.colors = colors
        self.name = name
        self.palette_type = palette_type

    def _html(self):
        return """<div style='padding: 10px; margin: 5px;'>
                  <h3>{name}</h3>{colors}</div>""".format(
            colors=' '.join([c._html() for c in self.colors]), name=self.name)

    def show(self):
        return HTML(self._html())

    @classmethod
    def from_hex_list(cls, colors, palette_type=None, name=None):
        """Create ColorPalette from list of color hex values or color names.

        Args:
            colors (list of str): List of color hex values or names.
            palette_type (str, optional): Type of palette:
                'sequential', 'diverging', 'categorical'
            name (str, optional): Name of color palette.

        """
        hex_list = [Color(color) for color in colors]
        return cls(hex_list, palette_type, name)

    def sort_by_hue(self, ascending=True):
        new_palette = ColorPalette.from_hex_list(
            colors=self.colors[:],
            palette_type=self.palette_type,
            name=self.name)
        new_palette.colors.sort(key=lambda x: x.get_hue(), reverse=ascending)
        return new_palette

    def sort_by_luminance(self, ascending=True):
        new_palette = ColorPalette.from_hex_list(
            colors=self.colors[:],
            palette_type=self.palette_type,
            name=self.name)
        new_palette.colors.sort(
            key=lambda x: x.get_luminance(), reverse=ascending)
        return new_palette

    def sort_by_saturation(self, ascending=True):
        new_palette = ColorPalette.from_hex_list(
            colors=self.colors[:],
            palette_type=self.palette_type,
            name=self.name)
        new_palette.colors.sort(
            key=lambda x: x.get_saturation(), reverse=ascending)
        return new_palette

    def expand_palette(self, target_color_count):
        """Linearly expand the color palette up to the target color count."""
        palette_color_count = len(self.colors)
        if target_color_count <= palette_color_count:
            return self
        target_color_count = target_color_count - 1
        extrapolation_count = [
            target_color_count // (palette_color_count - 1)
        ] * (palette_color_count - 1)
        for i in range(target_color_count % (palette_color_count - 1)):
            extrapolation_count[i] += 1

        extrapolated_palette = []
        for i, count in enumerate(extrapolation_count):
            extrapolated_palette.extend(self.colors[i].linear_gradient(
                self.colors[i + 1], count + 1)[:-1])
        extrapolated_palette.extend([self.colors[-1]])

        return ColorPalette.from_hex_list(
            colors=extrapolated_palette,
            palette_type=self.palette_type,
            name=self.name)

    def shift_palette(self, target_color, percent=10):
        """Shift each color in the palette toward the given target color.

        Args:
            target_color (str): Color hex value or name.
            percent (int): Distance to shift the current palette toward the
                target color.
        """
        shifted_colors = [
            color.linear_gradient(Color(target_color), n=100)[percent - 1]
            for color in self.colors
        ]
        return ColorPalette.from_hex_list(
            colors=shifted_colors,
            palette_type=self.palette_type,
            name=self.name)

    def to_hex_list(self):
        """Return list of hex values of colors in the palette."""
        return [color.get_hex_l() for color in self.colors]

    def __getitem__(self, key):
        if isinstance(key, str):
            color_slice = Color(key)
        else:
            color_slice = self.colors[:][key]

        if isinstance(color_slice, Color):
            color_slice = [color_slice]

        return ColorPalette(
            colors=color_slice, palette_type=self.palette_type, name=self.name)

    def __repr__(self):
        return "Color Palette '{name}': \n{colors}".format(
            name=self.name,
            colors='\n'.join(
                ["'{},'".format(color.get_web()) for color in self.colors]))


class ColorPalettes:
    def __init__(self):
        self._palettes = OrderedDict()

        config_filename = options.get_option('config.color_palettes')
        try:
            self._from_yaml(config_filename)
        except FileNotFoundError:
            pass

    def show(self):
        return HTML("""<h2>Color Palettes</h2><div>{palettes}</div>""".format(
            palettes=' '.join([v._html() for k, v in self._palettes.items()])))

    def _add_palette(self, palette):
        self._palettes[palette.name.lower()] = palette

    def __getitem__(self, item):
        try:
            return self._palettes[item.lower()]
        except (KeyError):
            raise KeyError("""Invalid color palette name.
                See chartify.color_palettes.show() for
                the available color palettes.""")

    def __repr__(self):
        return "Color Palettes: \n{palettes}".format(palettes='\n'.join([
            "'{}'".format(palette.name)
            for key, palette in self._palettes.items()
        ]))

    def _to_yaml(self, filename):
        """Write the color palettes to a yaml file"""
        palette_list = []
        for palette in self._palettes.values():
            hex_color_list = [color.get_hex_l() for color in palette.colors]
            palette_list.append(
                [hex_color_list, palette.palette_type, palette.name])

        with open(filename, 'w') as outfile:
            yaml.dump(palette_list, outfile, default_flow_style=False)

    def _from_yaml(self, filename):
        """Load color palettes from a yaml file"""
        palette_list = yaml.load(open(filename))
        for palette in palette_list:
            hex_color_list, palette_type, name = palette
            self._add_palette(
                ColorPalette.from_hex_list(
                    colors=hex_color_list,
                    palette_type=palette_type,
                    name=name))

    def create_palette(self, colors, palette_type, name):
        """Create ColorPalette from list of color hex values or color names.

        Args:
        colors (list of str): List of color hex values or names.
        palette_type (str, optional): Type of palette:
            'sequential', 'diverging', 'categorical'
        name (str, optional): Name of color palette.
        """
        new_palette = ColorPalette.from_hex_list(
            colors=colors,
            palette_type=palette_type,
            name=name,
            )
        self._add_palette(new_palette)


color_palettes = ColorPalettes()

# See available bokeh palettes here
# https://bokeh.pydata.org/en/latest/docs/reference/palettes.html
color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Category20",
        palette_type='categorical',
        # Reorder the palette to prioritize the bolder colors first.
        colors=palettes.Category20[20][::2] + palettes.Category20[20][1::2]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Category10",
        palette_type='categorical',
        colors=palettes.Category10[10]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Colorblind",
        palette_type='categorical',
        colors=palettes.Colorblind[8]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Dark2", palette_type='categorical', colors=palettes.Dark2[8]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Pastel1", palette_type='categorical',
        colors=palettes.Pastel1[9]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="RdBu", palette_type='diverging', colors=palettes.RdBu[3]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="RdGy", palette_type='diverging', colors=palettes.RdGy[5]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Greys",
        palette_type='sequential',
        colors=palettes.Greys[9][::-1][2:]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Greens",
        palette_type='sequential',
        colors=palettes.Greens[9][::-1][2:]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Blues",
        palette_type='sequential',
        colors=palettes.Blues[9][::-1][2:]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Reds",
        palette_type='sequential',
        colors=palettes.Reds[9][::-1][2:]))

color_palettes._add_palette(
    ColorPalette.from_hex_list(
        name="Oranges",
        palette_type='sequential',
        colors=palettes.Oranges[9][::-1][2:]))

all_colors = ColorPalette(
    name='All colors',
    colors=[
        Color(rgb=[c / 255. for c in color_tuple])
        for color_tuple in colour.RGB_TO_COLOR_NAMES
    ])
all_colors = all_colors.sort_by_hue()
color_palettes._add_palette(all_colors)
