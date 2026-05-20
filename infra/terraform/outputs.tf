output "data_lake_bucket" {
  description = "S3 bucket used as the data lake."
  value       = aws_s3_bucket.data_lake.bucket
}

output "ecr_repository_url" {
  description = "ECR repository URL for application images."
  value       = aws_ecr_repository.app.repository_url
}

output "pipeline_role_arn" {
  description = "IAM role ARN for pipeline workloads."
  value       = aws_iam_role.pipeline.arn
}

