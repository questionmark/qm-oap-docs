MonitoringTypes and ProctoringProviders
---------------------------------------

..  od:service::    deliveryodata


..  od:feed::   MonitoringTypes MonitoringType

    :method GET: read only
    :filter ID: primary key
    :filter Name: the symbolic name of this monitoring type

    $orderby is *not* supported.

    The MonitoringTypes feed contains data about methods of monitoring
    assessments. Entries are defined by the :od:type:`MonitoringType`
    type.


..  od:feed::   ProctoringProviders ProctoringProvider

    :method GET: read only
    :filter ID: primary key
    :filter Name: the symbolic name of this monitoring type

    $orderby is *not* supported.

    .. versionadded::   2018.04

    The ProctoringProviders feed contains data about the configuration
    of external proctoring providers integrated through a proctoring
    API. Entries are defined by the :od:type:`ProctoringProvider` type.

    ..  od:action:: AppointmentDateRange Edm.String
        :input: TimeZoneID Edm.String, AttemptID Edm.Int32

        Reserved for internal use.


..  od:type::   MonitoringType

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The numeric ID of this monitoring type.
    
    ..  od:prop::   Name  Edm.String

        A language-independent name to be used as an alternative key for
        this monitoring type.  This version of the key is used to
        look-up language dependent human-readable text and is set to a
        (readable) symbolic textual identifier for this type of
        monitoring. Example values are: "UNMONITORED",
        "QSB_WITH_EVENTS", etc.
        
        You should not assume any specific behaviour based purely on the
        name. Monitoring types contain additional attributes that
        determine how (monitored) attempts are launched by the
        participant, some of which are exposed here to help API
        consumers to select an appropriate type for a specific Schedule
        or Attempt.
            
    ..  od:prop::   RequireQSB  Edm.Boolean
        :notnull:
        
        A flag indicating whether or not Attempts launched with this
        MonitoringType *MUST* use Questionmark's Secure Browser
        technology.

    ..  od:prop::   RequireDeviceEvents  Edm.Boolean
        :notnull:
        
        A flag indicating whether or not Attempts launched with this
        Monitoring type *MUST* use Questionmark's next-generation device
        monitoring technology.  Requires a next-generation Questionmark
        Secure Browser client.

    ..  od:prop::   SystemCheckUrl   Edm.String
        
        An optional URL that will be displayed to the participant on
        entering the exam lobby to assist with checking compatibility
        of the participant's device against the technology requirements
        of this monitoring technology.

        The special URL "about:blank" should be used to indicate that no
        system check page is required.  A null value means that the
        default system check will be used.

    ..  od:prop::   ProctoringProviderId   Edm.Int32

        The ID of the optional ProctoringProvider entity.  See also
        :od:prop:`ProctoringProvider`.

    ..  od:prop::   ProctoringProviderOptions   Edm.String

        A text string containing options to be used in conjunction with
        the associated ProctoringProvider.  This property means that it
        is possible to use the same provider (including API credentials)
        in multiple different configurations, each with its own
        associated MonitoringType.

    ..  od:prop::   ProctoringProvider  ProctoringProvider
        
        An optional navigation property to the ProctoringProvider
        associated with this monitoring type.

    ..  od:prop::   RequireTestCenter   Edm.Boolean

        If True, any associated Schedule entity created with this
        MonitoringType is required to have an associated TestCenter.

        Attempts associated with this MonitoringType must be associated
        with an AttemptList and an open TestCenter: these constraints
        are implemented automatically when using the actions related to
        the :od:type:`Schedule` entity to start or resume an assessment.

    ..  od:prop::   TranslationToolLangs  Edm.String

        .. versionadded::   2021.08

        Languages supported for translation tools.

    ..  od:prop::   TextToSpeech  Edm.Boolean

        .. versionadded::   2021.08

        If True, text-to-speech is enabled for this monitoring type.

    ..  od:prop::   RequireObserver  Edm.Boolean

        .. versionadded::   2021.08

        If True, an observer is required for attempts using this type.

    ..  od:prop::   RequireConfirmation  Edm.Boolean

        .. versionadded::   2021.08

        If True, confirmation is required before starting.

    ..  od:prop::   RequirePasscode  Edm.Boolean

        .. versionadded::   2021.08

        If True, a passcode is required to start the assessment.

    ..  od:prop::   Category  Edm.String

        .. versionadded::   2021.08

        A category for grouping monitoring types.

    ..  od:prop::   Disabled    Edm.Boolean

        .. versionadded::   2020.06
                    
        A MonitoringType can be disabled by setting this flag to True.
        When disabled, all associated Schedules become inactive and
        Attempts cannot be launched.

    ..  od:prop::   RulesOfConductID  Edm.Int32

        The ID of an associated :od:type:`RulesOfConduct` entity.  See
        :od:prop:`MonitoringType.RulesOfConduct` for more information.

        .. versionadded::   2021.08

    ..  od:prop::   RulesOfConduct  RulesOfConduct
        
        Navigation property to an optional :od:type:`RulesOfConduct`
        entity associated with this assessment.  When scheduling with
        this monitoring type the associated rules of conduct are used by
        default. These rules may themselves be overridden in the
        :od:type:`Assessment` or :od:type:`Schedule` entities.

        .. versionadded::   2021.08


