tm_parser

Michael Perkins, 2023

## Installation

Recommend you use a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

    python -m pip install --upgrade pip
    pip install -r requirements.txt

## Instructions:

In troopmaster, under reports -> advancement -> individual history
- select all the scouts you want to report
- select all the ranks you want to report
- Do not select "Omit details on completed ranks"
- Other than that, any other options can be included or excluded (I only tested a few configurations. if it doesn't work, select everything)

generate the report and save it to a PDF.

by default, the output is to the console in YAML format

Then run:

    python -m tm_parser INPUTFILE.pdf

Options:

    -t --output-type  [yaml], json or toml

    -o --outfile output filename

This produces output of the desired type. 

YAML can be read in python with: 

    import yaml

    with open('output.yaml') as f:

        scouts = yaml.safe_load(f)


## Using TmParser in code:

    from tm_parser import TmParser

    #initializing the parser automatically parses the file and stores
    #the information in TmParser().scouts
    parser = TmParser(infile='filename.pdf')


    # Iterating on the parser yields scouts
    for scout in parser:
        print('----------------------------------------------')
        print(f"{scout['Data']['Name']:26}Date       Eagle Req")
        print('----------------------------------------------')
        ## do something with scout
        if "Merit Badges" in scout:

            #sort merit badges by date ascending
            for badge, data in sorted(scout['Merit Badges'].items(), 
                                        key=lambda x: x[1]['date']):
                print(f"{badge:26}{data['date']} {data['eagle_required']}")


Yields:

    ----------------------------------------------
    Smith, John               Date       Eagle Req
    ----------------------------------------------
    Climbing                  2017-03-11 False
    Mammal Study              2017-06-29 False
    Leatherwork               2017-06-30 False
    Swimming                  2017-06-30 True
    Kayaking                  2018-06-29 False
    Wilderness Survival       2018-06-29 False
    Rifle Shooting            2018-06-29 False
    First Aid                 2018-09-29 True

By default the information is a dictionary, with the scout names as keys, and each scout is a dictionary with the following keys:
- Activity Totals
- Data - contains biographical data
- Leadership
- Merit Badges
- Order of the Arrow
- Partial Merit Badges
- Rank Advancement
- Training Courses

All dates have been parsed into datetime.date objects, in YYYY-MM-DD format, and are null if not assigned in the incoming data. 
