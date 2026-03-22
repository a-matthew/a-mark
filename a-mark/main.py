# ================================
# Name: 'a-mark'/main.py
# Author: 'a-matthew'/Mateusz A.
# Year: 2022-2026
# Comments: No LLMs are used.
# Quick references:
# https://docs.python.org/3/library/stdtypes.html
# https://docs.python.org/3/library/configparser.html
# https://pillow.readthedocs.io/en/stable/index.html
# ================================

import argparse
import operator

# Built-in
import os
import textwrap
from configparser import RawConfigParser  # , ConfigParser
from os.path import abspath

import numpy

# Custom
from PIL import Image, ImageDraw, ImageFont

DEBUG = 1
PATH_DIRECTORY_MODULE = os.path.split(os.path.realpath(__file__))[0]


def effect_coordinates_calculate(
    effect_type, effect_position, text_size, image_size
) -> tuple[float, float]:
    """
    Calculate initial XY text-box coordinates.
    """
    effect_coordinates = (0.0, 0.0)
    if effect_position == "top" and effect_type == "horizontal":
        try:
            effect_coordinates = (
                image_size[0] / 2.0,
                0.0,
            )
        except Exception as e:
            print("effect_coordinates_calculate: failure!")
            print(e)
    elif effect_position == "center":
        try:
            effect_coordinates = (
                image_size[0] / 2.0,
                image_size[1] / 2.0 - text_size / 2.0,
            )
        except Exception as e:
            print("effect_coordinates_calculate: failure!")
            print(e)
    elif effect_position == "bottom" and effect_type == "horizontal":
        try:
            effect_coordinates = (
                image_size[0] / 2.0,
                image_size[1],
            )
        except Exception as e:
            print("effect_coordinates_calculate: failure!")
            print(e)
    if DEBUG == 1:
        print(
            f"effect_coordinates_calculate|effect_coordinates[0]: {effect_coordinates[0]}"  # noqa: E501
        )
        print(
            f"effect_coordinates_calculate|effect_coordinates[1]: {effect_coordinates[1]}"  # noqa: E501
        )
    return effect_coordinates


def effect_offset_calculate(
    effect_type, effect_position, effect_offset
) -> tuple[float, float]:
    """
    Calculate the overall offset of the XY coordinates.
    """
    if effect_position == "top" and effect_type == "horizontal":
        try:
            effect_offset = numpy.array(effect_offset) * numpy.array(
                [1.0, 1.0]
            )  # 'Hadamard product'
        except Exception as e:
            print("effect_offset_calculate: failure!")
            print(e)
    elif effect_position == "center":
        try:
            # effect_offset = numpy.array(effect_offset) * numpy.array(
            #    [1, 0]
            # )  # 'Hadamard product'
            pass
        except Exception as e:
            print("effect_offset_calculate: failure!")
            print(e)
    elif effect_position == "bottom" and effect_type == "horizontal":
        try:
            effect_offset = numpy.array(effect_offset) * numpy.array(
                [1.0, -1.0]
            )  # 'Hadamard product'
        except Exception as e:
            print("effect_offset_calculate: failure!")
            print(e)
    if DEBUG == 1:
        print(f"effect_offset_calculate|effect_offset[0]: {effect_offset[0]}")
        print(f"effect_offset_calculate|effect_offset[1]: {effect_offset[1]}")
    return tuple(effect_offset)


def effect_anchor_calculate(effect_type, effect_position) -> str:
    """
    Calculate the anchor point of the XY coordinates.
    """
    effect_anchor = ""
    if effect_position == "top" and effect_type == "horizontal":
        effect_anchor = "mt"
    elif effect_position == "center":
        effect_anchor = "mm"
    elif effect_position == "bottom" and effect_type == "horizontal":
        effect_anchor = "mb"
    return effect_anchor


def text_line_spacing_calculate(
    effect_position, text_size, text_spacing, index
) -> float:
    """
    Calculate the text line-specific offset.
    """
    try:
        line_spacing = index * (text_size + text_spacing)
        if effect_position == "center":
            if index % 2 == 1:
                line_spacing = index / 2 * (text_size + text_spacing) + 0.5 * (
                    text_size + text_spacing
                )
            else:
                line_spacing = -(index / 2) * (text_size + text_spacing)
    except Exception as e:
        print("text_line_spacing_calculate: failure!")
        print(e)
    return float(line_spacing)


def text_lines_translate(effect_type, effect_position, text_lines) -> list[str]:
    """
    Translate order of text lines.
    """
    if effect_position == "top" and effect_type == "horizontal":
        try:
            pass
        except Exception as e:
            print("text_lines_translate: failure!")
            print(e)
    elif effect_position == "center":
        try:
            pass
        except Exception as e:
            print("text_lines_translate: failure!")
            print(e)
    elif effect_position == "bottom" and effect_type == "horizontal":
        try:
            text_lines.reverse()
        except Exception as e:
            print("text_lines_translate: failure!")
            print(e)
    if DEBUG == 1:
        print(f"text_lines_translate|text_lines: {text_lines}")
    return list(text_lines)


