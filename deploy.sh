#!/bin/bash
set -e

mkdir -p build

echo "Zipping Lambda functions..."
cd lambdas/submit_handler
zip -r ../../build/submit_handler.zip .
cd ../../lambdas/worker_handler
zip -r ../../build/worker_handler.zip .
cd ../../
echo "Uploading to S3..."
aws s3 cp build/submit_handler.zip s3://genesis-test-bucket-11158/
aws s3 cp build/worker_handler.zip s3://genesis-test-bucket-11158/

echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file infra/stack.json \
  --stack-name async-api \
  --capabilities CAPABILITY_NAMED_IAM
