TestCenter
----------

..  od:service::    deliveryodata

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

    ..  od:prop::   Administrators  Administrator
        :collection:

        The administrators that have been set as owners of this
        TestCenter.
                
    ..  od:prop::   Schedules  Schedule
        :collection:

        The associated schedules
