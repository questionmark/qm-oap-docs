Result
------

..  od:service::    deliveryodata


..  od:feed::   Results Result

    :method GET: read only
    :filter ID: primary key
    :filter AssessmentID: the related assessment
    :filter ParticipantName: for filtering by Participant
    :filter GroupName: for filtering by Group
    :filter WhenFinished: for filtering by data of submission
    :expand Answers: the answers associated with this result

    The Results feed contains data about assessment results.  Entries
    are defined by the :od:type:`deliveryodata.Result` type.

    ..  od:action:: PurgeResultsByParticipantName
        :input: ParticipantName Edm.String

        .. versionadded::   2018.05
        
        Purges all results for a *named* participant, all answers and other
        data associated with the results are removed.  The results are
        also removed from the Results Warehouse.
        
        To invoke this action use http POST with a JSON body like this::
        
            POST /deliveryodata/<customer-id>/Results/PurgeResultsByParticipantName
            
            {
                "ParticipantName": "bob"
            }

        The PurgeResultsByParticipantName action returns a 202 accepted
        response on success, result deletion happens asynchronously to
        ensure that it doesn't conflict with the delivery of
        assessments.
        
        The participant is passed by *name* and not by ParticipantID.  This
        ensures that it is possible to delete results for participants that
        have already been deleted from the repository and for participants
        that were never created as real users.
        
        ..  warning::   Matching results of open assessments are also
                        removed by this action.  Users of open
                        assessments are typically prompted to enter
                        their name at the start of the assessment
                        without authentication.  Users are free to
                        choose any name and this is recorded in the
                        database as the participant name.  
                        
    ..  od:action:: PurgeParticipantAndResultsByParticipantName
        :input: ParticipantName Edm.String
        
        .. versionadded::   2018.05

        Similar to PurgeResultsByParticipantName but also removes the
        Participant's user account if one exists in the repository.

    ..  od:action:: PurgeResultsByAssessmentId
        :input: AssessmentID Edm.String

        .. versionadded::   2018.05

        Similar to PurgeResultsByParticipantName except that all results
        for a given assessment are removed instead.

        To invoke this action use http POST with a JSON body like this::
        
            POST /deliveryodata/<customer-id>/Results/PurgeResultsByAssessmentId
            
            {
                "AssessmentID": "2185231530264478"
            }

        ..  warning::   The AssessmentID is a *string* and not an Int64.

    ..  od:action:: PurgeResultsByRetentionPolicy
        :input: AdministratorName Edm.String, RunType Edm.String

        .. versionadded::   2020.11
        
        It is possible to configure an area with a retention policy for
        results, effectively a number of days after which *Result* data
        will be purged by this method.  If a policy has not been set,
        or is invalid, then no action is taken.

        The AdministratorName allows the caller to provide the name of
        the end user that triggered the action (for auditing purposes).
        
        The RunType parameter can be used to provide a description of
        the trigger for the action (for auditing purposes).  The value
        "Scheduled" is reserved for Questionmark use and indicates that
        an automated periodic clean-up process was responsible for the
        action.

        ..  warning::   The PurgeResultByRetentionPolicy action cannot
                        be undone.  Use of this method on the
                        Questionmark OnDemand platform requires a
                        Questionmark approved retention policy to have
                        been configured for the tenant concerned.
        
    ..  od:action:: ReplayResultsByDateRange
        :input: StartDate Edm.DateTime, EndDate Edm.DateTime

        .. versionadded::   2021.03

        Reserved for internal use.

    ..  od:action:: ReplayResultsByIDList
        :input: ResultIds Collection(Edm.Int32)

        .. versionadded::   2022.02

        Reserved for internal use.

 
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
    
    ..  od:prop::   TestCenterName Edm.String

        The name of the Test Center where the participant took the
        assessment that generated this result.  This value is populated
        automatically if the assessment was created using an associated
        :od:type:`Schedule`.

        .. versionadded::   2019.02
            
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

    ..  od:prop::   Special1 Edm.String
    
        See :qm:field:`A_Result.Special_1`.
        
        The special field values (Special1..Special10) are populated
        from :od:type:`AttemptMetadata`, from input parameters in PIP
        calls or from default values configured in System Settings.

        .. versionadded::   2019.02

    ..  od:prop::   Special2 Edm.String

    ..  od:prop::   Special3 Edm.String

    ..  od:prop::   Special4 Edm.String

    ..  od:prop::   Special5 Edm.String

    ..  od:prop::   Special6 Edm.String

    ..  od:prop::   Special7 Edm.String

    ..  od:prop::   Special8 Edm.String

    ..  od:prop::   Special9 Edm.String

    ..  od:prop::   Special10 Edm.String

    ..  od:prop::   StillGoing Edm.Boolean
    
        A boolean indicating if the participant's attempt is in progress
        (True) or complete (False).
        
        .. versionadded::   2019.02

    ..  od:prop::   TimeTaken Edm.Int32
    
        The length of tie taken on the assessment (in seconds).

        .. versionadded::   2019.02

    ..  od:prop::   ScheduleName Edm.String
    
        The name of the schedule that was used to launch the
        corresponding Attempt.  This value is the name at the time the
        participant launched their attempt at the Assessment, if the
        Schedule is subsequently renamed or deleted the original value
        can still be retrieved here.

        .. versionadded::   2019.02

    ..  od:prop::   FirstName Edm.String
    
        The first name of the Participant *at the time they launched the
        corresponding Attempt*.  See :od:prop:`Participant.FirstName`.

        .. versionadded::   2019.02

    ..  od:prop::   LastName Edm.String
    
        The first name of the Participant *at the time they launched the
        corresponding Attempt*.  See :od:prop:`Participant.LastName`.

        .. versionadded::   2019.02

    ..  od:prop::   AttemptId Edm.Int32
    
        The :od:prop:`Attempt.ID` of the corresponding Attempt.

        .. versionadded::   2020.02

    ..  od:prop::   Assessment  Assessment
        :notnull:
        
        A navigation property to the associated Assessment (see also
        :od:prop:`AssessmentID`).

    ..  od:prop::   Answers Answer
        :collection:
        
        A navigation property to the Participant's Answers

    ..  od:prop::   ScoringTasks ScoringTask
        :collection:
        
        A navigation property to the ScoringTasks associated with this
        result, if any.  One ScoringTasks is associated with the result
        for each unscored Answer.

    ..  od:prop::   Attempt Attempt
        
        A navigation property to the Attempt associated with this
        result, if any.

        .. versionadded::   2020.02

    ..  od:prop::   TopicScores TopicScore
        :collection:
        
        .. versionadded::   2021.11
        
        A navigation property to the TopicScores associated with this
        result, if any.

    ..  od:action:: Purge

        .. versionadded::   2018.05

        Purges this result from the repository, all answers and other
        data associated with the result are removed.  The result is
        also removed from the Results Warehouse.
        
        To invoke this action use http POST with an empty JSON body::
        
            POST /deliveryodata/<customer-id>/Result(123457)/Purge
            
            {
                
            }

        The Purge action returns a 202 accepted response on success, result
        deletion happens asynchronously to ensure that it doesn't conflict
        with the delivery of assessments.        

    ..  od:action:: ReplayResult

        .. versionadded::   2021.03

        Reserved for internal use.


