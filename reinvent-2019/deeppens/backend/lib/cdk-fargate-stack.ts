import ec2 = require("@aws-cdk/aws-ec2");
import ecs = require("@aws-cdk/aws-ecs");
import ecr = require('@aws-cdk/aws-ecr');
import ecs_patterns = require("@aws-cdk/aws-ecs-patterns");
import cdk = require("@aws-cdk/core");
import sm = require("@aws-cdk/aws-secretsmanager");
import iam = require('@aws-cdk/aws-iam');


// CONFIGURATION VARIABLES
// Will need to be configured per deploy


const APIID_SECRET_ARN = 'arn:aws:secretsmanager:eu-west-1:202848742610:secret:DrawingBackend-API_ID-fMlzfc';
const IOT_ENDPOINT_SECRET_ARN='arn:aws:secretsmanager:eu-west-1:202848742610:secret:DrawingBackend-IOT_ENDPOINT-tZRvFi';
const IMAGE_ARN = 'arn:aws:ecr:eu-west-1:202848742610:repository/drawing-backend';

export class CdkFargateStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, "DeepPensVPC", {
      maxAzs: 3, // Default is all AZs in region
    });

    const cluster = new ecs.Cluster(this, "DeepPensCluster", {
      vpc: vpc,
    });

       // Pass in OS variable set earlier in the codebuild script and pulled from Secrets Manager
    const docker_image_tag = process.env.DOCKER_IMAGE_TAG

    // Create a load-balanced Fargate service and make it public
    const loadBalancedFargateService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, "DeepPensService", {
      cluster: cluster, // Required
      cpu: 256, // Default is 256
      desiredCount: 2, // Default is 1
      healthCheckGracePeriod: cdk.Duration.seconds(10), // Default is 60
      taskImageOptions: {
           image: ecs.ContainerImage.fromEcrRepository(ecr.Repository.fromRepositoryArn(this, 'drawing-backend', IMAGE_ARN), docker_image_tag),
        enableLogging: true,
	    containerPort: 8080,
        secrets: {
          APIID: ecs.Secret.fromSecretsManager(sm.Secret.fromSecretAttributes(this, "ImportedSecretAPI", {
              secretArn: APIID_SECRET_ARN
          })),
          IOT_ENDPOINT: ecs.Secret.fromSecretsManager(sm.Secret.fromSecretAttributes(this, "ImportedSecretIOT_ENDPOINT", {
              secretArn: IOT_ENDPOINT_SECRET_ARN
          }))
        },
      },
      memoryLimitMiB: 512, // Default is 512
      publicLoadBalancer: true, // Default is false
    });

    // grant the task role rights to talk to IoT Data API
    loadBalancedFargateService.taskDefinition.taskRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName('AWSIoTDataAccess')
    );
    // Cloudwatch access
    loadBalancedFargateService.taskDefinition.taskRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName('CloudWatchFullAccess')
    );

  }
}
