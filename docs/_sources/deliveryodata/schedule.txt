Schedule and ScheduleMetadata
-----------------------------

..  od:service::    deliveryodata

These entities represent the next-generation scheduling API that has
been redesigned to focus on the different monitoring types available in
Questionmark OnDemand and OnPremise.

The Schedules discussed here are *not* related to the G_Schedule table
and they are *not* related to the classic schedule entities created
using QMWISe.

The Schedule entity presents an alternative to creating
:od:type:`Attempt` entities directly.  It supports scheduling to
participants and/or groups including creating exceptions to enable
additional time or to reschedule individual group members.  It also
provides a way for your to safely limit the number of attempts the
participant is allowed at an assessment without having to manage the
information yourself in an external entity.


The following call illustrates the simplest way to create a schedule
called "Demo Schedule" for the Group with ID 8320236::

    POST https://ondemand.questionmark.com/deliveryodata/<customer>/Schedules

    {
        "ID": 0,
        "Name": "Demo Schedule",
        "AssessmentID": "65433000065433",
        "GroupID": 8320236,
        "MonitoringTypeID": 1
    }

Example response::

    201 Created
    
    {
        "odata.metadata": "https://ondemand.questionmark.com/deliveryodata/<customer>/$metadata#Schedules/@Element",
        "ID": 11609,
        "ParentScheduleID": null,
        "ExternalID": null,
        "Name": "Demo Schedule",
        "AssessmentID": "65433000065433",
        "Language": null,
        "GroupID": 8320236,
        "ParticipantID": null,
        "StartFrom": null,
        "StartTo": null,
        "ResumeTo": null,
        "ReportFrom": null,
        "ReportTo": null,
        "ExtraTime": null,
        "MaxAttempts": null,
        "MonitoringTypeID": 1,
        "ObserverID": null,
        "Created": "2017-08-15T12:04:28.0154826Z",
        "Modified": "2017-08-15T12:04:28.0154826Z",
        "Hidden": false,
        "Disabled": false,
        "ResumeAllowed": false,
        "TestCenterID": null
    }

The ID is a unique key for the Schedule and is set automatically on
creation, the input value is ignored.

The AssessmentID and one of the GroupID or ParticipantID MUST be
specified.



Schedules Reference
~~~~~~~~~~~~~~~~~~~


