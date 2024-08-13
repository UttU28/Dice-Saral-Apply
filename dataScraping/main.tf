terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
  backend "azurerm" {
    resource_group_name  = "thisstoragerg"
    storage_account_name = "dicestorage02"
    container_name       = "13form"
    key                  = "datascrapingState"
  }
}


data "azurerm_log_analytics_workspace" "analytics_workspace" {
  name                = local.dicesaralapply-log-analytics-workspace
  resource_group_name = local.dicesaralapply-rg
}

resource "azurerm_container_app_environment" "app_environment" {
  name                = local.dicesaralapply-app-environment
  location            = local.general-location
  resource_group_name = local.dicesaralapply-rg
}

resource "azurerm_container_app_job" "job" {

  name                         = local.jobscraping-name
  location                     = local.general-location
  container_app_environment_id = azurerm_container_app_environment.app_environment.id
  resource_group_name          = local.dicesaralapply-rg
  replica_timeout_in_seconds   = 300
  # Job scheduling: every 20 minutes, from 7 AM to 5 PM CT
  schedule_trigger_config {
    cron_expression = "*/20 12-23 * * *" # Converts to CT with UTC offset (-5 in Standard Time)
  }

  template {
    container {
      name   = "${local.acrName}-random-string"
      image  = local.acrUrl
      cpu    = 0.75
      memory = "1.5Gi"

      env {
        name  = "databaseServer"
        value = local.databaseServer
      }
      env {
        name  = "databaseName"
        value = local.databaseName
      }
      env {
        name  = "databaseUsername"
        value = local.databaseUsername
      }
      env {
        name  = "databasePassword"
        value = local.databasePassword
      }
      env {
        name  = "blobConnectionString"
        value = local.blobConnectionString
      }
      env {
        name  = "databaseContainer"
        value = local.databaseContainer
      }
      env {
        name  = "jobDataFile"
        value = local.jobDataFile
      }
      env {
        name  = "rawDataFile"
        value = local.rawDataFile
      }
    }
  }

  secret {
    name  = "registry-credentials"
    value = local.acrPassword
  }
  registry {
    server               = "${local.acrName}.azurecr.io"
    username             = local.acrName
    password_secret_name = "registry-credentials"
  }
}