# Config execute

You can execute the necessary commands by specifying them in the configuration file section:

```yaml
# ...

backup:
  - ~/my_db1.sql
  - ~/my_db2.sql
  - ~/my_db3.sql

# ...

execute:
  - mysqldump -u root -p00000 my_db1 > ~/my_db1.sql
  - mysqldump -u root -p00000 my_db2 > ~/my_db2.sql
  - mysqldump -u root -p00000 my_db3 > ~/my_db3.sql

# ...
```
