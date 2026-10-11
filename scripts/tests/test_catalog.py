"""Index fixtures do not require a Sailry build, native UI, or image decoder."""

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "catalog.py"
SPEC = importlib.util.spec_from_file_location("theme_catalog", SCRIPT)
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


def manifest(identity="fixture"):
    return {
        "version": 1, "id": identity, "name": "Fixture", "package_version": "0.1.0",
        "description": "Fixture description", "homepage": "https://sailry.dev",
        "license": {"author": "Sailry", "name": "Apache-2.0", "text": "Fixture license"},
        "light": {"theme": {"mode": "light"}, "assets": {
            "background.window": {"path": "assets/background.png"}}},
        "dark": {"theme": {"mode": "dark"}, "assets": {
            "background.window": {"path": "assets/background.png"}}},
    }


class Catalog(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.package = self.root / "fixture"
        (self.package / "assets").mkdir(parents=True)
        (self.package / "assets/background.png").write_bytes(b"fixture resource")
        self.manifest = manifest()
        self.write()

    def write(self):
        (self.package / "theme.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_indexes_manifest_metadata(self):
        result = catalog.catalog(self.root)
        self.assertEqual(result["version"], 1)
        self.assertEqual(len(result["themes"]), 1)
        entry = result["themes"][0]
        self.assertEqual({key: value for key, value in entry.items() if key != "digest"}, {
            "id": "fixture", "path": "fixture", "name": "Fixture", "package_version": "0.1.0",
            "author": "Sailry", "license": "Apache-2.0", "description": "Fixture description",
            "homepage": "https://sailry.dev",
        })
        self.assertRegex(entry["digest"], r"^sha256:[a-f0-9]{64}$")

    def test_sorts_packages_by_id(self):
        second = self.root / "alpha"
        second.mkdir()
        value = manifest("alpha")
        for mode in ("light", "dark"):
            del value[mode]["assets"]
        (second / "theme.json").write_text(json.dumps(value), encoding="utf-8")
        self.assertEqual([entry["id"] for entry in catalog.catalog(self.root)["themes"]],
                         ["alpha", "fixture"])

    def test_resources_change_digest(self):
        initial = catalog.catalog(self.root)
        self.assertEqual(initial, catalog.catalog(self.root))
        (self.package / "assets/background.png").write_bytes(b"changed resource")
        changed = catalog.catalog(self.root)
        self.assertNotEqual(initial["themes"][0]["digest"], changed["themes"][0]["digest"])
        self.assertEqual(initial["themes"][0]["package_version"], changed["themes"][0]["package_version"])

    def test_unreferenced_files_do_not_change_digest(self):
        initial = catalog.catalog(self.root)
        (self.package / "README.md").write_text("Updated package guide", encoding="utf-8")
        (self.package / "assets/unused.png").write_bytes(b"unused resource")
        self.assertEqual(initial, catalog.catalog(self.root))

    def test_keeps_source_files_unchanged(self):
        before = {path.relative_to(self.package): path.read_bytes()
                  for path in self.package.rglob("*") if path.is_file()}
        catalog.generate(self.root)
        catalog.generate(self.root, check=True)
        self.assertEqual(before, {path.relative_to(self.package): path.read_bytes()
                                for path in self.package.rglob("*") if path.is_file()})

    def test_check_rejects_stale_index_without_writing(self):
        catalog.generate(self.root)
        target = self.root / "catalog.json"
        initial = target.read_bytes()
        self.manifest["name"] = "Updated name"
        self.write()
        with self.assertRaisesRegex(ValueError, "Catalog is stale"):
            catalog.generate(self.root, check=True)
        self.assertEqual(target.read_bytes(), initial)

    def test_rejects_unreleased_version_bumps(self):
        for version in ("0.1.1", "1.0.0", 1, None):
            with self.subTest(version=version):
                self.manifest["package_version"] = version
                self.write()
                with self.assertRaisesRegex(ValueError, "must remain 0.1.0"):
                    catalog.catalog(self.root)

    def test_rejects_invalid_format_and_identity(self):
        for key, value in (("version", 2), ("version", True), ("id", "other"),
                           ("id", "../escape"), ("id", "Uppercase")):
            with self.subTest(key=key, value=value):
                self.manifest = manifest()
                self.manifest[key] = value
                self.write()
                with self.assertRaises(ValueError):
                    catalog.catalog(self.root)

    def test_rejects_unsafe_resource_paths(self):
        for path in ("../outside.png", "assets/../outside.png", "/assets/image.png",
                     "https://example.com/image.png", "assets\\image.png", "assets//image.png",
                     "assets/image.svg", "assets/image.png?query"):
            with self.subTest(path=path):
                self.manifest["light"]["assets"]["background.window"]["path"] = path
                self.write()
                with self.assertRaisesRegex(ValueError, "local raster paths"):
                    catalog.catalog(self.root)

    def test_rejects_missing_resource(self):
        (self.package / "assets/background.png").unlink()
        with self.assertRaisesRegex(ValueError, "resource is missing"):
            catalog.catalog(self.root)

    def test_rejects_symbolic_links(self):
        resource = self.package / "assets/background.png"
        external = self.root / "outside.png"
        external.write_bytes(resource.read_bytes())
        resource.unlink()
        resource.symlink_to(external)
        with self.assertRaisesRegex(ValueError, "symbolic links"):
            catalog.catalog(self.root)
        resource.unlink()
        resource.write_bytes(external.read_bytes())
        original = self.root / "original"
        self.package.rename(original)
        self.package.symlink_to(original, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symbolic links"):
            catalog.catalog(self.root)

    def test_rejects_resource_budget_overflow(self):
        with mock.patch.object(catalog, "FILE_LIMIT", 1):
            with self.assertRaisesRegex(ValueError, "too large"):
                catalog.catalog(self.root)
        with mock.patch.object(catalog, "PACKAGE_LIMIT", 1):
            with self.assertRaisesRegex(ValueError, "package limit"):
                catalog.catalog(self.root)

    def test_rejects_invalid_variants_and_metadata(self):
        fixtures = []
        for key, value in (("name", ""), ("license", {}), ("light", []),
                           ("dark", {"theme": {}, "assets": []}),
                           ("homepage", "https://user:secret@example.com")):
            sample = copy.deepcopy(manifest())
            sample[key] = value
            fixtures.append(sample)
        for sample in fixtures:
            with self.subTest(sample=sample):
                self.manifest = sample
                self.write()
                with self.assertRaises(ValueError):
                    catalog.catalog(self.root)


if __name__ == "__main__":
    unittest.main()
