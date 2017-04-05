# traceroute values
Value List hop (\d*)
Value List ip ([0-9]*.[0-9]*.[0-9]*.[0-9]*)
Value List name (\S*)
Value List rtt1 ([0-9]*\.?[0-9]+)
Value List rtt2 ([0-9]*\.?[0-9]+)
Value List rtt3 ([0-9]*\.?[0-9]+)
Value error-text (\.*)

# start of parse
Start
  ^traceroute -> Record Traceroute

#reading values
Traceroute
  ^\s+${hop}\s+${name}\s+\(${ip}\)\s+${rtt1} ms\s+${rtt2} ms\s+${rtt3} ms
