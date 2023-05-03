# G2ModelExtractor
Extracts models and model motion data from Grandia 2 files

## How to use
Make sure you have [python 3.10](https://www.python.org/downloads/release/python-3100/) or newer installed for this to work. Make sure to tick the `Add to PATH` box at the start.
Once python is installed, you can call the script through `Command Prompt` or `Powershell` or any other terminal you choose.
Calling will look like this: `python main.py [list of files to parse]` where `[list of files to parse]` is a list of the filepaths to files to open. Files to open could look like `content/data/afs/c01/c01_ryum.dat`, giving a space between each file to parse. An example would look like:
```
python main.py content/data/afs/c01/c01_ryum.dat content/data/afs/c02_elna.dat
```

All models and motions parsed will be added to the `./models/` directory.