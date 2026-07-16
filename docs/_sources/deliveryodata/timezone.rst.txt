Timezone
--------

..  od:service::    deliveryodata


..  od:feed::   Timezones Timezone

    :method GET: for reading test centres
    :filter ID: the primary key

    ..  od:action:: GetSupportedTimezones Timezone
        :collection:
        :input: ProctorProviderId Edm.Int32

        Reserved for internal use.


..  od:type::   Timezone

    .. versionadded::   2021.05

    This entity is subject to change and is reserved for future use.
        
    ..  od:prop::   ID      Edm.String
        :notnull:
        :key:

        The ID of this Timezone.

    ..  od:prop::   Name    Edm.String

        The name of this Timezone.

    ..  od:prop::   BaseUTCOffset    Edm.String

    ..  od:prop::   BaseUTCOffsetMinutes    Edm.Double
        :notnull:

    ..  od:prop::   CurrentUTCOffset    Edm.String

    ..  od:prop::   CurrentUTCOffsetMinutes    Edm.Double
        :notnull:

    ..  od:prop::   CurrentUTCTime    Edm.DateTime
        :notnull:

        The current time in UTC.

    ..  od:prop::   CurrentTimezoneTime    Edm.DateTime
        :notnull:

        The local time in this timezone.
