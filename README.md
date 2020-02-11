# EpithyStackManager

Serverless stack manager for Cloudformation. Creates CI/CD for pure SAM applications within AWS.
Bypasses code pipeline & code deploy. In development.

## Prerequisites

### SAM CLI

This package assumes you have the SAM CLI (Nov 25, 2019 update or later) installed on your developer instance. See: https://github.com/awsdocs/aws-sam-developer-guide/blob/master/doc_source/serverless-sam-cli-install-linux.md

## Usage

``` bash
# Resolve dependencies and create a .aws-sam/build/ directory.
$ sam build
```

This will run a dev server. CoreUI must have this built in somewhere as a dependency.
Make sure you have SSH'd to your EC2 instance with -L 3000:localhost:3000 to forward the port.

``` bash
# Deploy the application. Use the guided method so you can fill in information about your S3 bucket and region.
$ sam deploy --guided
```
