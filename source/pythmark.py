# Name: 'Pythmark'
# Author: Matthew A.

# Builtin
import os, argparse, configparser, textwrap, operator # https://docs.python.org/3/library/stdtypes.html#
from os.path import abspath
from configparser import ConfigParser

# Custom
from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)  # https://pillow.readthedocs.io/en/stable/index.html

DEBUG = 1
DIRECTORY_MODULE = os.path.split(os.path.realpath(__file__))[0]
# If a component is an absolute path, all previous components are thrown away and joining continues from the absolute path component.
# Just don't use references with slashes in paths.


def effect_coordinates_calculate(
    effect_type, effect_position, image_size
) -> tuple[float, float]:
    effect_coordinates = (0.0, 0.0)  # Apparently "None" can't be used here
    if effect_position == "top" and effect_type == "horizontal":
        effect_coordinates = (
            image_size[0] / 2,
            0.0,
        )
    elif effect_position == "center":
        effect_coordinates = (image_size[0] / 2, image_size[1] / 2)
    elif effect_position == "bottom" and effect_type == "horizontal":
        effect_coordinates = (
            image_size[0] / 2,
            image_size[1],
        )
    if DEBUG == 1:
        print(f"Width {image_size[0]}, Height: {image_size[1]}")
    return effect_coordinates


def effect_anchor_calculate(effect_type, effect_position) -> str:
    effect_anchor = ""
    if effect_position == "top" and effect_type == "horizontal":
        effect_anchor = "mt"
    elif effect_position == "center":
        effect_anchor = "mm"
    elif effect_position == "bottom" and effect_type == "horizontal":
        effect_anchor = "mb"
    return effect_anchor


def config_read(
    path_config, path_input, path_output, effect_type, effect_position, text_width_line
) -> object:
    config = ConfigParser()
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
        text_font_family = (
            config.get("text", "TEXT_FONT_FAMILY")
            if config.get("text", "TEXT_FONT_FAMILY") != None
            else "/usr/share/fonts/qualitype/QTGaromand-Bold.otf"
        )
        if DEBUG == 1:
            print(f"text_font_family: {text_font_family}")
        text_size_font = (
            int(config.getint("text", "TEXT_SIZE_FONT"))
            if config.getint("text", "TEXT_SIZE_FONT") != None
            else 50
        )
        if DEBUG == 1:
            print(f"text_size_font: {text_font_family}")
        text_color_font = (
            config.get("text", "TEXT_COLOR_FONT")
            if config.get("text", "TEXT_COLOR_FONT") != None
            else "255, 76, 48, 128"
        )
        if DEBUG == 1:
            print(f"text_color_font: {text_color_font}")
        text_width_line = (
            int(config.get("text", "TEXT_WIDTH_LINE"))
            if config.get("text", "TEXT_WIDTH_LINE") != None
            else 20
        )
        if DEBUG == 1:
            print(f"text_width_line: {text_width_line}")
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
            "path_config": path_config,
            "path_input": path_input,
            "path_output": path_output,
            "effect_type": effect_type,
            "effect_position": effect_position,
            "text_font_family": text_font_family,
            "text_size_font": text_size_font,
            "text_color_font": text_color_font,
            "text_width_line": text_width_line,
            "text_caption": text_caption,
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
            lines_text = textwrap.wrap(
                text=dictionary_config["text_caption"],
                width=dictionary_config["text_width_line"],
                placeholder=" (...)",
            )
            if DEBUG == 1:
                print(lines_text)
            offset_line_text = (0, 0)
            for line_text in lines_text:
                image_draw.text(
                    xy=tuple(
                        map(
                            operator.add,
                            effect_coordinates_calculate(
                                dictionary_config["effect_type"],
                                dictionary_config["effect_position"],
                                tuple_image[0].size,
                            ),
                            offset_line_text,
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
                offset_line_text = tuple(
                    map(
                        operator.add,
                        offset_line_text,
                        (0, dictionary_config["text_size_font"]),
                    )
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
        help="Path to the config file.",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--path_input",
        help="Path to the input folder. All images in ['.jpg', '.png'] format will be processed.",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--path_output",
        help="Path to the output folder.",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--effect_type",
        help="Type of the effect ['horizontal', 'diagonal'].",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--effect_position",
        help="Position of the effect ['bottom', 'center', 'top'].",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--text_width_line",
        help="Width of the text line, counted in characters per line.",
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
        args.text_width_line,
    )
    list_images = image_read(dictionary_config)
    image_write(dictionary_config, list_images)

# PS: No GPTs/LLMs were harmed in production of this code

