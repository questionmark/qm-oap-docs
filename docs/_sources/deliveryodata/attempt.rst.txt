Attempt, AttemptLists and AttemptMetadata
-----------------------------------------

..  od:service::    deliveryodata


..  od:feed::   Attempts Attempt

    :method GET: reading attempt entities
    :method POST: creating attempt entities
    :method PATCH: limited support for some properties, see property descriptions for details
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


..  od:feed::   SessionAuditLog SessionAuditLog

    :method GET: read only


..  od:type::   Attempt

    The attempt entity and the corresponding feed are being developed as
    the preferred way to control assessment delivery in Questionmark's
    *next generation* toolset.  The entity was introduced to
    Questionmark OnDemand during 2015 covering initial use cases centred
    on proctoring, allowing assessments to be launched into a lockable
    lobby with corresponding controls for proctoring.  It was extended
    in 2016 to cover external delivery through printing and scanning.

    It is currently be extended further to support both proctored and
    unproctored scenarios providing support for a wide range of
    scheduling modules including a new Scheduling API based on the
    :od:feed:`Schedules` feed.

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        Attempts are identified by a numeric ID automatically assigned
        on creation.  You cannot control this value.

    ..  od:prop::   AttemptListID  Edm.Int32

        .. versionadded:: 2016.09

        This optional field allows attempts to be grouped together (for
        the purposes of simultaneously proctoring multiple running
        assessments).  An attempt may only be associated with a single
        :od:type:`AttemptList`.

    ..  od:prop::   ExternalAttemptID  Edm.String
        :notnull:
        
        An external identifier for the attempt.  This value is intended
        to be used by external scheduling modules that contain their own
        business rules.  Such a module may set this property on creation
        and then use it later to locate information in its own database
        that relates to this attempt.  The property is intended to store
        an ID to external information rather than providing a
        string-encoded binary data store. The underlying data model
        enforces a uniqueness constraint on this property so API clients
        should ensure they adopt an appropriate strategy for preventing
        duplication.  For example, a GUID or a short URL would be
        appropriate whereas a simple encoded integer would not.  Values
        are constrained to be ASCII strings of maximum length 64
        characters.
        
        This required property provides an important defence against the
        accidental creation of multiple attempts where only one is
        allowed, for example, through a race condition in the calling
        application.  By guaranteeing the uniqueness of this property's
        value the API will return an error if the caller attempts to
        create a an attempt with an external ID that matches an attempt
        that has already been created.

    ..  od:prop::   ScheduleID  Edm.Int32

        .. versionadded:: 2017.07

        An optional ID for the associated :od:type:`Schedule` entity.
        Unlike the ExternalAttemptID this value is used by the API's own
        *internal* scheduling features.  It is used in conjunction with
        the :od:prop:`AttemptNumber` to manage attempt limits with a
        high degree of defence against race conditions ensuring that
        callers cannot create two attempts that reference the same
        Schedule with the same AttemptNumber. 

        When creating attempts yourself you should leave this property
        as NULL.
        
    ..  od:prop::   AttemptNumber  Edm.Int32

        .. versionadded:: 2017.07
        
        An optional attempt number used in conjunction with the
        :od:prop:`ScheduleID` to control the way attempts are created
        for a scheduled assessment.  When creating attempts yourself you
        should leave this property as NULL.
        
    ..  od:prop::   ParticipantID  Edm.Int32
        :notnull:

        All attempts must be for a specified participant, this value is
        required.  Attempts are non-transferable, you can't modify this
        value once the attempt has been created.  This value must also
        be the ID of an existing :od:type:`Participant` entity.
        
    ..  od:prop::   AssessmentID  Edm.Int64
        :notnull:

        All attempts must be for a specified assessment, this value is
        required.  You can't modify this value once the attempt has been
        created.  This value must also be the ID of an existing
        :od:type:`Assessment` entity.  See also
        :od:prop:`Assessment.Language` below.
        
    ..  od:prop::   AssessmentSnapshotID  Edm.Int32
    
        An attempt may optionally be associated with a specific snapshot
        of the assessment.  You can't modify this value once the attempt
        has been created.  If specified, this value must be the ID of an
        :od:type:`AssessmentSnapshot` entity.
        
        This feature is currently only implemented for external delivery
        methods.  In other words, an attempt for a specified snapshot
        *must* be delivered externally (e.g., using printing and
        scanning) and scored by uploading a result file to the
        :od:feed:`deliveryodata.AnswerUploads` feed.
        
    ..  od:prop::   Language  Edm.String

        The optional Language property allows you to control which
        language the assessment will be delivered in.  By default this
        value is NULL and the participant will be offered a choice of
        languages when the assessment starts if it is available in
        multiple languages.

        The language is fixed on attempt creation and cannot be changed.
        If a language is specified the assessment *must* be available in
        that language.  The assessment is then started in that language
        and the participant is not offered a choice. 

        Specifying a snapshot automatically specifies the language of
        the assessment, the value of this property is ignored if
        :od:prop:`AssessmentSnapshotID` is specified.
        
    ..  od:prop::   MonitoringTypeID  Edm.Int32

        .. versionadded::   2017.11

        An optional reference to a :od:type:`MonitoringType` entity.
        
        Online assessments may be proctored or *monitored* using a range
        of technical approaches depending on the requirements.  In some
        cases, *all* attempts at an assessment are managed in the same
        way but this is not required.  The monitoring type can be
        controlled on an attempt-by-attempt basis switching between
        different configurations of the monitoring toolset. 

        For more information see :od:type:`MonitoringType`.        
                        
    ..  od:prop::   LockRequired  Edm.Boolean
        :notnull:

        Online assessments may be proctored.  A proctored assessment may
        not be started until a second actor (the Proctor) has approved
        it.  There are many ways of providing this approval but for the
        purposes of this API, assessments proctored using
        Quesetionmark's built-in proctoring tools are indicated by
        setting LockRequired to True on creation.  The value may not be
        modified.
        
        When the participant launches (or resumes) an attempt that
        requires a lock they are taken to the exam lobby.  The lobby is
        automatically locked on entry and the participant is not allowed
        to start the assessment until the attempt is unlocked (see
        :od:prop:`LockStatus` below for more information).

    ..  od:prop::   LockStatus  Edm.Boolean
        :notnull:
        
        For proctored attempts, the lock status property indicates
        whether or not the lobby is currently locked.  The value True
        indicates that the lobby is locked, False indicates that it is
        unlocked.  If the participant is in the lobby while it is locked
        they are not allowed to proceed to the assessment itself.
        
        This property can be modified (either to lock or unlock the
        lobby) using the PATCH method.  If the participant is waiting in
        the lobby they are notified immediately, typically by enabling
        (or disabling) the button used to start the assessment itself.

        It is recommended that on creation, this value is set to match
        the value of :od:prop:`LockRequired`, however, when the
        participant enters or re-enters the lobby the lock status will
        automatically be set to True if LockRequired is True.
        
    ..  od:prop::   ParticipantSystemCheckUrl   Edm.String

        .. versionadded:: 2016.12
        
        An optional URL that will be displayed to the participant on
        entering the exam lobby to assist with checking compatibility
        of the participant's device against the technology requirements
        of the proctoring process.
        
        This property may be PATCHed.
        
        ..  note::  if you omit this value or pass NULL a default system
                    check page is shown.  To explicitly indicate that no
                    system check is required pass the special URL
                    "about:blank".

    ..  od:prop::   UnlockCode   Edm.String

        .. versionadded:: 2017.03
        
        An optional alpha-numeric string that may be used by the
        participant to start their test *without* unlocking the lobby. 
        The purpose of this code is to allow participants to be issued
        with a code (typically a 6-digit pin number) that they can use
        instead of waiting for a proctor to unlock their exam manually
        using the proctor controls.  This technique can be used in cases
        where the proctor does not have access to the controls (for
        whatever reason) or for convenience when proctoring groups of
        people (see :od:type:`deliveryodata.AttemptList`). It is
        critical that the participant is only given the unlock code by
        the proctor once they are satisfied that the participant's
        environment has been secured and that any extended
        identification checks have completed successfully.
        
        This property may be PATCHed.
        
    ..  od:prop::   UnlockCodeExpiresDateTime   Edm.DateTime
    
        .. versionadded:: 2017.07

        The expiry time of the :od:prop:`UnlockCode` in UTC.  After this
        time the unlock code will be considered void and will not permit
        the participant to start the test.

        If you create an Attempt with an UnlockCode, or PATCH the
        UnlockCode in an Attempt then the expiry time will be set
        automatically to 15 minutes from the current time if it is not
        provided (or is NULL).  If you want a longer expiry time you
        must calculate the required value yourself and ensure it is set
        in the same request (POST or PATCH) as the UnlockCode.
        
    ..  od:prop::   ResultID  Edm.Int32
        
        As soon as the candidate starts taking the assessment online, or
        as soon as an external system uploads a set of answers, a result
        record is created.  This value is set automatically and will
        always be NULL on creation.  See
        :od:type:`deliveryodata.Result` for more information.
        
        In branching scenarios this ID is updated to point to a new
        Result each time the assessment branches.  Therefore, this ID is
        the ID of the current (or latest) assessment in any chain of
        branched assessments.

    ..  od:prop::   NextBranchedAttemptID  Edm.Int32
    
        .. versionadded:: 2017.11
        
        Reserved for future use.

    ..  od:prop::   ParticipantFacingQMLobbyUrl  Edm.String
    
        In order to start the assessmet described by the attempt the
        candidate must launch the participant-facing lobby URL.  This is
        a time-limited cryptographically signed URL that must be sent
        to the participant's browser to allow them to enter the lobby
        (and hence to start the assessment itself).
        
        If the assessment is marked as requiring Questionmark Secure
        this link may be a specially encrypted qmsb: URL suitable for
        launching Questionmark Secure automatically if it is already
        installed. Determining whether or not Questionmark Secure is
        installed is out of scope for the lobby as currently implemented.
        
        ..  warning::   in future this URL may launch unproctored
                        assessments directly without directing the
                        candidate to the lobby first.
        
        This property is read only.  The property's value is updated
        each time the entity is retrieved but is only present when the
        entity is retrieved directly from the *entity's* URL.  If the
        entity is retrieved as part of a larger collection (even if that
        collection contains a single member) then its value will be
        NULL.  In practice this means that a URL such as::
        
            deliveryodata/123456/Attempts(42)
        
        can be used to retrieve the URL for the participant but that a
        general URL such as::
        
            deliveryodata/123456/Attempts
        
        cannot.
        
        As the URL is time limited it must be retrieved immediately
        prior to the start of the assessment.  The link is only valid
        for a single request, to re-enter the lobby after a failure the
        entity will need to be retrieved again to obtain a new link.
        
        ..  note::  The time window is sufficient to cover
                    network latency and page load times but is not long
                    enough to allow it to be retrieved in advance and
                    stored for later use. A suitable implementation
                    would be to retrieve the entity when the participant
                    clicks a 'start test' button and then use this link
                    to redirect the participant's browser to the lobby
                    without further user intervention.
                    
                    This time window may be variable in future to
                    accommodate unproctored sessions or third party
                    proctoring solutions (see
                    :od:prop:`ParticipantFacingProctorSystemWidgetUrl`
                    for more information).
        
    ..  od:prop::   ProctorFacingQMControlsWidgetUrl  Edm.String

        This property contains a URL that can be used by a proctor to
        access a widget suitable for controlling the attempt.  The
        controls allow the proctor to unlock, pause, continue and
        terminate the attempt.
        
        This property is read only.  The property's value is updated
        each time the entity is retrieved but, like
        ParticipantFacingQMLobbyUrl, it is only present when the entity
        is retrieved directly from the *entity's* URL.
        
        It is intended that the entity will be retrieved when the
        participant is ready to take the assessment and this link passed
        to the proctor's browser for use during the session. The link
        may be accessed multiple times and may also be stored by the
        proctoring system for the duration of the session and re-used to
        bring up the controls on an as-needed basis.  The link is
        time-limited, it will remain valid throughout the session but if
        the participant's attempt is split over multiple proctoring
        sessions a new link will need to be generated each time.

    ..  od:prop::   ReviewUrl   Edm.String

        Reserved for future use.

    ..  od:prop::   ParticipantFacingProctorSystemWidgetUrl  Edm.String

        Reserved for future use.
        
    ..  od:prop::   LastModifiedDateTime  Edm.DateTime
        :notnull:
    
        A time stamp of when the attempt was last modified.  Set
        automatically, it cannot be modified directly but a call to the
        PATCH method on the associated feed will cause it to be updated.
        
    ..  od:prop::   Disabled Edm.Boolean
        :notnull:

        .. versionadded:: 2021.04

        If True then any associated Schedule is disabled *for the
        associated Participant*.  An Attempt may be disabled due to an
        administrative issue that requires administrative intervention
        before the Participant can be allowed to resume taking the
        scheduled assessment.  The Disabled flag affects the permitted
        actions returned by the various actions that return
        :od:type:`ActionableSchedule`.

    ..  od:prop::   Result  Result

        .. versionadded:: 2017.11
        
        This optional field allows you to navigate to the currently
        associated Result entity.  See also :od:prop:`ResultID`.

    ..  od:prop::   BranchedResults Result
    
        .. versionadded:: 2020.01

        Assessment branching allows a single Attempt to be used to
        control access to a chain of Assessments through conditional
        branching.  An AssessmentOutcome can be configured to branch to
        the next Assessment in the chain.  The Result navigation
        property always points to the the result of the current (or
        last) Assessment in the chain.  To gain access to all the
        results associated with the Attempt use the BranchedResults
        navigation property instead.  The :od:prop:`Result.WhenStarted`
        time can be used to determine the order in which the results
        were generated.

    ..  od:prop::   Schedule  Schedule

        .. versionadded:: 2017.07
        
        This optional field allows you to navigate to the associated
        Schedule entity.  See also :od:prop:`ScheduleID`.

    ..  od:prop::   MonitoringType  MonitoringType

        .. versionadded:: 2017.11
        
        This optional field allows you to navigate to the associated
        MonitoringType entity.  See also :od:prop:`MonitoringTypeID`.

    ..  od:prop::   Appointments Appointment
        :collection:

        .. versionadded:: 2019.05

        When used with a MonitoringType that requires appointments to be
        pre-booked, this navigation property exposes the information
        about the Appointments associated with the Attempt.
                            
    ..  od:prop::   AnswerUpload  AnswerUpload

        A navigation property to a set of answers uploaded from an
        external delivery system.  The presence of a related
        AnswerUpload entity indicates that the attempt has been taken
        externally. There can only ever be a single set of uploaded answers
        associated with an attempt.
        
    ..  od:prop::   AttemptList  AttemptList

        .. versionadded:: 2016.09
        
        This optional field allows you to navigate to an associated
        AttemptList entity.  See also :od:prop:`AttemptListID`.

    ..  od:prop::   AttemptMetadata  AttemptMetadata
        :collection:
        
        .. versionadded:: 2016.12
        
        This optional field allows you to navigate to the associated
        AttemptMetdata entities.  See :od:type:`AttemptMetadata` for
        more information.

    ..  od:prop::   SessionAuditLog  SessionAuditLog

        .. versionadded:: 2019.02
        
        This optional field allows you to navigate to the session audit
        log for this attempt.  The audit log is a detailed trail of
        evidence collected during the assessment that can help validate
        the fairness of the overall process.



