# Find the ideal ski area near you

The goal of this project is to help skiers find the best ski areas near them. You can view all the ski areas on a map of the US and Canada while filtering for specific mountain characteristics like vertical descent and average annual snowfall.

## How this codebase works

1. The scripts in the `etl` folder are used to extract, transform and load the data. The data is scraped from SkiCentral.com, processed into the proper formats and stored in a local SQLite database.

![Data Pipeline](./imgs/pipeline.jpg)

2. The data is visualized via a Streamlit dashboard. [It is hosted here](https://ski-areas-3kab8metmvnlqxkxj2geyu.streamlit.app/).

![Dashboard Preview](./imgs/dashboard.png)
