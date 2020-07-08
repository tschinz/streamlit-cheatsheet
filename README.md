# Cheat Sheet for Streamlit

![assets/logo.svg](assets/logo.svg)

## Description
It is launched on [Heroku](https://dashboard.heroku.com) as the [streamlit-cheatsheet app](https://streamlit-cheatsheet.herokuapp.com/).

Displays a steamlit dash app which shows examples on how to use the streamlit library.

## Project Structure
```
  +-- assets/                     # project images
  +-- data/                       # data files
  +-- config.py                   # dashboard project config
  +-- functions.py                # dashboard project specific functions
  +-- app.py                      # streamlit main webapp
  +-- .gitignore
  +-- LICENSE                     # The project license
  +-- README.md                   # This file
```

## Usage
### Install virtual environment
#### Install pipenv
```bash
pip install pipenv
```
#### Install requirements
```bash
pipenv install
```

#### Launch locally
```python
pipenv shell
streamlit run app.py
```

## Credits
* **tschinz** - [Github Profile](https://github.com/tschinz) 

## License

:copyright: [All rights reserved](LICENSE)

---

## Find us on
> [zawiki](https://zawiki.zapto.org) &nbsp;&middot;&nbsp;
> Github [tschinz](https://github.com/tschinz) &nbsp;&middot;&nbsp;
> Twitter [@tschinz](https://twitter.com/tschinz) &nbsp;&middot;&nbsp;
