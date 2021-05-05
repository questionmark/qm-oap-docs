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

        .. versionadded:: 2017.11

    ..  od:prop::   PrimaryAddress2  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   PrimaryCity  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   PrimaryState  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   PrimaryZIPCode  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   PrimaryCountry  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   PrimaryPhone  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   PrimaryFax  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   PrimaryEmail  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   SecondaryAddress1  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   SecondaryAddress2  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   SecondaryCity  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   SecondaryState  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   SecondaryZIPCode  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   SecondaryCountry  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   SecondaryPhone  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   SecondaryFax  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   SecondaryEmail  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Salutation  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   OrganizationName  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Department  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Title  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   AssistantName  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   ManagerName  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Gender  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   URL  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details  Edm.String

        The details field.  See :qm:field:`G_Participant.Details`.
        Often used to contain a human-friendly representation of the
        participant's full name.
            
    ..  od:prop::   Details1  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details2  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details3  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details4  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details5  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details6  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details7  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details8  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details9  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details10  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details11  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details12  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details13  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details14  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details15  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details16  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details17  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details18  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details19  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   Details20  Edm.String

        .. versionadded:: 2017.11

    ..  od:prop::   PreferredLang  Edm.String

        The preferred language of the participant.  This is specified
        using ISO two-letter language codes with additional region
        qualification through the use of 2-letter country codes, e.g,
        en-US for English as spoken in the United States.
 
        .. versionadded:: 2017.11
            
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

    ..  od:prop::   Groups Group
        :collection:
        
        Navigation property to the Groups this participant is a member
        of.

    ..  od:prop::   Schedules Schedule
        :collection:

        .. versionadded:: 2017.11
        
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

        .. versionadded:: 2017.11

        Returns a collection of :od:type:`ActionableSchedule` related to
        this participant.  It takes no parameters and is bound to a
        specific Participant so is called like this::
        
            POST /deliveryodata/<customer-id>/Participant(123456)/ActionableSchedules
            
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

    ..  od:action:: ActionableSchedule ActionableSchedule
        :input: ScheduleID Edm.Int32

        .. versionadded:: 2017.11

        Returns a single :od:type:`ActionableSchedule` related to
        this participant and the Schedule referred to in the input
        parameter.
        
        It is called like this::
        
            POST /deliveryodata/<customer-id>/Participant(123456)/ActionableSchedule
            
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
        
         
       
