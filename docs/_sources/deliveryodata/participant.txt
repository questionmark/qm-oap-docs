Participant
-----------

..  od:service::    deliveryodata

..  od:type::   Participant

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
            
    ..  od:prop::   Details  Edm.String

        The details field.  See :qm:field:`G_Participant.Details`.
        Often used to contain a human-friendly representation of the
        participant's full name.
            
    ..  od:prop::   RegistrationDateTime  Edm.DateTime
        :notnull:
        
        The date and time when the participant was first registered.
        Sourced from :qm:field:`G_Participant.Date_Registration` but
        converted to UTC.

    ..  od:prop::   Groups Group
        :collection:
        
        Navigation property to the Groups this participant is a member
        of.    
