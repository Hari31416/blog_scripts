import os, subprocess


def pascal_case_to_snake_case(pascal_case_string):
    snake_case_string = ""
    for i, char in enumerate(pascal_case_string):
        if i > 0 and char.isupper():
            snake_case_string += "_"
        snake_case_string += char.lower()
    return snake_case_string


def render_manim_file(manim_file_path, class_name):
    file_dir = os.path.dirname(manim_file_path)
    file_name = os.path.basename(manim_file_path)
    os.chdir(file_dir)
    output_file = f"{pascal_case_to_snake_case(class_name)}"
    command = f"manim {file_name} -o {output_file} {class_name}"
    subprocess.run(command, shell=True)


def get_colors(dark_mode: bool = False):
    """Get the primary and background colors for the scene.

    Parameters
    ----------
    dark_mode : bool, optional
        Whether to use dark mode or not, by default False

    Returns
    -------
    Tuple
        Tuple containing the BACKGROUND_COLOR, PRIMARY_COLOR, PRIMARY_COLORS
    """
    from manim.utils.color import (
        BLACK,
        WHITE,
        GRAY_A,
        RED_A,
        BLUE_A,
        GREEN_A,
        MAROON_A,
        TEAL_A,
        DARKER_GRAY,
    )

    BACKGROUND_COLOR = WHITE
    PRIMARY_COLOR = BLACK

    PRIMARY_COLORS = [
        WHITE,
        GRAY_A,
        RED_A,
        MAROON_A,
        BLUE_A,
        GREEN_A,
        TEAL_A,
        DARKER_GRAY,
    ]
    if dark_mode:
        PRIMARY_COLORS = [c.invert() for c in PRIMARY_COLORS]
        BACKGROUND_COLOR = BACKGROUND_COLOR.invert()
        PRIMARY_COLOR = PRIMARY_COLOR.invert()

    return BACKGROUND_COLOR, PRIMARY_COLOR, PRIMARY_COLORS
