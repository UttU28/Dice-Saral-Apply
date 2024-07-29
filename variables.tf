# Variables definition

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "thisresourcegroup"
}

variable "app_service_plan_name" {
  description = "Name of the App Service Plan"
  type        = string
  default     = "thatappserviceplan"
}

variable "app_service_name" {
  description = "Name of the Web App"
  type        = string
  default     = "dicesaralapply"
}

variable "registry_name" {
  description = "Name of the Azure Container Registry"
  type        = string
  default     = "thisacr"
}

variable "image_name" {
  description = "Name of the Image"
  type        = string
  default     = "imagename"
}

variable "location" {
  description = "Location for the resources"
  type        = string
  default     = "East US"
}

variable "app_service_plan_sku" {
  description = "SKU for the App Service Plan"
  type        = string
  default     = "F1"
}

variable "app_service_plan_tier" {
  description = "SKU for the App Service Plan"
  type        = string
  default     = "Free"
}
