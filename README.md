# NAPALM-SROS

A SROS (Nokia, ex ALU) NAPALM driver.

## Installation

TODO: Describe the installation process

## Usage

This driver tries to use netconf when possible (ncclient library) and if the function can't be implemented with netconf, revert back to ssh (netmiko library).

You must configured the following in your SR 7750 router (version 14.0 or later):
```
    system
        security
            user "xxx"
                password "yyyy"
                access console netconf
    system
        netconf
            no shutdown
        exit
        ssh
        exit
```

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