Use launch template
    - this may improve time from ssm access to being usable/configured
    - meaning more time spent in init

Wrap with script to allow:
    - specification of resources
        - instance type
        - disk size
        - number of instances
    - maybe auto instance naming
        - could use local username here as default and append a number
    - synchronous deploy and then collect instance id to display
