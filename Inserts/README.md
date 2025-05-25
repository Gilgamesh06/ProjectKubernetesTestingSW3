## Instalar PSQL

* Se necesita instalar PSQL para poder ejecutar los scripts de pruebas


    ## Para instalar ejecuta el siguiente comando:

    ```bash
    sudo apt install postgresql-client
    ```

    ## Comprobar la versión de PSQL:

    ```bash
    psql --version
    ```

    ## Ubicarse en la ruta del script y ejecutar:

     ```bash
     psql -h localhost -p 5433 -U Solus -d ecommerce_inventario -f ./schema_inventario.sql
     ```

    ## Ingresar con la contraseña: 123456

    ## Verificar que las tablas se crearon:

    ```bash
    psql -h localhost -p 5433 -U Solus -d ecommerce_inventario
    ```

    ## Dentro de PSQL:
    
    ```bash
    \dt
    ```

    ```bash
    \d producto
    ```
