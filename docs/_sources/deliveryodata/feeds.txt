Delivery OData Feeds
--------------------

..  od:service::    deliveryodata

..  od:feed::   Administrators Administrator

    :method GET: feed is read only
    :filter ID: primary key
    :filter Name: administrator name
    :expand Groups: associated groups
    :expand TestCenters: associated test centers

    The Administrators feed contains data about users with administrator
    roles in the user data base.  A user with an administrator role is
    defined as being a user with *any* role other than special
    Participant role.


..  od:feed::   Answers Answer
    :mle:

    :method GET: feed is read only
    :filter QuestionID: ID of the associated Question
    :filter ResultID: ID of the associated Result
    :expand Question: expands the associated Question
    :expand Result: expands the associated Result
    :expand ScoringTask: expands the associated ScoringTask, due to
                         a known issue this expansion will *only* return
                         entities that are associated with a ScoringTask.

    $orderby is *not* supported.

    The Answers feed contains detailed information about the answers
    given by participants.  Each question that a participant answers
    generates a unique record in this feed.


..  od:feed::   AnswerUploads AnswerUpload
    :mle:
    
    :method GET: returns AnswerUpload metadata entities
    :method POST: submits new AnswerUpload file for scoring
    :filter AttemptID: the primary key

    $orderby is *not* supported.

    The AnswerUpload feed is used for external delivery use cases where
    response data is obtained externally (e.g., through printing and
    scanning) and must be submitted for scoring through the API.  It
    also maintains a record of the raw response data in its uploaded
    form for future audit.


..  od:feed::   Assessments Assessment
    
    :method GET: feed is read only
    :filter ID: primary key
    :filter Name: assessment name
    :expand Results: expands the associated Results    

    The Assessments feed provides information about the assessment
    catalog. That is, all the assessments that have been published for
    delivery.
    
..  od:feed::   AssessmentSnapshots AssessmentSnapshot

    :method GET: reading snapshot entities
    :method POST: creating snapshot entities
    :method PATCH: some properties may be updated, see entity for details
    :filter ID: primary key
    :filter AssessmentID: the assessment used to create the snapshot ($orderby not supported)
    :filter CreatedDateTime: the time the snapshot was created ($orderby only, $filter not supported)
        
    The AssessmentSnapshots feed contains information about snapshots of
    assessments.  Snapshots are versions of an assessment that have
    fixed any randomisation, such as which questions are picked and the
    order they are presented, including the order of any shuffled
    choices.  Snapshots are used for making an exact record of the
    assessment that was delivered to the participant.  At the time of
    writing they are used only for external delivery workflows,
    including printing and scanning.
    
..  od:feed::   AssessmentSnapshotsData AssessmentSnapshotData
    :mle:

    :method GET: feed is read only
    :filter ID: primary key

    $orderby is *not* supported.

    An auxiliary feed to :od:feed:`AssessmentSnapshots` which contains
    the raw XML data describing the snapshot.  Values are normally
    obtained by navigation from the associated
    :od:type:`deliveryodata.AssessmentSnapshot` rather than directly.
    
..  od:feed::   AttemptLists AttemptList

    .. versionadded:: OnDemand 2016.09

    :method GET: reading attempt list entities
    :method POST: creating attempt list entities
    :filter ID: primary key
    :filter ExternalAttemptListID: external reference
    :expand Attempts: expands the associated Attempts    

    $orderby is *not* supported.

    The AttemptLists feed supports the arbitrary grouping of attempts
    allowing a pre-defined group of attempts to be managed by a single
    proctor or external business process.    

