Participant
-----------

..  od:service::    deliveryodata


..  od:feed::   Participants Participant

    :method GET: read participant entities
    :method POST: create participant entity
    :method PATCH: update participant entity (some properties read only)
    :method DELETE: delete participant entity, deletes the user from the system entirely
    :filter ID: primary key
    :filter Name: filtering by participant name
    :expand Groups: the collection of groups this participant is a member of

    The Participants feed contains data about users that have the
    special Participant role.


..  od:type::   Participant

    ..  od:prop::   Password  Edm.String

        The Participant's password.  This field is not available during
        a GET operation and will always appear to be set to null but it
        can provided when creating (POST) or updating (PATCH) a
        Participant record.

        .. versionadded::   2021.02

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The numeric ID of the Participant.

    ..  od:prop::   Name  Edm.String

        The name of the Participant. See
        :qm:field:`G_Participant.Participant_Name`.

    ..  od:prop::   FirstName  Edm.String

        The first name of the Participant.  See
        :qm:field:`G_Participant.First_Name`.

    ..  od:prop::   LastName  Edm.String

        The last name of the Participant.  See
        :qm:field:`G_Participant.Last_Name`.

    ..  od:prop::   MiddleName  Edm.String

        The middle name of the Participant.  See
        :qm:field:`G_Participant.Middle_Name`.

    ..  od:prop::   PrimaryAddress1  Edm.String

    ..  od:prop::   PrimaryAddress2  Edm.String

    ..  od:prop::   PrimaryCity  Edm.String

    ..  od:prop::   PrimaryState  Edm.String

    ..  od:prop::   PrimaryZIPCode  Edm.String

    ..  od:prop::   PrimaryCountry  Edm.String

    ..  od:prop::   PrimaryPhone  Edm.String

    ..  od:prop::   PrimaryFax  Edm.String

    ..  od:prop::   PrimaryEmail  Edm.String

    ..  od:prop::   SecondaryAddress1  Edm.String

    ..  od:prop::   SecondaryAddress2  Edm.String

    ..  od:prop::   SecondaryCity  Edm.String

    ..  od:prop::   SecondaryState  Edm.String

    ..  od:prop::   SecondaryZIPCode  Edm.String

    ..  od:prop::   SecondaryCountry  Edm.String

    ..  od:prop::   SecondaryPhone  Edm.String

    ..  od:prop::   SecondaryFax  Edm.String

    ..  od:prop::   SecondaryEmail  Edm.String

    ..  od:prop::   Salutation  Edm.String

    ..  od:prop::   OrganizationName  Edm.String

    ..  od:prop::   Department  Edm.String

    ..  od:prop::   Title  Edm.String

    ..  od:prop::   AssistantName  Edm.String

    ..  od:prop::   ManagerName  Edm.String

    ..  od:prop::   Gender  Edm.String

    ..  od:prop::   URL  Edm.String

    ..  od:prop::   Details  Edm.String

        The details field.  See :qm:field:`G_Participant.Details`.
        Often used to contain a human-friendly representation of the
        participant's full name.

    ..  od:prop::   Details1  Edm.String

    ..  od:prop::   Details2  Edm.String

    ..  od:prop::   Details3  Edm.String

    ..  od:prop::   Details4  Edm.String

    ..  od:prop::   Details5  Edm.String

    ..  od:prop::   Details6  Edm.String

    ..  od:prop::   Details7  Edm.String

    ..  od:prop::   Details8  Edm.String

    ..  od:prop::   Details9  Edm.String

    ..  od:prop::   Details10  Edm.String

    ..  od:prop::   Details11  Edm.String

    ..  od:prop::   Details12  Edm.String

    ..  od:prop::   Details13  Edm.String

    ..  od:prop::   Details14  Edm.String

    ..  od:prop::   Details15  Edm.String

    ..  od:prop::   Details16  Edm.String

    ..  od:prop::   Details17  Edm.String

    ..  od:prop::   Details18  Edm.String

    ..  od:prop::   Details19  Edm.String

    ..  od:prop::   Details20  Edm.String

    ..  od:prop::   DateOfBirth  Edm.String

        .. versionadded:: 2022.01

        The optional date of birth of the participant.

    ..  od:prop::   PreferredLang  Edm.String

        The preferred language of the participant.  This is specified
        using ISO two-letter language codes with additional region
        qualification through the use of 2-letter country codes, e.g,
        en-US for English as spoken in the United States.

    ..  od:prop::   PreferredTimezone  Edm.String

        The preferred timezone of the participant.  Reserved for future
        use.

        .. versionadded:: 2021.05

    ..  od:prop::   SsoId  Edm.String

        .. versionadded:: 2021.02

        The unique identifier used by the external identity provider to
        identify the participant.

    ..  od:prop::   RegistrationDateTime  Edm.DateTime
        :notnull:

        The date and time when the participant was first registered.
        Sourced from :qm:field:`G_Participant.Date_Registration` but
        converted to UTC.

    ..  od:prop::   JobTitle  Edm.String

        The participant's job title.

    ..  od:prop::   PeopleSyncID  Edm.String

        .. versionadded::   2022.08

        An external identifier used for people synchronization.

    ..  od:prop::   Blocked  Edm.Boolean
        :notnull:

        .. versionadded::   2023.01

        If True, the participant account is blocked from access.

    ..  od:prop::   Groups Group
        :collection:

        Navigation property to the Groups this participant is a member
        of.

    ..  od:prop::   Schedules Schedule
        :collection:

        Navigation property to the Schedules related to this participant

    ..  od:action:: CheckPassword Edm.Boolean
        :input: Password Edm.String

        .. versionadded:: 2021.05

        Returns True if the input parameter matches the password set for
        this participant and False otherwise.

    ..  od:action:: SendWelcomeEmail

        .. versionadded:: 2021.05

        Generates the standard Welcome email for the participant.  A
        participant created through this API does not automatically get
        an email notification of their new account so this action must
        be used if a notification is required.  It can be called at any
        time to resend the message.

    ..  od:action:: ActionableSchedules ActionableSchedule
        :collection:
        :input: ShowHidden Edm.Boolean

        Returns a collection of :od:type:`ActionableSchedule` related to
        this participant.  It is bound to a specific Participant and takes
        an optional ``ShowHidden`` parameter (defaults to False)::

            POST /deliveryodata/<customer-id>/Participants(123456)/ActionableSchedules

            {
            }

        A Schedule is *actionable* if the Participant can take some
        action in relation to it (typically start or resume).  If there
        are no actionable schedules an empty value is returned as
        follows::

            Content-Type: application/json; charset=utf-8

            {
                "odata.metadata": "https://ondemand.questionmark.eu/deliveryodata/<customer-id>/$metadata#Collection(QM.DeliveryODataService.DTO.ActionableSchedule)",
                "value": []
            }

        ..  note::  ``ShowHidden`` is optional and defaults to False, in
                    which case hidden schedules are excluded.  Pass True
                    to include schedules that are hidden.  To determine
                    whether a specific hidden schedule is actionable for a
                    Participant, use :od:action:`ActionableSchedule`
                    passing the ScheduleID explicitly, to avoid returning
                    hidden Schedules that apply to all Participants.

    ..  od:action:: ActionableSchedule ActionableSchedule
        :input: ScheduleID Edm.Int32

        Returns a single :od:type:`ActionableSchedule` related to
        this participant and the Schedule referred to in the input
        parameter.

        It is called like this::

            POST /deliveryodata/<customer-id>/Participants(123456)/ActionableSchedule

            {
                "ScheduleID": 12345
            }

        If there are no actions available then 404 status code is
        returned.

        See :od:action:`ActionableSchedules` for more information.

        ..  warning::   as of the 2021.05 release, if a participant has
                        an exception schedule and the parent schedule ID
                        is passed to this action then the exception
                        schedule is evaluated *instead*.  As a result,
                        the returned ActionableSchedule may have a
                        *different* ID from the passed parameter value.

    ..  od:action:: Upsert UpsertParticipantResponse
        :collection:
        :input: Name Edm.String, Password Edm.String, FirstName Edm.String, LastName Edm.String, MiddleName Edm.String, PrimaryAddress1 Edm.String, PrimaryAddress2 Edm.String, PrimaryCity Edm.String, PrimaryState Edm.String, PrimaryZIPCode Edm.String, PrimaryCountry Edm.String, PrimaryPhone Edm.String, PrimaryFax Edm.String, PrimaryEmail Edm.String, SecondaryAddress1 Edm.String, SecondaryAddress2 Edm.String, SecondaryCity Edm.String, SecondaryState Edm.String, SecondaryZIPCode Edm.String, SecondaryCountry Edm.String, SecondaryPhone Edm.String, SecondaryFax Edm.String, SecondaryEmail Edm.String, Salutation Edm.String, OrganizationName Edm.String, Department Edm.String, Title Edm.String, JobTitle Edm.String, AssistantName Edm.String, ManagerName Edm.String, Gender Edm.String, URL Edm.String, Details Edm.String, Details1 Edm.String, Details2 Edm.String, Details3 Edm.String, Details4 Edm.String, Details5 Edm.String, Details6 Edm.String, Details7 Edm.String, Details8 Edm.String, Details9 Edm.String, Details10 Edm.String, Details11 Edm.String, Details12 Edm.String, Details13 Edm.String, Details14 Edm.String, Details15 Edm.String, Details16 Edm.String, Details17 Edm.String, Details18 Edm.String, Details19 Edm.String, Details20 Edm.String, PreferredLang Edm.String, PreferredTimezone Edm.String, DateOfBirth Edm.String, SsoId Edm.String, PeopleSyncID Edm.String, Blocked Edm.Boolean, ReplaceExistingGroups Edm.Boolean, Groups Collection(Edm.String)

        Creates a participant when one with a matching Name does not
        exist or updates the existing participant otherwise.  Omitted
        parameters are ignored.  The Groups parameter is a list of Group
        names the participant should belong to; pass ReplaceExistingGroups
        as True to replace the participant's current group membership
        rather than adding to it.

        To invoke this action use http POST with a JSON body like this::

            POST /deliveryodata/<customer-id>/Participants/Upsert

            {
                "Name": "bob",
                "PrimaryEmail": "bob@example.com",
                "Groups": ["GroupA", "GroupB"]
            }

    ..  od:action:: ScheduleAndLaunch CustomScheduleAndLaunchResponse
        :input: Name Edm.String, AssessmentID Edm.Int64, ExtraTime Edm.Int32, ScheduleDuration Edm.Int32, MaxAttempts Edm.Int32, MonitoringTypeID Edm.Int32, TestCenterID Edm.Int32, Hidden Edm.Boolean, ExternalID Edm.String, Language Edm.String, GroupID Edm.Int32, MinMinutesBetweenAttempts Edm.Int32

        Schedules the participant for an assessment and returns the
        information required to launch it in a single operation.  It is
        bound to a specific Participant so is called like this::

            POST /deliveryodata/<customer-id>/Participants(123456)/ScheduleAndLaunch

            {
                "AssessmentID": 1234567890123
            }

    ..  od:action:: UpsertParticipantAndSchedule UpsertParticipantAndScheduleResponse
        :collection:
        :input: Participant_Name Edm.String, Participant_Password Edm.String, Participant_FirstName Edm.String, Participant_LastName Edm.String, Participant_MiddleName Edm.String, Participant_PrimaryAddress1 Edm.String, Participant_PrimaryAddress2 Edm.String, Participant_PrimaryCity Edm.String, Participant_PrimaryState Edm.String, Participant_PrimaryZIPCode Edm.String, Participant_PrimaryCountry Edm.String, Participant_PrimaryPhone Edm.String, Participant_PrimaryFax Edm.String, Participant_PrimaryEmail Edm.String, Participant_SecondaryAddress1 Edm.String, Participant_SecondaryAddress2 Edm.String, Participant_SecondaryCity Edm.String, Participant_SecondaryState Edm.String, Participant_SecondaryZIPCode Edm.String, Participant_SecondaryCountry Edm.String, Participant_SecondaryPhone Edm.String, Participant_SecondaryFax Edm.String, Participant_SecondaryEmail Edm.String, Participant_Salutation Edm.String, Participant_OrganizationName Edm.String, Participant_Department Edm.String, Participant_Title Edm.String, Participant_JobTitle Edm.String, Participant_AssistantName Edm.String, Participant_ManagerName Edm.String, Participant_Gender Edm.String, Participant_URL Edm.String, Participant_Details Edm.String, Participant_Details1 Edm.String, Participant_Details2 Edm.String, Participant_Details3 Edm.String, Participant_Details4 Edm.String, Participant_Details5 Edm.String, Participant_Details6 Edm.String, Participant_Details7 Edm.String, Participant_Details8 Edm.String, Participant_Details9 Edm.String, Participant_Details10 Edm.String, Participant_Details11 Edm.String, Participant_Details12 Edm.String, Participant_Details13 Edm.String, Participant_Details14 Edm.String, Participant_Details15 Edm.String, Participant_Details16 Edm.String, Participant_Details17 Edm.String, Participant_Details18 Edm.String, Participant_Details19 Edm.String, Participant_Details20 Edm.String, Participant_PreferredLang Edm.String, Participant_PreferredTimezone Edm.String, Participant_DateOfBirth Edm.String, Participant_SsoId Edm.String, Participant_PeopleSyncID Edm.String, Participant_Blocked Edm.Boolean, Schedule_Name Edm.String, Schedule_ExternalID Edm.String, Schedule_ExternalProctoringID Edm.String, Schedule_AssessmentID Edm.Int64, Schedule_Language Edm.String, Schedule_GroupID Edm.Int32, Schedule_StartFrom Edm.DateTime, Schedule_StartTo Edm.DateTime, Schedule_ResumeTo Edm.DateTime, Schedule_ReportFrom Edm.DateTime, Schedule_ReportTo Edm.DateTime, Schedule_ExtraTime Edm.Int32, Schedule_MaxAttempts Edm.Int32, Schedule_MonitoringTypeID Edm.Int32, Schedule_ObserverID Edm.Int32, Schedule_Created Edm.DateTime, Schedule_CreatedBy Edm.String, Schedule_Modified Edm.DateTime, Schedule_ModifiedBy Edm.String, Schedule_Hidden Edm.Boolean, Schedule_Disabled Edm.Boolean, Schedule_ResumeAllowed Edm.Boolean, Schedule_ObserverInitiated Edm.Boolean, Schedule_TestCenterID Edm.Int32, Schedule_RulesOfConductID Edm.Int32, Schedule_ReportTemplateName Edm.String, Schedule_ReportedResult Edm.String, Schedule_MinMinutesBetweenAttempts Edm.Int32

        Combines :od:action:`Upsert` and scheduling in a single
        operation.  Parameters prefixed with ``Participant_`` describe the
        participant to create or update (matched by ``Participant_Name``)
        and parameters prefixed with ``Schedule_`` describe the schedule
        to create.  Omitted parameters are ignored.

    ..  od:action:: ActionableScheduleForObservation ActionableSchedule
        :input: ScheduleID Edm.Int32, ObserverID Edm.Int32

        Returns the :od:type:`ActionableSchedule` for the given Schedule
        evaluated for the specified observer.  It is bound to a specific
        Participant.


..  od:type::   UpsertParticipantResponse

    Response type returned by the Participant
    :od:action:`Upsert <Participant.Upsert>` action.

    ..  od:prop::   ParticipantID  Edm.Int32
        :notnull:


..  od:type::   UpsertParticipantAndScheduleResponse

    Response type returned by the
    :od:action:`UpsertParticipantAndSchedule <Participant.UpsertParticipantAndSchedule>`
    action.

    ..  od:prop::   ParticipantID  Edm.Int32
        :notnull:

    ..  od:prop::   ScheduleID  Edm.Int32
        :notnull:


..  od:type::   CustomScheduleAndLaunchResponse

    Response type returned by the
    :od:action:`ScheduleAndLaunch <Participant.ScheduleAndLaunch>` action.

    ..  od:prop::   ScheduleID  Edm.Int32
        :notnull:

    ..  od:prop::   LaunchURL  Edm.String
