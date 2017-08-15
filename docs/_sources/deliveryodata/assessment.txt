Assessment
----------

..  od:service::    deliveryodata

..  od:type::   Assessment

    Assessment entities are drawn from :qm:table:`S_Header_Ex` in the
    data model but contains only a subset of the properties.  They are
    read only in OData.
    
    ..  od:prop::   ID  Edm.Int64
        :key:
        :notnull:

        The full ID of the assessment, see
        :qm:field:`S_Header_Ex.Session_MID` for details of the
        underlying representation in the data model.
        
        ..  warning::   when serialised to JSON format, 64-bit integers
                        are converted to strings, even though they are
                        still correctly identified as 64-bit integers in
                        the metadata model.  OData aware tools should
                        correctly convert to a native integer type but
                        if you are parsing the JSON directly then you
                        should be aware that these strings differ from
                        the string representation used for the same ID
                        when used in QMWISe methods.  For details see
                        :ref:`assessmentid`.

    ..  od:prop::   Revision  Edm.Int32
        :notnull:

        See :qm:field:`S_Header_Ex.Revision`.
        
    ..  od:prop::   Name  Edm.String

        See :qm:field:`S_Header_Ex.Session_Name`.
        
    ..  od:prop::   Language  Edm.String

        See :qm:field:`S_Header_Ex.Lang`.
        
    ..  od:prop::   Description  Edm.String

        See :qm:field:`S_Header_Ex.Description`.
        
    ..  od:prop::   Author  Edm.String

        See :qm:field:`S_Header_Ex.Author`.
        
    ..  od:prop::   CreatedDateTime  Edm.DateTime
        :notnull:

        See :qm:field:`S_Header_Ex.Created_Date`.
        
    ..  od:prop::   Editor  Edm.String

        See :qm:field:`S_Header_Ex.Editor`.
        
    ..  od:prop::   Modified_Date  Edm.DateTime
        :notnull:

        See :qm:field:`S_Header_Ex.Modified_Date`.
        
    ..  od:prop::   Base  Edm.Boolean
        :notnull:

        See :qm:field:`S_Header_Ex.Base`.
        
    ..  od:prop::   Results  Result
        :collection:
        
        Navigation property to the collection of result entities
        associated with this assessment.

    ..  od:prop::   Groups  Group
        :collection:

        .. versionadded::   2017.10 (TBC) 
        
        Navigation property to the collection of Group entities
        associated with this assessment.  Assessments are a associated
        with groups through the concept of "Scheduling Permissions" that
        are set on *Published* Assessments.  By assigning a group to an
        assessment you enable (administrator) members of that group to
        create schedules for that assessment.
        
        These associations are used by the QMWISe method
        :qm:meth:`GetAssessmentListByAdministrator` to determine which
        assessments are returned.  This constrasts with the
        author-centric associations returned by
        :qm:meth:`GetAssessmentTreeByAdministrator` that are *not*
        available through OData.
        
        This relationship is represented in the model by
        :qm:table:`G_Session`.