..  od:feed::   TopicScores TopicScore


    :method GET: read only
    :filter ID: primary key
    :expand Result: the Result the TopicScore is associated with.

    .. versionadded::   2021.11


..  od:type::   TopicScore

    .. versionadded::   2021.11
    
    An entity representing a sub-score for the specified topic.  TopicScores
    are always associated with a related :od:type:`Result` entity.
    
    ..  od:prop::   ResultID    Edm.Int32
        :key:
        :notnull:

    ..  od:prop::   TopicID     Edm.Int32
        :key:
        :notnull:

    ..  od:prop::   PercentageScore Edm.Double
        :notnull:

    ..  od:prop::   TotalScore  Edm.Int32
        :notnull:

    ..  od:prop::   MaxScore    Edm.Int32
        :notnull:

    ..  od:prop::   ScoreBandTitle  Edm.String
    
    ..  od:prop::   NumQuestions    Edm.Int32
        :notnull:

    ..  od:prop::   TopicPath   Edm.String
    
    ..  od:prop::   Result  Result
    
    
..  od:feed::   ResultsAuditLog ResultAuditLog

    :method GET: read only
    :filter ID: primary key
    :filter MessageID: the unique ID used in the message queue
    :filter RequestUserID: the type of action requested
    :filter RequestDateTime: when the action was requested

    .. versionadded::   2018.05

    $orderby *is* supported so you can reverse sort the log using::
    
        $orderby=RequestDateTime desc


..  od:type::   ResultAuditLog

    .. versionadded::   2018.05

    An entity documenting auditable actions against the entity set of
    results.  Due to the importance of the result set some actions
    generate a ResultAuditLog entity automatically when they are called.
    This entity also allows the status of long running tasks (such as
    the bulk removal of data) to be tracked.
    
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The primary key of this entity.

    ..  od:prop::   MessageID Edm.String
    
        The unique message ID associated with this action.  This value
        is a longer key used internally to track the action from the
        initial point of the request through to completion.

    ..  od:prop::   RequestUserID Edm.Int32
        :notnull:

        The user (Administrator) that initiated the request.  This is
        typically the ID of the service account responsible for calling
        the API method that triggered the auditable action.
        
    ..  od:prop::   RequestType Edm.String

        The name of the auditable action such as
        PurgeResultsByResultIdCommand.
    
    ..  od:prop::   RequestData Edm.String

        The data associated with the request.
        
    ..  od:prop::   Source Edm.String
    
        The source of the request, for API calls this is the IP address
        of the machine that issued the request.
        
    ..  od:prop::   RequestDateTime Edm.DateTime
        :notnull:

        The time the request was made.
        
    ..  od:prop::   IsInQueue Edm.Boolean"
        :notnull:
    
        A boolean which is "true" if the request is waiting to be
        processed. Auditable actions are placed in a queue and actioned
        when system resources become available.  Once the action has
        been carried out this is updated to "false" and the remaining
        fields can be used to read back the outcome.
        
    ..  od:prop::   ProcessedDateTime Edm.DateTime
    
        The time the request was processed.
        
    ..  od:prop::   WasSuccessful Edm.Boolean
    
        A boolean flag indicating whether or not the request was
        successfully processed (true) or if it failed (false).
        
    ..  od:prop::   TotalResultsAffected Edm.Int32
        :notnull:
    
        The number of results affected by the request.
