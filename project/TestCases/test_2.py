import boto3
from datetime import datetime, timezone, timedelta
from Utils.AWS_CLI_utils import get_describe_scheduled_actions,calculate_elapsed_time,get_describe_scaling_activities



def test_B_1_calculate_elapsed_time_for_schd_action(account_details):
    
    scheduled_actions = get_describe_scheduled_actions(account_details,maxrec=1,starttime=datetime.utcnow())
    print(scheduled_actions)
    scheduled_actions = scheduled_actions.get('ScheduledUpdateGroupActions', [])
    
    if scheduled_actions:
        next_action = scheduled_actions[0]
        if next_action:
           next_action_start_time = next_action.get('StartTime')
            # Calculate and print the elapsed time
           elapsed_time = calculate_elapsed_time(next_action_start_time)
           assert elapsed_time
           print(f"Elapsed Time: {elapsed_time}")
    else:
            raise ValueError("There are no scheduled actions")   
        
def test_B_2_calc_instances_launched_vs_terminated(account_details):
    
    # Get the current date and time
    current_date = datetime.now(timezone.utc).date()
    
    response = get_describe_scaling_activities(account_details)
    activities = response.get('Activities', [])

    instances_launched = 0
    instances_terminated = 0
    activities_today = []
    activities_today= [activity for activity in activities if activity['StartTime'].date() == current_date]
    
    if activities_today:
       for activity in activities_today:
          if activity['StatusCode'] == 'Successful':
            if activity['Description'].startswith('Launching a new EC2 instance'):
                instances_launched += 1
            elif activity['Description'].startswith('Terminating EC2 instance'):
                instances_terminated += 1
       print(f"\ninstances_launched : {instances_launched}")  
       print(f"instances_terminated : {instances_terminated}")      
    else:
        raise ValueError("There were no activities found on current date upto now 'current_time'")
    
    
