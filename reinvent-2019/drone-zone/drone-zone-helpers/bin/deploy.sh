# declare variables
BUCKET_NAME_PREFIX=<BUCKET-NAME-PREFIX>
DRONE_NAME=<DRONE-NAME>
REGION=<REGION>
DETECTION_MODEL_PATH=<MODEL-PATH>

# build, package, and deploy stack
aws s3 mb --region $REGION s3://$BUCKET_NAME_PREFIX-$REGION
sam build
sam package --output-template packaged.yaml --s3-bucket $BUCKET_NAME_PREFIX-$REGION  
sam deploy --region $REGION --template-file packaged.yaml --stack-name $DRONE_NAME --capabilities CAPABILITY_IAM \
    --parameter-overrides \
    CoreName=$DRONE_NAME \
    ThingsDetectionModelS3Path=$DETECTION_MODEL_PATH