..  od:type::   Schedule

    .. versionadded::   2017.07

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        A unique integer key for this schedule.
        
    ..  od:prop::   ParentScheduleID    Edm.Int32
    
        The ID to the optional parent schedule.  A schedule may have a
        parent if it is for a specific participant
        (:od:prop:`ParticipantID` is not null) *and* the parent is a
        group schedule *without* a ParticipantID).  Essentially, a child
        schedule is an exception for a specific candidate to a general
        schedule set out in the parent. You can think of these as being
        similar to the way calendar tools deal with recurring meetings
        and exceptions only, in this case, the 'recurrence' refers to
        one scheduling applying to multiple participants and the
        exception with the schedule for a specific participant.

    ..  od:prop::   ExternalID    Edm.String

        An external identifier for the schedule.  This value is intended
        to be used by external scheduling modules that contain their own
        business rules.  Such a module may set this property on creation
        and then use it later to locate information in its own database
        that relates to this schedule.
        
    ..  od:prop::   Name    Edm.String

        A human-readable name for this schedule.
        
    ..  od:prop::   AssessmentID    Edm.Int64
        :notnull:

        The assessment that is being scheduled.  This is required and
        cannot be changed using PATCH.
            
    ..  od:prop::   Language    Edm.String

        The language of the assessment that is being scheduled.  In
        cases where the assessment may be available in multiple
        languages this allows a schedule to be for a specific language
        version.
        
    ..  od:prop::   GroupID    Edm.Int32

        The (optional) group associated with this schedule.  The group
        information is copied to the result when the participants takes
        an attempt based on the schedule and so is then available for
        filtering results.  Groups are also used to control permissions
        and are used to determine which schedules are returned by the
        related actions.

    ..  od:prop::   ParticipantID    Edm.Int32

        The ID of the participant that this schedule is for.  This is
        optional though one of GroupID and/or ParticipantID *MUST* be
        present.  (In future, this constraint may be relaxed to enable
        assessments to be scheduled to all users.)
        
    ..  od:prop::   Disabled    Edm.Boolean
        :notnull:

        Set to True to disable this schedule.  The participant will not
        be able to start or resume the assessment even if the time is
        within the Start/Resume windows.

    ..  od:prop::   StartFrom    Edm.DateTime

        The UTC time that constrains when this schedule may be started
        by the participant.  If null there is not restriction and the
        participant may start the assessment now (subject to StartTo).

    ..  od:prop::   StartTo    Edm.DateTime

        The UTC time that constrains the latest time this schedule may
        be started by participant.  If null there is no restriction and
        the participant may start the assessment at any time in the
        future subject to StartFrom.
        
    ..  od:prop::   ResumeAllowed    Edm.Boolean
        :notnull:

        .. versionadded::   2017.11

        Set to True to enable failed attempts to be resumed using this
        schedule.  If False then the ResumeTo time is ignored.
        
    ..  od:prop::   ResumeTo    Edm.DateTime

        The UTC time that constrains when this schedule may be resumed
        by the participant.  If null there is not restriction and the
        participant may resume a partially completed assessment at any
        time.
        
    ..  od:prop::   ReportFrom    Edm.DateTime

        The UTC time that constrains when a coaching report may
        be viewed by the participant.  (Reserved for future use.)

    ..  od:prop::   ReportTo    Edm.DateTime

        The UTC time that constrains when a coaching report may
        be viewed by the participant.  (Reserved for future use.)

    ..  od:prop::   ExtraTime    Edm.Int32

        The number of minutes of extra time that should be allocated to
        participants launching an assessment from this schedule. This
        time may be negative to reduce the assessment time limit.
        
    ..  od:prop::   MaxAttempts    Edm.Int32

        The maximum number of attempts the participant is allowed at the
        assessment.

    ..  od:prop::   MonitoringTypeID    Edm.Int32
        :notnull:

        The type of monitoring that will be used during the assessment.
        If this value is null then no monitoring will be performed.
        
    ..  od:prop::   ObserverID    Edm.Int32

        The ID of an Administrator (observer) who will take the test on
        behalf of the participant.  (Reserved for future use.)
        
    ..  od:prop::   Created    Edm.DateTime
        :notnull:

        The UTC time the Schedule was created.
        
    ..  od:prop::   Modified    Edm.DateTime
        :notnull:

        The UTC time the Schedule was last modified.
        
    ..  od:prop::   Hidden    Edm.Boolean
        :notnull:

        Whether or not this Schedule should be hidden from the
        participant. A hidden schedule may still be initiated through
        the API but it won't show up in the participants *My
        Assessments* page.

    ..  od:prop::   ObserverInitiated    Edm.Boolean
        :notnull:

        Whether or not this Schedule is for an observational assessment.
        An observational assessment is hidden from the Participant as it
        must be initiated by an observer (an Administrator).  Defaults
        to false.
        
    ..  od:prop::   TestCenterID    Edm.Int32

        .. versionadded::   2017.11

        The ID of a TestCenter where participants must be located in
        order to take this test.  It is assumed that this test will be
        proctored and that access to launch the test will be controlled
        by the proctor.
        
    ..  od:prop::   Assessment  Assessment
    
        A navigation property to the Assessment.
        
    ..  od:prop::   Participant  Participant
    
        A navigation property to the optional Participant.

    ..  od:prop::   Group  Group
    
        A navigation property to the optional Group.
        
    ..  od:prop::   ParentSchedule  Schedule
    
        A navigation property to the (optional) parent schedule.
        
    ..  od:prop::   MonitoringType  MonitoringType
    
        A navigation property to the (optional) monitoring type.
        
    ..  od:prop::   TestCenter  TestCenter
    
        .. versionadded::   2017.11

        A navigation property to the optional TestCenter.

    ..  od:prop::   Observer  Administrator
    
        A navigation property to the optional Observer.

    ..  od:prop::   ScheduleMetadata  ScheduleMetadata
        :collection:
    
        A navigation property to the schedule metadata.

    ..  od:prop::   Attempts  Attempt
        :collection:
    
        A navigation property to all the attempts that have been
        initiated for this Schedule.

    ..  od:action:: ActionableSchedule ActionableSchedule
        :input: ParticipantID Edm.Int32

        Returns an actionable schedule for a specific participant,
        passed as an inputer parameter using http POST::
        
            POST /deliveryodata/<customer-id>/Schedule(654321)/ActionableSchedule
            
            {
                "PartipcantID": 123456
            }
            
    ..  od:action:: InvokeAction Edm.String
        :input: Action Edm.String, ParticipantID Edm.Int32, ObserverID Edm.Int32
        
        Invokes the specified action for a given participant.  The
        Action string is a text string for an action as previously
        returned by a *recent* call to ActionableSchedule or similar.

        The ParticipantID is the ID of the participant that is scheduled
        for the assessment and the (optional) ObserverID is the observer
        that will be observing the assessment (observational schedules
        only).
        
        For example::
        
            POST /deliveryodata/<customer-id>/Schedule(654321)/InvokeAction
            
            {
                "Action": "start",
                "ParticipantID": 123456
            }

        The return result is a URL (string) that is suitable for sending
        to the participant's browser (or the observer's browser) to
        initiate the specified action.


