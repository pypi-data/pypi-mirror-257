# PickleHandler

PickleHandler is a Python package that provides a convenient way to save and load data using the pickle module. It also includes logging functionality to track data loading and saving operations.

## Installation

To install PickleHandler, you can use pip:

```bash
pip install PickleHandler
```

## Usage
Here's a simple example demonstrating how to use PickleHandler:

<a href="https://colab.research.google.com/drive/1l_2Xo7o26cUt6nU698z8KUCmirFD7S4P" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

```bash
from PickleHandler import PickleHandler

# Initialize PickleHandler
handler = PickleHandler(folder_path="data", file_name="example.pkl")

# Save data
data = {"key": "value"}
handler.save(data, comment="Data saved 1")

# Load data
loaded_data = handler.load()
print(loaded_data)
```

## Contributing
Contributions are welcome! If you find a bug or have an idea for an improvement, please open an issue or submit a pull request on [GitHub](https://github.com/Prbn/PickleHandler).

Github: https://github.com/Prbn/PickleHandler

## License
This project is licensed under [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/) - see the [LICENSE file for details](https://github.com/Prbn/PickleHandler/blob/main/License).