..  od:feed::   AttemptMetadata AttemptMetadata

    :method GET: reading attempt metadata key-value pairs
    :method POST: creating attempt metadata key-value pairs
    :filter ID: primary key
    :filter AttemptID: associated attempt
    :expand Attempt: expands the associated Attempt    

    $orderby is *not* supported.

    The attempt metadata feed allows arbitrary metadata to be associated
    with an attempt.  Although entities can be created and accessed
    directly from this feed they are always associated with an Attempt
    and can be created in a single OData call at the same time as the
    Attempt itself.  For example::
    
        POST <service root>/Attempts
        Content-Type: application/json
        
        {
            ExternalAttemptID: "Demo/2016-10-07.3",
            ParticipantID: 1459320309,
            AssessmentID: "9788463565326947",
            AttemptMetadata: [
                {
                    Key: "S1",
                    Value: "Help"
                },
                {
                    Key: "S2",
                    Value: "Me!"
                }
            ]
        }

    The response is a new Attempt record::
    
        201 Created
        Content-Type: application/json; charset=utf-8

        {
            "odata.metadata": "<service root>/$metadata#Attempts/@Element",
            "ID": 180,
            "ParticipantFacingQMLobbyUrl": null,
            "ProctorFacingQMControlsWidgetUrl": "https://...",
            "ExternalAttemptID": "Demo/2016-10-07.3",
            "ParticipantID": 1459320309,
            "AssessmentID": "9788463565326947",
            "AssessmentSnapshotID": null,
            "ResultID": null,
            "LockStatus": false,
            "LockRequired": false,
            "ParticipantFacingProctorSystemWidgetUrl": null,
            "LastModifiedDateTime": "2016-10-07T16:20:00.341227Z",
            "Language": null,
            "AttemptListID": null
        }    

    You can see the newly created metadata records by expanding the
    AttemptMetadata::
    
        GET <service root>/Attempts(180)?$expand=AttemptMetadata
        
        200 OK
        Content-Type: application/json; charset=utf-8
        
        {
            odata.metadata: "<service root>/$metadata#Attempts/@Element",
            AttemptMetadata: [
                {
                    Id: 2,
                    AttemptId: 180,
                    Key: "S1",
                    Value: "Help"
                },
                {
                    Id: 3,
                    AttemptId: 180,
                    Key: "S2",
                    Value: "Me!"
                }
            ],
            ID: 180,
            ParticipantFacingQMLobbyUrl: "qmsb:...",
            ProctorFacingQMControlsWidgetUrl: "https://...",
            ExternalAttemptID: "Demo/2016-10-07.3",
            ParticipantID: 1459320309,
            AssessmentID: "9788463565326947",
            AssessmentSnapshotID: null,
            ResultID: null,
            LockStatus: false,
            LockRequired: false,
            ParticipantFacingProctorSystemWidgetUrl: null,
            LastModifiedDateTime: "2016-10-07T16:20:00.34Z",
            Language: null,
            AttemptListID: null
        }
                

..  od:feed::   Attempts Attempt

    :method GET: reading attempt entities
    :method POST: creating attempt entities
    :filter ID: primary key
    :filter ExternalAttemptID: reference in external system
    :filter ScheduleID: the associated schedule
    :filter AttemptListID: the associated attempt list
    :expand AnswerUpload: expands the optional associated AnswerUpload
    :expand AttemptList: expands the optional associated AttemptList
    :expand AttemptMetadata: expands the optional metadata
    :expand MonitoringType: expands the optional MonitoringType
    :expand Result: expands the optional Result

    $orderby is *not* supported.

    The Attempts feed contains an entry for each attempt at an
    assessment. Attempts represent the authority to take a test and link
    to a specific participant, a specific assessment and (sometimes) a
    specific snapshot.  There are also properties that can be used to
    control the security of the test.
    
    The attempt flow is a relatively new way of providing access to
    launch tests through the APIs.  Currently only used for specialist
    use cases such as online proctoring and printing and scanning the
    scope of the Attempts feed is gradually widening to provide a
    general platform for use by external systems that maintain their own
    business rules.    
    
..  od:feed::   Dimensions Dimension

    :method GET: this feed is read only
    :filter ID: primary key
    :expand Rubric: expands the associated Rubric    
    :expand DimensionScores: expands the associated collection of scores    
    
    The Dimensions feed contains information about the scoring
    dimensions associated with a rubric and is used for subjective
    marking.
    
..  od:feed::   DimensionScores DimensionScore

    :method GET: for reading individual scores
    :method PUT: for updating the scores
    :filter QuestionID: note that ordering is *not* supported
    :filter Order: supports $orderby only, cannot be used as a filter
    :expand Rubric: expands the associated Rubric    
    :expand Dimension: expands the Dimension of the Rubric

    The DimensionScores feed contains information about the actual
    scores awarded to an answer by a subjective marking process on a
    per-dimension basis.

