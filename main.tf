provider "aws" {
  region  = "us-east-1"
}

module "munki-repo" {
  source          = "grahamgilbert/munki-repo/aws"
  version         = "0.1.0"
  munki_s3_bucket = "macdevops2019-demo"
  username        = "${var.username}"
  password        = "${var.password}"
  prefix          = "macdevops2019demo"
}

variable "username" {
  default = "munki"
}

variable "password" {
  default = "ilovemunki"
}

output "cloudfront_url" {
  value = "${module.munki-repo.cloudfront_url}"
}


output "munki_bucket_id" {
  value = "${module.munki-repo.munki_bucket_id}"
}

output "username" {
  value = "${var.username}"
}

output "password" {
  value = "${var.password}"
}
