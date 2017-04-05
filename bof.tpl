# Bof values
Value Required primaryimage (\S+)
Value primaryconfig (\S+)
Value licensefile (\S+)
Value primarydns ([0-9]*.[0-9]*.[0-9]*.[0-9]*)
Value dnsdomain (\S+)
Value autonegotiate (\S+)
Value duplex (\S+)
Value speed (\S+)
Value wait (\S+)
Value persist (\S+)
Value lilocalsave (\S+)
Value liseparate (\S+)
Value fips1402 (\S+)
Value consolespeed ([0-9]*)

# Start of parse
Start
  # Record current values .
  ^BOF -> Record Bof

# reading values
Bof
  ^\s+primary-image\s+${primaryimage}
  ^\s+primary-config\s+${primaryconfig}
  ^\s+license-file\s+${licensefile}
  ^\s+primary-dns\s+${primarydns}
  ^\s+dns-domain\s+${dnsdomain}
  ^\s+autonegotiate\s+${autonegotiate}
  ^\s+duplex\s+${duplex}
  ^\s+speed\s+${speed}
  ^\s+wait\s+${wait}
  ^\s+persist\s+${persist}
  ^\s+no li-local-save\s+${lilocalsave}
  ^\s+no li-separate\s+${liseparate}
  ^\s+no fips-140-2\s+${fips1402}
  ^\s+console-speed\s+${consolespeed} -> Start
