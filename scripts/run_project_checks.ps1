param(
    [string]$Project = "projects/office-comedy-test",
    [string]$Episode = "ep01",
    [string]$TaskType = "",
    [string]$Stage = "current",
    [switch]$RequirePromptReview
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function Test-PythonCandidate {
    param([string]$Candidate)

    try {
        $output = & $Candidate -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $output) {
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

function Resolve-Python {
    $candidates = @()
    if ($env:PYTHON) {
        $candidates += $env:PYTHON
    }

    $candidates += @(
        "python",
        "python3"
    )

    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-PythonCandidate $candidate)) {
            return $candidate
        }
    }

    throw "No usable Python was found. Set PYTHON to a valid interpreter path."
}

function Invoke-CheckedCommand {
    param(
        [string]$Python,
        [string[]]$Arguments
    )

    Write-Host ""
    Write-Host ">> $Python $($Arguments -join ' ')"
    & $Python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE"
    }
}

Push-Location $RepoRoot
try {
    $python = Resolve-Python
    Write-Host "Using Python: $python"

    Invoke-CheckedCommand $python @("scripts/validate_all.py", $Project)

    if ($TaskType) {
        $readinessArgs = @("scripts/check_generation_readiness.py", $Project, "--episode", $Episode, "--task-type", $TaskType)
        if ($RequirePromptReview) {
            $readinessArgs += "--require-prompt-review"
        }
        Invoke-CheckedCommand $python $readinessArgs
    }

    Invoke-CheckedCommand $python @("scripts/generate_gate_report.py", $Project, "--episode", $Episode, "--stage", $Stage)
}
finally {
    Pop-Location
}
