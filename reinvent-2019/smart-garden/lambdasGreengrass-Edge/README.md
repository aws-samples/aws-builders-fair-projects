# Plant Watering

This project uses [Greengo](https://github.com/rpedigoni/greengo) to manage Greengrass operations, in an automated, reliable, and repeatable way. You may read more about it [on this article](https://read.acloud.guru/aws-greengrass-the-missing-manual-2ac8df2fbdf4).

## Environment setup
Start creating a Python virtualenv running Python 2.7. *Python 3.x is not supported on Greengrass Lambda yet, so using version as default for the project.* The [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/) lib is recommended to simplify management:

    mkvirtualenv plantwatering --python=python2.7

If not already activated, do it by executing:

    workon plantwatering

Then, install Greengo using `pip`:

    pip install git+git://github.com/rpedigoni/greengo.git#egg=greengo


## Running

### Create Greengrass resources
All Greengrass definitions are set on the `greengo.yaml` configuration file. The first step is to create those definitions on AWS:

    greengo create

The command above will create a Greengrass Core, its Lambda functions,  Device Resources, and MQTT subscriptions between entities. 

Also, the `create`  command will generate the necessary certificates (`./certs/`) and the Greengrass configuration file (`./config/config.json`).

You may open the AWS Console on Greengrass panel and navigate between the  generated entities.

 
### Setup Raspberry PI
 
Follow Greengrass documentation modules 1 and 2 to setup the Raspberry PI device. You may want to skip the config/certificates part as we'll use the ones provided by `greengo create`.

- https://docs.aws.amazon.com/greengrass/latest/developerguide/module1.html 
- https://docs.aws.amazon.com/greengrass/latest/developerguide/module2.html

With the device prepared, copy the generated certificates to it. From your machine, execute:

    rsync config/* pi@RASPBERRY_PI_ADDR:/tmp/config/
    rsync certs/* pi@RASPBERRY_PI_ADDR:/tmp/certs/

On the Raspberry PI device, move from /tmp/ to its correct location:

    mv /tmp/config/* /greengrass/config/
    mv /tmp/certs/* /greengrass/certs/

Create data folder required to run PlantWatering:
    
    mkdir /usr/plantwatering/

Then start Greengrass Core:

    /greengrass/ggc/core/greengrassd start

You should receive a confirmation message with the running PID for Greengrass Core service.


#### GPIO/USB connections

* Connect relay to Raspberry PI pin 18 (BCM).


### Deploy 

To get your definitions deployed to the devices, execute on your machine:

    greengo deploy

This command does exactly the same thing as clicking on the Deploy button on Greengrass AWS Console.


## Development and testing

After making changes to your Greengrass project (eg: editing lambda functions, creating MQTT subscriptions, etc), you must update its definitions on AWS. Do it by running:

    greengo update

Behind the scenes, `greengo` will remove all lambdas, resources and subscriptions, and then recreate them with a new Greengrass Group Version. 

After updating, run `greengo deploy` any time and the changes will be deployed to the devices.

## Troubleshooting

### Greengrass deployment

For  `greengo deploy` command, you may receive the following message:

    ERROR! TES service role is not associated with this account

Using the AWS CLI, check that an appropriate service role is associated with your account by using GetServiceRoleForAccount and ensure that the role has at least the AWSGreengrassResourceAccessRolePolicy permission applied. If you need to associate a Greengrass service role with your account, use AssociateServiceRoleToAccount:

    aws greengrass associate-service-role-to-account --role-arn YOUR_GG_ROLE_ARN

### PiCamera on RPi /dev/video0

    sudo modprobe bcm2835-v4l2