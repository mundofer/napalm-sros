# ping values
Value probes_sent (\d*)
Value packets_received (\d*)
Value rtt_min ([0-9]*\.?[0-9]+)
Value rtt_max ([0-9]*\.?[0-9]+)
Value rtt_avg ([0-9]*\.?[0-9]+)
Value rtt_stddev ([0-9]*\.?[0-9]+)
Value List ip ([0-9]*.[0-9]*.[0-9]*.[0-9]*)
Value List rtt ([0-9]*\.?[0-9]+)
Value error-text (\.*)

# start of parse
Start
  ^PING -> Record Ping

#reading values
Ping
  ^\d* bytes from ${ip}: icmp_seq=\d* ttl=\d* time=${rtt}ms.
  ^${probes_sent} packets transmitted, ${packets_received} packets received, \S* packet loss
  ^round-trip min = ${rtt_min}ms, avg = ${rtt_avg}ms, max = ${rtt_max}ms, stddev = ${rtt_stddev}ms -> Start
