param($network)

function Validate-Params {
    if (!$network) {
        Write-Host "Missing <network> parameter"
        exit
    }

    if (!($network -match "^\d{1,3}\.\d{1,3}\.\d{1,3}$")) {
        Write-Host "Invalid <network> format"
        exit
    }
}

function Scan-Network {
    foreach ($i in 0..254) {
        $h = "$network.$i"
        $output=$(ping -n 1 -l 1 -w 2000 $h | Select-String "bytes=1")
        if (!!$output) {
            $found=$output -match 'time.\d{1,6}ms'
            $found=$matches[0] -match '\d{1,6}ms'
            $duration=$matches[0]
            Write-Host "$h time=$duration"
        }
    }
}

Validate-Params
Scan-Network
