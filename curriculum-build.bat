@echo off
rem Build an iSAQB curriculum via the prebuilt builder image. Renders into .\build.
rem   curriculum-build.bat              all languages x formats
rem   curriculum-build.bat pdf DE       single format + language
rem   curriculum-build.bat pdf DE REMARKS
setlocal

set "IMAGE=ghcr.io/isaqb-org/curriculum-builder:2026.3-rev1"
set "DIGEST=sha256:6f0899bca1d2c8730803703c3b6f1f205f250d087b33cf0df5e344d0fcc1ab00"

set "REF=%IMAGE%"
if defined DIGEST set "REF=%IMAGE%@%DIGEST%"

set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

rem build.config is read inside the container from /project; only forward host overrides.
set "ENVOPTS="
if defined CURRICULUM_FILE set "ENVOPTS=%ENVOPTS% -e CURRICULUM_FILE=%CURRICULUM_FILE%"
if defined LANGUAGES       set "ENVOPTS=%ENVOPTS% -e LANGUAGES=%LANGUAGES%"
if defined SUFFIX_TAGS      set "ENVOPTS=%ENVOPTS% -e SUFFIX_TAGS=%SUFFIX_TAGS%"
if defined PREPRESS         set "ENVOPTS=%ENVOPTS% -e PREPRESS=%PREPRESS%"
if not defined RELEASE_VERSION set "RELEASE_VERSION=LocalBuild"

docker pull "%REF%" >nul || exit /b 1

docker run --rm ^
  -v "%REPO_ROOT%:/project" ^
  -w /project ^
  %ENVOPTS% ^
  -e "RELEASE_VERSION=%RELEASE_VERSION%" ^
  "%REF%" %*
if errorlevel 1 exit /b 1

echo Done. Output in %REPO_ROOT%\build\
endlocal
