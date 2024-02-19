from typing import Any
import fs

from . import base
from .compiler_base import (
    CompilerFloatBehavior, CompilerWarningState, LanguageStandard, CompilerWarningSettings, CompilerWarningLevel,
    UnsupportedSettingError, CompilerArgFormatter, LanguageConformance, CompilerSettings, UnsupportedLanguageError,
    CompilerOptimizationMode, is_lang_c, is_lang_cpp
)


class CompilerArgFormatterMSVC(CompilerArgFormatter):
    def format_beginning_args(self) -> list[str]:
        return ["/nologo"]

    @staticmethod
    def _format_language_type_args(language: LanguageStandard):
        if is_lang_c(language):
            return ["/TC"]
        elif is_lang_cpp(language):
            return ["/TP"]
        else:
            UnsupportedLanguageError(f"Language {language.name} is not supported.")

    def format_object_compilation_args(self, language: LanguageStandard) -> list[str]:
        args = self._format_language_type_args(language)
        args += ["/c", "\"%1\"", "/Fo\"%2\""]
        return args

    def format_debug_info_args(self, output_dir_path: str, output_base_name: str) -> list[str]:
        intermediate_pdb_path = fs.path.join(output_dir_path, f"{output_base_name}-lib.pdb")
        return [
            f"/Fd\"{intermediate_pdb_path}\"",
        ]

    def format_pch_creation_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        return [
            "/c",
            "\"%1\"",  # PCH input file (.cpp)
            "/Fo\"%3\"",  # PCH output library (.lib)
            f"/Yc\"{fs.path.basename(pch_header_path)}\"",
            "/Fp\"%2\""  # PCH output file (compiled .pch)
        ]

    def format_pch_usage_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        return [
            f"/Yu\"{fs.path.basename(pch_header_path)}\"",
            f"/Fp\"{pch_output_path}\"",
        ]

    def format_definition_compiler_arg(self, name: str, value: base.Any) -> str:
        if value is not None:
            return f"/D\"{name}={value}\""
        else:
            return f"/D\"{name}\""

    def format_include_dir_arg(self, include_dir: str) -> str:
        return f"/I\"{include_dir}\""

    def format_system_include_dir_arg(self, include_dir: str) -> str:
        return f"/I\"{include_dir}\""

    @staticmethod
    def format_language_std(std: LanguageStandard) -> list[str]:
        match std:
            case LanguageStandard.C89:
                raise UnsupportedLanguageError("C language standards older than C11 are not supported.")
            case LanguageStandard.C99:
                raise UnsupportedLanguageError("C language standards older than C11 are not supported.")
            case LanguageStandard.C11:
                return ['/std:c11']
            case LanguageStandard.C17:
                return ['/std:c17']
            case LanguageStandard.C23:
                return ['/std:c23']
            case LanguageStandard.C_LATEST:
                return ['/std:clatest']
            case LanguageStandard.CPP03:
                raise UnsupportedLanguageError("C++ language standards older than C++14 are not supported.")
            case LanguageStandard.CPP11:
                raise UnsupportedLanguageError("C++ language standards older than C++14 are not supported.")
            case LanguageStandard.CPP14:
                return ['/std:c++14']
            case LanguageStandard.CPP17:
                return ['/std:c++17']
            case LanguageStandard.CPP20:
                return ['/std:c++20']
            case LanguageStandard.CPP23:
                return ['/std:c++23']
            case LanguageStandard.CPP_LATEST:
                return ['/std:c++latest']
            case _:
                raise UnsupportedLanguageError(f"Unhandled language standard '{std}'.")

    @staticmethod
    def format_language_conformance(lang_conformance: LanguageConformance) -> list[str]:
        match lang_conformance:
            case LanguageConformance.MIN:
                return ["/permissive", "/volatile:ms"]
            case LanguageConformance.MAX:
                return ["/permissive-", "/volatile:iso", "/Zc:preprocessor"]
            case _:
                raise UnsupportedLanguageError(f"Unhandled language conformance option '{lang_conformance}'.")

    @staticmethod
    def _format_warning_level(warning_level: CompilerWarningLevel) -> list[str]:
        match warning_level:
            case CompilerWarningLevel.W0:
                return ["/W0"]
            case CompilerWarningLevel.W1:
                return ["/W1"]
            case CompilerWarningLevel.W2:
                return ["/W2"]
            case CompilerWarningLevel.W3:
                return ["/W3"]
            case CompilerWarningLevel.W4:
                return ["/W4"]
            case CompilerWarningLevel.All:
                return ["/Wall"]
            case _:
                raise UnsupportedSettingError()

    @staticmethod
    def _format_warning_version(ver: str) -> list[str]:
        return [f"/Wv:{ver}"]

    @staticmethod
    def _format_warning_state(warn: str, state: CompilerWarningState) -> list[str]:
        match state:
            case CompilerWarningState.DISABLE:
                return [f"/wd{warn}"]
            case CompilerWarningState.ENABLE:
                return [f"/w1{warn}"]
            case CompilerWarningState.REPORT_ONCE:
                return [f"/wo{warn}"]
            case CompilerWarningState.TREAT_AS_ERROR:
                return [f"/we{warn}"]
            case _:
                raise UnsupportedSettingError()

    @classmethod
    def _is_known_warning(cls, warn: str):
        return warn.isdigit()

    @classmethod
    def _format_warning_states(cls, states: dict[str, CompilerWarningState]) -> list[str]:
        l = []
        for warn, state in states.items():
            if cls._is_known_warning(warn):
                l += cls._format_warning_state(warn, state)
        return l

    @classmethod
    def format_warning_settings(cls, warning_settings: CompilerWarningSettings) -> list[str]:
        l = []
        l += cls._format_warning_level(warning_settings.level)
        l += cls._format_warning_version(warning_settings.version)
        if warning_settings.treat_as_errors:
            l += ["/WX"]
        l += cls._format_warning_states(warning_settings.warning_states)
        l += ['/experimental:external', '/external:anglebrackets', '/external:W0']
        return l

    @staticmethod
    def _format_float_behavior(beh: CompilerFloatBehavior) -> list[str]:
        match beh:
            case CompilerFloatBehavior.PRECISE:
                return ["/fp:precise"]
            case CompilerFloatBehavior.STRICT:
                return ["/fp:strict"]
            case CompilerFloatBehavior.FAST:
                return ["/fp:fast"]
            case _:
                raise UnsupportedSettingError()

    @staticmethod
    def _format_optimization_mode(opt: CompilerOptimizationMode) -> list[str]:
        match opt:
            case CompilerOptimizationMode.NONE:
                return ["/Od"]
            case CompilerOptimizationMode.MINIMIZE_SIZE:
                return ["/O1"]
            case CompilerOptimizationMode.MAXIMIZE_SPEED:
                return ["/O2"]

    @classmethod
    def _format_compiler_settings(cls, settings: CompilerSettings) -> list[str]:
        l = []
        # emit error for unknown arguments
        l += ["/options:strict"]
        l += cls.format_language_std(settings.lang_std)
        l += cls.format_language_conformance(settings.lang_conformance)
        l += cls.format_warning_settings(settings.warning_settings)
        l += ["/GR"] if settings.enable_rtti else ["/GR-"]
        l += ["/EHsc"] if settings.enable_exceptions else ["/EHs-"]
        l += cls._format_float_behavior(settings.float_behavior)
        # require to always define the class before declaring a pointer-to-member
        l += ["/vmb"]
        # when using Unity files the obj size grows quickly
        l += ["/bigobj"]
        l += ["/MDd"] if settings.use_debug_runtime else ["/MD"]
        if settings.enable_debug_info:
            # debug format: PDB
            l += ["/Zi"]
            # faster PDB generation
            l += ["/Zf"]
        # force synchronous PDB writes, since fastbuild uses multiple cl.exe instances.
        l += ["/FS"]
        l += cls._format_optimization_mode(settings.optimization_mode)
        if settings.enable_security_checks:
            # enable buffer security checks
            l += ['/GS']
            l += ['/sdl']
            # enable control flow guards
            l += ['/guard:cf']
            # enable EH continuation metadata(must be also present in linker args)
            l += ['/guard:ehcont']
            # enable all runtime checks.RTCc rejects conformant code, so it is not supported by
            # the C++ Standard Library
            l += ['/RTCsu']
        else:
            # disable buffer security checks
            l += ['/GS-']
            # + '/sdl- ' // it overrides / GS -
            # disable control flow guards
            l += ['/guard:cf-']
            # disable EH continuation metadata
            l += ['/guard:ehcont-']
        return l

    def format_settings_args(self, settings: CompilerSettings) -> list[str]:
        return self._format_compiler_settings(settings)


class CompilerArgFormatterClangCL(CompilerArgFormatterMSVC):
    pass
