$categories = @(
    @{ id="networking"; title="Networking"; icon="fas fa-network-wired"; desc="IP Addressing, DNS, DHCP, VLANs, Wi-Fi, VPN & Troubleshooting." }
    @{ id="windows"; title="Windows"; icon="fab fa-windows"; desc="CMD, PowerShell, Windows Administration & Troubleshooting." }
    @{ id="linux"; title="Linux"; icon="fab fa-linux"; desc="Essential Commands, Filesystem, Permissions & Shell Scripting." }
    @{ id="servers"; title="Servers"; icon="fas fa-server"; desc="Windows Server, Linux Server, Active Directory & Virtualization." }
    @{ id="cybersecurity"; title="Cybersecurity"; icon="fas fa-shield-alt"; desc="Firewalls, MFA, Phishing, Malware & Security Best Practices." }
    @{ id="cloud"; title="Cloud & AI"; icon="fas fa-cloud"; desc="AWS, Azure, Cloud Services, AI Tools & Modern IT Concepts." }
)

foreach ($cat in $categories) {
    $content = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$($cat.title) | MJ Tech Hub</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="css/themes.css">
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/responsive.css">
    <script src="js/theme.js"></script>
    <script src="js/main.js" defer></script>
</head>
<body>
    <main class="container py-4">
        <div style="margin-bottom: 2rem;">
            <a href="topics.html" style="color: var(--text-secondary); font-size: 0.85rem;"><i class="fas fa-arrow-left"></i> Back to Topics</a>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <i class="$($cat.icon)" style="font-size: 2.5rem; color: var(--brand-primary);"></i>
            <h1 style="font-size: 2.5rem; margin: 0; color: var(--text-primary);">$($cat.title)</h1>
        </div>
        <p style="color: var(--text-secondary); font-size: 1.1rem; max-width: 800px; margin-bottom: 3rem;">
            $($cat.desc)
        </p>
        
        <h2 class="section-title">| LEARNING PATH</h2>
        <div class="card" style="padding: 2rem; text-align: center; color: var(--text-muted);">
            <i class="fas fa-tools" style="font-size: 2rem; margin-bottom: 1rem;"></i>
            <h3>Curriculum coming soon</h3>
            <p>We are currently structuring the tutorials and content paths for this topic. Check back soon!</p>
        </div>
    </main>
</body>
</html>
"@
    $filename = "$($cat.id).html"
    Set-Content -Path $filename -Value $content
}

Write-Host "Generated category pages."
