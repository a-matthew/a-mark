# ================================
# Name: 'a-mark'/tests.py
# Author: 'a-matthew'/Mateusz A.
# Year: 2022-2026
# Comments: No LLMs are used.
# Quick references:
# https://docs.python.org/3/library/stdtypes.html
# ================================

# 1st built-in, 2nd custom

import argparse
import os
import subprocess

# isort: split

DEBUG = 1

AMARK_TEST_SUITES = [
    "test_01_effect_top.ini",
    "test_02_effect_center.ini",
    "test_03_effect_bottom.ini",
]
PATH_DIRECTORY_MODULE = os.path.split(os.path.realpath(__file__))[0]


def config_read(
    path_amark,
    path_input,
    path_output,
    path_tests,
) -> object:
    """
    Read configuration from argparse and default missing parameters.
    """
    try:
        if path_amark is None:
            path_amark = os.path.join(PATH_DIRECTORY_MODULE, "main.py")
        if DEBUG == 1:
            print(f"config_read|path_amark: {path_amark}")
        if path_input is None:
            path_input = os.path.join(PATH_DIRECTORY_MODULE, "input/")
        if DEBUG == 1:
            print(f"config_read|path_input: {path_input}")
        if path_output is None:
            path_output = os.path.join(PATH_DIRECTORY_MODULE, "tests/output")
        if DEBUG == 1:
            print(f"config_read|path_output: {path_output}")
        if path_tests is None:
            path_tests = os.path.join(PATH_DIRECTORY_MODULE, "tests/")
        if DEBUG == 1:
            print(f"config_read|path_tests: {path_tests}")
    except Exception as e:
        print("config_read: failure!")
        print(e)
    else:
        return {
            "path_amark": str(path_amark),
            "path_input": str(path_input),
            "path_output": str(path_output),
            "path_tests": str(path_tests),
        }


def amark_run(path_amark, path_config, path_input, path_output, name_output) -> None:
    """
    Run 'a-mark' with CLI parameters.
    """
    try:
        # print(f"amark_run|amark_test_suite: {amark_test_suite}")
        amark_command = [
            "python",
            f"{path_amark}",
            f"--path_config={path_config}",
            f"--path_input={path_input}",
            f"--path_output={path_output}",
            f"--name_output={name_output}",
        ]
        amark_process = subprocess.run(
            amark_command,
            shell=False,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if DEBUG == 1:
            print(f"amark_run|returncode {amark_process.returncode}")
            print(f"amark_run|stdout {amark_process.stdout}")
    except Exception as e:
        print("amark_run: failure!")
        print(e)


def amark_test_suite_run(
    amark_test_suite, path_tests, path_amark, path_input, path_output, name_output
) -> None:
    """
    Check if test suite exists, then run it.
    """
    try:
        for test_suite in os.listdir(path_tests):
            if test_suite.endswith(amark_test_suite):
                if DEBUG == 1:
                    print(f"amark_test_suite_run|test_suite: {test_suite}")
                amark_run(
                    path_amark,
                    os.path.join(path_tests, test_suite),
                    path_input,
                    path_output,
                    name_output,
                )
    except Exception as e:
        print("amark_test_suite: failure!")
        print(e)


def amark_test_run(config) -> None:
    """
    Run tests for 'a-mark'.
    """
    for amark_test_suite in AMARK_TEST_SUITES:
        amark_test_suite_run(
            amark_test_suite,
            config["path_tests"],
            config["path_amark"],
            config["path_input"],
            config["path_output"],
            f"{amark_test_suite.split(".")[0]}.jpg",
        )


if __name__ == "__main__":
    """
    Initialize main module with argument parsing.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_amark",
        help="(Optional) Path of the amark module (str).",
        type=str,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--path_input",
        help="(Optional) Path of the input data directory (str).",
        type=str,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--path_output",
        help="(Optional) Path of the output results directory (str).",
        type=str,
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--path_tests",
        help="(Optional) Path of the amark tests directory (str).",
        type=str,
        nargs="?",
        default=None,
    )
    args = parser.parse_args()
    config = config_read(
        args.path_amark,
        args.path_input,
        args.path_output,
        args.path_tests,
    )
    amark_test_run(config)
