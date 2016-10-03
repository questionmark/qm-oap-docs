Group
-----

..  od:service::    deliveryodata

..  od:type::   Group

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The numeric ID of the Group.
    
    ..  od:prop::   Name  Edm.String

        The name of the Group.
            
    ..  od:prop::   Description  Edm.String

        The optional description of the Group.

    ..  od:prop::   Participants  Participant
        :collection:
        
        Navigation property to the participants that are in the group.
    
    ..  od:prop::   Administrators  Administrator
        :collection:
        
        Navigation property to the administrators associated with the
        group.
    
    ..  od:prop::   SubGroups  Group
        :collection:
        
        Navigation property to the sub-groups of each group.
    
    ..  od:prop::   ParentGroup  Group
        
        For sub-groups, the optional parent group.
        
        ..  warning::   due to a known issue in the implementation of
                        this property it must only be expanded when the
                        Group being queried is known to be a sub-group.
                        Do not use it in general collections::
                        
                            <service root>/Groups?$expand=ParentGroup
                
    ..  od:prop::   PrintBatches  PrintBatch
        :collection:

        Navigation property to any PrintBatches associated with this Group.