..  od:type::   AttemptMetadata

    .. versionadded:: 2016.12
    
    AttemptMetadata entities store key-value pairs associated with each
    attempt.  They can store any arbitrary additional data but the
    intention is to support tagging of the data for reporting purposes.

    A number of keys have a reserved purpose.  The keys S1, S2,..., S10
    are treated as special field values and will be used to set the
    values in the result record, e.g., :qm:field:`A_Result.Special_1`,
    :qm:field:`A_Result.Special_2`, etc.  By default these values are set
    using the mapping rules defined in the system settings (within
    Enterprise Manager).  The mapping rules allow up to 10 fields from
    the associated :qm:table:`G_Participant` table to be copied
    automatically when the result is created.  A value provided in the
    AttemptMetadata always takes precedence over the mapping rule for a
    given special field. Special fields can be used to filter results in
    Questionmark Analytics and in Enterprise Reporter.

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        Unique ID of this metadata record.

    ..  od:prop::   AttemptID  Edm.Int32
        :notnull:

        ID of the associated Attempt, see :od:prop:`Attempt` for a more
        convenient navigation property.

    ..  od:prop::   Key  Edm.String
        :notnull:

        The name of the metadata field.  Any unicode string is allowed
        up to a maximum length of 200 unicode characters.
        
    ..  od:prop::   Value  Edm.String
        :notnull:

        The value of the metadata field.  The value may be any unicode
        string and is limited to 4000 unicode characters to accommodate
        values such as URNs or other URIs used to identify terms in an
        externally defined metadata schema.
        
    ..  od:prop::   Attempt  Attempt
        :notnull:
        
        A navigation property to the associated Attempt.


