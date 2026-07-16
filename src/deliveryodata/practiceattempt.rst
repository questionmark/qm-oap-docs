PracticeAttempt
---------------

..  od:service::    deliveryodata


..  od:feed::   PracticeAttempts PracticeAttempt

    :method GET: read practice attempt entities
    :method DELETE: delete a practice attempt entity
    :filter ID: primary key

    The PracticeAttempts feed provides access to information about
    practice attempts taken by participants.


..  od:type::   PracticeAttempt

    An entity representing a participant's practice attempt.

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The numeric ID of the practice attempt.

    ..  od:prop::   ParticipantID  Edm.Int32
        :notnull:

        A reference to the :od:type:`Participant` that took the practice
        attempt.

    ..  od:prop::   MonitoringTypeID  Edm.Int32
        :notnull:

        A reference to the :od:type:`MonitoringType` associated with the
        practice attempt.

    ..  od:prop::   AppointmentID  Edm.Int32

        An optional reference to the associated :od:type:`Appointment`.

    ..  od:prop::   SessionID  Edm.String

    ..  od:prop::   IsSecureBrowser  Edm.Boolean
        :notnull:

    ..  od:prop::   LastVisitedStep  Edm.String

    ..  od:prop::   OperatingSystem  Edm.String

    ..  od:prop::   Browser  Edm.String

    ..  od:prop::   ActivityLog  Edm.String

    ..  od:prop::   WhenStartedUtc  Edm.DateTime
        :notnull:

    ..  od:prop::   WhenFinishedUtc  Edm.DateTime

    ..  od:prop::   LastModifiedUtc  Edm.DateTime
        :notnull:
