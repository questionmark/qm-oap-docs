Participants
------------

This part of the guide is under development.  Please refer to the
`Participants <https://www.questionmark.com/content/participants>`_
section of the old guide for additional documentation.

Participant Methods
~~~~~~~~~~~~~~~~~~~


..  qm:meth::   CheckParticipant
    :input:     Participant_Name string, Password string
    :output:    CheckParticipantResponse CheckParticipantResponse

    This return value is multi-valued and is documented below using an
    explicit type.
    
    Given a participant name and a plain text password this method
    checks the participant's credentials against the corresponding user
    in the Questionmark database.

..  qm:xtype::   CheckParticipantResponse

    The element used for the return result of CheckParticipant.
    
    ..  qm:xfield:: Status int
    
        0.  The participant exists and the password was correct.
        1.  The participant exists but the password was incorrect.
        2.  The participant does not exist

    ..  qm:xfield:: Participant_ID string
        :optional:

        If the participant exists *and* the password matches, the ID of
        the participant record.

In the following example there is a participant with name j.doe but
their password does not match "mysecretpassword"::

    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP-ENV:Header/>
        <SOAP-ENV:Body>
            <CheckParticipant xmlns="http://questionmark.com/QMWISe/">
                <Participant_Name>j.doe</Participant_Name>
                <Password>mysecretpassword</Password>
            </CheckParticipant>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>

    <?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soap:Body>
            <CheckParticipantResponse xmlns="http://questionmark.com/QMWISe/">
                <Status>1</Status>
                <Participant_ID/>
            </CheckParticipantResponse>
        </soap:Body>
    </soap:Envelope>

When the password that is provided is correct, the response might look
like this::

    <?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soap:Body>
            <CheckParticipantResponse xmlns="http://questionmark.com/QMWISe/">
                <Status>0</Status>
                <Participant_ID>530016516</Participant_ID>
            </CheckParticipantResponse>
        </soap:Body>
    </soap:Envelope>


..  qm:meth::   CreateParticipant
    :input:     Participant Participant
    :output:    Participant_ID string

    Used to create a new participant in the repository.  The new user is
    created with the "Participant" role.  The following fields are
    mandatory when creating participants (despite having optional
    elements in the WSDL).
    
        1.  :qm:xfield:`Participant.Participant_Name`
        2.  :qm:xfield:`Participant.Password`
        3.  :qm:xfield:`Participant.Primary_Email`
        
    ..  note::  Perception and Classic OnDemand do not require the
                Primary_Email field to be set.  Also, if you omit the
                Password element, or leave it blank, a user with no
                password is created.  They will not be able to log in
                until a password is assigned.

    The password provided *must* satisfy the password policy in place
    for users with the Participant role.

    In the following example a weak password is provided and a
    corresponding fault is returned::
    
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Header/>
            <SOAP-ENV:Body>
                <CreateParticipant xmlns="http://questionmark.com/QMWISe/">
                    <Participant>
                        <Participant_Name>test1</Participant_Name>
                        <Password>password</Password>
                        <Primary_Email>user@example.com</Primary_Email>
                    </Participant>
                </CreateParticipant>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>    

        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <soap:Header/>
            <soap:Body>
                <soap:Fault>
                    <faultcode>soap:Server</faultcode>
                    <faultstring>Server was unable to process request. ---&gt; The remote server
                        returned an error: (406) Not Acceptable.</faultstring>
                    <detail/>
                </soap:Fault>
            </soap:Body>
        </soap:Envelope>
    
    A stronger password results in success::

        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Header/>
            <SOAP-ENV:Body>
                <CreateParticipant xmlns="http://questionmark.com/QMWISe/">
                    <Participant>
                        <Participant_Name>test1</Participant_Name>
                        <Password>Stronger23Pa$$word</Password>
                        <Primary_Email>user@example.com</Primary_Email>
                    </Participant>
                </CreateParticipant>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>    

        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <soap:Header/>
            <soap:Body>
                <CreateParticipantResponse xmlns="http://questionmark.com/QMWISe/">
                    <Participant_ID>46557971</Participant_ID>
                </CreateParticipantResponse>
            </soap:Body>
        </soap:Envelope>


