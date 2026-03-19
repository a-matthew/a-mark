# ================================
# Name: 'a-mark'
# Author: 'a-matthew'/Mateusz A.
# Year: 2022
# Comments: No LLMs are used.
# Quick references:
# https://docs.python.org/3/library/stdtypes.html
# https://docs.python.org/3/library/configparser.html
# https://pillow.readthedocs.io/en/stable/index.html
# ================================

import os, argparse, configparser, textwrap, operator
from os.path import abspath
from configparser import ConfigParser, RawConfigParser

from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)
import numpy

DEBUG = 1
DIRECTORY_MODULE = os.path.split(os.path.realpath(__file__))[0]
# If a component is an absolute path, all previous components are thrown away and joining continues from the absolute path component.
# Just don't use references with slashes in paths.


def effect_coordinates_calculate(
    effect_type, effect_position, text_size_font, image_size
) -> tuple[float, float]:
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
                image_size[1] / 2.0 - text_size_font / 2.0,
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
            f"effect_coordinates_calculate|effect_coordinates[0]: {effect_coordinates[0]}, effect_coordinates[1]: {effect_coordinates[1]}"
        )
    return effect_coordinates


def effect_offset_calculate(
    effect_type, effect_position, effect_offset
) -> tuple[float, float]:
    if effect_position == "top" and effect_type == "horizontal":
        try:
            effect_offset = numpy.array(effect_offset) * numpy.array([1.0, 1.0])
        except Exception as e:
            print("effect_offset_calculate: failure!")
            print(e)
    elif effect_position == "center":
        try:
            # effect_offset = numpy.array(effect_offset) * numpy.array([1, 0])
            pass
        except Exception as e:
            print("effect_offset_calculate: failure!")
            print(e)
    elif effect_position == "bottom" and effect_type == "horizontal":
        try:
            effect_offset = numpy.array(effect_offset) * numpy.array([1.0, -1.0])
        except Exception as e:
            print("effect_offset_calculate: failure!")
            print(e)
    if DEBUG == 1:
        print(
            f"effect_offset_calculate|effect_offset[0]: {effect_offset[0]}, effect_offset_calculate||effect_offset[1]: {effect_offset[1]}"
        )
    return tuple(effect_offset)


def effect_anchor_calculate(effect_type, effect_position) -> str:
    effect_anchor = ""
    if effect_position == "top" and effect_type == "horizontal":
        effect_anchor = "mt"
    elif effect_position == "center":
        effect_anchor = "mm"
    elif effect_position == "bottom" and effect_type == "horizontal":
        effect_anchor = "mb"
    return effect_anchor


# def text_spacing_calculate(text_font_size, text_spacing) -> tuple[float, float]:
#     try:
#         text_spacing = numpy.array(text_font_size) + numpy.array(text_spacing)
#     except Exception as e:
#         print("text_spacing_calculate: failure!")
#         print(e)
#     if DEBUG == 1:
#         print(f"text_spacing_calculate|text_spacing[1]: {text_spacing[1]}")
#     return tuple(text_spacing)