def config_read(
    path_config,
    path_input,
    path_output,
    name_output,
    effect_type,
    effect_position,
    effect_offset_horizontal,
    effect_offset_vertical,
    text_width_line,
    text_spacing,
) -> object:
    """
    Read configuration from confit.ini file and default missing parameters.
    """
    config = RawConfigParser()
    try:
        if path_config is None:
            path_config = os.path.join(PATH_DIRECTORY_MODULE, "config.ini")
        if DEBUG == 1:
            print(f"config_read|path_config: {path_config}")
        config.read(path_config)
        if path_input is None:
            path_input = (
                os.path.join(PATH_DIRECTORY_MODULE, config.get("path", "PATH_INPUT"))
                if config.get("path", "PATH_INPUT") is not None
                else os.path.join(PATH_DIRECTORY_MODULE, "input/")
            )
        if DEBUG == 1:
            print(f"config_read|path_input: {path_input}")
        if path_output is None:
            path_output = (
                os.path.join(PATH_DIRECTORY_MODULE, config.get("path", "PATH_OUTPUT"))
                if config.get("path", "PATH_OUTPUT") is not None
                else os.path.join(PATH_DIRECTORY_MODULE, "output/")
            )
        if DEBUG == 1:
            print(f"config_read|path_output: {path_output}")
        if name_output is None:
            pass
        if DEBUG == 1:
            print(f"config_read|name_output: {name_output}")
        if effect_type is None:
            effect_type = (
                config.get("effect", "EFFECT_TYPE")
                if config.get("effect", "EFFECT_TYPE") is not None
                else "horizontal"
            )
        if DEBUG == 1:
            print(f"config_read|effect_type: {effect_type}")
        if effect_position is None:
            effect_position = (
                config.get("effect", "EFFECT_POSITION")
                if config.get("effect", "EFFECT_POSITION") is not None
                else "center"
            )
        if DEBUG == 1:
            print(f"config_read|effect_position: {effect_position}")
        effect_offset_horizontal = (
            config.get("effect", "EFFECT_OFFSET_HORIZONTAL")
            if config.get("effect", "EFFECT_OFFSET_HORIZONTAL") is not None
            else 0
        )
        if DEBUG == 1:
            print(f"config_read|effect_offset_horizontal: {effect_offset_horizontal}")
        effect_offset_vertical = (
            config.get("effect", "EFFECT_OFFSET_VERTICAL")
            if config.get("effect", "EFFECT_OFFSET_VERTICAL") is not None
            else 0
        )
        if DEBUG == 1:
            print(f"config_read|effect_offset_vertical: {effect_offset_vertical}")
        text_size = (
            int(config.getint("text", "TEXT_SIZE"))
            if config.getint("text", "TEXT_SIZE") is not None
            else 50
        )
        if DEBUG == 1:
            print(f"config_read|text_size: {text_size}")
        text_width_line = (
            int(config.get("text", "TEXT_WIDTH_LINE"))
            if config.get("text", "TEXT_WIDTH_LINE") is not None
            else 20
        )
        if DEBUG == 1:
            print(f"config_read|text_width_line: {text_width_line}")
        text_spacing = (
            int(config.get("text", "TEXT_SPACING"))
            if config.get("text", "TEXT_SPACING") is not None
            else 5
        )
        if DEBUG == 1:
            print(f"config_read|text_spacing: {text_spacing}")
        text_font_family = (
            config.get("text", "TEXT_FONT_FAMILY")
            if config.get("text", "TEXT_FONT_FAMILY") is not None
            else "/usr/share/fonts/qualitype/QTGaromand-Bold.otf"
        )
        if DEBUG == 1:
            print(f"config_read|text_font_family: {text_font_family}")
        text_color = (
            config.get("text", "TEXT_COLOR")
            if config.get("text", "TEXT_COLOR") is not None
            else "255, 76, 48, 128"
        )
        if DEBUG == 1:
            print(f"config_read|text_color: {text_color}")
        text_caption = (
            config.get("text", "TEXT_CAPTION")
            if config.get("text", "TEXT_CAPTION") is not None
            else "LoremIpsum"
        )
        if DEBUG == 1:
            print(f"config_read|text_caption: {text_caption}")
    except Exception as e:
        print("config_read: failure!")
        print(e)
    else:
        return {
            "path_config": str(path_config),
            "path_input": str(path_input),
            "path_output": str(path_output),
            "name_output": str(name_output),
            "effect_type": str(effect_type),
            "effect_position": str(effect_position),
            "effect_offset_horizontal": int(effect_offset_horizontal),
            "effect_offset_vertical": int(effect_offset_vertical),
            "text_size": int(text_size),
            "text_width_line": int(text_width_line),
            "text_spacing": int(text_spacing),
            "text_font_family": str(text_font_family),
            "text_color": str(text_color),
            "text_caption": str(text_caption),
        }


