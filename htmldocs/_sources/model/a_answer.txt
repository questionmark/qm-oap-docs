A_Answer
--------

..  qm:table::  A_Answer

    Records in A_Answer are created/updated automatically when a
    participant submits a question block or the block is saved by the
    *Save As You Go* feature. 
    
    ..  note::  Perception 5.7 only creates A_Answer records on block
                submit, not during saves.
   
    ..  qm:field::  Result_ID int
        :key:
        :notnull:
    
        The ID of the associated result, see
        :qm:field:`A_Result.Result_ID`.
        
    ..  qm:field::  Question_MID int
        :key:
        :notnull:

        The ID of the associated question is split across two fields,
        MID and LID, for legacy reasons. The ID itself can be obtained
        using the procedure outlined in :ref:`midlid`.
        
        The ID refers to the question with the same MID and LID in
        :qm:table:`Q_Question_Ex`
        
    ..  qm:field::  Question_LID int
        :key:
        :notnull:

        See :qm:field:`A_Answer.Question_MID`
        
    ..  qm:field::  Revision int

        
    ..  qm:field::  Occurrence smallint
        :key:
        :notnull:

        The occurrence number of the answer.  This number will generally
        be 1 and is supported only for legacy reasons.  The occurrence
        number is part of the primary key for this table in the data
        model.  In some historic data there may be multiple records
        which differ only in occurrence number.  These records should be
        treated as duplicates.  Use of the record with the lowest
        occurrence number is recommended when resolving such ambiguities.
        
    ..  qm:field::  Block_Number smallint
        :key:
        :notnull:

        The number of the block in which the corresponding question was
        delivered.  This is the sequence number, so if jump blocks are
        used in such as a way as to cause the participant to visit the
        same block (definition) twice each occurrence of the block would
        have its own Block_Number.  The first question block in an
        assessment has block number 1.
        
    ..  qm:field::  Question_Number smallint

        The number of the question within the block.  The first question
        is number 1.  Explanation questions do not count towards the
        numbering.
        
    ..  qm:field::  Status smallint

        The status of the question when it was delivered.  These values
        are taken from the status values of
        :qm:field:`Q_Question_Ex.Status`.
        
    ..  qm:field::  Signature varchar(50)
	
	    This is a legacy field for internal use only.  It is set to an
	    empty string in newer result sets.

    ..  qm:field::  Times_Answered smallint

        Indicates if the participant answered the question, takes the
        values 0 or 1 only.
        
    ..  qm:field::  Max_Score int
    
        The maximum possible score for the question.
        
    ..  qm:field::  Actual_Score int
    
        The actual score achieved by the participant on this question.
    
    ..  qm:field::  Know_Time_Taken bit

        Whether or not the :qm:field:`A_Answer.Time_Taken` field is
        valid.
        
    ..  qm:field::  Time_Taken int
    
        The time the candidate took answering the question in seconds. 
        To be read in conjunction with
        :qm:field:`A_Answer.Know_Time_Taken`.
    
    ..  qm:field::  Number_Outcomes smallint
    
        The number of question outcomes that evaluated to true during
        the scoring of this question.
        
    ..  qm:field::  Outcome_Number smallint
    
        The order number of the first outcome to evaluate to true.
        
    ..  qm:field::  Outcome_Exponential int
    
        A bitfield representing flags indicating whether or not outcomes
        evaluated to true.  The least significant bit represents the
        result of evaluating the first outcome.  This field contains
        flags for the first 32 outcomes.
    
    ..  qm:field::  Outcome_Exponential_2 int

        A bitfield representing flags indicating whether or not outcomes
        evaluated to true.  The least significant bit represents the
        result of evaluating the 33rd outcome.  This field contains
        flags for outcomes 33 to 64.
    
    ..  qm:field::  Comment_ID int
    
        The ID of the comment associated with this answer (if given).
        This is a reference to a record in :qm:table:`A_Comment`.
        
    ..  qm:field::  Answer_Truncated varchar(200)
    
        The answer given by the participant, truncated to 50 characters.
        In the case of file upload questions this is an internal file
        name used to locate the file within the repository.
        
    ..  qm:field::  Know_Confidence bit
    
        Unused, should be False.
        
    ..  qm:field::  Confidence_Level smallint
    
        Unused, should be 0
        
    ..  qm:field::  Correct_Answer varchar(4000)
    
        Unused
        
    ..  qm:field::  Topic varchar(1020)
    
        The name of the topic, obtained from the deserialised QML of
        the question in :qm:field:`Q_QML_Ex.QML_Data`.
    
    ..  qm:field::  Answer_Full text
    
        The full answer given by the participant.

        The format of encoded answers depends on the question type.  In
        most cases the values representing the choices are
        colon-separated with colons escaped using back-slash (and
        back-slashes escaped by doubling).
        
        For Yes/No, Multiple choice, Multiple response, Likert and
        True/False the answer is taken as the *content* of the choice
        (effectively, the label visible to the participant taking the
        test).

        For Matrix, Pull-down list, Matching, Ranking and Select a blank
        questions the answer is the content of the option selected from
        the choice.  
        
        The following types have their own special encoding schemes:
        
        Survey matrix
            Choices are separated by the HTML-like line break string
            "<br/>"
        
        Job task analysis
            Choices are separated by the string "\|~", choices represent
            triples of identifiers (dimension, task and selected
            option) and these are separated by the string "^~".
            
        File upload
            The actual name of the file uploaded by the participant.
        
        
    

