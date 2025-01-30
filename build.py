import csv
import pathlib
import subprocess


CURRENT_DIR = pathlib.Path.cwd()

DATA_DIR = CURRENT_DIR / 'data'
STATE_OUTPUT_DIR = CURRENT_DIR / 'states'

SHAPEFILE = DATA_DIR / 'tl_2024_us_zcta520.shp'
BOUNDARY_FILE = DATA_DIR / 'cb_2018_us_state_500k.shp'
STATE_ABBR_LOOKUP_FILE = DATA_DIR / 'fips_and_state_abbr.csv'
OUTPUT_MERGED_FILE = DATA_DIR / 'zcta_with_states.shp'


def join_shape_and_boundary(shapefile: pathlib.Path = SHAPEFILE,
                            data_dir: pathlib.Path = DATA_DIR,
                            boundary_file: pathlib.Path = BOUNDARY_FILE,
                            output_file: pathlib.Path = OUTPUT_MERGED_FILE) -> None:
    if not output_file.exists():
        print(f'Generating {output_file}')
        cmd = f"""
ogr2ogr -f "ESRI Shapefile" '{str(output_file)}' '{str(data_dir)}' \
-sql "SELECT z.*, s.STUSPS
    FROM '{shapefile.stem}' z
    JOIN '{boundary_file.stem}' s
    ON ST_Intersects(z.geometry, s.geometry)" \
-dialect SQLITE
"""
        subprocess.run(cmd, shell=True)


def split_by_state(data_dir: pathlib.Path = DATA_DIR, output_dir: pathlib.Path = STATE_OUTPUT_DIR):
    with open(STATE_ABBR_LOOKUP_FILE) as f:
        reader = csv.DictReader(f)
        states = [row for row in reader]

    for row in states:
        state_name = row['state_name']
        state_code = row['state_abbreviation']

        output_geojson_file = STATE_OUTPUT_DIR / f'zcta_2024_{state_code}.json'
        output_geojson_file_min = STATE_OUTPUT_DIR / f'zcta_2024_{state_code}_min.json'
        cmd = f"""ogr2ogr -f "GeoJSON" {str(output_geojson_file)} zcta_with_states.shp -where \"STUSPS = '{state_code}'\""""

        if not output_geojson_file_min.exists():
            print(f'{state_name} -- generating GeoJSON file')
            subprocess.run(cmd, shell=True)
            minify_cmd = f'minify {str(output_geojson_file)} > {output_geojson_file_min}'
            subprocess.run(minify_cmd, shell=True)

            # clean up un-minified file
            output_geojson_file.unlink()


if __name__ == '__main__':
    join_shape_and_boundary()

    split_by_state()
