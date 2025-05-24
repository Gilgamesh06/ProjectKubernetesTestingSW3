#!/bin/bash

# Ingresar a la carpeta de Kubernetes
cd ~/ProjectKubernetesTestingSW3/Kubernetes 

# Crea el namespace: ecommerce

NAMESPACE="ecommerce"
sudo microk8s kubectl create namespace $NAMESPACE


# Crea los recursos compartidos

## RabbitMQ
sudo microk8s kubectl apply -f Rabbitmq/rabbitmq-deployment.yaml -n $NAMESPACE
sudo microk8s kubectl apply -f Rabbitmq/rabbitmq-service.yaml -n $NAMESPACE

# Database

## Inventario
sudo microk8s kubectl apply -f Microservicio-inventario/db-inventario.yaml -n $NAMESPACE
sudo microk8s kubectl apply -f Microservicio-inventario/pvc-db-inventario.yaml -n $NAMESPACE
## Venta
sudo microk8s kubectl apply -f Microservicio-venta/db-venta.yaml -n $NAMESPACE
sudo microk8s kubectl apply -f Microservicio-venta/pvc-db-venta.yaml -n $NAMESPACE
## Pedido
sudo microk8s kubectl apply -f Microservicio-pedido/db-pedido.yaml -n $NAMESPACE
sudo microk8s kubectl apply -f Microservicio-pedido/pvc-db-pedido.yaml -n $NAMESPACE
## Carrito 
sudo microk8s kubectl apply -f Microservicio-carrito/redis-carrito.yaml -n $NAMESPACE

# Crea los Microservicios: (Utiliza las imagenes que esta en dockerHub)

## Inventario
sudo microk8s kubectl apply -f Microservicio-inventario/inventario-deployment.yaml -n $NAMESPACE
sudo microk8s kubectl apply -f Microservicio-inventario/inventario-service.yaml -n $NAMESPACE
## Venta
sudo microk8s kubectl apply -f Microservicio-venta/venta-deployment.yaml -n $NAMESPACE
sudo microk8s kubectl apply -f Microservicio-venta/venta-service.yaml -n $NAMESPACE
## Pedido
sudo microk8s kubectl apply -f Microservicio-pedido/pedido-deployment.yaml -n $NAMESPACE
sudo microk8s kubectl apply -f Microservicio-pedido/pedido-service.yaml -n $NAMESPACE
## Carrito
sudo microk8s kubectl apply -f Microservicio-carrito/carrito-deployment.yaml -n $NAMESPACE
sudo microk8s kubectl apply -f Microservicio-carrito/carrito.service.yaml -n $NAMESPACE

# Crear el ConfigMap para Kong.yml
cd Kong
sudo microk8s kubectl create configmap kong-config --from-file=kong.yml -n $NAMESPACE

# Crear el Kong
kubectl apply -f kong-deployment.yaml -n $NAMESPACE
kubectl apply -f kong-service.yaml -n $NAMESPACE

cd ..