..  qm:meth::   DeleteParticipant
    :input:     Participant_ID string

..  qm:meth::   GetParticipant
    :input:     Participant_ID string
    :output:    Participant Participant

..  qm:meth::   GetParticipantByName
    :input:     Participant_Name string
    :output:    Participant Participant

..  qm:meth::   GetParticipantGroupList
    :input:     Participant_ID string
    :output:    GroupList GroupList

..  qm:meth::   GetParticipantList
    :output:    ParticipantList ParticipantList

..  qm:meth::   GetParticipantListByGroup
    :input:     Group_ID string
    :output:    ParticipantList ParticipantList

..  qm:meth::   SetParticipant
    :input:     Participant Participant

    Used to update information about a participant.  To use this method
    you should perform a :qm:meth:`GetParticipant` call to obtain the
    full information about the participant, modify only those fields
    that you want to change and pass the resulting
    :qm:xtype:`Participant` record to this method.
    
    See special notes under :qm:xfield:`Participant.Participant_ID`,
    :qm:xfield:`Participant.Participant_Name` and
    :qm:xfield:`Participant.Password` for important information about
    the special treatment of these values.

    ..  warning::   You cannot delete demographic values with this
                    method. If you pass a value as an empty string or
                    omit the corresponding element you may get
                    inconsistent results in Questionmark OnDemand.  In
                    Perception and Classic OnDemand the value will be
                    removed from the participant's record.

    Although :qm:meth:`GetParticipant` returns information about the
    groups that a participant is a member of you cannot use
    SetParticipant to alter this list.  Use
    :qm:meth:`AddGroupParticipantList` and
    :qm:meth:`DeleteGroupParticipantList` to make this type of change.
    
    The following sequence of XML requests/responses shows how you might
    update a participant's personal name, address and email while
    leaving other information unchanged (notice that Participant_Name
    *cannot* be modified)::

        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Header/>
            <SOAP-ENV:Body>
                <GetParticipant xmlns="http://questionmark.com/QMWISe/">
                    <Participant_ID>46557971</Participant_ID>
                </GetParticipant>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>

        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <soap:Header/>
            <soap:Body>
                <GetParticipantResponse xmlns="http://questionmark.com/QMWISe/">
                    <Participant>
                        <Participant_ID>46557971</Participant_ID>
                        <Participant_Name>j.doe</Participant_Name>
                        <Password/>
                        <First_Name>Jane</First_Name>
                        <Last_Name>Doe</Last_Name>
                        <Middle_Name/>
                        <Primary_Address_1>100 Main Street</Primary_Address_1>
                        <Primary_Address_2>Apartment 5</Primary_Address_2>
                        <Primary_City>Townsville</Primary_City>
                        <Primary_State>Western Territory</Primary_State>
                        <Primary_ZIP_Code/>
                        <Primary_Country>Elbonia</Primary_Country>
                        <Primary_Phone/>
                        <Primary_Fax/>
                        <Primary_Email>j.doe@example.com</Primary_Email>
                        <Secondary_Address_1/>
                        <Secondary_Address_2/>
                        <Secondary_City/>
                        <Secondary_State/>
                        <Secondary_ZIP_Code/>
                        <Secondary_Country/>
                        <Secondary_Phone/>
                        <Secondary_Fax/>
                        <Secondary_Email/>
                        <Salutation/>
                        <Organization_Name/>
                        <Department/>
                        <Title/>
                        <Assistant_Name/>
                        <Manager_Name/>
                        <Gender/>
                        <URL/>
                        <Details>Jane Doe</Details>
                        <Details_1></Details_1>
                        <Details_2></Details_2>
                        <Details_3></Details_3>
                        <Details_4/>
                        <Details_5></Details_5>
                        <Details_6/>
                        <Details_7/>
                        <Details_8/>
                        <Details_9/>
                        <Details_10/>
                        <Details_11/>
                        <Details_12/>
                        <Details_13/>
                        <Details_14/>
                        <Details_15/>
                        <Details_16/>
                        <Details_17/>
                        <Details_18/>
                        <Details_19/>
                        <Details_20/>
                        <GroupIDList/>
                        <Date_Registration>2017-01-05</Date_Registration>
                    </Participant>
                </GetParticipantResponse>
            </soap:Body>
        </soap:Envelope>

        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Header/>
            <SOAP-ENV:Body>
                <SetParticipant xmlns="http://questionmark.com/QMWISe/">
                    <Participant>
                        <Participant_ID>46557971</Participant_ID>
                        <Participant_Name>j.doe</Participant_Name>
                        <Password/>
                        <First_Name>Jane</First_Name>
                        <Last_Name>Smith</Last_Name>
                        <Middle_Name/>
                        <Primary_Address_1>57 Western Avenue</Primary_Address_1>
                        <Primary_Address_2></Primary_Address_2>
                        <Primary_City>Cityborough</Primary_City>
                        <Primary_State>Western Territory</Primary_State>
                        <Primary_ZIP_Code/>
                        <Primary_Country>Elbonia</Primary_Country>
                        <Primary_Phone/>
                        <Primary_Fax/>
                        <Primary_Email>j.smith@example.com</Primary_Email>
                        <Secondary_Address_1/>
                        <Secondary_Address_2/>
                        <Secondary_City/>
                        <Secondary_State/>
                        <Secondary_ZIP_Code/>
                        <Secondary_Country/>
                        <Secondary_Phone/>
                        <Secondary_Fax/>
                        <Secondary_Email/>
                        <Salutation/>
                        <Organization_Name/>
                        <Department/>
                        <Title/>
                        <Assistant_Name/>
                        <Manager_Name/>
                        <Gender/>
                        <URL/>
                        <Details>Jane Smith</Details>
                        <Details_1></Details_1>
                        <Details_2></Details_2>
                        <Details_3></Details_3>
                        <Details_4/>
                        <Details_5></Details_5>
                        <Details_6/>
                        <Details_7/>
                        <Details_8/>
                        <Details_9/>
                        <Details_10/>
                        <Details_11/>
                        <Details_12/>
                        <Details_13/>
                        <Details_14/>
                        <Details_15/>
                        <Details_16/>
                        <Details_17/>
                        <Details_18/>
                        <Details_19/>
                        <Details_20/>
                        <GroupIDList/>
                        <Date_Registration>2017-01-05</Date_Registration>
                    </Participant>
                </SetParticipant>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>

        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <soap:Header/>
            <soap:Body>
                <SetParticipantResponse xmlns="http://questionmark.com/QMWISe/"/>
            </soap:Body>
        </soap:Envelope>


