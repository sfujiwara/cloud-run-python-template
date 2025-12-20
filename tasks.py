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
def deploy(ctx):
    """Build Docker image in Cloud Build and deploy it to Cloud Run."""
    project = ctx["run"]["project"]

    cmd_lst = [
        "gcloud builds submit",
        f"--project {project}",
        "--config cloudbuild.yaml",
    ]
    cmd = " ".join(cmd_lst)
    ctx.run(cmd)
