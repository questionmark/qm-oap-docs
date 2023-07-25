Assessment
----------

..  od:service::    deliveryodata


..  od:feed::   Assessments Assessment
    
    :method GET: feed is read only
    :filter ID: primary key
    :filter Name: assessment name
    :expand Results: expands the associated Results    

    The Assessments feed provides information about the assessment
    catalog. That is, all the assessments that have been published for
    delivery.


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
        
    ..  od:prop::   ModifiedDateTime  Edm.DateTime
        :notnull:

        See :qm:field:`S_Header_Ex.Modified_Date`.
        
    ..  od:prop::   Base  Edm.Boolean
        :notnull:

        See :qm:field:`S_Header_Ex.Base`.
        
    ..  od:prop::   TimeLimit  Edm.Int32

        See :qm:field:`S_Header_Ex.Time_Limit`.

        .. versionadded::   2019.02
        
    ..  od:prop::   IsSecure  Edm.Boolean
        :notnull:

        A boolean indicating whether or not the *author* of the
        assessment has designated this assessment as for secure delivery
        only. Assessment entities with this flag set to True will not be
        available for scheduling (through the portal user interface)
        with a :od:type:`MonitoringType` that does not require use of
        Questionmark Secure.

        .. versionadded::   2020.08

    ..  od:prop::   SaveAnswers  Edm.Boolean
        :notnull:

        A boolean indicating whether or not this assessment is configured
        to save answers during delivery.  Assessments with this flag set
        to False **must not** be used with the :od:type:`Schedule` entity.

        .. versionadded::   2020.08

    ..  od:prop::   RulesOfConductID  Edm.Int32

        The ID of an associated :od:type:`RulesOfConduct` entity.  See
        :od:prop:`Assessment.RulesOfConduct` for more information.

        .. versionadded::   2021.08

    ..  od:prop::   Type    Edm.Int16

        Reserved for future use.

    ..  od:prop::   AssessmentOutcomes AssessmentOutcome
        :collection:
    
        Navigation property to the collection of AssessmentOutcomes
        possible for this Assessment.

        .. versionadded::   2020.08

    ..  od:prop::   AssessmentTranslations AssessmentTranslation
        :collection:
    
        Navigation property to the collection of AssessmentTranslations
        of this (base language) Assessment.

        .. versionadded::   2018.12

    ..  od:prop::   AssessmentSnapshots AssessmentSnapshot
        :collection:
    
        Navigation property to the collection of AssessmentSnapshots
        created from this Assessment.

        .. versionadded::   2020.02

    ..  od:prop::   Results  Result
        :collection:
        
        Navigation property to the collection of result entities
        associated with this assessment.

    ..  od:prop::   Groups  Group
        :collection:

        .. versionadded::   2017.11
        
        Navigation property to the collection of Group entities
        associated with this assessment.  Assessments are associated
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

    ..  od:prop::   RulesOfConduct  RulesOfConduct
        
        Navigation property to an optional :od:type:`RulesOfConduct`
        entity associated with this assessment.  When scheduling this
        assessment the associated rules of conduct are used instead of
        the default rules defined by the :od:type:`MonitoringType` used.
        These rules may themselves be overridden in the
        :od:type:`Schedule` entity itself.

        .. versionadded::   2021.08
        

..  od:type::   AssessmentOutcome

    An AssessmentOutcome is a defined score band associated with an
    assessment.

    .. versionadded::   2020.08

    ..  od:prop::   ID  Edm.Int64
        :key:
        :notnull:

        The full ID of the assessment related to this outcome, see
        :od:prop:`Assessment.ID` for details.

    ..  od:prop::   ScoreBandNumber  Edm.Int32
        :key:
        :notnull:

        The number of the outcome (score band), unique within each
        Assessment.

    ..  od:prop::   AssessmentName  Edm.String

        The name of the related Assessment.

    ..  od:prop::   ScoreBandTitle  Edm.String

        The title of this outcome, for example "Pass" or "Fail".
    
    ..  od:prop::   Assessment Assessment
        :notnull:
        
        Navigation property to the Assessment.
    

..  od:type::   AssessmentTranslation

    ..  od:prop::   ID                  Edm.Int64
        :key:
        :notnull:

        The ID of the :od:type:`Assessment` that this is a translation
        of.
        
    ..  od:prop::   Language            Edm.String
        :key:
        :notnull:

        The language this translation is represented by.
        
    ..  od:prop::   Revision            Edm.Int32
        :notnull:

        The revision of the Assessment that was translated.
        
    ..  od:prop::   Name         Edm.String
    
        The translated name of the Assessment.
        
    ..  od:prop::   Author              Edm.String
    
        The name of the user that created this translation.
            
    ..  od:prop::   CreatedDateTime     Edm.DateTime
        :notnull:

        The date and time this translation was created.
        
    ..  od:prop::   Editor              Edm.String

        The name of the user that last modified this translation.
 
    ..  od:prop::   ModifiedDateTime    Edm.DateTime
        :notnull:

        The date and time this translation was last modified.

    ..  od:prop::   TimeLimit  Edm.Int32

        Reserved for future use.
        
    ..  od:prop::   Assessment Assessment

        A navigation property to the base language version of the
        assessment.
        