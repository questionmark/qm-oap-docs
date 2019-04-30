Group
-----

..  od:service::    deliveryodata


..  od:feed::   Groups Group

    :method GET: read only
    :filter ID: primary key
    :filter Name: filtering by group name
    :filter RootGroupID: filtering by the top-level group (expected in 2018.02)
    :expand Administrators: the administrators responsible for the group
    :expand Participants: the participant members of the group
    :expand SubGroups: the optional list of sub-groups
    :expand ParentGroup: the optional parent group (:od:prop:`see warning <Group.ParentGroup>`)
    :expand PrintBatches: the optional list of associated PrintBatches

    The Groups feed contains data about groups of participants.  Entries
    are defined by the :od:type:`Group` type.


..  od:type::   Group

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The numeric ID of the Group.
    
    ..  od:prop::   Name  Edm.String

        The name of the Group.
            
    ..  od:prop::   Description  Edm.String

        The optional description of the Group.

    ..  od:prop::   RootGroupID  Edm.Int32
        :notnull:

        .. versionadded::   2017.11

        The numeric ID of the Group's top-level parent.  The group
        hierarchy does not have a single root node but instead supports
        multiple *root* groups that may have sub-groups (see
        :od:prop:`SubGroups`). For any group you can obtain the ID of
        the top-level group that contains this one using the
        RootGroupID.  For root groups themselves this value will be the
        same as :od:prop:`ID`.

    ..  od:prop::   Participants  Participant
        :collection:
        
        Navigation property to the participants that are in the group.
    
    ..  od:prop::   Administrators  Administrator
        :collection:
        
        Navigation property to the administrators associated with the
        group (sometime referred as group owners though role-based
        permissions are out of scope for this API)
    
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

    ..  od:prop::   AncestorGroups  Group
        :collection:
        
        .. versionadded::   2018.05

        Navigation property to all ancestors of this group *including
        the group itself*.  A group is in the collection of ancestors if
        it is the group itself or if it is a parent of a member of the
        collection.  This recursive definition ensures that all groups
        up to the root group are in the collection.

    ..  od:prop::   DescendantGroups  Group
        :collection:
        
        .. versionadded::   2018.05

        Navigation property to all descendants of this group *including
        the group itself*.  A group is in the collection of descendents
        if it is the group itself or if it is a subgroup of a member of
        the collection.  This recursive definition ensures that all
        subgroups possible by repeated expansion are included in a
        single filterable collection.
                            
    ..  od:prop::   SchedulableAssessments  Assessment
        :collection:

        .. versionadded::   2017.11

        All the assessments that have had scheduling permissions
        associated with this Group.  See :od:prop:`Assessment.Groups`
        for more information.

    ..  od:prop::   PrintBatches  PrintBatch
        :collection:

        Navigation property to any PrintBatches associated with this Group.
