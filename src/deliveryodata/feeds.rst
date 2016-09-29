Delivery OData Feeds
--------------------

..  od:service::    deliveryodata

The Delivery OData API implements version 3 of the OData standard which
is generally compatible with both version 3 and version 2 clients.


Features
~~~~~~~~

$filter
    Supported.  Filtering is only allowed on certain property values,
    see the feed descriptions below for details. The restrictions have
    been put in place to ensure that API requests do not have a negative
    effect on the delivery of assessments.

$orderby
    Supported.  Ordering can be used on any field marked as being
    suported in $filter.

$expand
    The expansion of navigation properties is supported though some
    special rules apply.  See each feed for details.  There is a limit
    on the depth of expansion that is allowed to ensure result sets are
    manageable, in particular, if an expansion results in too many
    entities (set at 100) then it may be truncated.
    
    If this is a problem then you can usually transform the query into
    a filtered request on the target feed instead.  For example, if
    there are too many answers associated with a result then an
    query such as::
    
        Results(12345678)?$expand=Answers
    
    can instead by written as::
    
        Answers?$filter=ResultID eq 12345678&$expand=Result        
        
$count
    Supported.
        
$format
    Not supported.  The service returns responses using JSON format by
    default.  To obtain XML responses you need to pass a suitably
    restrictive Accept: header as the $format query option is not
    supported.

$value
    For feeds labelled *Media Link Entry* the $value path component can
    be used to obtain the full media resource for an entity.  Access to
    simple property values is not supported. 

        
Feed Reference
~~~~~~~~~~~~~~


..  od:feed::   Administrators Administrator

    :method GET: feed is read only
    :filter ID: primary key
    :filter Name: administrator name
    :expand Groups: associated groups

    The Administrators feed contains data about users with administrator
    roles in the user data base.  A user with an administrator role is
    defined as being a user with *any* role other than special
    Participant role.


..  od:feed::   Answers Answer

    :method GET: feed is read only
    :filter QuestionID: ID of the associated Question
    :filter ResultID: ID of the associated Result
    :expand Question: expands the associated Question
    :expand Result: expands the associated Result
    :expand ScoringTask: expands the associated ScoringTask, due to
                         a known issue this expansion will *only* return
                         entities that are associated with a ScoringTask.

    The Answers feed contains detailed information about the answers
    given by participants.  Each question that a participant answers
    generates a unique record in this feed.
    

..  od:feed::   AnswerUploads AnswerUpload
    :mle:
    
    :method GET: returns AnswerUpload metadata entities
    :method POST: submits new AnswerUpload file for scoring

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
    :filter AssessmentID: the assessment used to create the snapshot
    
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

    An auxiliary feed to :od:feed:`AssessmentSnapshots` which contains
    the raw XML data describing the snapshot.  Values are normally
    obtained by navigation from the associated
    :od:type:`deliveryodata.AssessmentSnapshot` rather than directly.
    
..  od:feed::   Attempts Attempt

    :method GET: reading attempt entities
    :method POST: creating attempt entities
    :filter ID: primary key
    :expand AttemptMetadata: expands the optional metadata
    :expand AnswerUpload: expands the optional associated AnswerUpload
    :expand AttemptList: expands the optional associated AttemptList

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
    
..  od:feed::   AttemptMetadata AttemptMetadata

    ..  warning::  *New*, expected to be released in Q4 of 2016

    :method GET: reading attempt metadata key-value pairs
    :method POST: creating attempt metadata key-value pairs
    :filter ID: primary key
    :expand Attempt: expands the associated Attempt    

    The attempt metadata feed allows arbitrary metadata to be associated
    with an attempt.
         
..  od:feed::   AttemptLists AttemptList

    ..  note::  *New* in 2016.09

    :method GET: reading attempt list entities
    :method POST: creating attempt list entities
    :filter ID: primary key
    :expand Attempts: expands the associated Attempts    

    The AttemptLists feed supports the arbitrary grouping of attempts
    allowing a pre-defined group of attempts to be managed by a single
    proctor or external business process.    

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
    :expand Rubric: expands the associated Rubric    
    :expand Dimension: expands the Dimension of the Rubric

    The DimensionScores feed contains information about the actual
    scores awarded to an answer by a subjective marking process on a
    per-dimension basis.

..  od:feed::   Groups Group

    The Groups feed contains data about groups of participants.  Entries
    are defined by the :od:type:`deliveryodata.Group` type.

..  od:feed::   Participants Participant

    The Participants feed contains data about users that have the
    special Participant role.
    
..  od:feed::   PrintBatches PrintBatch

    The PrintBatches feed contains information about a group of users
    who have been assigned a particular snapshot of an assessment to
    take externally, typically through printing and scanning.
    
..  od:feed::   Questions Question

    The Questions feed contains records describing all the questions in
    the assessment catalog.
    
..  od:feed::   QuestionTranslations QuestionTranslation

    An auxiliary feed to :od:feed:`Questions` containing translated
    versions of the Questions.
    
..  od:feed::   Results Result

    The Results feed contains data about assessment results.  Entries
    are defined by the :od:type:`deliveryodata.Result` type.

..  od:feed::   Rubrics Rubric

    The Rubrics feed contains the scoring rules for subjective questions.
    
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
    

Entity Type Reference
~~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    administrator
    answer
    answerupload
    assessment
    assessmentsnapshot
    attempt
    group
    participant
    printbatch
    question
    result
    rubric
    scoringtask


    
