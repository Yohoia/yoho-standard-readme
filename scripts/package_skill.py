#!/usr/bin/env python3
"""Build and verify a self-contained installable copy of this skill."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


# This is the runtime contract. Add a path here when a runtime file is added,
# then let the bundled auditor verify that all shipped local references close.
RUNTIME_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/content.md",
    "references/visuals.md",
    "references/badges.md",
    "references/validation.md",
    "scripts/audit_readme.py",
    "scripts/preview_readme.mjs",
)


class PackageError(Exception):
    """A packaging failure safe to show directly to the CLI caller."""


def _sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _reject_symlink_path(root, relative):
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise PackageError(f"Runtime source path must not contain symlinks: {relative}")


def _output_path(raw_out, repo):
    if raw_out is None:
        parent = Path(tempfile.gettempdir()).resolve()
        try:
            output = Path(tempfile.mkdtemp(prefix="yoho-standard-readme-", dir=parent))
        except OSError as error:
            raise PackageError(f"Cannot reserve a temporary output directory: {error}") from error
        # The empty directory reserves a unique, safe name until atomic publish.
        created = True
    else:
        lexical = Path(raw_out).expanduser().absolute()
        if lexical.is_symlink():
            raise PackageError("Output path must not be a symlink")
        output = lexical.resolve(strict=False)
        created = False

    if output == repo or output in repo.parents or repo in output.parents:
        if created:
            output.rmdir()
        raise PackageError("Output must be separate from the source repository")
    if not output.parent.is_dir():
        if created:
            output.rmdir()
        raise PackageError(f"Output parent directory must already exist: {output.parent}")
    if not created:
        if output.exists() and not output.is_dir():
            raise PackageError(f"Output path is not a directory: {output}")
        if output.exists() and any(output.iterdir()):
            raise PackageError(f"Output directory must be new or empty: {output}")
    return output, created


def build_package(repo, raw_out=None):
    repo = Path(repo).expanduser().resolve()
    if not repo.is_dir():
        raise PackageError(f"Source repository is not a directory: {repo}")

    output, output_created = _output_path(raw_out, repo)
    stage = None
    published = False
    try:
        for relative in RUNTIME_FILES:
            source = repo / relative
            _reject_symlink_path(repo, relative)
            if not source.is_file():
                raise PackageError(
                    f"Runtime file is missing: {relative}. Add required runtime files to RUNTIME_FILES."
                )

        stage = Path(tempfile.mkdtemp(prefix=".yoho-skill-stage-", dir=output.parent))
        hashes = {}
        for relative in RUNTIME_FILES:
            source = repo / relative
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            source_hash, staged_hash = _sha256(source), _sha256(target)
            if source_hash != staged_hash:
                raise PackageError(f"Copied content did not match the source: {relative}")
            hashes[relative] = source_hash

        command = [
            sys.executable,
            str(stage / "scripts/audit_readme.py"),
            "--repo",
            str(stage),
        ]
        for document in (name for name in RUNTIME_FILES if name.lower().endswith((".md", ".markdown"))):
            command.extend(("--single", document))
        audit_process = subprocess.run(command, capture_output=True, text=True, check=False)
        try:
            audit_report = json.loads(audit_process.stdout)
        except json.JSONDecodeError as error:
            detail = audit_process.stderr.strip() or audit_process.stdout.strip()
            raise PackageError(f"Bundled documentation audit could not run: {detail or error}") from error
        if audit_process.returncode or audit_report.get("errors"):
            failures = [
                f"{item['document']}: {item['message']}"
                for item in audit_report.get("issues", [])
                if item.get("severity") == "error"
            ]
            raise PackageError(
                "Packaged references are not self-contained. Check RUNTIME_FILES and local links: "
                + "; ".join(failures)
            )

        # Detect edits made while packaging so the hashes describe one stable source version.
        for relative, expected in hashes.items():
            _reject_symlink_path(repo, relative)
            if _sha256(repo / relative) != expected:
                raise PackageError(f"Source changed while packaging; retry after edits settle: {relative}")

        audited_documents = [str(Path(item).relative_to(stage)) for item in audit_report["documents"]]
        try:
            os.replace(stage, output)
        except OSError as error:
            raise PackageError(f"Cannot publish package to {output}: {error}") from error
        stage = None
        published = True
        return {
            "source": str(repo),
            "output": str(output),
            "files": hashes,
            "audit": {
                "documents": audited_documents,
                "errors": audit_report["errors"],
                "warnings": audit_report["warnings"],
            },
        }
    finally:
        if stage is not None:
            shutil.rmtree(stage, ignore_errors=True)
        if output_created and not published and output.exists():
            try:
                output.rmdir()
            except OSError:
                # Preserve concurrent user data if anything appeared after reservation.
                pass


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Skill source repository (defaults to this checkout)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="New or empty destination directory (defaults to a unique OS temp path)",
    )
    args = parser.parse_args(argv)
    try:
        result = build_package(args.repo, args.out)
    except (PackageError, OSError) as error:
        parser.exit(1, f"Package failed: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
