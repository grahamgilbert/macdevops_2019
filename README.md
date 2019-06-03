# Building a Munki repo in 3 minutes with Terraform

This repo contains:

* A simple Munki repo (with one whole item in)
* A script to run Terraform, sync the Munki repo to S3 and write out a mobileconfig to allow a client to access the repo

You probably don't want to use this verbatim in production, but if you do, change the username and password in `main.tf`. (You also need to install and configure the aws cli, also out of scope for this repo)
