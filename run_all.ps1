$ErrorActionPreference = "SilentlyContinue"
Set-StrictMode -Version Latest

# Ensure we run from this script's directory
if ($PSScriptRoot) { Set-Location $PSScriptRoot }

$outDir = Join-Path (Get-Location) "out"
if (Test-Path $outDir) { Remove-Item -Recurse -Force $outDir }
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

Write-Host "Running AI Security Hackathon demos..." -ForegroundColor Cyan

# 1) Reconnaissance
Write-Host "[1/6] Recon: recon_ai.py" -ForegroundColor Yellow
& python recon_ai.py 2>&1 | Out-File -FilePath (Join-Path $outDir "recon.txt") -Encoding utf8

# 2) Exploitation (mock) - SQLi/XSS/SSTI
Write-Host "[2/6] Exploit: exploit_ai.py (SQLi/XSS/SSTI, mock)" -ForegroundColor Yellow
$env:MOCK_EXPLOIT = "1"
foreach ($t in @("SQLI", "XSS", "SSTI")) {
    $env:ATTACK_TYPE = $t
    & python exploit_ai.py 2>&1 | Out-File -FilePath (Join-Path $outDir ("exploit_" + $t.ToLower() + ".txt")) -Encoding utf8
}
$env:MOCK_EXPLOIT = $null
$env:ATTACK_TYPE = $null

# 3) Attack chain + Mermaid export (PNG if mmdc is available)
Write-Host "[3/6] Attack chain: attack_chain_sim.py (+ Mermaid)" -ForegroundColor Yellow
$env:WRITE_MERMAID = "1"
$env:EXPORT_PNG = "1"
& python attack_chain_sim.py 2>&1 | Out-File -FilePath (Join-Path $outDir "attack_chain.txt") -Encoding utf8
$env:WRITE_MERMAID = $null
$env:EXPORT_PNG = $null

if (Test-Path "attack_chain.mmd") { Copy-Item -Force "attack_chain.mmd" (Join-Path $outDir "attack_chain.mmd") }
if (Test-Path "attack_chain.png") { Copy-Item -Force "attack_chain.png" (Join-Path $outDir "attack_chain.png") }

# 4) Defense: entropy
Write-Host "[4/6] Defense: defense_anomaly.py" -ForegroundColor Yellow
& python defense_anomaly.py 2>&1 | Out-File -FilePath (Join-Path $outDir "defense_anomaly.txt") -Encoding utf8

# 5) Attacks demo (consolidated)
Write-Host "[5/6] Attacks demo: ai_attacks_demo.py" -ForegroundColor Yellow
& python ai_attacks_demo.py 2>&1 | Out-File -FilePath (Join-Path $outDir "attacks_demo.txt") -Encoding utf8

# 6) Environment info (optional)
Write-Host "[6/6] Environment info" -ForegroundColor Yellow
& python --version 2>&1 | Out-File -FilePath (Join-Path $outDir "env_python.txt") -Encoding utf8
& pip --version 2>&1 | Out-File -FilePath (Join-Path $outDir "env_pip.txt") -Encoding utf8

Write-Host "All done. Artifacts in 'out' folder:" -ForegroundColor Green
Get-ChildItem $outDir | Select-Object Name, Length


