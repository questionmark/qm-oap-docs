Attempt
-------

..  od:service::    deliveryodata

..  od:type::   Attempt

    The attempt entity and the corresponding feed are being developed as
    the preferred way to control assessment delivery in Questionmark's
    *next generation* toolset.  The entity was introduced to
    Questionmark OnDemand during 2015 covering initial use cases centred
    on proctoring, allowing assessments to be launched into a lockable
    lobby with corresponding controls for proctoring.  It was extended
    in 2016 to cover external delivery through printing and scanning.

    In future it is envisaged that this feed will be further extended to
    support third-party proctoring solutions and unproctored scenarios
    providing suport for a wide range of scheduling modules, not just
    those that use the native :qm:table:`G_Schedule` data model.

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        Attempts are identified by a numeric ID automatically assigned
        on creation.  You cannot control this value.

    ..  od:prop::   AttemptListID  Edm.Int32

        ..  note:: *New* in OnDemand 2016.09.

        This optional field allows attempts to be grouped together.  An
        attempt may only be associated with a single
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
        application.  By guaranteeing the uniqueness of this properties
        value the API will return an error if the caller attempts to
        create a an attempt with an external ID that matches an attempt
        that has already been created.

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
        
    ..  od:prop::   ResultID  Edm.Int32
        
        As soon as the candidate starts taking the assessment online, or
        as soon as an external system uploads a set of answers, a result
        record is created.  This value is set automatically and will
        always be NULL on creation.  See
        :od:type:`deliveryodata.Result` for more information.

    ..  od:prop::   ParticipantFacingQMLobbyUrl  Edm.String
    
        In order to start the assessmet described by the attempt the
        candidate must launch the participant-facing lobby URL.  This is
        a time-limited cryptographically signed URL that must be sent
        to the participant's browser to allow them to enter the lobby
        (and hence to start the assessment itself).
        
        If the assessment is marked as requiring Questionmark Secure
        this link will be a specially encrypted qmsb: URL suitable for
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

    ..  od:prop::   ParticipantFacingProctorSystemWidgetUrl  Edm.String

        For use with Questionmark's built-in proctoring functions.  This
        optional link is set on creation or PATCHed immediately prior to
        the start of the session.  When set, it indicates that the
        participant's session will be proctored remotely and that the
        lobby must show this page to the participant in the form of a
        pop-up window or panel in order to initiate their proctoring
        session.  This allows the proctoring system to be embedded
        within the assessment delivery experience.

        For sessions that are proctored on-site or via a third-party
        proctoring system this property may be set to NULL.

        Although not fully supported in the current version of
        Questionmark OnDemand due to the narrow time window provided for
        assessment launch, it is envisaged that third-party proctoring
        systems may be used by creating an unlocked attempt (specify
        LockRequired=False on creation).  The application would then
        retrieve the ParticipantFacingQMLobbyUrl (and optionally the
        ProctorFacingQMControlsWidgetUrl) and pass them to the
        third-party proctoring system which would then forward the
        launch link to the participant's browser once the proctor
        indicates that they are ready to start.
        
    ..  od:prop::   LastModifiedDateTime  Edm.DateTime
        :notnull:
    
        A time stamp of when the attempt was last modified.  Set
        automatically, it cannot be modified directly but a call to the
        PATCH method on the associated feed will cause it to be updated.

    ..  od:prop::   AnswerUpload  AnswerUpload

        A navigation property to a set of answers uploaded from an
        external delivery system.  The presence of a related
        AnswerUpload entity indicates that the attempt has been taken
        externally. There can only ever be a single set of uploaded answers
        associated with an attempt.
        
    ..  od:prop::   AttemptList  AttemptList

        ..  note:: *New* in OnDemand 2016.09.
        
        This optional field allows you to navigate to an associated
        AttemptList entity.  See also :od:prop:`AttemptListID`.


..  od:type::   AttemptMetadata

    ..  warning::  *New*, expected to be released in Q4 of 2016

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


..  od:type::   AttemptList

    ..  note:: *New* in OnDemand 2016.09.

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

        ..  warning::  *New*, expected to be released in Q4 of 2016

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
    
    ..  od:prop::   Attempts  Attempt
        :collection:
        
        A navigation property to the attempts in the list.

