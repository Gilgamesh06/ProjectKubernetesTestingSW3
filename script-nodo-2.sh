
# Habilita modulos y configura permisos 
sudo microk8s status --wait-ready
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube

# Habilita los puertos
sudo ufw allow 16443/tcp   # API server
sudo ufw allow 25000/tcp   # para el comando join
sudo ufw allow 10250/tcp   # para kubelet
sudo ufw allow 8472/udp    # para flannel (CNI)

newgrp microk8s

