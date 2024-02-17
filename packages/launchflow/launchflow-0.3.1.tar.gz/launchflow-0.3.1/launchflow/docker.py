import dataclasses
import enum
import re
from typing import List, Optional


class Provider(enum.Enum):
    GCP = "gcp"


@dataclasses.dataclass
class Dockerfile:
    contents: str

    def __post_init__(self) -> None:
        # Validate Dockerfile contents to catch syntax and usage issues
        self.validate_contents(self.contents)

    @staticmethod
    def validate_contents(
        contents: str, include_best_practice_checks: bool = False
    ) -> None:
        # Check 1: Correct Instruction Format
        if not re.match(
            r"^(FROM|RUN|CMD|LABEL|EXPOSE|ENV|ADD|COPY|ENTRYPOINT|VOLUME|USER|WORKDIR|ARG|ONBUILD|STOPSIGNAL|HEALTHCHECK|SHELL)\s",
            contents,
            re.MULTILINE | re.IGNORECASE,
        ):
            raise ValueError(
                "Invalid Dockerfile: Contains incorrect instruction format or unrecognized instructions."
            )

        # Check 2: Valid Instruction Sequence
        # This is a basic check and might need to be more sophisticated in real scenarios
        if not re.match(r"^FROM", contents):
            raise ValueError(
                "Invalid Dockerfile: 'FROM' must be the first instruction."
            )

        # Check 3: Proper Use of Shell Form vs. Exec Form
        if re.search(r'^CMD\s+["\']', contents, re.MULTILINE) or re.search(
            r'^ENTRYPOINT\s+["\']', contents, re.MULTILINE
        ):
            raise ValueError(
                "Invalid Dockerfile: Prefer exec form for CMD and ENTRYPOINT for proper signal handling."
            )

        # Check 4: Environment Variable Syntax
        if re.search(r'^ENV\s+[^\s]+=["\'].*["\']$', contents, re.MULTILINE):
            raise ValueError(
                "Invalid Dockerfile: Environment variables should be defined in 'key=value' format."
            )

        # Check 5: Correct Use of Build Arguments (ARG)
        if re.search(r'^ARG\s+[^\s]+=["\'].*["\']$', contents, re.MULTILINE):
            raise ValueError(
                "Invalid Dockerfile: Build arguments should be defined in 'key=value' format or simply as 'key'."
            )

        if include_best_practice_checks:
            # Check 6: Instruction Duplication
            if re.findall(r"^WORKDIR\s", contents, re.MULTILINE) or re.findall(
                r"^USER\s", contents, re.MULTILINE
            ):
                raise ValueError(
                    "Invalid Dockerfile: Unnecessary duplication of WORKDIR or USER instructions detected."
                )

            # Check 7: Layer Optimization
            if re.findall(
                r"^RUN\s+apt-get\s+install", contents, re.MULTILINE
            ) and not re.search(r"apt-get\s+clean", contents):
                raise ValueError(
                    "Invalid Dockerfile: Combine RUN instructions for package installation and cleanup to optimize layers."
                )

            # Check 8: Health Check
            if "HEALTHCHECK" not in contents:
                raise ValueError(
                    "Invalid Dockerfile: Include a HEALTHCHECK instruction for monitoring container health."
                )

            # Check 9: Label Usage
            if "LABEL" not in contents:
                raise ValueError(
                    "Invalid Dockerfile: Use LABEL instructions to provide important metadata about the image."
                )

    @classmethod
    def from_file(cls, path: str) -> "Dockerfile":
        # Open the file and read its contents
        with open(path) as f:
            return cls(f.read())


@dataclasses.dataclass
class DockerfileBuilder:
    base_image: str
    maintainer: Optional[str] = None
    workdir: Optional[str] = None
    environment_variables: Optional[dict] = None
    run_commands: Optional[List[str]] = None
    copy_files: Optional[List[str]] = None
    add_files: Optional[List[str]] = None
    exposed_ports: Optional[List[int]] = None
    command: Optional[str] = None
    entrypoint: Optional[str] = None
    user: Optional[str] = None
    volumes: Optional[List[str]] = None

    def build(self) -> Dockerfile:
        dockerfile_contents = [f"FROM {self.base_image}"]

        if self.maintainer:
            dockerfile_contents.append(f"LABEL maintainer={self.maintainer}")

        if self.environment_variables:
            for key, value in self.environment_variables.items():
                dockerfile_contents.append(f"ENV {key}={value}")

        if self.run_commands:
            for cmd in self.run_commands:
                dockerfile_contents.append(f"RUN {cmd}")

        if self.workdir:
            dockerfile_contents.append(f"WORKDIR {self.workdir}")

        if self.copy_files:
            for file in self.copy_files:
                dockerfile_contents.append(f"COPY {file} {file}")

        if self.add_files:
            for file in self.add_files:
                dockerfile_contents.append(f"ADD {file} {file}")

        if self.user:
            dockerfile_contents.append(f"USER {self.user}")

        if self.volumes:
            for volume in self.volumes:
                dockerfile_contents.append(f"VOLUME {volume}")

        if self.exposed_ports:
            for port in self.exposed_ports:
                dockerfile_contents.append(f"EXPOSE {port}")

        if self.entrypoint:
            dockerfile_contents.append(f"ENTRYPOINT {self.entrypoint}")

        if self.command:
            dockerfile_contents.append(f"CMD {self.command}")

        return Dockerfile("\n".join(dockerfile_contents))
