G_Test_Center
-------------

..  qm:table::  G_Test_Center

    ..  qm:field:: Test_Center_ID int
        :key:
        :notnull:

    ..  qm:field:: Label varchar(200)

    ..  qm:field:: Name varchar(200)

        The name of the Test Center (names must be unique).

    ..  qm:field:: Department varchar(200)

    ..  qm:field:: Location varchar(200)

    ..  qm:field:: Active bit

    ..  qm:field:: Time_Zone varchar(50)

    ..  qm:field:: Supported_Technology smallint

    ..  qm:field:: Capacity int

    ..  qm:field:: Address_1 varchar(200)

    ..  qm:field:: Address_2 varchar(200)

    ..  qm:field:: City varchar(200)

    ..  qm:field:: State varchar(200)

    ..  qm:field:: ZIP_Code varchar(200)

    ..  qm:field:: Country varchar(200)

    ..  qm:field:: Phone varchar(200)

    ..  qm:field:: Fax varchar(200)

    ..  qm:field:: Logo varchar(200)

    ..  qm:field:: Admin_Email varchar(250)

    ..  qm:field:: Properties varchar(4000)


..  qm:table::  G_Test_Center_Owner

    ..  qm:field:: Test_Center_ID int
        :key:
        :notnull:

        The Group ID.

    ..  qm:field:: User_ID int
        :key:
        :notnull:

        The administrator ID of a user that owns this Test Center.