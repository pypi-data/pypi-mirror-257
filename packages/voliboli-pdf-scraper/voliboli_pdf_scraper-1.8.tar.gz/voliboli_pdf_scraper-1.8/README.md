# Voliboli PDF Scraper

Main repository for scraping data of off installed statistics that are in PDF format. Data is stored in a Postgres database with the help of Flask server and GraphQL protocol.

![image](https://user-images.githubusercontent.com/48418580/233640399-525d336e-ad3f-449a-b311-060489326123.png)

## Tests

You can run test from the root of this repository using:

    pipenv run python tests/test_main.py

## Distribute

To generate the distribution archives, run:

    python3 -m pip install --upgrade build
    python3 -m build

You can then install this package locally from any other project using:

    pip install -e /path/to/root

where `root` is the top-level directory of this project.

## New Release

To deploy a new version you can use the following commands:

    twine upload --skip-existing dist/*
