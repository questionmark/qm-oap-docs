Scheduled Delivery
------------------

.. versionadded::   2017.07

.. warning::    This page documents parts of the API that should be
                considered to be of 'alpha' quality.  The details *are*
                subject to change in future versions.
                
The Delivery OData API contains a brand new schedule entity to enable
the scheduling of assessments from third-party applications, including
the scheduling of assessments that require special procotring.

Classic vs Next Generation Schedules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Classic schedules are described by the database tables
:qm:table:`G_Schedule` and :qm:table:`G_Schedule_Details` and by the
QMWISe schema type :qm:xtype:`Schedule`.

Classic schedules are the *only* way to schedule assessments in
Perception 5.

Next-generations schedules are being introduced with OnDemand 2017.07
and will gradually become the preferred way to schedule assessments in
Questionmark OnDemand and OnPremise.


Scheduling Permissions
~~~~~~~~~~~~~~~~~~~~~~

Permission to schedule an assessment is controlled by Group.  An
association exists between :od:type:`deliveryodata.Assessment` and
:od:type:`deliveryodata.Group` entities.  This association indicates
that *only* administrators that are owners of (one of) the associated
groups may schedule that assessment.  In the Questionmark portal the
types of action that a particular administrator may perform are further
limited by role and the permissions associated with that role.  Role
information is not exposed by the APIs.

To obtain a list of assessments that a given Administrator is associated
with you need to look at the Groups associated with that administrator
*and* the SchedulableAssessments associated with those groups::

    GET /deliveryodata/<customer_id>/Administrators(12345)/Groups?$expand=SchedulableAssessments

    {
        "odata.metadata": "https://ondemand.questionmark.com/deliveryodata/<customer-id>/$metadata#Groups",
        "value": [
            {
                "SchedulableAssessments": [
                    {
                        "ID": "3000000003",
                        "Revision": 1,
                        "Name": "Sample Test",
                        "Language": "-",
                        "Description": null,
                        "Author": "Manager",
                        "CreatedDateTime": "2017-03-14T18:04:39Z",
                        "Editor": "Manager",
                        "ModifiedDateTime": "2017-04-06T09:16:22Z",
                        "Base": true
                    }
                ],
                "ID": 517208256,
                "Name": "Test_Group",
                "Description": "",
                "RootGroupID": 517208256
            }
        ]
    }

