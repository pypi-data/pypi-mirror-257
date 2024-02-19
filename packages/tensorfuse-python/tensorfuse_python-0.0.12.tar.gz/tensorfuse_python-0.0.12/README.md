# Tensorfuse SDK

Python SDK package for Tensorfuse


# Usage

Default Logging:

```
from tensorfuse_python.tensorfuse_python import log_generic_event

status = log_generic_event(
    token=<AUTH_TOKEN>,
    log=<LOG_OBJECT>
)
```


Logging Using IDs:

```
from tensorfuse_python.tensorfuse_python import log_generic_event_using_ids

status = log_generic_event_using_ids(
    token=<AUTH_TOKEN>,
    teamId=<TEAM_ID>, 
    projectId=<PROJECT_ID>, 
    datasourceId=<DATASOURCE_ID>,  
    log=<LOG_OBJECT>
)
```


Logging Using Names:

```
from tensorfuse_python.tensorfuse_python import log_generic_event_using_names

status = log_generic_event_using_names(
    token=<AUTH_TOKEN>,
    teamName=<TEAM_NAME>, 
    projectName=<PROJECT_NAME>, 
    datasourceName=<DATASOURCE_NAME>,  
    log=<LOG_OBJECT>
)
```