..  od:type::   ActionableSchedule

    .. versionadded::   2017.08
    
    An actionable schedule is a list of actions that are currently
    relevant to a specific schedule *for a specific participant*.  Given
    that schedules specify time windows during which certain actions,
    such as starting or resuming the test, can take place the list of
    actions will vary from time to time and should not be cached for any
    length of time.  For example, a list of actions might be obtained
    while creating a web page showing a list of current schedules to a
    participant.

    ..  od:prop::    ScheduleID  Edm.Int32
        :notnull:
        
        The ID of the schedule these possible actions relate to
    
    ..  od:prop::    Name        Edm.String
        
        The human-readable name of this schedule.  This is repeated here
        to reduce the need to retrieve each schedule in full.

    ..  od:prop::    ParticipantID  Edm.Int32
        :notnull:
        
        All actionable schedules relate to a specific Participant.

    ..  od:prop::    ParticipantName    Edm.String
        
        The Participant's name.

    ..  od:prop::    Hidden   Edm.Boolean
        :notnull:
        
        Whether or not the schedule is hidden from the participant in
        the Questionmark portal.

    ..  od:prop::    AttemptsRemaining  Edm.Int32
        
        The number of attempts remaining on the schedule.

    ..  od:prop::    Actions     Edm.String
        :collection:
        
        A collection of symbolic strings representing allowable actions.
        For example "start" and "resume".  These strings are not
        intended to be used directly in the user interface but as keys
        for future calls to :od:action:`Schedule.InvokeAction`.


..  od:type::   ScheduleMetadata

    .. versionadded::   2017.07
    
    ScheduleMetadata entities store key-value pairs associated with a
    schedule.  They can store any arbitrary additional data but the
    intention is to support tagging of the data for reporting purposes.

    ScheduleMetadata is copied to the AttemptMetadata when the API is
    used to *automatically* create an associated Attempt using one of
    the launch actions.  A number of dynamic values are supported to
    enable a restricted set of fields to be copied from the Participant,
    TestCenter or Administrator (as an observer) entities into the
    AttemptMetadata to enable reporting based on arbitrary demographics.
    
    For example, a ScheduleMetadata field with *Key* "Country" and
    *Value* "%Participant.Primary_Country%" will cause the Participant's
    primary country to be looked up in the Participant record and copied
    to the AttemptMetadata with key "Country" on assessment launch.  If
    the participant's Primary_Country field was set to "US" then the
    AttemptMetadata would contain Key="Country", Value="US". 
    
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        Unique ID of this metadata record.

    ..  od:prop::   ScheduleID  Edm.Int32
        :notnull:

        ID of the associated Schedule, see :od:prop:`Schedule` for a more
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
        
    ..  od:prop::   Schedule  Schedule
        :notnull:
        
        A navigation property to the associated Schedule.
