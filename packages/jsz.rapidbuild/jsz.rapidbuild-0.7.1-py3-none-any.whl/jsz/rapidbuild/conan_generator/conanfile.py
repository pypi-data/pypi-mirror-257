from __future__ import annotations

from conans import ConanFile, tools
from conans.model import Generator
from conans.errors import ConanInvalidConfiguration, ConanException
import traceback
import os
import json
import subprocess
import re


required_conan_version = ">=1.43 <=1.62"


THIRD_PARTY_MANIFEST_FILENAME = "third_party_gen.json"
TOOLCHAIN_MANIFEST_FILENAME = "toolchain_gen.json"


def _sanitize_path(path: str):
    return os.path.normpath(path)


def _sanitize_paths(paths: list[str]):
    return [_sanitize_path(p) for p in paths]


class ToolchainDiscoveryError(RuntimeError):
    pass


class SemVer:
    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


class ToolchainDiscoveryWindows:
    """
    This discovery procedure covers the most common setups and does not even try to be exhaustive in terms
    uniquely identifying all possible configurations:
    * Target arch is ignored in the toolchain name (key), since only x86_64 is supported. However, VS uses
      different binaries for targeting different platforms.
    * Clang on Windows can be installed by a lot of means, see: https://github.com/conan-io/conan/issues/10955
    * LLVM installation from llvm.org is not self-sufficient - MSVC needs to be installed to use it (it provides
      the Windows C++ language runtime and the MSVC standard library). Therefore, an example windows LLVM toolchain
      could potentially use different VS installations present.
      
    Warning!
    The resulting toolchain ids/names do not convey their full configuration/identity and thus generated binaries
    can be different on various machines. Toolchains discovered using this class should be used only for package
    development and never for building that package for deployment - this should be handled by tools curated
    by the Conan community and by fully respecting the Conan settings.

    """

    def __init__(self):
        self.toolchains = {}

    def dump_to_json(self):
        return json.dumps(self.toolchains, indent=4)

    _TARGET_ARCHITECTURES = [
        "x86_64",
    ]

    _OS_WINDOWS_KEY = "win"

    def _add_toolchain(self, build_os, name, arch, tc):
        key_includes_os = False
        key_includes_arch = False
        
        key = ""
        if key_includes_os:
            key += f"{build_os}_"
        key += f"{name}_"
        if key_includes_arch:
            key += f"{arch}_"
        key = key.removesuffix("_")
        
        self.toolchains[key] = tc

    def discover_toolchains(self, conanfile):
        # TODO: Get rid of conanfile argument - we discover everything we can, disregarding conanfile settings.
        # The argument is required for tools.vcvars_dict, even though we override the important options.

        #
        # Detect Visual Studio installations.
        #
        valid_vc_vars = []
        vs_major_versions = []

        vs_installations = tools.vswhere()
        for vs_installation in vs_installations:
            try:
                ver = tools.Version(vs_installation["installationVersion"])
                major = str(ver.major)
                if major not in vs_major_versions:
                    vs_major_versions.append(major)
            except KeyError:
                raise ToolchainDiscoveryError("Unable to detect Visual Studio installations - internal error.")

        for vs_version in vs_major_versions:
            # VS uses different toolchains for targeting different architectures.
            for arch in self._TARGET_ARCHITECTURES:
                try:
                    vc_vars = tools.vcvars_dict(conanfile, arch=arch, compiler_version=vs_version, filter_known_paths=True)
                except ConanException as e:
                    raise ToolchainDiscoveryError("Unable to detect MSVC metadata - internal error.")
                else:
                    vc_tools_version = vc_vars["VCToolsVersion"]
                    vscmd_ver = vc_vars["VSCMD_VER"]
                    conanfile.output.info(f"MSVC -- found version {vc_tools_version} (VS: {vscmd_ver}) for arch {arch}.")
                    valid_vc_vars.append((vs_version, arch, vc_vars))

        for vs_version, arch, vc_vars in valid_vc_vars:
            self._add_toolchain(self._OS_WINDOWS_KEY, f"vs{vs_version}_msvc", arch,
                                self._generate_toolchain_manifest_vs_msvc(vc_vars))

        #
        # Detect clang installation.
        #
        clang_path = tools.which("clang")
        if clang_path is not None:

            try:
                args = [clang_path, "--version"]
                completed_proc = subprocess.run(args, check=True, capture_output=True, text=True)
                if completed_proc.stdout is not None:
                    output_lines = completed_proc.stdout.split(sep='\n')
                else:
                    raise ToolchainDiscoveryError("Cannot capture 'clang --version' output.")
            except subprocess.SubprocessError as e:
                raise ToolchainDiscoveryError("Could not execute 'clang --version'.")

            for line in output_lines:
                match = re.match(r"clang version (\d+)\.(\d+)\.(\d+)", line)
                if match is not None:
                    break
            else:
                raise ToolchainDiscoveryError("Could not parse 'clang --version' output.")

            major = match.group(1)
            minor = match.group(2)
            patch = match.group(3)
            conanfile.output.info(f"Compiler 'clang' -- found version {major}.{minor}.{patch}.")

            # Go up twice
            llvm_root_path = os.path.split(os.path.split(clang_path)[0])[0]
            for vs_version, arch, vc_vars in valid_vc_vars:
                self._add_toolchain(self._OS_WINDOWS_KEY, f"vs{vs_version}_llvm{major}", arch,
                                    self._generate_toolchain_manifest_vs_llvm(vc_vars, llvm_root_path,
                                                                              SemVer(major, minor, patch)))
        else:
            conanfile.output.info(f"Compiler 'clang' -- not found.")

    @staticmethod
    def gen_vswhere_json():
        return json.dumps(tools.vswhere(), indent=4)

    @staticmethod
    def gen_vcvars_json(conanfile):
        return json.dumps(tools.vcvars_dict(conanfile, only_diff=True), indent=4)

    @staticmethod
    def _generate_toolchain_manifest_vs_msvc(vc_vars):
        vc_tools_install_dir = _sanitize_path(vc_vars["VCToolsInstallDir"])
        vc_host_arch = vc_vars["VSCMD_ARG_HOST_ARCH"]
        vc_target_arch = vc_vars["VSCMD_ARG_TGT_ARCH"]

        vc_bin_path = os.path.join(f"{vc_tools_install_dir}", "bin", f"Host{vc_host_arch}", f"{vc_target_arch}")
        # vc_lib_path = os.path.join(f"{vc_tools_install_dir}", "lib", f"{vc_target_arch}")
        # vc_include_path = _sanitize_path(vc_tools_install_dir)

        toolchain = {
            "compiler_family": "msvc",
            "version": vc_vars["VCToolsVersion"],  # eg: 14.38.33130
            "compiler_path": os.path.join(vc_bin_path, "cl.exe"),
            "librarian_path": os.path.join(vc_bin_path, "lib.exe"),
            "linker_path": os.path.join(vc_bin_path, "link.exe"),
        }

        # TODO: some of these have the version hardcoded
        msvc_extra_files = [
            'c1.dll',
            'c1xx.dll',
            'c2.dll',
            'atlprov.dll',  # Only needed if using ATL
            'msobj140.dll',
            'mspdb140.dll',
            'mspdbcore.dll',
            'mspdbsrv.exe',
            'mspft140.dll',
            'msvcp140.dll',
            'vcruntime140.dll',
            'tbbmalloc.dll',  # Required as of 16.2(14.22 .27905)
            os.path.join('1033', 'clui.dll'),
            os.path.join('1033', 'mspft140ui.dll'),  # Localized messages for static analysis
        ]

        msvc_extra_files = [os.path.join(vc_bin_path, p) for p in msvc_extra_files if len(p) != 0]

        toolchain["compiler_extra_files"] = _sanitize_paths(msvc_extra_files)
        toolchain["toolchain_include_dirs"] = _sanitize_paths(vc_vars["INCLUDE"])
        toolchain["toolchain_lib_dirs"] = _sanitize_paths(vc_vars["LIB"])

        return toolchain

    @staticmethod
    def _generate_toolchain_manifest_vs_llvm(vc_vars, llvm_root_path, llvm_semver):
        toolchain = {
            "compiler_family": "clang",
            "version": str(llvm_semver),
            "compiler_path": os.path.join(llvm_root_path, "bin", "clang++.exe"),
            "librarian_path": os.path.join(llvm_root_path, "bin", "llvm-ar.exe"),
            "linker_path": os.path.join(llvm_root_path, "bin", "lld-link.exe"),  # Must use lld-link on Windows.
            "compiler_extra_files": [],  # TODO: proobably some DLLs from the binaries dir should be added here.
        }

        # Clang on Windows links against MSVC's stdlib, runtime, etc.

        # The arguments and their order are based upon the --verbose output from the clang driver,
        # compiling a simple cpp file.

        # The clang include path must be first in the list.
        clang_include_path = os.path.join(llvm_root_path, "lib", "clang", str(llvm_semver), "include")
        if not os.path.exists(clang_include_path):
            clang_include_path = os.path.join(llvm_root_path, "lib", "clang", str(llvm_semver.major), "include")
        if not os.path.exists(clang_include_path):
            raise RuntimeError("Could not determine clang include path.")

        clang_lib_dir_path =  os.path.join(llvm_root_path, "lib", "clang", str(llvm_semver), "lib", "windows")
        if not os.path.exists(clang_lib_dir_path):
            clang_lib_dir_path =  os.path.join(llvm_root_path, "lib", "clang", str(llvm_semver.major), "lib", "windows")
        if not os.path.exists(clang_include_path):
            raise RuntimeError("Could not determine clang lib dir path.")

        include_dirs = [clang_include_path]
        include_dirs.extend(_sanitize_paths(vc_vars["INCLUDE"]))

        lib_dirs = _sanitize_paths(vc_vars["LIB"])
        # The clang lib dir path must be last on the list.
        lib_dirs.append(clang_lib_dir_path)

        toolchain["toolchain_include_dirs"] = include_dirs
        toolchain["toolchain_lib_dirs"] = lib_dirs

        return toolchain


