# Scrapy Digimon Reference Book
Scrapy project that uses Item, ItemLoaders and Pipelines get all the digimons listed at the Digimon Reference Book and store then into a JSON file.

## How to Install
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## How to use the project
Run the following instruction at the command line
```
make json
```

After complition a file called `digimon.json` will be at the root of the project folder.

## Run Tests
```
make tests
```
