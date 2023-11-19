import boto3
from datetime import datetime, timezone

def get_asg_instance_properties(account_details):
    asg_client = get_describe_auto_scaling_grp(account_details)
    # Get the running instances in the Auto Scaling Group
    instance_ids = [instance['InstanceId'] for instance in asg_client['AutoScalingGroups'][0]['Instances']]

    # Get properties for each instance
    instances_properties = []
    for instance_id in instance_ids:
        response = get_describe_instances(account_details,instance_id)
        instance = response['Reservations'][0]['Instances'][0]
        properties = {
            'InstanceId': instance_id,
            'SecurityGroups': [sg['GroupId'] for sg in instance.get('SecurityGroups', [])],
            'ImageId': instance['ImageId'],
            'VpcId': instance['VpcId'],
            'LaunchTime': instance['LaunchTime'],
        }
        instances_properties.append(properties)
    
    return instances_properties
  
def get_longest_running_instance(instances_properties):
    longest_running_instance = None
    max_elapsed_time = None

    for instance_properties in instances_properties:
        launch_time = instance_properties['LaunchTime']
        elapsed_time = calculate_uptime(launch_time)

        if max_elapsed_time is None or elapsed_time > max_elapsed_time:
            max_elapsed_time = elapsed_time
            longest_running_instance = instance_properties

    return [longest_running_instance, max_elapsed_time]
 
def get_describe_auto_scaling_grp(account_details):
    asg_client = boto3.client('autoscaling',aws_access_key_id=account_details[0],aws_secret_access_key=account_details[1],region_name=account_details[2])
    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[account_details[3]])
    #assert asg_response
    #print(asg_response)
    return asg_response

def get_describe_instances(account_details,instanceid):
    ec2_client = boto3.client('ec2',aws_access_key_id=account_details[0],aws_secret_access_key=account_details[1],region_name=account_details[2]) 
    #assert ec2_client
    #print(ec2_client)  
    return ec2_client.describe_instances(InstanceIds=[instanceid])

def get_describe_scheduled_actions(account_details,maxrec,starttime):
    asg_client = boto3.client('autoscaling',aws_access_key_id=account_details[0],aws_secret_access_key=account_details[1],region_name=account_details[2])
    #assert asg_client
    #print(asg_client)
    asg_response = asg_client.describe_scheduled_actions(AutoScalingGroupName=account_details[3],MaxRecords=maxrec,StartTime=starttime)
    #assert asg_response
    #print(asg_response)
    return asg_response

def get_describe_scaling_activities(account_details):
    asg_client = boto3.client('autoscaling',aws_access_key_id=account_details[0],aws_secret_access_key=account_details[1],region_name=account_details[2])
    #assert asg_client
    #print(asg_client)
    asg_response = asg_client.describe_scaling_activities(AutoScalingGroupName=account_details[3])
    #assert asg_response
    #print(asg_response)
    return asg_response

def calculate_uptime(launch_time):
    current_time = datetime.now(timezone.utc)
    elapsed_time = current_time - launch_time
    return elapsed_time

def calculate_elapsed_time(next_action_start_time):
    # Convert the AWS response datetime to a timezone-aware datetime
    utc_timezone = timezone.utc
    next_action_start_time_aware = next_action_start_time.replace(tzinfo=utc_timezone)

    # Calculate the elapsed time from the current time
    current_time = datetime.now(utc_timezone)
    elapsed_time = next_action_start_time_aware - current_time

    # Format the elapsed time in hh:mm:ss
    elapsed_time_str = str(elapsed_time).split(".")[0]
    return elapsed_time_str