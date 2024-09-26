# [Project structure](#project_structure)

# Project structure <a name=project_structure>

Note:
- All files are not shown for the sake of clarity

```
qgis3-faa-dof-postgis                            # Main project directory
└───database_setup                               # Scripts, initial data to setup database
    └───sql                                      # SQL scripts to manage database
            ddl.sql                              # Setup database (tables) SQL script
            dml.sql                              # SQL script to insert initial data ('dict' tables)
```