def create_toolchain_discovery():
    detected_os = tools.detected_os()
    if detected_os == "Windows":
        return ToolchainDiscoveryWindows()
    else:
        raise NotImplementedError(f"Toolchain discovery not implemented on build OS: '{detected_os}'.")


# noinspection PyBroadException
class RapidGenerator(Generator):

    # noinspection PyPropertyDefinition
    @property
    def filename(self):
        pass

    @property
    def content(self):
        try:

            if self.conanfile.options.development:
                self.conanfile.output.info("RapidGenerator: Running toolchain discovery...")

                td = create_toolchain_discovery()
                td.discover_toolchains(self.conanfile)

                return {
                    THIRD_PARTY_MANIFEST_FILENAME: self._generate_third_party_manifest_json(),
                    TOOLCHAIN_MANIFEST_FILENAME: td.dump_to_json(),
                    # "debug_vswhere_output.json": td.gen_vswhere_json(),
                    # "debug_vcvars.json": td.gen_vcvars_json(self.conanfile),
                }
            else:
                return {
                    THIRD_PARTY_MANIFEST_FILENAME: self._generate_third_party_manifest_json(),
                }

        except Exception:
            traceback.print_exc()

    @staticmethod
    def _parse_definition(definition):
        # Preprocessor definition given on the command line.
        pattern = "^([_a-zA-Z][_a-zA-Z0-9]*)$"
        match = re.match(pattern, definition)
        if match is not None:
            name = match.group(1)
            return name, None

        # Preprocessor definition given on the command line, with value assignment.
        pattern = "^([_a-zA-Z][_a-zA-Z0-9]*)=(.*)$"
        match = re.match(pattern, definition)
        if match is not None:
            name = match.group(1)
            value = match.group(2)
            return name, value

    def _generate_third_party_manifest_json(self):
        deps_cpp_info = self.conanfile.deps_cpp_info
        targets_interfaces = {}
        for dep in deps_cpp_info.deps:
            dep_cpp_info = deps_cpp_info[dep]

            dep_interface = {
                "include_dirs": _sanitize_paths(dep_cpp_info.include_paths),
                "definitions": {},
                "link_libs": _sanitize_paths(dep_cpp_info.libs),
                "link_libs_dirs": _sanitize_paths(dep_cpp_info.lib_paths),
            }

            for d in dep_cpp_info.defines:
                name, value = self._parse_definition(d)
                dep_interface["definitions"][name] = value

            debug = False
            if debug:
                dep_interface["_impl"] = {
                    # cpp_info
                    "_includedirs": dep_cpp_info.includedirs,
                    "_libdirs": dep_cpp_info.libdirs,
                    "_resdirs": dep_cpp_info.resdirs,
                    "_bindirs": dep_cpp_info.bindirs,
                    "_builddirs": dep_cpp_info.builddirs,
                    "_libs": dep_cpp_info.libs,
                    "_defines": dep_cpp_info.defines,
                    "_cflags": dep_cpp_info.cflags,
                    "_cxxflags": dep_cpp_info.cxxflags,
                    "_sharedlinkflags": dep_cpp_info.sharedlinkflags,
                    "_exelinkflags": dep_cpp_info.exelinkflags,
                    "_frameworks": dep_cpp_info.frameworks,
                    "_frameworkdirs": dep_cpp_info.frameworkdirs,
                    "_system_libs": dep_cpp_info.system_libs,
                    # dep_cpp_info
                    "_include_paths": dep_cpp_info.include_paths,
                    "_lib_paths": dep_cpp_info.lib_paths,
                    "_bin_paths": dep_cpp_info.bin_paths,
                    "_build_paths": dep_cpp_info.build_paths,
                    "_res_paths": dep_cpp_info.res_paths,
                    "_framework_paths": dep_cpp_info.framework_paths,
                    "_build_modules_paths": dep_cpp_info.build_modules_paths,
                    "_version": dep_cpp_info.version,
                    # "_components": dep_cpp_info.components,
                }
                
            targets_interfaces[dep] = dep_interface
        return json.dumps(targets_interfaces, indent=4)


class Pkg(ConanFile):
    name = "rapidbuild"
    version = "0.7.1"
    license = "MIT"


def _validate_version(pkg_version: str):
    assert (Pkg.version == pkg_version)