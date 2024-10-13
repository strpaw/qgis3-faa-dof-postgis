# [Project structure](#project_structure)
# [Database setup](#database_setup)
## [Notes](#database_setup_notes)
## [Auxiliary scripts](#aux_scripts)
### [load_countries_states.py](#load_ctry_states)
## [Setup with alembic](#setup_alembic)
## [Setup with SQL scripts](#setup_sql)

# Project structure <a name=project_structure>


>- All files are not shown for the sake of clarity
>- Some alembic files are left without description (refer to the alembic documentation for more information)

```
qgis3-faa-dof-postgis                            # Main project directory
└───database_setup                               # Scripts, initial data to setup database
    │   .env_sample                              # Database credentials sample with formatting used by alembic scripts
    │   alembic.ini
    │
    ├───alembic_migrations                       # Alembic migration environment
    │   │   env.py                               
    │   │   README
    │   │   script.py.mako
    │   │
    │   └───versions
    │
    ├───initial_data                             # Inital data to populate database
    │       horizontal_acc.csv
    │       lighting.csv
    │       marking.csv
    │       oas.csv
    │       obstacle_type.csv
    │       tolerance_uom.csv
    │       verif_status.csv
    │       vertical_acc.csv
    │ 
    ├───python_scripts                           # Auxiliary scripts for database setup
    │       load_countries_states.py             # Populate spatial tables with countries, USA states data
    │       load_countries_states_config_sample.yml
    │
    └───sql                                      # SQL scripts to manage database
            ddl.sql                              # Setup database (tables) SQL script
            dml.sql                              # SQL script to insert initial data ('dict' tables)
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

## Setup with alembic <a name=setup_alembic>

1. Create file with connection details used by Alembic scripts;
   * location: `<main project dir>\database_setup>.env`
   * refer file `<main project dir>\database_setup>.env_sample` for the structure and content
2. `cd <main project dir>\database_setup`
3. Execute commands:
   * `alembic upgrade 8e1` (create db schema)
   * `alembic upgrade 211` (populate tables with initial data, non-spatial tables)
4. Load countries, USA states spatial data. See [load_countries_states.py](#load_ctry_states)

## Setup with SQL scripts <a name=setup_sql>

Execute SQL scripts, using for example pgAdmin:

* `<main project dir>\database_setup>\ddl.sql` (create tables)
* `<main project dir>\database_setup>\ddl.sql` (populate data)
