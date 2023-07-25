G_Schedule
----------

..  qm:table::  G_Schedule

    ..  qm:field:: Schedule_ID int
        :notnull:
        :key:
        
    ..  qm:field:: Session_MID int
        :notnull:

    ..  qm:field:: Session_LID int
        :notnull:

    ..  qm:field:: Session_Name varchar(200)
        :notnull:

    ..  qm:field:: Participant_ID int

    ..  qm:field:: Group_ID int

    ..  qm:field:: Schedule_Name varchar(200)
        :notnull:

    ..  qm:field:: Restrict_Times bit
        :notnull:

    ..  qm:field:: Schedule_Starts datetime

    ..  qm:field:: Schedule_Stops datetime

    ..  qm:field:: Restrict_Attempts bit
        :notnull:

    ..  qm:field:: Max_Attempts int

    ..  qm:field:: Use_Conditions bit
        :notnull:

    ..  qm:field:: Monitored smallint

    ..  qm:field:: Restrict_R_Access_Part bit
        :notnull:

    ..  qm:field:: Restrict_R_Access_Admin bit
        :notnull:

    ..  qm:field:: R_Access_Part_From datetime

    ..  qm:field:: R_Access_Part_To datetime

    ..  qm:field:: R_Access_Admin_From datetime

    ..  qm:field:: R_Access_Admin_To datetime

    ..  qm:field:: Test_Center_ID int

    ..  qm:field:: Group_Tree_ID int

    ..  qm:field:: Min_Days_Between_Attempts int

    ..  qm:field:: Time_Limit_Override bit

    ..  qm:field:: Time_Limit int

    ..  qm:field:: Lang varchar(10)
        :notnull:

    ..  qm:field:: Participant_Lang bit
        :notnull:


..  qm:table::  G_Schedule_Details

    The basic Schedule table is not relegated to a view but is extended
    by creating an extension table keyed on the same identifier.

    ..  qm:field:: Schedule_ID int
        :notnull:
        :key:

    ..  qm:field:: Web_Delivery bit
        :notnull:

    ..  qm:field:: Offline_Delivery bit
        :notnull:

    ..  qm:field:: APack_File varchar(100)

    ..  qm:field:: Resume_Allowed smallint

    ..  qm:field:: RRA_ResultID int

    ..  qm:field:: RRA_Enabled bit

    ..  qm:field:: ResultFilterID int