def text_lines_translate(effect_type, effect_position, text_lines) -> list[str]:
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
    effect_type,
    effect_position,
    effect_offset_horizontal,
    effect_offset_vertical,
    text_width_line,
    text_spacing,
) -> object:
    config = RawConfigParser()
    try:
        if path_config == None:
            path_config = os.path.join(DIRECTORY_MODULE, "config.ini")
            if DEBUG == 1:
                print(f"path_config: {path_config}")
        config.read(path_config)
        if path_input == None:
            path_input = (
                os.path.join(DIRECTORY_MODULE, config.get("path", "PATH_INPUT"))
                if config.get("path", "PATH_INPUT") != None
                else os.path.join(DIRECTORY_MODULE, "input/")
            )
        if DEBUG == 1:
            print(f"path_input: {path_input}")
        if path_output == None:
            path_output = (
                os.path.join(DIRECTORY_MODULE, config.get("path", "PATH_OUTPUT"))
                if config.get("path", "PATH_OUTPUT") != None
                else os.path.join(DIRECTORY_MODULE, "output/")
            )
        if DEBUG == 1:
            print(f"path_output: {path_output}")
        if effect_type == None:
            effect_type = (
                config.get("effect", "EFFECT_TYPE")
                if config.get("effect", "EFFECT_TYPE") != None
                else "horizontal"
            )
        if DEBUG == 1:
            print(f"effect_type: {effect_type}")
        if effect_position == None:
            effect_position = (
                config.get("effect", "EFFECT_POSITION")
                if config.get("effect", "EFFECT_POSITION") != None
                else "center"
            )
        if DEBUG == 1:
            print(f"effect_position: {effect_position}")
        effect_offset_horizontal = (
            config.get("effect", "EFFECT_OFFSET_HORIZONTAL")
            if config.get("effect", "EFFECT_OFFSET_HORIZONTAL") != None
            else 0
        )
        if DEBUG == 1:
            print(f"effect_offset_horizontal: {effect_offset_horizontal}")
        effect_offset_vertical = (
            config.get("effect", "EFFECT_OFFSET_VERTICAL")
            if config.get("effect", "EFFECT_OFFSET_VERTICAL") != None
            else 0
        )
        if DEBUG == 1:
            print(f"effect_offset_vertical: {effect_offset_vertical}")
        text_size_font = (
            int(config.getint("text", "TEXT_SIZE_FONT"))
            if config.getint("text", "TEXT_SIZE_FONT") != None
            else 50
        )
        if DEBUG == 1:
            print(f"text_size_font: {text_size_font}")
        text_width_line = (
            int(config.get("text", "TEXT_WIDTH_LINE"))
            if config.get("text", "TEXT_WIDTH_LINE") != None
            else 20
        )
        if DEBUG == 1:
            print(f"text_width_line: {text_width_line}")
        text_spacing = (
            int(config.get("text", "TEXT_SPACING"))
            if config.get("text", "TEXT_SPACING") != None
            else 5
        )
        if DEBUG == 1:
            print(f"text_spacing: {text_spacing}")
        text_font_family = (
            config.get("text", "TEXT_FONT_FAMILY")
            if config.get("text", "TEXT_FONT_FAMILY") != None
            else "/usr/share/fonts/qualitype/QTGaromand-Bold.otf"
        )
        if DEBUG == 1:
            print(f"text_font_family: {text_font_family}")
        text_color_font = (
            config.get("text", "TEXT_COLOR_FONT")
            if config.get("text", "TEXT_COLOR_FONT") != None
            else "255, 76, 48, 128"
        )
        if DEBUG == 1:
            print(f"text_color_font: {text_color_font}")
        text_caption = (
            config.get("text", "TEXT_CAPTION")
            if config.get("text", "TEXT_CAPTION") != None
            else "LoremIpsum"
        )
        if DEBUG == 1:
            print(f"text_caption: {text_caption}")
    except Exception as e:
        print("config_read: failure!")
        print(e)
    else:
        return {
            "path_config": str(path_config),
            "path_input": str(path_input),
            "path_output": str(path_output),
            "effect_type": str(effect_type),
            "effect_position": str(effect_position),
            "effect_offset_horizontal": int(effect_offset_horizontal),
            "effect_offset_vertical": int(effect_offset_vertical),
            "text_size_font": int(text_size_font),
            "text_width_line": int(text_width_line),
            "text_spacing": int(text_spacing),
            "text_font_family": str(text_font_family),
            "text_color_font": str(text_color_font),
            "text_caption": str(text_caption),
        }


def image_read(dictionary_config) -> list[tuple]:
    format_image = [".jpg", ".png"]
    list_images = []
    try:
        path_input = abspath(dictionary_config["path_input"])
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


