# [Project structure](#project_structure)

# Project structure <a name=project_structure>

Note:
- All files are not shown for the sake of clarity
- Some alembic files are left without description (refer to alembic doc for more informatin)

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
