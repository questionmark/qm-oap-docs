Administrator
-------------

..  od:service::    deliveryodata


..  od:feed::   Administrators Administrator

    :method GET: returns the feed of Administrators
    :method POST: creates an Administrator *with no role*
    :method PATCH: updates an Administrator
    :method DELETE: deletes an Administrator
    :filter ID: primary key
    :filter Name: administrator name
    :expand Groups: associated groups
    :expand TestCenters: associated test centers

    The Administrators feed contains data about users with administrator
    roles in the user data base.  A user with an administrator role is
    defined as being a user with *any* role other than special
    Participant role.

    The feed can be used to create, update and delete Administrators. 
    Note that creating an Administrator editor does not associate the
    new user with any role.  You can use the :od:action:`Upsert` action
    to create a user with one or more existing Administrator roles.

    If you want to promote a user that exists in the Portal as a
    Participant (or as an authenticated user with no assigned role) to
    being an Administrator then you may POST to the Administrators feed
    to create the entity representing the user and then assign the
    additional roles but the recommended approach would be to use the
    :od:action:`Upsert` action.
    
    ..  od:action:: Upsert
        :input: Name Edm.String, Email Edm.String, Password Edm.String, FirstName Edm.String, LastName Edm.String, Department Edm.String, SsoId Edm.String, Url Edm.String, AlternateName Edm.String, Roles Collection(Edm.String), Groups Collection(Edm.String)

        .. versionadded::   2021.08
                
        To invoke this action use http POST with a JSON body like this::
        
            POST /deliveryodata/<customer-id>/Administrators/Upsert
            
            {
                "Name": "bob",
                "Email": "bob@example.com",
                "Groups": ["GroupA", "GroupB"],
                "Roles": ["Author", "Reporter"]
            }

        The action creates the user if they don't exist or updates an
        existing user with matching Name.  Omitted parameters are
        ignored. The Groups parameter contains a list of Group names
        that are used to assign the user as an owner of those groups. 
        (Only root groups may be specified.)  The Roles parameter
        contains a list of Role names that should be assigned to the
        user.
        
        The purpose of Upsert is to provide a more efficient
        implementation of the individual combined operations to reduce
        the impact of network latency on integrated systems.
        

..  od:type::   Administrator

    Administrator entities are drawn from :qm:table:`G_User` in the data
    model but contain only a subset of the properties.  They are read
    only in OData.

    ..  od:prop::   Password Edm.String
    
        The Administrator's password.  This field is not available
        during a GET operation and will always appear to be set to null
        but it can be provided when creating (POST) or updating (PATCH)
        an Administrator's record.        

        .. versionadded::   2021.05

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

    ..  od:prop::   SsoId  Edm.String

        .. versionadded::   2021.05

    ..  od:prop::   Url  Edm.String

        .. versionadded::   2021.05

    ..  od:prop::   AlternateName  Edm.String

        .. versionadded::   2021.05

    ..  od:prop::   Groups  Group
        :collection:
        
        Navigation property to the Groups associated with this
        administrator as per :qm:table:`G_Owner`.  An Administrator may
        be associated with multiple Group entities.

        Ownership is currently limited to root groups, that is, Groups
        where the RootGroupID matches the Group ID (and the navigation
        property ParentGroup is empty).
        
        You can modify this list using the special $links property.
        
        .. versionadded::   2021.08

        To add a Group to the list you must use the full URL of the
        Group Entity and POST it to the following URL::
        
            POST /deliveryodata/<customer-id>/Administrator(<administrator-id>)/$links/Groups
            
            {
                "url": "https://<platform>/deliveryodata/<customer-id>/Groups(<group-id>)"
            }

        You must replace <customer-id>, <administrator-id>, <platform>
        and <group-id> accordingly.

        To remove a Group membership use the DELETE operation as follows::
        
            DELETE /deliveryodata/<customer-id>/Administrator(<administrator-id>)/$links/Groups(<group-id>)
        

    ..  od:prop::   Roles  Role
        :collection:
        
        Navigation property to the Roles associated with this
        administrator.  An Administrator may be associated with multiple
        Role entities *or no Role entities*.  In the latter case, the
        user is merely an authenticated user of the platform and not an
        administrator at all.  This behaviour enables Administrators to
        be created *with the API* without an associated Role and for the
        Role to be added by a later call.  Users created without a role
        through the Portal user interface do not appear in the
        Administrators feed until they are assigned a non-Participant
        role *in the user interface*.

        You can modify this list using the special $links property.
        
        .. versionadded::   2021.08

        To add a Role to the list you must use the full URL of the
        Role Entity and POST it to the following URL::
        
            POST /deliveryodata/<customer-id>/Administrator(<administrator-id>)/$links/Roles
            
            {
                "url": "https://<platform>/deliveryodata/<customer-id>/Groups(<role-id>)"
            }

        You must replace <customer-id>, <administrator-id>, <platform>
        and <role-id> accordingly.  Note that Role IDs are actually
        strings with the name of the Role, e.g., Roles('Author').

        To remove a Group membership use the DELETE operation as follows::
        
            DELETE /deliveryodata/<customer-id>/Administrator(<administrator-id>)/$links/Roles(<group-id>)
        
        ..  warning::   DELETE operation planned for release in 2022


    ..  od:prop::   TestCenters  TestCenter
        :collection:
        
        .. versionadded::   2017.11

        Navigation property to the TestCenters associated with this
        administrator as per :qm:table:`G_Test_Center_Owner`.  An
        Administrator may be associated with multiple TestCenter
        entities.
        
        The client application can use this information to control
        access to TestCenter-specific functions such as opening
        TestCenters and proctoring exams being taken on site.

    ..  od:action:: CheckPassword Edm.Boolean
        :input: Password Edm.String
        
        .. versionadded:: 2021.05

        Returns True if the input parameter matches the password set for
        this administrator and False otherwise.

    ..  od:action::   AllGroups Group
        :collection:
        :input: GroupName Edm.String
        
        .. versionadded::   2020.03
        
        ..  warning::   Previously documented as a navigation property
                        in error.

        An action that evaluates all Groups owned by this administrator
        as per :qm:table:`G_Owner` *including all sub-groups* owned by
        inheritance.  The required GroupName parameter is a filter
        limiting the list of returned groups to those that contain the
        filter string.  GroupName may be passed as the empty string to
        return an unfiltered list.        

    ..  od:action:: ActionableSchedulesForObservation ActionableSchedule
        :collection:

        .. versionadded:: 2017.11

        Returns a collection of actionable schedules related to this
        administrator *as an assessment observer*.  It takes no
        parameters and is bound to a specific Administrator so is called
        like this::
        
            POST /deliveryodata/<customer-id>/Administrator(456789)/ActionableSchedulesForObservation
            
            {
            }


..  od:type::   Role

    Role entities are simple entities that allow access to read the list
    of roles defined in the portal.
    
    This entity is subject to change.

        .. versionadded::   2021.05

    ..  od:prop::   ID  Edm.String
        :key:
        :notnull:
