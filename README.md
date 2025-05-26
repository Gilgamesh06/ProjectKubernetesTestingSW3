# Proyecto Final Software 3

* En este proyecto se busca realizar pruebas de rendimiento a un Backend que tiene la siguiente estructura:

    * **Microservicio-inventario** (SpringBoot)
    * **Microservicio-carrito** (SpringBoot)
    * **Microservicio-venta** (SpringBoot)
    * **Microservicio-pedido** (SpringBoot)
    * **Kong** (API Gateway)
    * **RabbitMQ** (Gestor de mensajeria)

* Para estas pruebas Se definira tres tipos de configuraciones

    1. [Despliege con Docker Compose](##despliege-con-docker-compose)
    2. [Despliege con Kubernetes Un Nodo](##despliege-con-kubernetes-un-nodo)
    3. [Despliege con Kubernetes Dos Nodos](##despliege-con-kubernetes-dos-nodos)


    ## Despliege con Docker Compose

    * Para desplegar con docker compose solo debemos ejecutar los comandos:

        ```bash
        cd Docker 
        sudo docker compose up --build
        ```

    ## Despliege con Kubernetes Un Nodo

    * Ejecutar los siguientes comandos 

    ```bash
    sudo chmod +x script-nodo-2.sh
    ./script-nodo-2.sh
    chmod +x Kubernetes/script.sh
    ./Kubernetes/script.sh
    ```

    ## Depliege con kubernetes Dos Nodos

    * Ejecutar los siguientes comandos en el Nodo 2: 

        ```bash
            sudo chmod +x script-nodo-2.sh
            ./script-nodo-2.sh
        ```

    * Ejecutar los siguientes comandos en el Nodo 1: 

        ```bash
        sudo chmod +x script-nodo-1.sh
        # en el nodo 1 (**Nodo padre**) 
        ./script-nodo-1.sh
        # Debera retonar un linea como esta
        ```
        ```bash
        Join node with: microk8s join 192.168.1.10:25000/abcdef1234567890abcdef1234567890
        ```
        * Ejecutar esa linea de codigo en el Nodo 2
    
    * Ejecutar los siguietnes comandos en el Nodo 1:

        ```bash
            sudo chmod +x script-nodo-2.sh
            ./script-nodo-2.sh
        ```
