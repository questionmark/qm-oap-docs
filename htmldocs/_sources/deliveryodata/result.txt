Result
------

..  od:service::    deliveryodata

..  od:type::   Result

    Result entities are drawn from :qm:table:`A_Result` in the data
    model but contain only a subset of the properties.  Result entities
    are generally read-only with the exception of the
    :od:prop:`Result.Status` and :od:prop:`Result.ExtraTime` properties.
    
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:
        
        See :qm:field:`A_Result.Result_ID`.

    ..  od:prop::   AssessmentID    Edm.Int64
        :notnull:
        
        The OData feed exposes the Assessment using a combined ID rather
        than the MID+LID forms found in the data model.  See
        :qm:field:`A_Result.Session_MID` for more information.
    
    ..  od:prop::   ParticipantName Edm.String
    
        The name of the participant, see
        :qm:field:`A_Result.Participant`.
    
    ..  od:prop::   GroupName Edm.String

        The name of the participant's group, see
        :qm:field:`A_Result.Member_Group`.
    
    ..  od:prop::   ParticipantDetails Edm.String
    
        See :qm:field:`A_Result.Participant_Details`. 
    
    ..  od:prop::   Status Edm.Int16

        See :qm:field:`A_Result.Status` for details of the permitted
        values.
        
        Unlike most fields in this entity the value of Status may be set
        directly by a PATCH/MERGE or PUT request. A very limited set of
        transitions is permitted:
        
        In progress results (value 1) may be paused (6) or terminated
        (7).  Similarly paused results may be returned to *in progress*
        (1) or terminated (7).  All other transitions will generate
        errors if attempted.        
        
        Setting the status using OData does not dynamically affect the
        state of the running assessment but it may change the behaviour
        when an assessment is resumed (e.g., after a device or network
        failure).  Questionmark software uses an additional component,
        known as the Real Time Service (RTS), to signal state changes to
        the client's device.        
         
    ..  od:prop::   MaxScore Edm.Int32
    
        Taken from :qm:field:`A_Result.Max_Score`.

    ..  od:prop::   TotalScore Edm.Int32
    
        Taken from :qm:field:`A_Result.Total_Score`.

    ..  od:prop::   ScoreBandTitle Edm.String
    
        Taken from :qm:field:`A_Result.Score_Band_Title`.
    
    ..  od:prop::   PercentageScore Edm.Int16
    
        Taken from :qm:field:`A_Result.Percentage_Score`.
    
    ..  od:prop::   WhenFinished Edm.DateTime
    
        Taken from :qm:field:`A_Result.When_Finished_UTC`.  Despite
        having no UTC suffix this time is always expressed in UTC.

    ..  od:prop::   WhenStarted Edm.DateTime
    
        Taken from :qm:field:`A_Result.When_Started_UTC`.  Despite
        having no UTC suffix this time is always expressed in UTC.

    ..  od:prop::   ExtraTime Edm.Int32
    
        May be set directly using PATCH/MERGE or PUT messages on the
        entity.  See also the comments under :od:prop:`Result.Status`
        for limitations on the use of this adjustment for a running
        assessment.
        
        See :qm:field:`A_Result.EXTRA_TIME` for information about the
        interpretation of this field's value.

