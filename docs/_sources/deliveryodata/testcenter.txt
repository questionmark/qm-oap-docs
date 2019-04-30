TestCenter
----------

..  od:service::    deliveryodata


..  od:feed::   TestCenters TestCenter

    :method GET: for reading test centres
    :filter ID: the primary key
    :filter Name: the test center name

    $orderby is *not* supported.


..  od:type::   TestCenter

    .. versionadded::   2017.11

    The information in this entity is read directly from the
    :qm:table:`G_Test_Center` table.
    
    ..  od:prop::   ID      Edm.Int32
        :notnull:

        The ID of this TestCenter.
        
    ..  od:prop::   Label      Edm.String

    ..  od:prop::   Name      Edm.String

    ..  od:prop::   Department      Edm.String

    ..  od:prop::   Location      Edm.String

    ..  od:prop::   Active      Edm.Boolean

    ..  od:prop::   TimeZone      Edm.String

    ..  od:prop::   SupportedTechnology      Edm.Int16

    ..  od:prop::   Capacity      Edm.Int32

    ..  od:prop::   Address1      Edm.String

    ..  od:prop::   Address2      Edm.String

    ..  od:prop::   City      Edm.String

    ..  od:prop::   State      Edm.String

    ..  od:prop::   ZipCode      Edm.String

    ..  od:prop::   Country      Edm.String

    ..  od:prop::   Phone      Edm.String

    ..  od:prop::   Fax      Edm.String

    ..  od:prop::   Logo      Edm.String

    ..  od:prop::   AdminEmail      Edm.String

    ..  od:prop::   Properties      Edm.String

    ..  od:action:: Open
        :input: ExternalAttemptListID Edm.String
        
        Opens a TestCenter.  Opening a test center creates a new
        AttemptList entity, marks it as open and associates
        it with the TestCenter.  The AttemptList is created with
        the given ExternalAttemptListID which must be unique.
        
        For example::
        
            POST /deliveryodata/<customer-id>/TestCenter(3824)/Open
            
            {
                "ExternalAttemptListID": "94a253aa-6a2e-48f2-9031-ebd343a5dfd1"
            }

        To avoid errors from race conditions if you call the Open action
        on a TestCenter that is already open and you pass the
        ExternalAttemptListID of the current open AttemptList then a
        success code is returned and no further action is taken.

    ..  od:action:: Close

        Closes a TestCenter.  The associated AttemptList is closed but
        it remains associated with the TestCenter.
        
    ..  od:prop::   Administrators  Administrator
        :collection:

        The administrators that have been set as owners of this
        TestCenter.
                
    ..  od:prop::   Schedules  Schedule
        :collection:

        The associated schedules

    ..  od:prop::   AttemptLists  AttemptList
        :collection:

        Each time a TestCenter is opened it is associated with an
        AttemptList that is then used to group together the Attempts
        that are proctored together.  Each AttemptList represents a
        single session or sitting.
