# NAPALM-SROS

A SROS (Nokia, ex ALU) NAPALM driver.

## Installation

TODO: Describe the installation process

## Usage

This driver prevously used netconf calls when possible (ncclient library) and if the function couldn't be implemented with netconf, it reverted back to ssh (netmiko library).

However I'm having many problems with the netconf calls (router problems, no library problems) so I reverted to do everything using netmiko.

You must configured the following in your SR 7750 router (version 14.0 or later):
```
    system
        security
            user "xxx"
                password "yyyy"
                access console
    system
        ssh
        exit
```

## Things that work:
- open
- close
- get_facts
- ping
- traceroute
- get_config (running and startup)
- get_interfaces
- get_interfaces_ip
- get_ports (not a standard NAPALM call. Implemented here due to the SR7750 way of configure)
- cli
- is_alive

## Things that don't work:

All the other NAPALM calls:
- _lock
- _unlock
- _load_candidate
- load_replace_candidate
- load_merge_candidate
- compare_config
- commit_config
- discard_config
- rollback

A lot of error checking must be done

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

The first version.

## Credits

- Original author: Fernando Garcia
- Using templates from: David Barroso

## License

Apache 2.0 (see LICENSE file)