# Table of Contents
 
* [Project structure](#project_structure)
* [Database setup](#database_setup)
  * [Notes](#database_setup_notes)
  * [Auxiliary scripts](#aux_scripts)
    * [load_countries_states.py](#load_ctry_states)
    * [obstacle_types.py](#obstacle_types)
  * [Setup with alembic](#setup_alembic)
  * [Setup with SQL scripts](#setup_sql)
* [Plugin installation](#plugin_install)

# Project structure <a name=project_structure>


>- All files are not shown for the sake of clarity
>- Some alembic files are left without description (refer to the alembic documentation for more information)

```
qgis3-faa-dof-postgis                            # Main project directory
│   create_plugin_package.ps1                    # PowerShell script to create plugin zip package 
├───database_setup                               # Scripts, initial data to setup database
│   │   .env_sample                              # Database credentials sample with formatting used by alembic scripts
│   │   alembic.ini
│   │
│   ├───alembic_migrations                       # Alembic migration environment
│   │   │   env.py                               
│   │   │   README
│   │   │   script.py.mako
│   │   │
│   │   └───versions
│   │
│   ├───initial_data                             # Inital data to populate database
│   │       horizontal_acc.csv
│   │       lighting.csv
│   │       marking.csv
│   │       oas.csv
│   │       obstacle_type.csv
│   │       tolerance_uom.csv
│   │       verif_status.csv
│   │       vertical_acc.csv
│   │ 
│   ├───python_scripts                           # Auxiliary scripts for database setup
│   │       load_countries_states.py             # Populate spatial tables with countries, USA states data
│   │       load_countries_states_config_sample.yml
│   │
│   └───sql                                      # SQL scripts to manage database
│           ddl.sql                              # Setup database (tables) SQL script
│           ddl_views.sql                        # Setup database (views) SQL script
│           dml.sql                              # SQL script to insert initial data ('dict' tables)
└───qgis3_plugin
    └───faa_dof_manager                          #  Plugin directory
```
# Database setup <a name=database_setup>

## Notes <a name=database_setup_notes>

Before executing SQL/Alembic scripts to setup database:
* create database
* create PostGIS extension
* create admin user for database
* create `dof` schema
* repository does not contain spatial data for populating tables: `dof.country`, `dof.us_state`
* script `<main project dir>\database_setup>\ddl.sql` (populate data) contains only examples of selected USA states geometries
* populating spatial data
  * load spatial data directly from data files (created by your own) using QGIS, ogr2ogr, shp2pgsql etc.
  * adjust script `<main project dir>\database_setup>\ddl.sql` with geometry for spatial tables

## Auxiliary scripts <a name=aux_scripts>

Scripts to load data, extract obstacle types from DOF file ect.

### load_countries_states.py <a name=load_ctry_states>

#### Purpose

Script to load spatial data (countries, USA states) to the database.

#### Input

* spatial data with countries, USA states boundaries
* format supported by GeoPandas (example gpkg)

#### Output

FAA DOF database.

#### Usage

1. `cd <main project dir>\database_setup\scripts`
2. Create and edit configuration file `load_countries_states_config.yml`, see `load_countries_states_config.yml` for more information:
3. Run `python load_countries_states.py`, use `python load_countries_states.py - h` for more information


### obstacle_types.py <a name=obstacle_types>

#### Purpose

Script to get obstacle types from DOF.dat file.

#### Input

* obstacle data file, the whole file for all states/countries (DOF.dat)

### Output

* CSV file with unique obstacle types get from input file

#### Usage

> Notes
> * script uses `obstacle_types_config.yml` configuration file which must be in the directory when script is executed
> * script uses `DOF.dat` data file which must be in the directory when script is executed

1. `cd <main project dir>\database_setup\scripts`
2. Edit configuration file `obstacle_types_config.yml`
3. Run `python obstacle_types.py`

## Setup with alembic <a name=setup_alembic>

1. Create file with connection details used by Alembic scripts;
   * location: `<main project dir>\database_setup>.env`
   * refer file `<main project dir>\database_setup>.env_sample` for the structure and content
2. `cd <main project dir>\database_setup`
3. Execute commands:
   * `alembic upgrade 8e1` (create db schema)
   * `alembic upgrade 211` (populate tables with initial data, non-spatial tables)
   * `alembic upgrade f88` (create views)
4. Load countries, USA states spatial data. See [load_countries_states.py](#load_ctry_states)

## Setup with SQL scripts <a name=setup_sql>

Execute SQL scripts, using for example pgAdmin:

* `<main project dir>\database_setup>\ddl.sql` (create tables)
* `<main project dir>\database_setup>\ddl.sql` (populate data)
* `<main project dir>\database_setup>\ddl_views.sql` (create views)

# Plugin installation <a name=plugin_install>

1. Open `PowerShell`
2. `cd <main project directory>`
3. Run script: `.\create_plugin_package.ps1`
4. Open Plugin dialog windows in QGIS: `Main menu > Plugins > Manage and Install Plugins...`:
 ![Opeing plugins dialog](/doc_img/plugin_installation/1_plugins_menu.png)
5. Chose `Install from ZIP`:
![Install from ZIP option](/doc_img/plugin_installation/2_install_from_ZIP.png)

6. Select ZIP file created in the step 3 and press `Install Plugin` button:
![Select ZIP and install](/doc_img/plugin_installation/3_select_install.png)