Participant Types
~~~~~~~~~~~~~~~~~

..  qm:xtype::  Participant

    Most of the data in the Participant element is optional and
    corresponds directly to the similarly named demographic fields
    available through the administrative user interface.
    
    ..  qm:xfield:: Participant_ID string
        :optional:

        The numeric ID of the participant.  On creation, this field
        should be left blank or omitted and a random ID will be be
        generated automatically.  When updating the information for a
        participant with :qm:meth:`SetParticipant` you must specify this
        field as it is used to identify the participant being updated.
        
    ..  qm:xfield:: Participant_Name string
        :optional:

        The user name of the participant.  On creation this field is
        *required*.  When updating the information for a participant
        with :qm:meth:`SetParticipant` you should always pass the
        existing participant name (for backwards compatibility).
        
        ..  warning::   In Questionmark OnDemand, any attempt to change
                        the name of a participant using
                        :qm:meth:`SetParticipant` will be ignored
                        whereas in Perception and Classic OnDemand the
                        participant's user name will be changed.  For
                        compatibility you should not rely on being able
                        to change participant names. 
                            
    ..  qm:xfield:: Password string
        :optional:

        The user's password.  On creation this field must contain a
        password that satisfies the password policy in operation.  When
        reading participant information this field is always blank, on
        update you should leave it blank unless you want to force a
        password change in which case pass the new password in this
        field and ensure it satisfies the password policy.
        
    ..  qm:xfield:: First_Name string
        :optional:

    ..  qm:xfield:: Last_Name string
        :optional:

    ..  qm:xfield:: Middle_Name string
        :optional:

    ..  qm:xfield:: Use_Correspondence int
        :optional:

        This field is no longer used and should be set to 0.  See also
        :ref:`qmwise_optional`.        
        
    ..  qm:xfield:: Primary_Address_1 string
        :optional:

    ..  qm:xfield:: Primary_Address_2 string
        :optional:

    ..  qm:xfield:: Primary_City string
        :optional:

    ..  qm:xfield:: Primary_State string
        :optional:

    ..  qm:xfield:: Primary_ZIP_Code string
        :optional:

    ..  qm:xfield:: Primary_Country string
        :optional:

    ..  qm:xfield:: Primary_Phone string
        :optional:

    ..  qm:xfield:: Primary_Fax string
        :optional:

    ..  qm:xfield:: Primary_Email string
        :optional:

    ..  qm:xfield:: Secondary_Address_1 string
        :optional:

    ..  qm:xfield:: Secondary_Address_2 string
        :optional:

    ..  qm:xfield:: Secondary_City string
        :optional:

    ..  qm:xfield:: Secondary_State string
        :optional:

    ..  qm:xfield:: Secondary_ZIP_Code string
        :optional:

    ..  qm:xfield:: Secondary_Country string
        :optional:

    ..  qm:xfield:: Secondary_Phone string
        :optional:

    ..  qm:xfield:: Secondary_Fax string
        :optional:

    ..  qm:xfield:: Secondary_Email string
        :optional:

    ..  qm:xfield:: Salutation string
        :optional:

    ..  qm:xfield:: Organization_Name string
        :optional:

    ..  qm:xfield:: Department string
        :optional:

    ..  qm:xfield:: Title string
        :optional:

    ..  qm:xfield:: Assistant_Name string
        :optional:

    ..  qm:xfield:: Manager_Name string
        :optional:

    ..  qm:xfield:: Gender string
        :optional:

    ..  qm:xfield:: URL string
        :optional:

    ..  qm:xfield:: Details string
        :optional:

    ..  qm:xfield:: Details_1 string
        :optional:

    ..  qm:xfield:: Details_2 string
        :optional:

    ..  qm:xfield:: Details_3 string
        :optional:

    ..  qm:xfield:: Details_4 string
        :optional:

    ..  qm:xfield:: Details_5 string
        :optional:

    ..  qm:xfield:: Details_6 string
        :optional:

    ..  qm:xfield:: Details_7 string
        :optional:

    ..  qm:xfield:: Details_8 string
        :optional:

    ..  qm:xfield:: Details_9 string
        :optional:

    ..  qm:xfield:: Details_10 string
        :optional:

    ..  qm:xfield:: Details_11 string
        :optional:

    ..  qm:xfield:: Details_12 string
        :optional:

    ..  qm:xfield:: Details_13 string
        :optional:

    ..  qm:xfield:: Details_14 string
        :optional:

    ..  qm:xfield:: Details_15 string
        :optional:

    ..  qm:xfield:: Details_16 string
        :optional:

    ..  qm:xfield:: Details_17 string
        :optional:

    ..  qm:xfield:: Details_18 string
        :optional:

    ..  qm:xfield:: Details_19 string
        :optional:

    ..  qm:xfield:: Details_20 string
        :optional:

    ..  qm:xfield:: Authenticate_Ext int
        :optional:

        This field is no longer used and should be set to 0.  See also
        :ref:`qmwise_optional`.        
        
        
    ..  qm:xfield:: GroupIDList GroupIDList
        :optional:

        Used to return a list of IDs identifying the groups that the
        participant is a member of.
        
        ..  note::  On create and update this field is ignored.  You
                    cannot use this field to modify group memberships
                    using :qm:meth:`SetParticipant` or to enrole
                    participants automatically on creation.
        
    ..  qm:xfield:: Date_Registration string
        :optional:


..  qm:xtype::  GroupIDList

    ..  qm:xfield:: Group_ID string
        :optional:
        :max: unbounded    

        The ID of a group that the participant is a member of.


..  qm:xtype::  ParticipantList

    ..  qm:xfield:: Participant Participant
        :optional:
        :max: unbounded    


