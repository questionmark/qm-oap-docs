Answer
------

..  od:service::    deliveryodata

..  od:type::   Answer

    Answer entities are drawn from :qm:table:`A_Answer` in the data
    model but contain only a subset of the properties.  They are read
    only in OData.
    
    ..  od:prop::   QuestionID  Edm.Int64
        :key:
        :notnull:
        
        The fulle ID of the question being answered, see
        :qm:field:`A_Answer.Question_MID`. for more information.

    ..  od:prop::   ResultID  Edm.Int32
        :key:
        :notnull:
        
        The ID of the associated Result, see
        :qm:field:`A_Answer.Result_ID`.

    ..  od:prop::   BlockNumber  Edm.Int16
        :key:
        :notnull:
        
        The sequence number of the block within the which the question
        was presented.  See :qm:field:`A_Answer.Block_Number`.

    ..  od:prop::   Occurrence  Edm.Int16
        :key:
        :notnull:
        
        See :qm:field:`A_Answer.Occurrence`.
    
    ..  od:prop::   QuestionNumber  Edm.Int16
        :notnull:
        
        The sequence number of the question presented within the block. 
        See :qm:field:`A_Answer.Question_Number`.
    
    ..  od:prop::   TimesAnswered  Edm.Int16
        :notnull:

        See :qm:field:`A_Answer.Times_Answered`.

    ..  od:prop::   MaxScore  Edm.Int32
        :notnull:

        See :qm:field:`A_Answer.Max_Score`.

    ..  od:prop::   ActualScore  Edm.Int32
        :notnull:

        See :qm:field:`A_Answer.Actual_Score`.

    ..  od:prop::   Question  Question

        Navigation property to the a single Question associated with
        this answer.
    
    ..  od:prop::   Result  Result

        Navigation property to the single Result associated with this
        answer.

    ..  od:prop::   ScoringTask  ScoringTask

        Navigation property to an optional ScoringTask associated with
        this answer.  ScoringTasks are only associated with answers that
        require subjective marking.
    
    


    
                
    
   