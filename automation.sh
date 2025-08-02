#!/bin/bash 
                                           # updating system and upgrading
    sudo apt update -y && sudo apt upgrade -y 
    sudo apt-get update 

                                       # installing docker compose (gpg-key, plugin, certificate)
    sudo apt-get install -y ca-certificates curl gnupg lsb-release
    sudo install -m 0755 -d /etc/apt/keyrings -y 
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -y | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

                                           # verifying status of docker 
    sudo systemctl status docker 

                                                 # starting docker
    sudo systemctl start docker 
    sudo systemctl enable docker --now 
                                              # verifying docker status 
    if sudo systemctl is-active --quiet docker; then
        echo "docker started" 
    else 
        echo "docker not running" 
    fi
                                        # installing helm &&b bitnami repo 
    curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
                                        # adding bitnami repo 
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update 
    helm version 
                                      #  adding plugin
    helm plugin install https://github.com/helm/chart-docs
                                           # helm-s3
    helm plugin install https://github.com/hypnoglow/helm-s3.git --version v0.13.0
                                         # helm-gcs
    helm plugin install https://github.com/hayorov/helm-gcs.git
     helm plugin list 

     