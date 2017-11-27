MonitoringType
--------------

..  od:service::    deliveryodata

..  od:type::   MonitoringType

    .. versionadded::   2017.07

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

        .. versionadded::   2017.11
        
        A flag indicating whether or not Attempts launched with this
        MonitoringType *MUST* use Questionmark's Secure Browser
        technology.

    ..  od:prop::   RequireDeviceEvents  Edm.Boolean
        :notnull:

        .. versionadded::   2017.11
        
        A flag indicating whether or not Attempts launched with this
        Monitoring type *MUST* use Questionmark's next-generation device
        monitoring technology.  Requires a next-generation Questionmark
        Secure Browser client (expected early 2018).

    ..  od:prop::   SystemCheckUrl   Edm.String

        .. versionadded::   2017.11
        
        An optional URL that will be displayed to the participant on
        entering the exam lobby to assist with checking compatibility
        of the participant's device against the technology requirements
        of this monitoring technology.

        The special URL "about:blank" should be used to indicate that no
        system check page is required.  A null value means that the
        default system check will be used.