def image_write(dictionary_config, list_images):
    try:
        image_font = ImageFont.truetype(
            dictionary_config["text_font_family"], dictionary_config["text_size_font"]
        )
    except Exception as e:
        print(f"image_write|font_read: failure!")
        print(e)
    for tuple_image in list_images:
        image_draw = ImageDraw.Draw(tuple_image[0])
        try:
            lines_text = text_lines_translate(
                dictionary_config["effect_type"],
                dictionary_config["effect_position"],
                textwrap.wrap(
                    text=dictionary_config["text_caption"],
                    width=dictionary_config["text_width_line"],
                    placeholder=" (...)",
                ),
            )
            for index, line_text in enumerate(lines_text):
                line_text_spacing = index * (
                    dictionary_config["text_size_font"]
                    + dictionary_config["text_spacing"]
                )
                if dictionary_config["effect_position"] == "center":
                    if index % 2 == 1:
                        line_text_spacing = index / 2 * (
                            dictionary_config["text_size_font"]
                            + dictionary_config["text_spacing"]
                        ) + 0.5 * (
                            dictionary_config["text_size_font"]
                            + dictionary_config["text_spacing"]
                        )
                    else:
                        line_text_spacing = -(index / 2) * (
                            dictionary_config["text_size_font"]
                            + dictionary_config["text_spacing"]
                        )
                image_draw.text(
                    xy=tuple(
                        map(  # Maps can call functions https://docs.python.org/3/library/functions.html#map
                            operator.add,
                            numpy.array(
                                effect_coordinates_calculate(
                                    dictionary_config["effect_type"],
                                    dictionary_config["effect_position"],
                                    dictionary_config["text_size_font"],
                                    tuple_image[0].size,
                                )
                            ),
                            numpy.array(
                                effect_offset_calculate(
                                    dictionary_config["effect_type"],
                                    dictionary_config["effect_position"],
                                    (
                                        dictionary_config["effect_offset_horizontal"],
                                        dictionary_config["effect_offset_vertical"]
                                        + line_text_spacing,
                                    ),
                                )
                            ),
                        )
                    ),
                    text=line_text,
                    font=image_font,
                    anchor=effect_anchor_calculate(
                        dictionary_config["effect_type"],
                        dictionary_config["effect_position"],
                    ),
                    fill=tuple(
                        [
                            int(n)
                            for n in dictionary_config["text_color_font"].split(", ")
                        ]
                    ),
                )
        except Exception as e:
            print("image_write|text_draw: failure!")
            print(e)
        try:
            tuple_image[0].save(
                os.path.join(abspath(dictionary_config["path_output"]), tuple_image[1])
            )
        except Exception as e:
            print("image_write|image_write: failure!")
            print(e)
            print(
                os.path.join(abspath(dictionary_config["path_output"]), tuple_image[1])
                + tuple_image[1]
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_config",
        help="(Optional) Path to the config file (module's config.ini used by default!) (str).",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--path_input",
        help="(Optional) Path to the input folder. All images in ['.jpg', '.png'] format will be processed (str).",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--path_output",
        help="(Optional) Path to the output folder (str).",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--effect_type",
        help="(Optional) Type of the effect ['horizontal', 'diagonal'] (str).",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--effect_position",
        help="(Optional) Position of the effect ['bottom', 'center', 'top'] (str).",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--effect_offset_horizontal",
        help="(Optional) Horizontal offset of the effect (int).",
        type=int,
        nargs="?",
    )
    parser.add_argument(
        "--effect_offset_vertical",
        help="(Optional) Vertical offset of the effect (int).",
        type=int,
        nargs="?",
    )
    parser.add_argument(
        "--text_width_line",
        help="(Optional) Width of the text line, counted in characters per line (int).",
        type=int,
        nargs="?",
    )
    parser.add_argument(
        "--text_spacing",
        help="(Optional) Spacing of the text multi-line, counted in pixels between the lines (int).",
        type=int,
        nargs="?",
    )
    args = parser.parse_args()
    dictionary_config = config_read(
        args.path_config,
        args.path_input,
        args.path_output,
        args.effect_type,
        args.effect_position,
        args.effect_offset_horizontal,
        args.effect_offset_vertical,
        args.text_width_line,
        args.text_spacing,
    )
    list_images = image_read(dictionary_config)
    image_write(dictionary_config, list_images)
