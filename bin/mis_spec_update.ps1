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

$log_file = "$PACKAGE_ROOT/mistools/logs/mis_rpt_spec_refresh.log"

# db server instance..
$serv = new-object ('Microsoft.SqlServer.Management.Smo.Server') "ltcc-db"

# db instance..
$db = $serv.Databases["coll18_production"]

$bpath = "$PACKAGE_ROOT/mistools/schema/"

Write-Output ("Starting backup on {0}" -f $bdate) > $log_file

foreach ( $tables in $db.Tables ) {

    if ( ($tables.Name.StartsWith('CAST') -or $tables.Name.StartsWith("CAHR")) -and $tables.Name.EndsWith("RPT") )
    {

        $options = new-object ('Microsoft.SqlServer.Management.Smo.ScriptingOptions')
        $options.FileName = ("{0}dbo.{1}.Table.sql" -f $bpath, $tables.Name)
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

    }
}

# db server instance..
$serv = new-object ('Microsoft.SqlServer.Management.Smo.Server') "ltcc-ods"

# db instance..
$db = $serv.Databases["ODS_production"]

foreach ( $tables in $db.Tables ) {

    if ( $tables.Name.StartsWith('L56_DOD') -or $tables.Name.StartsWith("L56_COCI") -or $tables.Name.StartsWith("L56_DOD_IPEDS"))
    {

        $options = new-object ('Microsoft.SqlServer.Management.Smo.ScriptingOptions')
        $options.FileName = ("{0}dbo.{1}.Table.sql" -f $bpath, $tables.Name)
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

    }

    if ( $tables.Name.StartsWith('L56_NscDetailFileStage') )
    {
        $options = new-object ('Microsoft.SqlServer.Management.Smo.ScriptingOptions')
        $options.FileName = ("{0}dbo.{1}.Table.sql" -f $bpath, $tables.Name)
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
    }
}

exit 0
