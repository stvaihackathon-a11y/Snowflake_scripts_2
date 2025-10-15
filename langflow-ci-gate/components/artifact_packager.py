# components/artifact_packager.py
from langflow.custom import CustomComponent
import subprocess, os, json

class ArtifactPackager(CustomComponent):
    display_name = "Artifact Packager"
    description = "Builds and pushes Docker image OR zips artifacts for the pipeline."

    def build(self, image_tag: str = "latest", push: bool = True):
        build = subprocess.run(["docker", "build", "-t", image_tag, "."], capture_output=True, text=True)
        if push:
            push_r = subprocess.run(["docker", "push", image_tag], capture_output=True, text=True)
        return {"build_ok": build.returncode == 0, "push_ok": (push_r.returncode == 0) if push else True}

