Administrator
-------------

..  od:service::    deliveryodata

..  od:type::   Administrator

    Administrator entities are drawn from :qm:table:`G_User` in the data
    model but contain only a subset of the properties.  They are read
    only in OData.
    
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:
        
        See :qm:field:`G_User.User_ID`.

    ..  od:prop::   Name  Edm.String
        
        See :qm:field:`G_User.User_Name`.

    ..  od:prop::   FirstName  Edm.String
        
        See :qm:field:`G_User.First_Name`.

    ..  od:prop::   LastName  Edm.String
        
        See :qm:field:`G_User.Last_Name`.

    ..  od:prop::   Department  Edm.String
        
        See :qm:field:`G_User.Department`.

    ..  od:prop::   Email  Edm.String
        
        See :qm:field:`G_User.Email`.

    ..  od:prop::   Groups  Group
        :collection:
        
        Navigation property to the Groups associated with this
        administrator as per :qm:table:`G_Owner`.  An Administrator may
        be associated with multiple Group entities.