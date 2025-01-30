# Split US boundaries by state

You can use the files in the states folder as is or rebuild yourself.

The build script will:

1. Join the ZCTA shape files with the boundary files so the zip codes are labeled by state
2. Split that file by state abbrevation as geojson files
3. Minify the json files
4. (optionally) Clean up the non-minified files

It uses subprocess with shell=True. Use at your own risk.

Inspired by https://github.com/OpenDataDE/State-zip-code-GeoJSON

## setup

1. Install [gdal](https://formulae.brew.sh/formula/gdal) which gives you `ogr2ogr2`
2. Install [minify](https://github.com/tdewolff/homebrew-tap/) for json minifying
3. Download the most recent US Census Bureau Shapefiles
    - Downloads: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
    - Web Interface
    - Select a recent year
    - Select "Zip Code Tabulation Areas" as the layer type
    - Note: past 2010 this will only give you a single US files instead of separate ones hence the need for the next file
4. Download US state and equivalents boundary files
    - Downloads: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
    - Web Interface
    - Select a recent year
    - Select "States (and equivalent)" as the layer type
5. Modify the environment variables at the top of build if your file names are different

## build

Unzip what you downloaded into the data folder

## helpful links

- https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
- https://www.census.gov/programs-surveys/geography/guidance/geo-areas/zctas.html
