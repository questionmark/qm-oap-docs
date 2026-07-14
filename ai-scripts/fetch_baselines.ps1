<#
.SYNOPSIS
    Capture live OData $metadata (CSDL/EDMX) baselines for the three OAP services.

.DESCRIPTION
    Downloads $metadata for Delivery (v3), Authoring (v4) and Results (v3) into
    ignore/metadata-baselines/ as <service>.<yyyy-MM-dd>.metadata.xml. These files
    are the machine-readable source of truth consumed by reconcile_odata.py.

    ignore/ is outside src/ so the baselines are never picked up by the Sphinx build.

    Requires PowerShell 7+ (pwsh).

.PARAMETER Tenant
    Tenant id used in the service URLs. Defaults to 406611.

.PARAMETER OutDir
    Output directory. Defaults to ignore/metadata-baselines (relative to repo root).

.EXAMPLE
    pwsh ai-scripts/fetch_baselines.ps1
    pwsh ai-scripts/fetch_baselines.ps1 -Tenant 406611
#>
param(
    [string]${Tenant} = "406611",
    [string]${OutDir} = ".\ignore\metadata-baselines"
)

Set-StrictMode -Version Latest
${ErrorActionPreference} = "Stop"

# service -> $metadata URL. Note the differing path shapes per service:
#   delivery  : /deliveryodata/<tenant>/$metadata
#   authoring : /authoringapi/<tenant>/odata/$metadata
#   results   : /analyticsodata/<tenant>/odata/$metadata   (docs redirect to Help)
${base} = "https://ondemand.questionmark.com"
${services} = @{
    delivery  = "${base}/deliveryodata/${Tenant}/`$metadata"
    authoring = "${base}/authoringapi/${Tenant}/odata/`$metadata"
    results   = "${base}/analyticsodata/${Tenant}/odata/`$metadata"
}

New-Item -ItemType Directory -Force -Path ${OutDir} | Out-Null
${date} = Get-Date -Format "yyyy-MM-dd"

foreach (${name} in ${services}.Keys) {
    ${url} = ${services}[${name}]
    ${out} = Join-Path ${OutDir} "${name}.${date}.metadata.xml"
    try {
        Invoke-WebRequest -Uri ${url} -OutFile ${out} -UseBasicParsing
        ${size} = (Get-Item ${out}).Length
        Write-Host "OK   ${name} -> ${out} (${size} bytes)"
    }
    catch {
        Write-Host "FAIL ${name} : $(${_}.Exception.Message)"
    }
}
