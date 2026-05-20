variable "project_name" {
  description = "Project name used to prefix AWS resources."
  type        = string
  default     = "bigdata-ml-platform"
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "eu-west-1"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}

