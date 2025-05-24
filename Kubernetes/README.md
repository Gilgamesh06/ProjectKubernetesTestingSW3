# Kubernetes

* Para este proyecto se trabajara en un cluster con dos Nodos:

    * Para ello se debe ralizar la siguiente configuracion en las VMs 

    * Pueden descargar las imangenes de las maquinas virtuales aqui:

        [Imagenes]()

    ## Configuracion

    * **Paso 1:** Habilitar modulos y configurar permisos en ambas VMs

        ```bash
        sudo microk8s status --wait-ready
        sudo usermod -a -G microk8s $USER
        sudo chown -f -R $USER ~/.kube
        ```    
        > **Nota** Ejecutar comandos en ambas VMs luego cerrar sesion y volver a entrar o ejecutar `newgrp microk8s`

    * **Paso 2:** En la VM que sera el **nodo maestro** (`nodo1`)

        1. Obtener el comando para unir los nodos

            ```bash
                microk8s add-node
            ```
            * Genera una salida como esta:

            ```bash
            Join node with: microk8s join 192.168.1.10:25000/abcdef1234567890abcdef1234567890
            ```
            * Ese comado se debe copiar en el nodo segundario para unirlo al cluster

        > **Nota:** Las dos maquinas deben tener conexion y debe tener los puertos abiertos el nodo maestro

    * **Paso 3:** Verificar el estado del cluster

        * En el **nodo maestro**se debe ejecutar este comando 

            ```bash
                microk8s kubectl get nodes
            ```
            * Debe salir los dos nodos con el estado de `Ready`

    * **Paso 4: (`Opcional`)** Abrir puertos si usa firewall

        * Si estas usando `ufw`, se debe permitir los siguientes puertos

        ```bash
        sudo ufw allow 16443/tcp   # API server
        sudo ufw allow 25000/tcp   # para el comando join
        sudo ufw allow 10250/tcp   # para kubelet
        sudo ufw allow 8472/udp    # para flannel (CNI)
        ```
    

        
        
