$ErrorActionPreference = "Continue"

npm run lint
$lintExit = $LASTEXITCODE

npm run test:unit -- --watch=false
$testExit = $LASTEXITCODE

if ($lintExit -ne 0 -or $testExit -ne 0) {
  exit 1
}

exit 0
