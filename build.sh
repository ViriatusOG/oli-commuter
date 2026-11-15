#!/usr/bin/env bash
# Build the debug APK for Oli Commuter.
#
#   ./build.sh                 -> build/Oli-Commuter-debug.apk
#   ./build.sh assembleRelease -> any other Gradle task, with the same toolchain
#
# Needs a JDK 21 and an Android SDK with platform 36. By default it looks for
# them in ../.android-tooling (next to this repository); override with
# JAVA_HOME and ANDROID_HOME, or point ANDROID_TOOLING at wherever they live.
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"

TOOL="${ANDROID_TOOLING:-$REPO/../.android-tooling}"

if [ -d "$TOOL/jdk21" ] || [ -d "$TOOL/sdk" ]; then
  # Everything the build writes — Gradle's caches, the SDK's state, npm's cache,
  # the debug keystore — stays inside $TOOL. Nothing outside it is touched.
  for jdk in jdk21 jdk17; do [ -x "$TOOL/$jdk/bin/javac" ] && { export JAVA_HOME="${JAVA_HOME:-$TOOL/$jdk}"; break; }; done
  export ANDROID_HOME="${ANDROID_HOME:-$TOOL/sdk}"
  export ANDROID_USER_HOME="${ANDROID_USER_HOME:-$TOOL/android-home}"
  export GRADLE_USER_HOME="${GRADLE_USER_HOME:-$TOOL/gradle-home}"
  export npm_config_cache="${npm_config_cache:-$TOOL/npm-cache}"
  mkdir -p "$TOOL/home"
  export HOME="$TOOL/home"
elif [ -z "${JAVA_HOME:-}" ] || [ -z "${ANDROID_HOME:-}" ]; then
  echo "No toolchain at $TOOL." >&2
  echo "Set JAVA_HOME and ANDROID_HOME, or ANDROID_TOOLING to a folder holding jdk21/ and sdk/." >&2
  exit 1
fi
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export PATH="${JAVA_HOME:+$JAVA_HOME/bin:}$PATH"
[ -f android/local.properties ] || { mkdir -p android && printf 'sdk.dir=%s\n' "$ANDROID_HOME" > android/local.properties; }
[ -d node_modules/@capacitor/android ] || npm install

echo "==> web bundle -> android/app/src/main/assets/public"
npx cap sync android

echo "==> gradle ${1:-assembleDebug}"
( cd android && ./gradlew --no-daemon "${@:-assembleDebug}" )

for variant in debug release; do
  out="android/app/build/outputs/apk/$variant/app-$variant.apk"
  [ -f "$out" ] || continue
  mkdir -p build
  name="Oli-Commuter-$variant.apk"
  cp "$out" "build/$name"
  echo
  echo "==> build/$name"
  ls -lh "build/$name"
done
