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
        :qm:field:`S_Header_Ex.Session_MID`.
        
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