import invoke
import uvicorn


@invoke.task
def serve(ctx):
    """Start API server."""
    uvicorn.run(app="server.main:app", port=8080, reload=True)


@invoke.task
def docker_build(ctx):
    """Build Docker image in local environment."""
    cmd = "docker build -t cloud-run-python-template ."
    ctx.run(cmd)


@invoke.task
def docker_run(ctx):
    """Run Docker container in local environment."""
    cmd = "docker run --rm -p 8080:8080 cloud-run-python-template"
    ctx.run(cmd)


@invoke.task
def gcloud_builds_submit(ctx):
    """Build Docker image in Cloud Build and push it to Artifact Registry."""
    project = ctx["run"]["project"]
    ar_location = ctx["run"]["artifact_registry"]["location"]
    repository = ctx["run"]["artifact_registry"]["repository"]

    image = f"{ar_location}-docker.pkg.dev/{project}/{repository}/cloud-run-python-template:latest"

    cmd = f"gcloud builds submit --project {project} -t {image} ."
    ctx.run(cmd)


@invoke.task
def gcloud_run_deploy(ctx):
    """Deploy Docker image to Cloud Run."""
    project = ctx["run"]["project"]
    cloud_run_location = ctx["run"]["cloud_run"]["location"]
    artifact_registry_location = ctx["run"]["artifact_registry"]["location"]
    repository = ctx["run"]["artifact_registry"]["repository"]

    image = f"{artifact_registry_location}-docker.pkg.dev/{project}/{repository}/cloud-run-python-template:latest"

    cmd_lst = [
        "gcloud run deploy cloud-run-python-template",
        f"--project {project}",
        f"--image {image}",
        f"--region {cloud_run_location}",
        "--platform managed",
        "--allow-unauthenticated",
    ]
    cmd = " ".join(cmd_lst)
    ctx.run(cmd)
