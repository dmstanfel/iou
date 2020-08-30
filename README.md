# iou

`iou` is a script for calculating how utilities payments should be redistributed amongst a group of roommates. Instead of requesting each other back and forth on venmo, this script can be used to reduce the number of transactions.

## Installation

`iou` does not have any third party dependencies. All you need is a Python 3 interpreter. For a list of Python 3 downloads and installers, refer to the official [release page](https://www.python.org/downloads).

Once you have a python interpreter installed check its installation by opening up a terminal window and running:

```sh
python3 --help
```

Output from this command will confirm you have properly configured your Python interpreter.

Clone this repository to a conveinent directory. For information on how to clone repositories refer to [the documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

## Usage

`iou` is a script which is executed on the command line. In order to get output, users must provide input in the form of a JSON configuration file containing roommates and the utilites that they paid for a given month. An example configuration file appears as such.

```JSON
{
    "Georgina": {
        "Water": 112.23,
        "Electricity": 110.34
    },
    "Amy": {
        "Internet": 60.34
    },
    "Jeff": {

    },
    "James": {

    }
}
```

Where the utilties and their values are included in the body of each roommates name. Save this file with the extension `.json` in a convenient directory. 

Calculating the redistribution then can be accomplished by running `iou.py` with the JSON file as input. If this configuration file is stored at `/Users/user1/Documents/August-2020.json` running `iou.py` against can be accomplished by navigating into the `iou` directory and running:

```sh
cd /Users/user1/Documents/iou

python3 iou.py -c /Users/user1/Documents/August-2020.json
```

Executing `iou` on this JSON file results in the following output:

```

################################################################################

The grand total for utilities this month was: $ 282.91

Splitting this evenly results in everyone paying [70.72, 70.72, 70.72, 70.73]

Georgina paid $ 222.57 and is owed $ 151.85 for this months utilities.
Amy paid $ 60.34 and owes $ 10.38 for this months utitlities.
Jeff paid $ 0.00 and owes $ 70.73 for this months utitlities.
James paid $ 0.00 and owes $ 70.72 for this months utitlities.

Amy owes:
        Georgina $ 10.38 for this months utilites.
James owes:
        Georgina $ 70.72 for this months utilites.
Jeff owes:
        Georgina $ 70.73 for this months utilites.

################################################################################

```

Instead of multiple transfers and requests, Georgina, Amy, James and Jeff can send each other money the fewest number of times.