def image_read(config) -> list[tuple]:
    """
    Read all images from the input path.
    """
    format_image = [".jpg", ".png"]
    list_images = []
    try:
        path_input = abspath(config["path_input"])
        for file_name in os.listdir(path_input):
            file_extension = os.path.splitext(file_name)[
                1
            ]  # Split extensions from names
            if file_extension.lower() in format_image:
                try:
                    list_images.append(
                        (Image.open(os.path.join(path_input, file_name)), file_name)
                    )
                except Exception:
                    print(f"images_read|image_read: {file_name} failure!")
    except Exception as e:
        print("images_read|path_read: failure!")
        print(e)
    return list_images


def image_write(config, list_images):
    """
    Write effects to all loaded images.
    """
    try:
        image_font = ImageFont.truetype(config["text_font_family"], config["text_size"])
    except Exception as e:
        print("image_write|font_read: failure!")
        print(e)
    for tuple_image in list_images:
        image_draw = ImageDraw.Draw(tuple_image[0])
        try:
            lines_text = text_lines_translate(
                config["effect_type"],
                config["effect_position"],
                textwrap.wrap(
                    text=config["text_caption"],
                    width=config["text_width_line"],
                    placeholder=" (...)",
                ),
            )
            for index, line_text in enumerate(lines_text):
                line_text_spacing = text_line_spacing_calculate(
                    config["effect_position"],
                    config["text_size"],
                    config["text_spacing"],
                    index,
                )
                image_draw.text(
                    xy=tuple(
                        map(  # noqa: E501 Maps can call functions https://docs.python.org/3/library/functions.html#map
                            operator.add,
                            numpy.array(
                                effect_coordinates_calculate(
                                    config["effect_type"],
                                    config["effect_position"],
                                    config["text_size"],
                                    tuple_image[0].size,
                                )
                            ),
                            numpy.array(
                                effect_offset_calculate(
                                    config["effect_type"],
                                    config["effect_position"],
                                    (
                                        config["effect_offset_horizontal"],
                                        config["effect_offset_vertical"]
                                        + line_text_spacing,
                                    ),
                                )
                            ),
                        )
                    ),
                    text=line_text,
                    font=image_font,
                    anchor=effect_anchor_calculate(
                        config["effect_type"],
                        config["effect_position"],
                    ),
                    fill=tuple([int(n) for n in config["text_color"].split(", ")]),
                )
        except Exception as e:
            print("image_write|text_draw: failure!")
            print(e)
        try:
            if config["name_output"] == "None":  # By default str()
                tuple_image[0].save(
                    os.path.join(abspath(config["path_output"]), tuple_image[1])
                )
            else:
                tuple_image[0].save(
                    os.path.join(abspath(config["path_output"]), config["name_output"])
                )
        except Exception as e:
            print("image_write|image_write: failure!")
            print(e)
            print(os.path.join(abspath(config["path_output"]), tuple_image[1]))


if __name__ == "__main__":
    """
    Initialize main module with argument parsing.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_config",
        help="(Optional) Path of the config file (module's config.ini used by default!) (str).",  # noqa: E501
        type=str,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--path_input",
        help="(Optional) Path of the input directory. All images in ['.jpg', '.png'] format will be processed (str).",  # noqa: E501
        type=str,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--path_output",
        help="(Optional) Path of the output directory (str).",  # noqa: E501
        type=str,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--name_output",
        help="(Optional) Name of the output file (by default the same as original) (str).",  # noqa: E501
        type=str,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--effect_type",
        help="(Optional) Type of the effect ['horizontal', 'diagonal'] (str).",  # noqa: E501
        type=str,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--effect_position",
        help="(Optional) Position of the effect ['bottom', 'center', 'top'] (str).",  # noqa: E501
        type=str,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--effect_offset_horizontal",
        help="(Optional) Horizontal offset of the effect (int).",  # noqa: E501
        type=int,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--effect_offset_vertical",
        help="(Optional) Vertical offset of the effect (int).",  # noqa: E501
        type=int,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--text_width_line",
        help="(Optional) Width of the text line, counted in characters per line (int).",  # noqa: E501
        type=int,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--text_spacing",
        help="(Optional) Spacing of the text multi-line, counted in pixels between the lines (int).",  # noqa: E501
        type=int,
        nargs="?",
        default=None,
    )
    args = parser.parse_args()
    config = config_read(
        args.path_config,
        args.path_input,
        args.path_output,
        args.name_output,
        args.effect_type,
        args.effect_position,
        args.effect_offset_horizontal,
        args.effect_offset_vertical,
        args.text_width_line,
        args.text_spacing,
    )
    try:
        list_images = image_read(config)
        image_write(config, list_images)
    except Exception as e:
        print("__main__|image_write: failure!")
        print(e)
