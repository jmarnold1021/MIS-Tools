# not sure what exact version of .NET this powershell uses
#https://learn.microsoft.com/en-us/dotnet/api/microsoft.sqlserver.management.smo.scriptingoptions?view=sql-smo-160

#param (
#    #[string]$price = 100,
#    [string]$Report
#    #[string]$username = $(throw "-username is required."),
#    #[string]$password = $( Read-Host -asSecureString "Input password" ),
#    #[switch]$SaveData = $false
#)

# seems once the .NET object code is loaded can begin sourcing it...
[System.Reflection.Assembly]::LoadWithPartialName( 'Microsoft.SqlServer.SMO' ) | out-null
[System.Reflection.Assembly]::LoadWithPartialName( 'System.IO.Compression.FileSystem' ) | out-null

$PACKAGE_ROOT = $PSScriptRoot + '\..'
cd $PACKAGE_ROOT

$log_file = "$PACKAGE_ROOT/mistools/logs/mis_rpt_backup.log"

# db server instance..
$serv = new-object ('Microsoft.SqlServer.Management.Smo.Server') "ltcc-db"

# db instance..
$db = $serv.Databases["coll18_production"]

$bdate = Get-Date -Format "yyMMdd"
$bpath = "\\ltcc-app\MIS\MIS_SQL_Backups\mis_rpt_bac_" + $bdate

New-Item -Path $bpath -ItemType Directory | out-null

Write-Output "Starting backup on " + $bdate > $log_file
foreach ( $tables in $db.Tables ) {

    if ( ($tables.Name.StartsWith('CAST') -or $tables.Name.StartsWith("CAHR")) -and $tables.Name.EndsWith("RPT") )
    {

        # if ($Report -ne '' -and $Report  # new need

        $options = new-object ('Microsoft.SqlServer.Management.Smo.ScriptingOptions')
        $options.FileName = $bpath + "\dbo.{0}.Table.sql" -f $tables.Name
        $options.ScriptDrops  = $true
        $options.AnsiFile     = $true
        $options.NoCollation  = $true
        $options.ToFileOnly = $true
        Write-Output ("Writing Drops {0}" -f $tables.Name) >> $log_file
        $tables.EnumScript($options)# | out-null

        $options.ScriptDrops        = $false
        $options.AppendToFile       = $true
        $options.IncludeIfNotExists = $true
        $options.ScriptSchema       = $true
        $options.Indexes            = $true
        Write-Output ("Writing Schemas {0}" -f $tables.Name) >> $log_file
        $tables.EnumScript($options) | out-null

        # once append file has been set I guess can't just turn off from old path name. unless .FileName is appending paths or someting odd.
        $options = new-object ('Microsoft.SqlServer.Management.Smo.ScriptingOptions')
        $options.FileName = $bpath + "\dbo.{0}.Data.sql" -f $tables.Name
        $options.IncludeIfNotExists = $false
        $options.ScriptSchema       = $false
        $options.ScriptData         = $true
        Write-Output ("Writing Data {0}" -f $tables.Name) >> $log_file
        $tables.EnumScript($options) | out-null

    }
}

$bzip = "\\ltcc-app\MIS\MIS_SQL_Backups\mis_rpt_bac_" + $bdate + ".zip"

Write-Output ("Archiving Data {0} to {1}" -f $bpath, $bzip) >> $log_file
[System.IO.Compression.ZipFile]::CreateFromDirectory($bpath, $bzip)

Remove-Item $bpath -Recurse

exit 0