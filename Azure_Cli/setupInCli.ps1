#this file automates Azure setup

#login to azure account
az login

#Create a resource group
az group create --name Assignment --location IsraelCentral

#Register the Microsoft.Compute provider
az provider register --namespace Microsoft.Compute

#register the microsoft.insights
az provider register --namespace Microsoft.Insights

#Register the Microsoft.ContainerService Namespace
az provider register --namespace Microsoft.ContainerService

# check the status of the registration
az provider show --namespace Microsoft.Compute --query "registrationState" --output table
az provider show --namespace Microsoft.Insights --query "registrationState" --output table
az provider show --namespace Microsoft.ContainerService --query "registrationState" --output table

#create AKS cluster
az aks create --resource-group Assignment --name NatashaCluster --node-count 1 --enable-addons monitoring --generate-ssh-keys

#install kebernetes cli
az aks install-cli

#Get AKS Cluster Credentials
az aks get-credentials --resource-group Assignment --name NatashaCluster

#Check Cluster Nodes
kubectl get nodes

#checking that every thing works good:
az aks show --resource-group Assignment --name NatashaCluster --query "provisioningState"
kubectl get nodes