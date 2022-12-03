===============
Next Bus Bot
===============

A bot/ cli tool that gives you the waiting times for next buses at your favorite bus stop.

It works only for the IDFM/RATP Network.

.. warning::

   This is a toy project to learn bot programming, API interfacing and Python Packaging.
   I am not responsible if you arrive late at your work.
   For serious travel planning, use your favorite app.


API Response
==============

When everything is working fine:

.. code-block::
   {
   "nextDepartures":{
      "data":[
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Centre Commercial Ulis 2",
            "time":"2",
            "destination":{
               "stopPointId":"stop_point:IDFM:11330",
               "stopAreaId":"stop_area:IDFM:60998"
            }
         },
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Christ de Saclay",
            "time":"3",
            "destination":{
               "stopPointId":"stop_point:IDFM:484340",
               "stopAreaId":"stop_area:IDFM:63290"
            }
         },
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Gare du Guichet",
            "time":"4",
            "destination":{
               "stopPointId":"stop_point:IDFM:11415",
               "stopAreaId":"stop_area:IDFM:63025"
            }
         },
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Campus HEC",
            "time":"6",
            "destination":{
               "stopPointId":"stop_point:IDFM:20384",
               "stopAreaId":"stop_area:IDFM:483697"
            }
         },
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Centre Commercial Ulis 2",
            "time":"11",
            "destination":{
               "stopPointId":"stop_point:IDFM:11330",
               "stopAreaId":"stop_area:IDFM:60998"
            }
         },
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Centre Commercial Ulis 2",
            "time":"11",
            "destination":{
               "stopPointId":"stop_point:IDFM:11330",
               "stopAreaId":"stop_area:IDFM:60998"
            }
         },
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Centre Commercial Ulis 2",
            "time":"15",
            "destination":{
               "stopPointId":"stop_point:IDFM:11330",
               "stopAreaId":"stop_area:IDFM:60998"
            }
         },
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Gare de Jouy en Josas",
            "time":"16",
            "destination":{
               "stopPointId":"stop_point:IDFM:20416",
               "stopAreaId":"stop_area:IDFM:63523"
            }
         },
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Campus HEC",
            "time":"18",
            "destination":{
               "stopPointId":"stop_point:IDFM:20384",
               "stopAreaId":"stop_area:IDFM:483697"
            }
         },
         {
            "lineId":"line:IDFM:C01561",
            "shortName":"9",
            "lineDirection":"Gare du Guichet",
            "time":"20",
            "destination":{
               "stopPointId":"stop_point:IDFM:11415",
               "stopAreaId":"stop_area:IDFM:63025"
            }
         }
      ],
      "statusCode":200
   },
   "crowdsourcingReports":{
      "congestions":[
         {
            "directionId":"stop_area:IDFM:60998",
            "nearTimeReports":{
               "rating":"None"
            }
         },
         {
            "directionId":"stop_area:IDFM:483697",
            "nearTimeReports":{
               "rating":"None"
            }
         }
      ],
      "statusCode":200
   }
}

When there are some errors (e.g. no more buses available):