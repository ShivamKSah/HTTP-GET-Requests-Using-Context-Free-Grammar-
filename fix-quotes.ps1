# PowerShell script to fix escaped quotes in React component files

$frontendPath = ".\frontend\src"
$filesToFix = @(
    "components\AIAssistant.tsx",
    "components\NotificationContainer.tsx", 
    "components\ParseTreeVisualization.tsx",
    "components\ValidationForm.tsx",
    "pages\DashboardPage.tsx",
    "pages\ErrorsPage.tsx",
    "pages\GrammarPage.tsx",
    "pages\LandingPage.tsx",
    "pages\LibraryPage.tsx",
    "pages\ValidatorPage.tsx",
    "contexts\APIContext.tsx",
    "contexts\NotificationContext.tsx"
)

Write-Host "Fixing escape character issues in React components..."

foreach ($file in $filesToFix) {
    $filePath = Join-Path $frontendPath $file
    if (Test-Path $filePath) {
        Write-Host "Processing: $file"
        
        # Read the file content
        $content = Get-Content $filePath -Raw
        
        # Replace escaped quotes with regular quotes
        $content = $content -replace 'className=\\"', 'className="'
        $content = $content -replace '\\">', '">'
        $content = $content -replace '\\"', '"'
        
        # Write back to file
        Set-Content -Path $filePath -Value $content -NoNewline
        
        Write-Host "Fixed: $file"
    } else {
        Write-Host "File not found: $file"
    }
}

Write-Host "All files processed!"