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
    └───sql                                      # SQL scripts to manage database
            ddl.sql                              # Setup database (tables) SQL script
            dml.sql                              # SQL script to insert initial data ('dict' tables)
```
