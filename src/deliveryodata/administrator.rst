Administrator
-------------

..  od:service::    deliveryodata


..  od:feed::   Administrators Administrator

    :method GET: feed is read only
    :filter ID: primary key
    :filter Name: administrator name
    :expand Groups: associated groups
    :expand TestCenters: associated test centers

    The Administrators feed contains data about users with administrator
    roles in the user data base.  A user with an administrator role is
    defined as being a user with *any* role other than special
    Participant role.


..  od:type::   Administrator

    Administrator entities are drawn from :qm:table:`G_User` in the data
    model but contain only a subset of the properties.  They are read
    only in OData.

    ..  od:prop::   Password Edm.String
    
        The Administrator's password.  This field is not available
        during a GET operation and will always appear to be set to null
        but it can provided when creating (POST) or updating (PATCH) an
        Administrator's record.        

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

    ..  od:prop::   AllGroups  Group
        :collection:

        .. versionadded::   2020.03
        
        Navigation property to the Groups associated with this
        administrator as per :qm:table:`G_Owner` *including all
        sub-groups* owned by inheritance.  An Administrator may be
        associated with multiple Group entities.

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

        .. versionadded::   2021.05

    ..  od:prop::   ID  Edm.String
        :key:
        :notnull:
