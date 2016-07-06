A_Result
--------

..  qm:table::  A_Result

    Records in A_Result are created automatically when a participant
    starts taking an assessment and they are updated each time a block
    is submitted.
    
    ..  qm:field::  Result_ID int
        :key:
        :notnull:
        
        Unique identifier for this result.  Result IDs are generated
        using an algorithm that is designed to create unique, random
        32-bit values.  The value 0 is not allowed.
    
    ..  qm:field::  When_Started datetime
    
        The date and time the test was started.  The value of this field
        is stored in the repository timezone.  See
        :ref:`timezones`.
        
        See also: :qm:field:`A_Result.When_Started_UTC`.

    ..  qm:field::  Session_MID int
        :notnull:
    
        The word 'Session' here is a misnomer.  This refers to the ID of
        the content itself, in other words, the ID of the quiz, test or
        exam that was actually taken.
        
        The ID is split across two fields, MID and LID, for legacy
        reasons. The ID itself can be obtained using the procedure
        outlined in :ref:`midlid`.  It can also be read directly on
        databases that support :od:svc:`Delivery OData <deliveryodata>`
        as :qm:field:`A_result.Assessment_ID`.

    ..  qm:field::  Session_LID int
        :notnull:
    
        See :qm:field:`A_Result.Session_MID`.

    ..  qm:field::  Session_Last_Modified datetime
        :notnull:
    
        The time when the assessment content was last modified.  This
        field can be used to help identify which version of the
        assessment was used during the test.  See
        :qm:field:`S_Header_Ex.Modified_Date`.
    
    ..  qm:field::  Write_Answer_Data bit
        
        Whether or not detailed answer information is saved in
        :qm:table:`A_Answer`.  This behaviour is controlled in the
        assessment, see :qm:field:`S_Header_Ex.Save_Answer_Data`. 
    
    ..  qm:field::  Participant varchar(200)

        Stored using the :ref:`varchar <varchar>` encoding in the database.

    ..  qm:field::  Member_Group varchar(200)
    
        The value of this field depends on the method used to launch the
        assessment.  For *open* assessments it is self-declared by the
        participant.  For *scheduled* assessments it is taken from the
        top-level group associated with the schedule.  For assessments
        launched from external integrations using PIP the value is taken
        from the data field mapped to GROUP by the PIP file.  

        Stored using the :ref:`varchar <varchar>` encoding in the database.
        
    ..  qm:field::  Participant_Details varchar(200)
    
    ..  qm:field::  Hostname varchar(200)

    ..  qm:field::  IP_Address varchar(200)

    ..  qm:field::  Signature varchar(50)

    ..  qm:field::  Still_Going bit

    ..  qm:field::  Status smallint
    
        The status of the result, stored as in integer value with the
        following interpretations:
        
        0.  No longer used, may indicate a failure during assessment
            launch.  Referred to in the Enterprise Manager user
            interface as "Recently Started" or just "Started".
        
        1.  In Progress
        
            Indicates the assessment is currently active.  Also referred
            to as "Running" in some reports.  This value indicates the
            *last seen* status.  In cases where the client fails during
            the test and it is not resumed to completion then the result
            may be left with this status value permanently.

        2.  Finished Normally
        
            Abbreviated to "Finished" in some reports.  The test was
            submitted by the participant.
        
        3.  Finished, Time Limit Exceeded
        
            Also known as "Expired" in some reports.  Indicates that a
            timed test was submitted by the participant but after the
            expected end of the test.  There are settings that control
            how much leeway is given and the behaviour of timed tests
            that are interrupted (e.g., by power failure) and later
            resumed. This status value may be seen if the leeway setting
            is too small to allow for internet latency or system
            performance but may also indicate a client-side failure of
            the test timing.

        4.  Finished at Time Limit
        
            Also known as "Timed out" in some reports.  This status
            indicates that the test was submitted automatically by the
            client when the time limit was reached.
        
        5.  Finished at User Request
            
            Also known as "Quit" in some reports.  This status indicates
            that the test was submitted as a result of the participant
            selecting the "Quit" button.  The option to quit an
            assessment is not enabled by default and this value is
            rarely seen in practice.

        6.  Paused by Proctor
        
            Indicates that a proctored test was paused by the proctor.
            This value should be treated as a special case of *in
            progress*.  The test is assumed to be active but can only be
            continued with the permission of the proctor who will cause
            the status to be set back to 1 (in progress) when the
            participant is permitted to continue.
            
        7.  Terminated by Proctor            
            
            Indicates that a proctored tests was terminated by the
            proctor, presumably due to a violation of the rules of
            conduct or a technical issue requiring the assessment
            attempt to be invalidated.

        8.  Reserved for future use
        
        9.  Finished, Scanned In
        
            The result was imported from an external delivery system,
            typically a paper-based Printing and Scanning process.

        All other values of the status field are reserved for future use.


    ..  qm:field::  Feedback smallint

    ..  qm:field::  Number_Sections smallint

    ..  qm:field::  When_Finished datetime

    ..  qm:field::  Max_Score int

        The maximum score possible on the assessment.  In simple cases
        this is just the sum of the maximum scores of the associated
        A_Answer records but the calculation here ignores questions with
        an experimental status and *may* ignore blocks that the
        participant failed to visit in multi-block tests (either due to
        running out of time, the application of jump rules or simply
        abandoning the test as *in progress*).

    ..  qm:field::  Total_Score int

        The total score achieved by the participant.  Calculated in a
        similar way to the Max_Score.  In Perception 5.7 partial scores
        are not available for assessments marked as *in progress*.
        
    ..  qm:field::  Special_1 varchar(200)

    ..  qm:field::  Special_2 varchar(200)

    ..  qm:field::  Special_3 varchar(200)

    ..  qm:field::  Special_4 varchar(200)

    ..  qm:field::  Special_5 varchar(200)

    ..  qm:field::  Special_6 varchar(200)

    ..  qm:field::  Special_7 varchar(200)

    ..  qm:field::  Special_8 varchar(200)

    ..  qm:field::  Special_9 varchar(200)

    ..  qm:field::  Special_10 varchar(200)

    ..  qm:field::  Time_Taken int

    ..  qm:field::  Score_Band_Title varchar(200)

        Assessment outcomes can be classified according to score bands.
        This field contains the ID of the score band for the percentage
        score achieved by the candidate.  It is only available when the
        result is finalised (i.e., is not paused or in progress).
        
    ..  qm:field::  Score_Band_Number int

    ..  qm:field::  Percentage_Score smallint

        The percentage score achieved by the candidate, obtained from
        :qm:field:`A_Result.Total_Score` and
        :qm:field:`A_Result.Max_Score`. The percentage is always rounded
        to an integer with #.5 rounding away from zero.
                
    ..  qm:field::  Schedule_Name varchar(200)

    ..  qm:field::  Monitored bit

    ..  qm:field::  Monitor_Name varchar(200)

    ..  qm:field::  Time_Limit_Disabled bit

    ..  qm:field::  Disabled_By varchar(200)

    ..  qm:field::  Image_Ref varchar(255)

    ..  qm:field::  ScoreBand_ID int NOT NULL
        :notnull:

    ..  qm:field::  First_Name varchar(200)

    ..  qm:field::  Last_Name varchar(200)

    ..  qm:field::  Primary_Email varchar(255)

    ..  qm:field::  Restrict_R_Access_Part bit

    ..  qm:field::  Restrict_R_Access_Admin bit

    ..  qm:field::  R_Access_Part_From datetime

    ..  qm:field::  R_Access_Part_To datetime

    ..  qm:field::  R_Access_Admin_From datetime

    ..  qm:field::  R_Access_Admin_To datetime

    ..  qm:field::  Course varchar(1020)

    ..  qm:field::  Member_Sub_Group_1 varchar(200)

    ..  qm:field::  Member_Sub_Group_2 varchar(200)

    ..  qm:field::  Member_Sub_Group_3 varchar(200)

    ..  qm:field::  Member_Sub_Group_4 varchar(200)

    ..  qm:field::  Member_Sub_Group_5 varchar(200)

    ..  qm:field::  Member_Sub_Group_6 varchar(200)

    ..  qm:field::  Member_Sub_Group_7 varchar(200)

    ..  qm:field::  Member_Sub_Group_8 varchar(200)

    ..  qm:field::  Member_Sub_Group_9 varchar(200)

    ..  qm:field::  Test_Center varchar](200)

    ..  qm:field::  Lang varchar(10)
        :notnull:

    ..  qm:field::  When_Started_UTC datetime

        The date and time the test was started in UTC.  This field was
        not available on early Questionmark systems and so may be
        missing for older records.

    ..  qm:field::  When_Finished_UTC datetime

        The date and time the test was *finished* in UTC.  This field
        was not available on early Questionmark systems and so may be
        missing for older records.

    ..  qm:field::  TimeStamp_UTC datetime

        The date and time the result record was created.  Reserved for
        future use.
        
    ..  qm:field::  Assessment_ID bigint

    ..  qm:field::  EXTRA_TIME int
        
        The value indicates the number of extra *minutes* that the
        participant is allowed compared with the time limit originally
        set for the assessment.  The extra time does *not* include any
        extra time allocated when the assessment was scheduled so the
        total time available for the assessment is the sum of the
        original assessment time limit, the extra time allocated in the
        schedule and any extra time allocated in this field.
    
        
