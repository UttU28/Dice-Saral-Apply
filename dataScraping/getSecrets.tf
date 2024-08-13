provider "azurerm" {
  features {}
}

data "azurerm_key_vault" "thiskeyvault" {
  name                = "thisdicekeyvault"
  resource_group_name = "thisresourcegroup"
}

data "azurerm_key_vault_secret" "general-location" {
  name         = "general-location"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "jobscraping-rg" {
  name         = "jobscraping-rg"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "jobscraping-name" {
  name         = "jobscraping-name"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "jobscraping-app-environment" {
  name         = "jobscraping-app-environment"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "jobscraping-log-analytics-workspace" {
  name         = "jobscraping-log-analytics-workspace"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "acrName" {
  name         = "acrName"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "acrPassword" {
  name         = "acrPassword"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

# Define local variables to store the secret values
locals {
  general-location                    = data.azurerm_key_vault_secret.general-location.value
  jobscraping-rg                      = data.azurerm_key_vault_secret.jobscraping-rg.value
  jobscraping-name                    = data.azurerm_key_vault_secret.jobscraping-name.value
  jobscraping-app-environment         = data.azurerm_key_vault_secret.jobscraping-app-environment.value
  jobscraping-log-analytics-workspace = data.azurerm_key_vault_secret.jobscraping-log-analytics-workspace.value
  acrName                             = data.azurerm_key_vault_secret.acrName.value
  acrPassword                         = data.azurerm_key_vault_secret.acrPassword.value
  acrUrl                              = "${local.acrName}.azurecr.io/${local.jobscraping-image}:latest"
}

