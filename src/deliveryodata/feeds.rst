Delivery OData Feeds
--------------------

..  od:service::    deliveryodata

The Delivery OData API implements version 3 of the OData standard which
is generally compatible with both version 3 and version 2 clients.


Features
~~~~~~~~

$top and $skip
    If a feed request would cause too many entities to be returned the
    collection returned will be truncated.

    For example::
    
        <service root>/Results
    
    There are likely to be lots of results in the repository. The
    returned collection contains the first *page* of results and a
    continuation link that can be used to retrieve the next *page*, and
    so on.

    This technique was not possible with previous APIs (compare
    :qm:meth:`GetResultList`), but it does require some special handling
    on the client side. Questionmark's OData feeds make extensive use of
    paging and also impose an upper limit on the number of records that
    will be returned for each request to improve performance of both the
    service and the client itself.  The limit is currently set to 100.

    You can individually control how many results you retrieve (if you
    want fewer than 100) using the $top and $skip options::
    
            <service root>/Results?$top=10&$orderby=WhenFinished desc
        
    This query retrieves the 10 most recent results.  To get the next
    10 just add $skip::
    
            <service root>/Results?$top=10&$skip=10&$orderby=WhenFinished desc
    
    The format of the continuation links may vary depending on the type
    of index used to satisfy the query internally.  When paging through
    a large feed it is better to use the continuation links provided in
    the previous response than to manually set $top and $skip.
    
$filter
    Supported.  Filtering is only allowed on certain property values,
    see the feed descriptions below for details. The restrictions have
    been put in place to ensure that API requests do not have a negative
    effect on the delivery of assessments.
    
    Example filter::
    
        <service root>/Results?$filter=ParticipantName eq 'user123'
    
    Although spaces are shown in the above URL parameter values should
    be appropriately escaped for use in HTTP.
    
    The representation of values (such as 'user123' above) is defined by
    the OData specification.  Take care to match the type of any values
    provided in filters with the type of the corresponding property.
    In particular, note that 64-bit integers use an 'L' suffix::
    
        <service root>/Results?$filter=AssessmentID eq 9962000009962L

    More complex examples::
    
        <service root>/ScoringTasks?$filter=Group/Name eq 'CS101' and Status lt 3

    ...returns all ScoringTask entities relating to the Group with name
    CS101 that have a status less then 3 (Scored).
    
    ::

        <service root>/ScoringTasks/$count?$filter=Group/Name eq 'CS101' and Status eq 2

    ...returns the count of all ScoringTask entities relating to the
    Group with name CS101 that have a status of 2 (Saved).
    
    ::

        <service root>/ScoringTasks?$filter=Group/Name eq 'CS101' and Assessment/ID eq 1234567890L

    ...returns all ScoringTask entities relating to the Group with name
    CS101 and the assessment with ID 1234567890.
    
    ::

        <service root>/Results?$filter=GroupName eq 'CS101' and Assessment/ID eq 1234567890L&$orderby=WhenFinished desc

    ...returns all result entities relating to the group with name CS101
    and the assessment with ID 1234567890 ordered by the most recently
    submitted first.
    
    ::

        <service root>/Results?$filter=Assessment/ID eq 1234567890L and ParticipantName eq 'JaneSmith'&$orderby=WhenFinished

    ...returns all result entities relating to JaneSmith's attempts at
    the specific assessment with ID 1234567890 ordered from the first to
    the last attempt.
        
$orderby
    Supported.  Ordering can usually be used on any field marked as
    being suported in $filter.  Exceptions are noted in the feed
    descriptions.

    Example::
    
        <service root>/Results?$orderby=WhenFinished desc
        
$expand
    The expansion of navigation properties is supported though some
    special rules apply.  See each feed for details.  There is a limit
    on the depth of expansion that is allowed to ensure result sets are
    manageable.  Example expansion::
    
        <service root>/Results?$expand=Answers
    
    A deeper expansion::
    
        <service root>/Results(12345678)?$expand=Answers/Question
    
    The above not only lists all answers for the result but, within each
    answer entity, the Question itself is also expanded.  Bear in mind
    that use of expansion can dramatically increase the complexity of
    the query used to retrieve the data and the number of entities
    returned.  A maximum depth of 2 expansions is supported (as above).
    
    If an expansion results in too many child entities being returned
    for a single entity then the expansion itself will be truncated. 
    The limit is set to 100, the same as for base feeds.
    
    If this is a problem then you can usually transform the query into a
    filtered request on the target feed instead.  If an OData response
    exceeds 100 entities a continuation link is provided that can be
    used to retrieve the next 100 results, and so on.
    
    For example, if there are too many answers associated with a result
    then a query such as::
    
        Results(12345678)?$expand=Answers
    
    can instead be retrieved as separate queries::
    
        <service root>/Results(12345678)
        <service root>/Answers?$filter=ResultID eq 12345678
        <service root>/Answers?$filter=ResultID eq 12345678&$skip=100
        <service root>/Answers?$filter=ResultID eq 12345678&$skip=200
        ...
            
    If a feed's entity type is related to another type via a navigation
    property with a *target* multiplicity of 0..1 and $expand is
    supported for that property then it is possible to use the expansion
    directly in filters and orderings.
    
    For example, to view Answers to a specific question ordered by
    the date when the corresponding result was submitted (most recent
    first) you could use a query like this::
    
        <service root>/Answers?$filter=QuestionID eq 100000000373L&$orderby=Result/WhenFinished desc

    This query shows an orderby query with an implicit expansion of
    depth 1.  In the feed descriptions, allowed filters are described in
    terms of their immediate parent entity (depth 0), however, if a
    filter is supported at depth 0 you may assume that it will also be
    supported at depth 1 when filtering or ordering related entities.
            
$count
    Supported on base feeds only.  Cannot be used in combination with
    navigation properties.  This is OK::

        <service root>/Results/$count
        
    This is not::
    
        <service root>/Results(12345678)/Answers/$count
        
$format
    Not supported.  The service returns responses using JSON format by
    default.  To obtain XML responses you need to pass a suitably
    restrictive Accept: header as the $format query option is not
    supported.

$value
    For feeds labelled *Media Link Entry* the $value path component can
    be used to obtain the full media resource for an entity.  Access to
    simple property values is not supported. 

$select
    This query option is not currently supported by the Delivery OData
    API.
    
        
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
    :mle:

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
    :expand Administrators: the administrators responsible for the group
    :expand Participants: the participant members of the group
    :expand SubGroups: the optional list of sub-groups
    :expand ParentGroup: the optional parent group (:od:prop:`see warning <Group.ParentGroup>`)
    :expand PrintBatches: the optional list of associated PrintBatches

    The Groups feed contains data about groups of participants.  Entries
    are defined by the :od:type:`Group` type.

..  od:feed::   Participants Participant

    :method GET: read only
    :filter ID: primary key
    :filter Name: filtering by participant name
    :expand Groups: the collection of groups this participant is a member of

    The Participants feed contains data about users that have the
    special Participant role.
    
..  od:feed::   PrintBatches PrintBatch

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


    
