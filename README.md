## Metadata
- Name: 'a-mark'.
- Author: a-matthew/Mateusz A.
- Purpose: Adding watermarks to images (incl. batch mode by default).
- Format: CLI (planned UI/Flatpak).
- License: 
  - [Project](LICENSE.txt)

## Setup
### Dependencies:
  - Version: __Python 3.14__
  - Manager: __venv__
    - https://docs.python.org/3/library/venv.html
  - Formatter: __Black__
    - https://pypi.org/project/black/
### Installation:
  1. `python3.14 -m venv {path}/a-mark/venv-3.14`
  2. `cd {path}/a-mark`
  3. `source venv-3.14/bin/activate`
  4. `pip install --upgrade pip`
  5. `pip install -r requirements.txt`
  6. double check with `which python` (Linux)
### Usage:
  - `a-mark/main.py`
    - configured using 'config.ini' file, or used via CLI arguments
  - `a-mark/tests.py`

## Example
### Watermark on top of the image
<img src="./a-mark/tests/output/test_01_effect_top.jpg" width=50% height=50%>

### Watermark in the center of the image ('interwoven' pattern)
<img src="./a-mark/tests/output/test_02_effect_center.jpg" width=50% height=50%>

### Watermark at the bottom of the image
<img src="./a-mark/tests/output/test_03_effect_bottom.jpg" width=50% height=50%>
