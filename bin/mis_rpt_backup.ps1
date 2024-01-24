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
# this will also throw an odd syntax error...I looked into it a bit here...
# https://stackoverflow.com/questions/9929452/in-powershell-object-not-loading-though-i-call-loadwithpartialname
# looks like the final comment refers to a new shell which is how I was fixing it. The failed backups were due to out of date configs.
[System.Reflection.Assembly]::LoadWithPartialName( 'Microsoft.SqlServer.SMO' ) | out-null
[System.Reflection.Assembly]::LoadWithPartialName( 'System.IO.Compression.FileSystem' ) | out-null

Write-Output ($USERPROFILE)

$PACKAGE_ROOT = $PSScriptRoot + '\..'
#$CONFIG_ROOT  = $env:USERPROFILE + '\Documents\MIS-Tools\configs.json' -- this should happen since it is what caused the backups to fail.
cd $PACKAGE_ROOT

$RETENTION_DAYS = 60

$log_file = "$PACKAGE_ROOT/mistools/logs/mis_rpt_backup.log"

# db server instance..
$serv = new-object ('Microsoft.SqlServer.Management.Smo.Server') "ltcc-db23"

# db instance..
$db = $serv.Databases["coll18_prod"]

$bdate = Get-Date -Format "yyMMdd"
$bpath = "\\ltcc-app23\MIS\MIS_SQL_Backups\mis_rpt_bac_"

New-Item -Path ($bpath + $bdate) -ItemType Directory | out-null

Write-Output ("Starting backup on {0}" -f $bdate) > $log_file
foreach ( $tables in $db.Tables ) {

    if ( ($tables.Name.StartsWith('CAST') -or $tables.Name.StartsWith("CAHR")) -and $tables.Name.EndsWith("RPT") )
    {

        $options = new-object ('Microsoft.SqlServer.Management.Smo.ScriptingOptions')
        $options.FileName = ("{0}{1}\dbo.{2}.Table.sql" -f $bpath,$bdate,$tables.Name)
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
        $options.DriDefaults        = $true
        $options.Indexes            = $true
        Write-Output ("Writing Schemas {0}" -f $tables.Name) >> $log_file
        $tables.EnumScript($options) | out-null

        # once append file has been set I guess can't just turn off from old path name. unless .FileName is appending paths or someting odd.
        $options = new-object ('Microsoft.SqlServer.Management.Smo.ScriptingOptions')
        $options.FileName = ("{0}{1}\dbo.{2}.Data.sql" -f $bpath,$bdate,$tables.Name)
        $options.IncludeIfNotExists = $false
        $options.ScriptSchema       = $false
        $options.DriDefaults        = $false
        $options.ScriptData         = $true
        Write-Output ("Writing Data {0}" -f $tables.Name) >> $log_file
        $tables.EnumScript($options) | out-null

    }
}

$bzip = $bpath + $bdate + ".zip"

Write-Output ("Archiving Data {0}{1} to {2}" -f $bpath,$bdate,$bzip) >> $log_file
[System.IO.Compression.ZipFile]::CreateFromDirectory(($bpath+ $bdate), $bzip) # the powershell compress has soe odd status banner...so use .NET one from FileSystem

Remove-Item ($bpath + $bdate) -Recurse


Write-Output ("Cleaning Backups older than {0} days" -f $RETENTION_DAYS) >> $log_file
Get-ChildItem -Path ($bpath + "*.zip")  | Where-Object {($_.LastWriteTime -lt (Get-Date).AddDays(-$RETENTION_DAYS))} | Remove-Item

exit 0
