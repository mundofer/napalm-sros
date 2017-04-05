# Interface values
Value Required name (\S+)
Value ipv4 ([0-9]*.[0-9]*.[0-9]*.[0-9]*)
Value ipv4mask ([0-9]*)
Value List ipv6 ([0-9a-fA-F]*:[0-9a-fA-F:]*)
Value List ipv6mask ([0-9]*)
Value port (\S+)

# Start of parse
Start
  # Record current values and change state.
  ^-* -> Int

  # reading values
Int
  ^\S+ -> Continue.Record
  ^${name}\s+(Up|Down)\s+(Up/Down|Up/Up|Down/Down)\s+(Network|Access)\s+${port}
  ^   ${ipv6}/${ipv6mask}\s+\S+
  ^   ${ipv4}/${ipv4mask}\s+\S+