..  od:feed::   Groups Group

    :method GET: read only
    :filter ID: primary key
    :filter Name: filtering by group name
    :filter RootGroupID: filtering by the top-level group (expected in 2018.02)
    :expand Administrators: the administrators responsible for the group
    :expand Participants: the participant members of the group
    :expand SubGroups: the optional list of sub-groups
    :expand ParentGroup: the optional parent group (:od:prop:`see warning <Group.ParentGroup>`)
    :expand PrintBatches: the optional list of associated PrintBatches

    The Groups feed contains data about groups of participants.  Entries
    are defined by the :od:type:`Group` type.

..  od:feed::   MonitoringTypes MonitoringType

    :method GET: read only
    :filter ID: primary key
    :filter Name: the symbolic name of this monitoring type

    $orderby is *not* supported.

    The MonitoringTypes feed contains data about methods of monitoring
    assessments. Entries are defined by the :od:type:`MonitoringType`
    type.

..  od:feed::   Participants Participant

    :method GET: read only
    :filter ID: primary key
    :filter Name: filtering by participant name
    :expand Groups: the collection of groups this participant is a member of

    The Participants feed contains data about users that have the
    special Participant role.
    
..  od:feed::   PrintBatches PrintBatch

    :method GET: read only
    :filter ID: primary key
    :filter GroupID: the ID of the group associated with this batch

    $orderby is *not* supported.

    The PrintBatches feed contains information about a group of users
    who have been assigned a particular snapshot of an assessment to
    take externally, typically through printing and scanning.
    
..  od:feed::   Questions Question

    :method GET: read only
    :filter ID: primary key
    :filter QuestionType: see note in entity type on space padding

    The Questions feed contains records describing all the questions in
    the assessment catalog.
    
..  od:feed::   QuestionTranslations QuestionTranslation

    An auxiliary feed to :od:feed:`Questions` containing translated
    versions of the Questions.
    
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

..  od:feed::   Rubrics Rubric

    :method GET: read only

    The Rubrics feed contains the scoring rules for subjective questions.

..  od:feed::   Schedules Schedule

    :method GET: for reading schedules
    :method PATCH: for updating writable properties of a schedule
    :filter ID: primary key
    :filter ParticipantID: the associated participant
    :filter GroupID: the associated group
    :filter StartFrom: the schedule start time
    :filter MonitoringTypeID: the associated monitoring type
    :filter TestCenterID: the associated test center    

    $orderby is *not* supported.


..  od:feed::   ScoringResults ScoringResult

    :method GET: for reading scoring results
    :method PUT: for updating the score    
    :filter QuestionID: the question being answered
    :filter ResultID: the result that generated the scoring task
    :expand ScoringTask: the task
    :expand Rubric: the scoring rules
    :expand DimensionScores: the individual dimension scores
    
    The Scoring Results feed contains the scores awarded by subjective
    marking.  ScoringResults are associated with ScoringTasks. 

..  od:feed::   ScoringTasks ScoringTask

    :method GET: for reading scoring tasks
    :method PUT: for updating the status of a scoring task    
    :filter QuestionID: the question being answered
    :filter ResultID: the result that generated the scoring task
    :filter Status: the status of the scoring task
    :expand Assessment: expands the assessment that was being taken    
    :expand Question: expands the question that was answered    
    :expand Result: expands the result that generated the scoring task
    :expand Answer: expands the answer that generated the scoring task
    :expand Group: expands the optional Group related to this task    
    :expand ScoringResult: use with caution, see :od:prop:`ScoringTask.ScoringResult` for details    

    The ScoringTasks feed contains one entity for each :od:type:`Answer`
    that requires subjective scoring.  The scores actually awarded are
    in the associated :od:type:`ScoringResult`.

..  od:feed::   TestCenters TestCenter

    :method GET: for reading test centres
    :filter ID: the primary key
    :filter Name: the test center name

    $orderby is *not* supported.
    
    