In the above response the administrator is associated with a single
Group (called "Test_Group" and that group is associated with a single
"Sample Test" assessment.

Bear in mind that it is possible for the same assessment to show up
multiple times (associated with different groups) so if you are
processing a response to this message to create a flat list you will
have to remove duplicates.

For very long lists the Groups themselves may prove a useful way to
hierarchically present the assessment list to the end user for selection.


Creating a Schedule
~~~~~~~~~~~~~~~~~~~

To create a schedule you POST to the Schedules feed endpoint.  There are
only a few required pieces of information.  A human-readable Name for
the schedule, the AssessmentID of the assessment to be scheduled, one of
GroupID or ParticipantID to identify who the schedule is for and the ID
of a monitoring type that describes how the assessment will be monitored
(e.g., proctored versus unproctored).

You can obtain a list of MonitoringTypes directly from the API::

    GET /deliveryodata/<customer-id>/MonitoringTypes

Monitoring types do not have human-friendly names, they have symbolic
names that are designed to be used as keys to translated text for a
multi-lingual user interface.  Once you have selected a monotring type
use its ID when creating a schedule::

    POST /deliveryodata/<customer-id>/Schedules

    {
        "Name": "Demo Schedule",
        "AssessmentID": "3000000003",
        "GroupID": 517208256,
        "MonitoringTypeID": 1
    }

This creates a schedule for the Sample Test returned in the previous
example for all members of the group with ID 517208256 (the "Test_Group"
also returned in the previous example).  There are no time limits on
when the participants can start the test and no limit on the number of
attempts.

In future, creating a schedule will be all that is required for a third
party integration as the schedule will then show up in the Questionmark
portal when the participant logs in and they'll be able to launch the
test from there.  That functionality is not available yet (as of
2017.08) and so this API assumes that the external system will go on to
create its own user interface for the participant.

Active Schedules
~~~~~~~~~~~~~~~~

A third-party user interface for a participant needs to know which
schedules are active for that participant.  A schedule is active if
there is some action that the participant may take (such as starting or
resuming the test).

To discover the list of active schedules you can call an OData action.
In the current release this action is bound to the Schedules feed but
this will change (expected 2017.10) so the following flow should be
considered experimental for now, notice that OData actions are invoked
using the POST method::

    POST /deliveryodata/<customer-id>/Schedules/ActionableSchedulesForParticipant
    
    {
        "ParticipantID": 80200535
    }

The response will look like this::

    {
        "odata.metadata": "https://ondemand.questionmark.com/deliveryodata/<customer-id>/$metadata#Collection(QM.DeliveryODataService.DTO.ActionableSchedule)",
        "value":
        [
            {
                "ScheduleID": 11887,
                "Name": "Demo Schedule",
                "Hidden": false,
                "AttemptsRemaining": null,
                "Actions":
                [
                    "start"
                ]
            }
        ]
    }

The result is a list of ActionableSchedule objects.  You can see the ID
of the schedule, the name (for display to the user when there are
multiple assessments available) and information about the number of
attempts remaining.

The Actions list is just a list of strings containing the names of
actions that are allowed.  In this case just one: "start".


Launching a Scheduled Test
~~~~~~~~~~~~~~~~~~~~~~~~~~

If a schedule is active for a participant then there will be a non-empty
list of actions in the associated AcitonableSchedule returned by the
previous request.

To enable the participant to launch the test you need to convert the
action into a URL that can be passed to the user's browser to invoke the
action.  You do this using the InvokeAction action::

    POST /deliveryodata/<customer-id>/Schedules(11887)/InvokeAction

    {
        "Action": "start",
        "ParticipantID": 80200535
    }

The response will look something like this::

    {
        "odata.metadata": "https://ondemand.questionmark.com/deliveryodata/<customer-id>/$metadata#Edm.String",
        "value": "https://ondemand.questionmark.com/lobby/<customer-id>/lobby/SystemCheck/17896?nonce=2c2b0ec9-1b96-44c7-853d-9557e271eb24&timestamp=2017-08-21T13:40:28.3237534Z&role=participant&signature=23228c229ce90ffd3fdaa2b73f94c95718457686474655f50229c4d91f211f9d"
    }

The URL obtained in the value of the result can be passed to the
participant's browser to enable them to launch the test.  The link is
time-limited, you should ensure that your application redirects the
participant to this link while handling a request for a suitable action
(such as the response to a button press).  If the participant is too
slow to load the URL it will expire and you'll have to generate another
one by invoking the action again.


Modiyfing a Schedule
~~~~~~~~~~~~~~~~~~~~

Schedules may be patched, though some properties may not be changed.
(E.g., the AssessmentID is fixed on creation).  The following call will
update the Schedule created in the previous example so that it can be
resumed::

    PATCH /deliveryodata/<customer-id>/Schedules(11887)

    {
        "ResumeAllowed": true
    }

If the participant has started an assessment but has not completed it
and the schedule is resumable then the test may be resumed.  This is
indicated using the "resume" action::

    POST /deliveryodata/<customer-id>/Schedules/ActionableSchedulesForParticipant
    
    {
        "ParticipantID": 80200535
    }

Responds with::

    {
        "odata.metadata": "https://ondemand.questionmark.com/deliveryodata/<customer-id>/$metadata#Collection(QM.DeliveryODataService.DTO.ActionableSchedule)",
        "value":
        [
            {
                "ScheduleID": 11887,
                "Name": "Demo Schedule",
                "Hidden": false,
                "AttemptsRemaining": null,
                "Actions":
                [
                    "resume"
                ]
            }
        ]
    }
 
A schedule is never marked with both "start" and "resume" actions. 
(This is a significant departure from classic schedules where multiple
attempts can be started simultaneously.  In next-generation schedules
the participant must complete the current attempt before progressing to
the next one if the schedule is resumable.)


Managing Attempts: Schedule Reporting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next generation schedules use the same Attempt concept as non-scheduled
delivery but the actions described above take care of managing the
Attempts. You may still use the Attempts to discover detailed
information about who has attempted the assessment and what results have
been completed or are in progress::

    GET /deliveryodata/<customer-id>/Attempts?$filter=ScheduleID%20eq%2011887&$expand=Result

This query returns all Attempts for a schedule using a filter.  By
expanding the Results associated with the attempts we can see the status
and outcome of the associated attempts.

This data could be used to construct a dashboard report for the schedule::

    {
        "odata.metadata": "https://ondemand.questionmark.com/deliveryodata/<customer-id>/$metadata#Attempts",
        "value": [
            {
                "Result": {
                    "ID": 390765738,
                    "AssessmentID": "3000000003",
                    "ParticipantName": "Stuart Dent",
                    "GroupName": null,
                    "ParticipantDetails": null,
                    "Status": 2,
                    "MaxScore": 1,
                    "TotalScore": 1,
                    "ScoreBandTitle": "Pass",
                    "PercentageScore": 100,
                    "WhenFinished": "2017-08-21T13:59:41.347",
                    "WhenStarted": "2017-08-21T13:48:20.123",
                    "ExtraTime": null
                },
                "ID": 17897,
                "ExternalAttemptID": "72f2b164084748ac835802f329bdadf2",
                "ParticipantFacingQMLobbyUrl": null,
                "ProctorFacingQMControlsWidgetUrl": null,
                "UnlockCodeExpiresDateTime": null,
                "ParticipantID": 80200535,
                "AssessmentID": "3000000003",
                "AssessmentSnapshotID": null,
                "ScheduleID": 11887,
                "AttemptNumber": 1,
                "ResultID": 390765738,
                "LockStatus": false,
                "LockRequired": false,
                "ParticipantFacingProctorSystemWidgetUrl": null,
                "LastModifiedDateTime": "2017-08-21T12:48:20.157Z",
                "Language": null,
                "ParticipantSystemCheckUrl": "null",
                "UnlockCode": null,
                "AttemptListID": null,
                "MonitoringTypeID": 1
            }
        ]
    }