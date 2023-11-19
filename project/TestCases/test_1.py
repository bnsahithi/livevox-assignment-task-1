import pytest
import boto3
from datetime import datetime, timezone
from Utils.AWS_CLI_utils import get_describe_auto_scaling_grp,get_asg_instance_properties,calculate_uptime,get_longest_running_instance


def test_A_1_current_cap_desired_cap_should_be_same(account_details):
    ##1- ASG desire running count should be same as running instances. if mismatch fails
    asg_response = get_describe_auto_scaling_grp(account_details)
    for group in asg_response['AutoScalingGroups']:
        desired_count = group['DesiredCapacity']
        running_count = len(group['Instances'])
        print(f"Auto Scaling Group: {account_details[3]}")
        print(f"Desired Instance Count: {desired_count}")
        print(f"Running Instance Count: {running_count}")

        # Compare the counts and raise an exception if they are not equal
        if desired_count != running_count:
            raise ValueError(f"Mismatch between desired and running instance counts in Auto Scaling Group '{account_details[3]}'")
        print(f"Successfully Verified : Desired Instance Count and Running Instance Count to be same")

def test_A_2_unique_availability_zones_foreach_ec2_instance(account_details):
    
    response = get_describe_auto_scaling_grp(account_details)
    instances= []
    if 'AutoScalingGroups' in response and response['AutoScalingGroups']:
        asg = response['AutoScalingGroups'][0]
        instances= asg.get('Instances', [])
    
    assert len(instances) >= 2, "At least two instances are required for the test."

    unique_zones= set(instance['AvailabilityZone'] for instance in instances)
    
    try:
       assert len(unique_zones) == len(instances)
       print(f"Instances are present in unique availability zones")
       
    except AssertionError as e:
       print(f"Duplicate availability zones found across the instances: {e}")
       raise  # Reraise the exception to mark the test as failed    
    
def test_A_3_same_properties_across_ec2_instances(account_details):
    # Get properties for instances in the Auto Scaling Group
    instances_properties = get_asg_instance_properties(account_details)
    
    # Check if all instances have the same properties
    first_instance_properties = instances_properties[0]
    
    for instance_properties in instances_properties[1:]:
        assert instance_properties['SecurityGroups'] == first_instance_properties['SecurityGroups'], f"Security Groups mismatch for instance {instance_properties['InstanceId']}"
        assert instance_properties['ImageId'] == first_instance_properties['ImageId'], f"Image ID mismatch for instance {instance_properties['InstanceId']}"
        assert instance_properties['VpcId'] == first_instance_properties['VpcId'], f"VPC ID mismatch for instance {instance_properties['InstanceId']}"
         
    print(f"Instances SecurityGroups : {first_instance_properties['SecurityGroups']}") 
    print(f"Instances ImageId : {first_instance_properties['ImageId']}") 
    print(f"Instances VpcId : {first_instance_properties['VpcId']}") 
    print("All instances in the Auto Scaling Group have the same Security Groups, Image ID, and VPC ID.")

def test_A_4_longest_running_instance(account_details):
    # Get properties for instances in the Auto Scaling Group
    instances_properties = get_asg_instance_properties(account_details)
    
    # Calculate and print the uptime for each instance
    for instance_properties in instances_properties:
        uptime = calculate_uptime(instance_properties['LaunchTime'])
        print(f"Instance {instance_properties['InstanceId']} Uptime: {uptime}")

    # Get the instance with the longest uptime
    longest_running_instance = get_longest_running_instance(instances_properties)

    if longest_running_instance:
       print(f"\nThe instance with the longest uptime is {longest_running_instance[0]['InstanceId']} with uptime: {longest_running_instance[1]}")
    else:
       print("\nNo instances found in the Auto Scaling Group.")