..  od:type::       AttemptMetadataKeyValue

    A complex type used to pass metadata key-value pairs in contexts
    where the associated :od:type:`Attempt` is implicit and the complete
    entity is not required.

    ..  od:prop::   Key  Edm.String
        :notnull:

    ..  od:prop::   Value  Edm.String
        :notnull:


..  od:type::   Appointment

    .. versionadded:: 2019.05

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

    ..  od:prop::   AttemptID  Edm.Int32
        :notnull:

        The ID of the associated :od:type:`Attempt`

    ..  od:prop::   ExternalID  Edm.String

        The ID of the appointment in the (external) proctoring system.

    ..  od:prop::   AppointmentStartUtc  Edm.DateTime
        :notnull:

        The UTC time the appointment is due to start.

    ..  od:prop::   TimeZoneID  Edm.String

        The time zone in which the appointment was booked.

    ..  od:prop::   TimezoneTime_Title  Edm.String

        A human-friendly representation of the time zone.

    ..  od:prop::   AppointmentStart  Edm.DateTime

        The local time the appointment is due to start (in the time zone
        indicated by :od:prop:`TimeZoneID`.

    ..  od:prop::   Status  Edm.String

        The status of this appointment.  The status values may vary
        depending on the proctoring provider in use.

    ..  od:prop::   Attempt  Attempt
    
        The :od:type:`Attempt` associated with this Appointment.

    
    
..  od:type::   AttemptList

    .. versionadded:: 2016.09

    AttemptLists are used to enable a single proctor to control multiple
    running assessments simultaneously.
    
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        AttemptLists are identified by a numeric ID automatically
        assigned on creation.  You cannot control this value.

    ..  od:prop::   ExternalAttemptListID  Edm.String
        :notnull:
        
        An external identifier for the attempt list.  See
        :od:prop:`Attempt.ExternalAttemptID` for an explanation of the
        basic concept of external identifiers.  This property is used by
        external applications in a similar way to identify whole lists
        of attempts.
        
        Values are constrained to be ASCII strings of maximum length 64
        characters.
        
    ..  od:prop::   ProctorFacingQMControlsUrl  Edm.String

        .. versionadded:: 2017.03

        This property contains a URL that can be used by a proctor to
        load a page suitable for controlling *all* attempts in the
        attempt list.  The controls allow the proctor to unlock, pause,
        continue and terminate the attempt.
        
        This property is read only.  The property's value is updated
        each time the entity is retrieved but, like the similar
        :od:prop:`Attempt.ProctorFacingQMControlsWidgetUrl` it is only
        present when the entity is retrieved directly from the
        *entity's* URL.
        
        It is intended that this link is passed to the proctor's browser
        for use during a proctoring session. The link may be accessed
        multiple times and may also be stored by the proctoring system
        for the duration of the session and re-used to bring up the
        controls on an as-needed basis.  The link is time-limited, it
        will remain valid throughout the session but if the attempts are
        split over multiple proctoring sessions a new link will need to
        be generated each time.

    ..  od:prop::   CreatedDateTime  Edm.DateTime
        :notnull:
    
        A time stamp of when the attempt list was created.  Set
        automatically, it cannot be modified.

    ..  od:prop::   TestCenterID  Edm.Int32

        .. versionadded:: 2019.02
        
        The ID of a :od:type:`TestCenter` entity associated with this
        list of Attempts.  This value is optional, AttemptLists can be
        created to manage groups of Attempts that should be proctored
        together without requiring an associated TestCenter.

    ..  od:prop::   Open  Edm.Boolean
        :notnull:

        .. versionadded:: 2019.02

        Used in conjunction with :od:prop:`TestCenterID` to track the
        AttemptList associated with an *open* TestCenter.  A TestCenter
        can have at most one open AttemptList at any time.
        
    ..  od:prop::   Attempts  Attempt
        :collection:
        
        A navigation property to the attempts in the list.

    ..  od:prop::   TestCenter  TestCenter
        
        A navigation property to the optional associated TestCenter.


..  od:type::   SessionAuditLog

    .. versionadded:: 2019.02

    This is a media link entry whose value is a csv file containing
    detailed information captured during an Attempt. You can
    download the file using OData's $value suffix.
    
    This data is currently experimental and is not available in all
    OnDemand environments or OnPremise.
    
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The ID of the Attempt for which this is the data.
        
    ..  od:prop::   Attempt  Attempt
        :notnull:

        Navigation property back to the owning Attempt.
