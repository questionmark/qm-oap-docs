A_TopicScore
------------

..  qm:table::  A_TopicScore

    Records in A_TopicScore are created automatically when a participant
    completes an assessment.  They contain topic-specific scoring and
    score-band information.

    ..  qm:field::  Result_ID int
        :key:
        :notnull:

        Refers to the associated result, see
        :qm:field:`A_Result.Result_ID`.

    ..  qm:field::  Topic_ID int
        :key:
        :notnull:

        Refers to the associated topic, see :qm:field:`Q_Topic.Topic_ID`.

    ..  qm:field::  Percentage_Score float
    
        Although stored as a float in the data model percentage scores
        are rounded to integers using the same method as
        :qm:field:`A_Result.Percentage_Score`.
        
    ..  qm:field::  Actual_Score int

        Calcualted in the same way as :qm:field:`A_Result.Total_Score`
        but counting only questions that are in the associated topic.
        Experimental questions do not contribute to the value.
         
    ..  qm:field::  Maximum_Score int

        Calcualted in the same way as :qm:field:`A_Result.Max_Score` but
        counting only questions that are in the associated topic.
        Experimental questions do not contribute to the value.

    ..  qm:field::  Score_Band_Name varchar(200)

        The name of the topic scoreband that applies to this score.
        
    ..  qm:field::  Num_Questions int
    
    ..  qm:field::  Topic varchar(1020)
        :notnull:

    ..  qm:field::  Description varchar(1020)