..  od:feed::   RulesOfConduct RulesOfConduct

    :method GET: reading rules of conduct entities
    :method POST: creating rules of conduct entities
    :method PATCH: limited support for some properties, see property descriptions for details

    The RulesOfConduct feed contains all the defined rules of conduct.


..  od:type::   RulesOfConduct

    .. versionadded::   2021.05

    The rules of conduct entity is used to create a template for a set
    of rules for conducting an assessment.  The template contains two
    HTML-fragments, one that will be presented to the Participant at the
    start of the test and one that will be presented to the Proctor
    overseeing the process.
    
    Rules of conduct may be associated with :od:type:`MonitoringType`,
    :od:type:`Assessment` or :od:type:`Schedule` entities.  The rules
    that are active for an attempt are determined by looking first at
    the Schedule, then at the Assessment and finally at the
    MonitoringType itself.
    
    Rules of conduct may be made available in multiple languages and,
    where available, the lobby will attempt to match the language used
    for the rules of conduct to the user interface language selected by
    the participant on entry.
        
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

    ..  od:prop::   Name  Edm.String

        The name of this rules templates.
        
    ..  od:prop::   ParticipantRules  Edm.String
    
        A string containing an HTML fragment (such as a <div>) that will
        be shown to the participant in the lobby prior to starting the
        assessment.  The participant must click to acknowledge that they
        have read and agree to the rules.

    ..  od:prop::   ProctorRules  Edm.String
    
        A string containing an HTML fragment that may be shown to the
        proctor.  Visibility of proctor-facing rules depends on the
        proctoring provider.

    ..  od:prop::   Language  Edm.String

    ..  od:prop::   CreatedDateTime  Edm.DateTime

    ..  od:prop::   ModifiedDateTime  Edm.DateTime

    ..  od:prop::   RulesOfConductTranslations  Edm.RulesOfConductTranslation
    

..  od:type::   RulesOfConductTranslation

    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

    ..  od:prop::   ParticipantRules  Edm.String

    ..  od:prop::   ProctorRules  Edm.String

    ..  od:prop::   Language  Edm.String
        :key:

    ..  od:prop::   CreatedDateTime  Edm.DateTime

    ..  od:prop::   ModifiedDateTime  Edm.DateTime

    ..  od:prop::   RulesOfConduct  RulesOfConduct

         

..  od:feed::   RulesOfConductTranslations RulesOfConductTranslation

    :method GET: read only
    :filter ID: the rules of conduct ID
    :filter Language: the translation language

    The RulesOfConductTranslations feed provides access to translated
    versions of rules of conduct.

..  od:type::   ProctoringProvider

    .. versionadded::   2018.04

    An entity used to hold the API credentials and connection
    information associated with an external provider of proctoring
    services.
    
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The numeric ID of this proctoring provider entity, allocated
        automatically by the API.
    
    ..  od:prop::   Name  Edm.String
    
        The human readable string identifier to use for the proctoring
        provider.

    ..  od:prop::   Protocol  Edm.String
    
        The protocol to use when communicating with the proctoring
        provider.  This property's value is taken from a limited
        vocabulary of supported protocols.  Information about the
        allowable values will be published in future versions of the
        documentation.

    ..  od:prop::   Url  Edm.String

        The URL of the provider's API endpoint.

    ..  od:prop::   Key  Edm.String

        The API key to use with the provider's API endpoint.

    ..  od:prop::   Secret  Edm.String

        The API secret to use with the provider's API endpoint.  Although
        this value may be POSTed when creating an entity and updated
        using PATCH it cannot be read back and is replaced by an encrypted
        version in the response to GET requests.

    ..  od:prop::   WebhookSecret  Edm.String

        .. versionadded::   2021.05

        The API secret that has been given to the proctoring provider
        for use with Webhook-based callbacks.  Although this value may
        be POSTed when creating an entity and updated using PATCH it
        cannot be read back and is replaced by an encrypted version in
        the response to GET requests.
        
        The supported Webhooks are determined by the
        :od:prop:`Protocol`.

    ..  od:prop::   MonitoringTypes  MonitoringType
        :collection:
        
        A navigation property to the MonitoringTypes that are associated
        with this ProctoringProvider entity.
    
    ..  od:action:: AvailableAppointments Edm.DateTime
        :collection:
        :input: LocalDate Edm.DateTime, TimeZoneID Edm.String, AttemptID Edm.Int32

        Reserved for internal use.
    
