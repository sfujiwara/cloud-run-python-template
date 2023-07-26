import invoke
import uvicorn


@invoke.task
def start(ctx):
    """Start API server."""
    uvicorn.run(app="app.main:app", reload=True)


@invoke.task
def docker_build(ctx):
    """Build Docker image."""
    project = ctx["run"]["project"]
    region_ar = ctx["run"]["artifact_registry"]["region"]
    repository = ctx["run"]["artifact_registry"]["repository"]
    cmd = f"PROJECT={project} REPOSITORY={repository} REGION={region_ar} docker-compose build"
    ctx.run(cmd)


@invoke.task
def docker_push(ctx):
    """Push Docker image to Artifact Registry."""
    project = ctx["run"]["project"]
    region_ar = ctx["run"]["artifact_registry"]["region"]
    repository = ctx["run"]["artifact_registry"]["repository"]
    cmd = f"PROJECT={project} REPOSITORY={repository} REGION={region_ar} docker-compose push"
    ctx.run(cmd)


@invoke.task
def deploy(ctx):
    """Deploy Docker image to Cloud Run."""
    project = ctx["run"]["project"]
    region_ar = ctx["run"]["artifact_registry"]["region"]
    repository = ctx["run"]["artifact_registry"]["repository"]
    region_cr = ctx["run"]["cloud_run"]["region"]

    image = f"{region_ar}-docker.pkg.dev/{project}/{repository}/cloud-run-python-template:latest"

    cmd_lst = [
        "gcloud run deploy",
        "--project", project,
        "--platform", "managed",
        "--region", region_cr,
        "--image", image,
        "cloud-run-python-template",
    ]
    cmd = " ".join(cmd_lst)
    ctx.run(cmd)
