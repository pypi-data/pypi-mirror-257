# Documentation of relay board py
This is the actual documentation of the package and the relay board.

1. [Purpose](#purpose)
    * [Applications](#applications)
    * [Relay board](#relay-board)
2. [Specification](#specification)
    * [Naming](#naming)
    * [Characteristics](#characteristics)
2. [Package installation](#package-installation)
3. [Package usage](#package-usage)
    * [Arguments](#arguments)
    * [Pattern-files](#pattern-files)
4. [Use-cases](#use-cases)
    * [Switch programmer](#switch-programmer)
    * [Switch target](#switch-target)
    * [Adapters](#adapters)
        * [Adapter TC2050-430](#adapter-tc2050-430)
        * [Adapter J-Link](#adapter-j-link)
        * [Adapter ST-Link](#adapter-st-link)
        * [Adapter Generic](#adapter-generic)
    * [Example connection](#example-connection)

<a id="purpose"></a>
## Purpose
When developing an embedded device, there is often the challenge to program a device and
disconnect the programmer after programming, to not disturb the device
(low-power states, power-consumption, etc.).

The relay board is a tool to provide **galvanic isolation** between multiple devices
(e.g. a programmer and a device).
The relay board (which has a unique serial number) is connected via USB to a host PC
and controlled by a python package/API.

Each relay of the relay board switches signals from the common port
to the normally opened or the normally closed port.
The relays of the board can be controlled **individually**.

Another use-case of the relay board is to minimize the number of (potentially expensive)
programmers in the setup.
A single programmer can be used to program two devices by switching the ports.
Relay boards can even be **cascaded**, to enable the connection of more devices.

The relay board cannot only be used during development, but also as **generic** multi-pin switcher,
e.g. during production, testing, measurements etc.

<a id="applications"></a>
### Applications
- galvanic isolation between ports
- cost savings (by only having one programmer for multiple devices)
- cascading of relay boards
- ...

<a id="relay-board"></a>
### Relay board
Relay board **RB-1-10**:

<img src="img/RB_1_10_00.jpg" width="500"/>

<a id="specification"></a>
## Specification

<a id="naming"></a>
### Naming

| Name   |  Description                                                        |
| :---   | :------------------------------------------------------------------ |
| COM    | The common port of a relay                                          |
| NC     | The normally connected port of a relay (connected if relay is open) |
| NO     | The normally opened port of a relay (connected if relay is closed)  |
| Target | The device to be programmed, analyzed, debugged, ...                |

<a id="characteristics"></a>
### Characteristics
Characteristiscs of **RB-1-10**:

| Property                                         | Value |
| :----------------------------------------------- | :---- |
| Number of individually switchable pins COM/NO/NC | 10    |
| Maximum voltage per pin                          | 60 V  |
| Maximum current per pin                          | 2 A   |

<a id="package-installation"></a>
## Package installation
Install the `relay_board_py` package via `pip`:
```bash
python3 -m pip install relay_board_py
```

TODO: Using pipenv! With Link

<a id="package-usage"></a>
## Package usage
1. Execute package directly as module:
```bash
python3 -m relay_board_py -s RB90FJ7SIHYU1F -c 1,7 -o 2 -r
```

2. Integrate into own python module:
```python
from relay_board_py.relay_board import RelayBoard

RelayBoard.main(['-s', 'RB90FJ7SIHYU1F', '-c', '1,7', '-o', '2', '-r'])
```

<a id="arguments"></a>
### Arguments
```bash
    -h, --help          show this help message and exit
    -s SERIAL_NUMBER    Serial-number in single operation mode
    -o OPEN             Specify relay ids to be opened "-o 1,2,3"
    -c CLOSE            Specify relay ids to be closed "-c 1,2,3"
    -f FILE             File path to json file containing the patterns
    -p PATTERN          Pattern to be used in provided json file
    -r                  Reset relay-board(s) first, before executing the operations
    -i                  Print info about relay-board(s)
```

Relay boards can be controlled:
- by serial-number (arguments: -s, -o, -c)
- by json pattern file (argumments: -f, -p)

<a id="pattern-files"></a>
### Pattern files
For more complex relay board control, json "pattern" files can be defined:
```json
{
    "aliases": {
        "A1": "RB90FJ7SIHYU1F",
        "A2": "RB9ZIRP7TWC305"
    },
    "patterns": {
        "P1": {
            "A1": {
                "open": [1],
                "close": [2]
            },
            "A2": {
                "open": [3],
                "close": [4]
            }
        },
        "P2": {
            "A1": {
                "open": [10],
                "close": [1, 2]
            }
        }
    }
}
```

**aliases**:
Creates an alias name for each relay board serial number to be used.
The alias can be **any** string.

**patterns**:
Creates one or multiple patterns. The pattern name can be **any** string you want.
Inside a pattern, add all relay board aliases to be used for **this** pattern.
Finally, define for each alias the state (close, open) as list of relay ids of the relay board.

The pattern file can be executed the following way:
```bash
python -m relay_board_py -f example_pattern.json -p P2 -r
```

<a id="use-cases"></a>
## Use-cases
<a id="switch-programmer"></a>
### Switch programmer
A single programmer (e.g. a J-Link) can be switched between multiple targets.

After power up, all relays are switched from **COM**-port to **NC**-port (NC = normally connected):
<img src="img/RB_1_10_COM_programmer_NC.svg" width="800"/>

All relays can be switched from **COM**-port to **NO**-port (NO = normally opened):

<img src="img/RB_1_10_COM_programmer_NO.svg" width="800"/>

And **each** relay/pin can be also switched **individually**:

<img src="img/RB_1_10_COM_programmer_NO_NC.svg" width="800"/>

<a id="switch-target"></a>
### Switch target
The pins of a target can be switched between multiple devices (programmer, power supply, etc.).

All connected pins of a target can be swtiched individually to fulfill different purposes:

<img src="img/RB_1_10_COM_target_NO_NC.svg" width="800"/>


<a id="adapters"></a>
### Adapters
There are multiple adapters available to enable easy connection to the relay board.

<a id="adapter-tc2050-430"></a>
#### Adapter TC2050-430
This is a generic adapter between [TC2050-IDC-430](https://www.tag-connect.com/product/tc2050-idc-430-legged-cable-for-use-with-msp430-fet430)
(14 pins) to [TC2050-IDC](https://www.tag-connect.com/product/tc2050-idc-tag-connect-2050-idc) (10 pins).

<img src="img/Adapter_TC2050_430_A.jpg" height="150"/> <img src="img/Adapter_TC2050_430_B.jpg" height="150"/>

<a id="adapter-j-link"></a>
#### Adapter J-Link
This is an adapter between J-Link (20 pins) to 10 pins (e.g. for TC2050-IDC).

<img src="img/Adapter_J_LINK_A.jpg" height="150"/> <img src="img/Adapter_J_LINK_B.jpg" height="150"/>

<a id="adapter-st-link"></a>
#### Adapter ST-Link
This is an adapter between ST-Link (20 pins) to 10 pins (e.g. for TC2050-IDC).

<img src="img/Adapter_ST_LINK_A.jpg" height="150"/> <img src="img/Adapter_ST_LINK_B.jpg" height="150"/>

<a id="adapter-generic"></a>
#### Adapter Generic
This is a generic 10 pins adapter. Can be used for custom adapters (e.g. just use 6 pins).

<img src="img/Adapter_Generic_A.jpg" height="150"/> <img src="img/Adapter_Generic_B.jpg" height="150"/>
<img src="img/Adapter_Generic_C.jpg" height="150"/>


<a id="example-connection"></a>
### Example connection

Relay board with certain pattern:

<img src="img/RB_1_10_00_pattern.jpg" width="500"/>

Relay board with connected accessories:

<img src="img/RB_1_10_00_connected.jpg" width="700"/>
