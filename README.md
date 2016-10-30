    Description:
        Command line tool to serialise/deserialise input file. The operation
        steps looks as below:
            1) Read/deserialise the input file.
                It supports three kinds of formats: pickle, csv and yaml.
            2) Write/serialise to the output file.
                It supports the same three formats as reading. But user can
                combine the formats, for example, reading csv format and then
                writing as yaml. If "outputFile" specified, then it would do
                serialisation operation, else it would skip this step and do
                display operation(described by step 3).
            3) Display the deserialised data as human readable format.
                There are two kinds of displaying modes, one is "text" and the
                other is "html". The "text" mode calls Terminal command "cat" to
                display in Terminal. The "html" mode calls web browser to open a
                html file.

    Requirements:
        Linux Operation System(Tested on CentOs7)
        Python 2.7+<3.0
        YAMl

    Install:
        python setup.py install

    Usage:
        # deserialise input file and display it
        contacts -d <displayer> -i <input file> -r <input file format>

        # serialise input file and save as another output file
        contacts -d <displayer> -i <input file> -o <output file> -r <input
        file format> -w <output file format>

    Usage Examples:
        # The example files used here(addressbook.*) are located in the
        # "src/data" directory or "installedDir/data" directory.

        # deserialise by Python native pickle module and call web browser to
        # show the result.
        contacts -d html -i src/data/addressbook.pik -r pickle

        # deserialise a yaml format file and show the result in Terminal,
        # if <displayer> is not specified, contacts would uses Terminal command
        # "cat" as default displayer.
        contacts -i src/data/addressbook.yaml -r yaml

        # serialise yaml format file depend on input csv file.
        contacts -i src/data/addressbook.csv -r csv -o
        /usr/tmp/addressbook.yaml -w yaml

        # add options during serialisation(specified delimiter="\"" during
        # csv writing, default is "\t") as below.
        contacts -i src/data/addressbook.csv -r csv -o
        /usr/tmp/addressbook.csv -w csv -wd "delimiter=\""

        # query help document
        contacts --help