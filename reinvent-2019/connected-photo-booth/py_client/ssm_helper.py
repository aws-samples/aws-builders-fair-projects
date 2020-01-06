import boto3
import configparser

ssm = boto3.client('ssm')

__SSM_BASE_PATH__ = "/Cerebro"
__CONFIG_FILE_PATH__ = "cerebro.ssm_config"

def store_parameters():
	config_parser = configparser.ConfigParser()
	config_parser.read(__CONFIG_FILE_PATH__)

	print(config_parser.sections())

	for section in config_parser.sections():
		print("Section: %s" % section)

		for item in config_parser.items(section):
			print("Item: ")
			print(item)
			print(item[0], item[1])
			param_name = "%s/%s/%s" % (__SSM_BASE_PATH__, section, item[0])
			param_value = item[1]
			param_description = "Description for Key: %s" % item[0]
			print(param_name, param_value, param_description)
			ssm.put_parameter(\
				Name=param_name,\
				Description=param_description,\
				Value=param_value,\
				Type='String',\
				Overwrite=True\
				)

			print("Finished putting the parameter: %s" % item[0])

		print("next ...")

	print("All processed!")

def retrieve_parameters():

	ssm_param_list = []
	next_token = None
	while True:
		print("---------------- ")
		if next_token:
			response = ssm.get_parameters_by_path(Path="/Cerebro", Recursive=True, NextToken=next_token)
		else:
			response = ssm.get_parameters_by_path(Path="/Cerebro", Recursive=True)

		if "NextToken" in response:
			next_token = response["NextToken"]
		else:
			next_token = None

		for param in response["Parameters"]:
			print(param)
		print(next_token)
		#print(response["Parameters"], next_token)

		ssm_param_list += response["Parameters"]

		if not next_token:
			break

		#break

	print("all retrieved")
	print(len(ssm_param_list))
	#print(ssm_param_list)

	return ssm_param_list

retrieve_parameters()

