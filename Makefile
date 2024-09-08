# Variables
LAMBDA_NAME = test-lambda
PACKAGE_FILE = test-lambda.zip
LAMBDA_FOLDER = lambda_code

.PHONY: apply destroy

apply:
	terraform -chdir=terraform apply --auto-approve

destroy:
	terraform -chdir=terraform destroy --auto-approve

# Package the Lambda function
package:
	cd $(LAMBDA_FOLDER) && zip -r -D ../$(PACKAGE_FILE) *

dependencies:
	cd venv/lib/python3.12/site-packages && zip -r ../../../../$(PACKAGE_FILE) .

# Upload the package to S3
upload: package
	aws lambda update-function-code \
    --function-name  $(LAMBDA_NAME) \
    --zip-file fileb://test-lambda.zip
# Clean up the package file
clean:
	cd $(LAMBDA_FOLDER) && rm -f $(PACKAGE_FILE)

# Default rule
all: package upload clean