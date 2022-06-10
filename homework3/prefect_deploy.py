from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner

DeploymentSpec(
    name="cron-schedule-deployment",
    flow_location="/MLOps_zoomcamp/homework3/homework.py",
    schedule=CronSchedule(
        cron="0 9 15 * *",
        timezone="America/New_York"
        ),
    flow_runner=SubprocessFlowRunner(),
)