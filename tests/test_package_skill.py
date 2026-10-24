import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


CHECKOUT = Path(__file__).resolve().parents[1]
SCRIPT = CHECKOUT / "scripts/package_skill.py"
EXPECTED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/content.md",
    "references/visuals.md",
    "references/badges.md",
    "references/validation.md",
    "scripts/audit_readme.py",
    "scripts/preview_readme.mjs",
}


class SkillPackageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.repo = self.root / "source"
        self.repo.mkdir()
        self.write("SKILL.md", "# Fixture skill\n\n[Content](references/content.md)\n"
                   "[Visuals](references/visuals.md)\n[Badges](references/badges.md)\n"
                   "[Validation](references/validation.md)\n")
        self.write("references/content.md", "# Content\n\n[Rules](visuals.md#rules)\n")
        self.write("references/visuals.md", "# Visuals\n\n## Rules\n\n[Preview](../scripts/preview_readme.mjs)\n\n[Badges](badges.md)\n")
        self.write("references/badges.md", "# Badges\n\n[Visual rules](visuals.md#rules)\n")
        self.write("references/validation.md", "# Validation\n\n[Content](content.md)\n")
        self.write("agents/openai.yaml", 'interface:\n  display_name: "Fixture skill"\n')
        self.write("scripts/preview_readme.mjs", '// Fixture preview\nconsole.log("preview");\n')
        shutil.copyfile(CHECKOUT / "scripts/audit_readme.py", self.repo / "scripts/audit_readme.py")
        self.write("docs/verification.md", "# Development-only verification\n")
        self.write("README.md", "# Development-only README\n")
        self.output = self.root / "package"

    def write(self, name, text):
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def run_package(self, output=True, *extra):
        command = [sys.executable, str(SCRIPT), "--repo", str(self.repo)]
        if output:
            command.extend(("--out", str(self.output)))
        return subprocess.run(command + list(extra), capture_output=True, text=True)

    def assert_no_staging(self):
        self.assertEqual(list(self.root.glob(".yoho-skill-stage-*")), [])

    def assert_failed_without_package(self, result):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertFalse(self.output.exists())
        self.assert_no_staging()

    def test_real_cli_builds_self_contained_runtime_and_reports_source_hashes(self):
        result = self.run_package()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        actual = {str(path.relative_to(self.output)) for path in self.output.rglob("*") if path.is_file()}
        self.assertEqual(actual, EXPECTED_FILES)
        self.assertEqual(set(report["files"]), EXPECTED_FILES)
        self.assertEqual(report["source"], str(self.repo))
        self.assertEqual(report["output"], str(self.output))
        self.assertEqual(report["audit"]["errors"], 0)
        self.assertEqual(set(report["audit"]["documents"]), {name for name in EXPECTED_FILES if name.endswith(".md")})
        for relative in EXPECTED_FILES:
            source, installed = (self.repo / relative).read_bytes(), (self.output / relative).read_bytes()
            self.assertEqual(installed, source)
            self.assertEqual(report["files"][relative], hashlib.sha256(source).hexdigest())
        self.assert_no_staging()

    def test_empty_existing_output_is_allowed(self):
        self.output.mkdir()
        result = self.run_package()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.output / "SKILL.md").is_file())

    def test_default_output_is_unique_os_temp_package(self):
        result = self.run_package(False)
        self.assertEqual(result.returncode, 0, result.stderr)
        target = Path(json.loads(result.stdout)["output"])
        self.addCleanup(shutil.rmtree, target)
        self.assertEqual(target.parent, Path(tempfile.gettempdir()).resolve())
        self.assertTrue((target / "references/visuals.md").is_file())
        self.assertFalse(target.is_relative_to(self.repo))

    def test_selected_source_content_is_not_replaced_by_checkout_content(self):
        self.write("references/content.md", "# Selected source version\n\nActual selected-source content.\n")
        result = self.run_package()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.output / "references/content.md").read_text(),
                         "# Selected source version\n\nActual selected-source content.\n")

    def test_new_referenced_runtime_document_requires_explicit_manifest_entry(self):
        self.write("references/new-guide.md", "# New runtime guide\n")
        self.write("references/content.md", "# Content\n\n[New guide](new-guide.md)\n")
        self.assert_failed_without_package(self.run_package())

    def test_bad_local_anchor_rejects_package(self):
        self.write("references/content.md", "# Content\n\n[Missing anchor](visuals.md#absent)\n")
        self.assert_failed_without_package(self.run_package())

    def test_html_references_are_checked_in_real_installed_copy(self):
        self.write("references/visuals.md", '# Visuals\n\n## Rules\n\n<img src="missing.png" alt="Real asset">\n')
        self.assert_failed_without_package(self.run_package())

    def test_source_development_link_cannot_pass_because_file_exists_in_checkout(self):
        self.write("references/validation.md", "# Validation\n\n[Record](../docs/verification.md)\n")
        self.assertTrue((self.repo / "docs/verification.md").is_file())
        self.assert_failed_without_package(self.run_package())

    def test_missing_runtime_file_fails_without_output_or_partial_package(self):
        (self.repo / "agents/openai.yaml").unlink()
        self.assert_failed_without_package(self.run_package())

    def test_failed_validation_preserves_preexisting_empty_output(self):
        self.output.mkdir()
        self.write("references/content.md", "# Content\n\n[Missing](absent.md)\n")
        result = self.run_package()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(self.output.is_dir())
        self.assertEqual(list(self.output.iterdir()), [])
        self.assert_no_staging()

    def test_nonempty_output_is_preserved_byte_for_byte(self):
        self.output.mkdir()
        kept = self.output / "keep.bin"
        kept.write_bytes(b"user data\x00\xff")
        result = self.run_package()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(list(self.output.iterdir()), [kept])
        self.assertEqual(kept.read_bytes(), b"user data\x00\xff")
        self.assert_no_staging()

    def test_source_same_ancestor_and_nested_outputs_are_rejected(self):
        for target in (self.repo, self.repo / "package", self.root):
            with self.subTest(target=target):
                result = self.run_package(False, "--out", str(target))
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertTrue((self.repo / "SKILL.md").is_file())
                self.assert_no_staging()
        self.assertFalse((self.repo / "package").exists())

    def test_output_file_is_preserved(self):
        self.output.write_bytes(b"existing file")
        result = self.run_package()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.output.read_bytes(), b"existing file")
        self.assert_no_staging()

    def test_missing_output_parent_is_not_created(self):
        self.output = self.root / "absent-parent/package"
        self.assert_failed_without_package(self.run_package())
        self.assertFalse(self.output.parent.exists())

    def test_output_symlink_is_not_followed_or_replaced(self):
        destination = self.root / "empty-target"
        destination.mkdir()
        self.output.symlink_to(destination, target_is_directory=True)
        result = self.run_package()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(self.output.is_symlink())
        self.assertEqual(list(destination.iterdir()), [])
        self.assert_no_staging()

    def test_symlink_parent_does_not_allow_output_inside_source(self):
        alias = self.root / "source-alias"
        alias.symlink_to(self.repo, target_is_directory=True)
        self.output = alias / "package"
        self.assert_failed_without_package(self.run_package())

    def test_symlinked_source_file_cannot_escape_runtime_content(self):
        outside = self.root / "outside.md"
        outside.write_text("# Outside\n")
        source = self.repo / "references/content.md"
        source.unlink()
        source.symlink_to(outside)
        self.assert_failed_without_package(self.run_package())
        self.assertEqual(outside.read_text(), "# Outside\n")

    def test_source_root_alias_resolves_to_the_selected_repository(self):
        alias = self.root / "source-alias"
        alias.symlink_to(self.repo, target_is_directory=True)
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(alias), "--out", str(self.output)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["source"], str(self.repo))


if __name__ == "__main__":
    unittest.main()
