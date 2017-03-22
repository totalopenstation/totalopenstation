.. _tds:

==================
Tripod Data System
==================

TDS (Tripod Data Systems) is a technique designed to use your handheld devices
as rough as you can to make it compatible with intense external environment.
They also provide the versatility in the range of friendly software for the
mobile computing and for various industries as well.

This format is designed to work with these devices and espacially with Survey Pro software.

The format is a comma separated ASCII file containing record types, headers,
recorded data and comments.

Each record is made of one line of text, with comma-separated fields of ASCII
text format::

  AH,DC%s,MA%s,ME%s,RA%s

This format is the base of other formats :
 - :ref:`if_carlson_rw5`

Record type
-----------

General Raw Data
________________
+---------------+------------------------------------------+
| Record Type   | Explanation                              | 
+===============+==========================================+
| --            | Note                                     |
+---------------+------------------------------------------+
| JB            | Job                                      |
+---------------+------------------------------------------+
| MO            | Mode Setup                               |
+---------------+------------------------------------------+

Conventional Raw Data
_____________________
+---------------+------------------------------------------+
| Record Type   | Explanation                              |
+===============+==========================================+
| AP            | Adjusted point                           |
+---------------+------------------------------------------+
| AT            | Attributes                               |
+---------------+------------------------------------------+
| BK            | Backsight                                |
+---------------+------------------------------------------+
| CF            | Cut Sheet                                |
+---------------+------------------------------------------+
| DE            | Design point / location                  |
+---------------+------------------------------------------+
| DL            | Define a Location                        |
+---------------+------------------------------------------+
| DP            | Deleted point                            |
+---------------+------------------------------------------+
| FC            | Feature Code                             |
+---------------+------------------------------------------+
| LS            | Line of Sight                            |
+---------------+------------------------------------------+
| MD            | Multiple Distances                       |
+---------------+------------------------------------------+
| OC            | Occupy Point                             |
+---------------+------------------------------------------+
| OE            | Offset delta                             |
+---------------+------------------------------------------+
| OF            | Off Center Shot                          |
+---------------+------------------------------------------+
| RB            | Repeat Backsight                         |
+---------------+------------------------------------------+
| RD            | Repeat Directional                       |
+---------------+------------------------------------------+
| RE            | Remote Elevation                         |
+---------------+------------------------------------------+
| RF            | Repeat Foresight                         |
+---------------+------------------------------------------+
| RS            | Resection                                |
+---------------+------------------------------------------+
| SD            | Deltas                                   |
+---------------+------------------------------------------+
| SK            | Stake Out                                |
+---------------+------------------------------------------+
| SL            | Slope Staking                            |
+---------------+------------------------------------------+
| SP            | Store Point                              |
+---------------+------------------------------------------+
| SR            | Slope Staking Reference Offset           |
+---------------+------------------------------------------+
| SU            | Sun Shot                                 |
+---------------+------------------------------------------+
| TR/SS/OB      | Traverse / Sideshot / Observation        |
+---------------+------------------------------------------+

GPS Raw Data
____________
+---------------+------------------------------------------+
| Record Type   | Explanation                              |
+===============+==========================================+
| AH            | GPS Antenna Height                       |
+---------------+------------------------------------------+
| BL            | GPS Base Line                            |
+---------------+------------------------------------------+
| BP            | Set Base Receiver Position               |
+---------------+------------------------------------------+
| CG            | COGO settings                            |
+---------------+------------------------------------------+
| CS            | Coordinate System Identity               |
+---------------+------------------------------------------+
| CT            | Calibration Point                        |
+---------------+------------------------------------------+
| CV            | RMS Covariance of GPS Base Line          |
+---------------+------------------------------------------+
| DG            | Datum Grid                               |
+---------------+------------------------------------------+
| DT            | Datum                                    |
+---------------+------------------------------------------+
| EE            | GPS Edit Point                           |
+---------------+------------------------------------------+
| EP            | Geodetic position                        |
+---------------+------------------------------------------+
| EQ            | Equipment                                |
+---------------+------------------------------------------+
| ES            | Ellipsoid                                |
+---------------+------------------------------------------+
| GK            | GPS stakeout                             |
+---------------+------------------------------------------+
| GO            | GPS Offset Shot                          |
+---------------+------------------------------------------+
| GP            | GPS Point                                |
+---------------+------------------------------------------+
| GR            | GPS adjusted point                       |
+---------------+------------------------------------------+
| GS            | GPS Store Point                          |
+---------------+------------------------------------------+
| HA            | Horizontal Calibration (Adjust)          |
+---------------+------------------------------------------+
| PE            | Extended Projection                      |
+---------------+------------------------------------------+
| PJ            | Projection                               |
+---------------+------------------------------------------+
| RP            | Local coordinates of calibration point   |
+---------------+------------------------------------------+
| RX            | Receiver Setup                           |
+---------------+------------------------------------------+
| ST            | Local site settings                      |
+---------------+------------------------------------------+
| VA            | Vertical Calibration (Adjust)            |
+---------------+------------------------------------------+

Legacy Raw Data
_______________
+---------------+------------------------------------------+
| Record Type   | Explanation                              |
+===============+==========================================+
| AA            | Accumulating Angle-right |br|            |
|               | not used in SPCE                         |
+---------------+------------------------------------------+
| BB            | Bench level, backsight |br|              |
|               | not used in SPCE                         |
+---------------+------------------------------------------+ 
| BG            | Base Point Geoid Model Elevation |br|    |
|               | no longer supported in SPCE 3.5 |br|     |
|               | replaced by VA                           |
+---------------+------------------------------------------+
| BS            | Bench level, side shots |br|             |
|               | not used in SPCE                         |
+---------------+------------------------------------------+
| BT            | Bench level, traverse |br|               |
|               | not used in SPCE                         |
+---------------+------------------------------------------+
| HC            | Horizontal Control Point |br|            |
|               | not supported in SPro 3.5 |br|           |
|               | replaced with CT                         |
+---------------+------------------------------------------+
| LE            | Vertical Ellipsoid Height Setup          |
+---------------+------------------------------------------+
| LG            | Vertical Geoid Model Setup |br|          |
|               | no longer supported in SPCE3.5           |
+---------------+------------------------------------------+
| LM            | Horizontal Mapping Plane Setup |br|      |
|               | no longer supported in SPCE3.5           |
+---------------+------------------------------------------+
| LH            | Local transforming coefficients |br|     |
|               | for horizontal |br|                      |
|               | no longer supported in SPCE3.5 |br|      |
|               | replaced by Horizontal adjustment HA     |
+---------------+------------------------------------------+
| LV            | Local transforming coefficients |br|     |
|               | for vertical |br|                        |
|               | no longer supported in SPCE3.5 |br|      |
|               | replaced by Vertical adjustment VA       |         
+---------------+------------------------------------------+
| VC            | Vertical Control point |br|              |
|               | not supported in SPro 3.5 |br|           |
|               | replaced with C                          |
+---------------+------------------------------------------+

Field headers
-------------

General and Conventional field list
___________________________________
+--------------+-----------------------------------------+
| Field header | Explanation                             |
+==============+=========================================+
| ``--``       | Note                                    |
+--------------+-----------------------------------------+
| AD           | Azimuth Direction                       |
+--------------+-----------------------------------------+
| AL           | Angle Left                              |
+--------------+-----------------------------------------+
| AR           | Angle Right                             |
+--------------+-----------------------------------------+
| AS           | Ahead on station                        |
+--------------+-----------------------------------------+
| AU           | Angle Unit                              |
+--------------+-----------------------------------------+
| AZ           | Azimuth                                 |
+--------------+-----------------------------------------+
| BC           | Back Circle                             |
+--------------+-----------------------------------------+
| BD           | Backsight direct                        |
+--------------+-----------------------------------------+
| BP           | Back point                              |
+--------------+-----------------------------------------+
| BS           | Backsight                               |
+--------------+-----------------------------------------+
| BV           | Backsight reverse                       |
+--------------+-----------------------------------------+
| CE           | Change elevation                        |
+--------------+-----------------------------------------+
| CF           | Slope used                              |
+--------------+-----------------------------------------+
| CR           | Circular Reading                        |
+--------------+-----------------------------------------+
| DE           | Declination                             |
+--------------+-----------------------------------------+
| DS           | Design Slope                            |
+--------------+-----------------------------------------+
| DT           | Date (JB Record)                        |
+--------------+-----------------------------------------+
| DT           | Date (SU Record) |br|                   |
|              | [MMDDYYYY]                              |
+--------------+-----------------------------------------+
| E            | Adj. Easting                            |
+--------------+-----------------------------------------+
| EC           | Earth Curvature                         |
+--------------+-----------------------------------------+
| ED           | Delta easting                           |
+--------------+-----------------------------------------+
| EG           | Sun Position                            |
+--------------+-----------------------------------------+
| EL           | Elevation or Adj. Elevation             |
+--------------+-----------------------------------------+
| EO           | EDM offset                              |
+--------------+-----------------------------------------+
| FD           | Foresight direct                        |
+--------------+-----------------------------------------+
| FE           | Foresight elevation                     |
+--------------+-----------------------------------------+
| FN           | Feature code name                       |
+--------------+-----------------------------------------+
| FP           | Foresight point                         |
+--------------+-----------------------------------------+
| FV           | Foresight reverse                       |
+--------------+-----------------------------------------+
| GD           | Grade                                   |
+--------------+-----------------------------------------+
| GH           | Greenwich hour angle                    |
+--------------+-----------------------------------------+
| HC           | Horizontal dist. to center line         |
+--------------+-----------------------------------------+
| HD           | Horizontal distance                     |
+--------------+-----------------------------------------+
| HD           | Horizontal or relative horizontal dist. |
+--------------+-----------------------------------------+
| HH           | Horizontal distance to hinge point      |
+--------------+-----------------------------------------+
| HI           | Height of Instrument                    |
+--------------+-----------------------------------------+
| HR           | Height of Rod                           |
+--------------+-----------------------------------------+
| LA           | Latitude                                |
+--------------+-----------------------------------------+
| LD           | Delta elevation                         |
+--------------+-----------------------------------------+
| LO           | Longitude                               |
+--------------+-----------------------------------------+
| LR           | Left/Right Offset                       |
+--------------+-----------------------------------------+
| N            | Adj. Northing                           |
+--------------+-----------------------------------------+
| ND           | Delta northing                          |
+--------------+-----------------------------------------+
| NM           | Job Name                                |
+--------------+-----------------------------------------+
| OB           | Observed slope                          |
+--------------+-----------------------------------------+
| OD           | Offset Direction                        |
+--------------+-----------------------------------------+
| OE           | Offset Delta                            |
+--------------+-----------------------------------------+
| OL           | Offset length                           |
+--------------+-----------------------------------------+
| OP           | Occupy point                            |
+--------------+-----------------------------------------+
| PN           | Point name                              |
+--------------+-----------------------------------------+
| SD           | Slope Distance                          |
+--------------+-----------------------------------------+
| SF           | Scale Factor                            |
+--------------+-----------------------------------------+
| SM           | Semi-diameter of Sun |br|               |
|              | in DMS                                  |
+--------------+-----------------------------------------+
| ST           | Station                                 |
+--------------+-----------------------------------------+
| TM           | Time (JB – Record) |br|                 |
|              | [HH:MM:SS]                              |
+--------------+-----------------------------------------+
| TM           | Time (EP – Record) |br|                 |
|              | [HHMMSS]                                |
+--------------+-----------------------------------------+
| TM           | Time (SU – Record) |br|                 |
|              | [HH.dddddd] in UTC Time                 |
+--------------+-----------------------------------------+
| TN           | Attribute name                          |
+--------------+-----------------------------------------+
| TV           | Attribute value in string form          |
+--------------+-----------------------------------------+
| UN           | Distance Unit                           |
+--------------+-----------------------------------------+
| VC           | Vertical distance to center point       |
+--------------+-----------------------------------------+
| VD           | Vertical or relative vertical distance  |
+--------------+-----------------------------------------+
| VH           | Vertical distance to hinge point        |
+--------------+-----------------------------------------+
| ZD           | Zenith Direct                           |
+--------------+-----------------------------------------+
| ZE           | Zenith or Zenith angle                  |
+--------------+-----------------------------------------+
| ZV           | Zenith Reverse                          |
+--------------+-----------------------------------------+

General and Conventional enumerated field list
______________________________________________

+---------+--------+-----------------------+---------------------+----------------+
| Field   | Type   | 0                     | 1                   | 2              |
+=========+========+=======================+=====================+================+
| AD      | enum   | North                 | South               |                |
+---------+--------+-----------------------+---------------------+----------------+
| AU      | enum   | degree                | grads               |                |
+---------+--------+-----------------------+---------------------+----------------+
| CF      | bool   | cut                   | fill                |                |
+---------+--------+-----------------------+---------------------+----------------+
| EC      | enum   | off                   | on                  |                |
+---------+--------+-----------------------+---------------------+----------------+
| OD      | int    | Center                | Right               | Left           |
+---------+--------+-----------------------+---------------------+----------------+
| UN      | enum   | Feet                  | Meter               | US Survey Feet |
+---------+--------+-----------------------+---------------------+----------------+
| EG      | string | Left Trailing edge    | Right Trailing Edge | center         |
+---------+--------+-----------------------+---------------------+----------------+

GPS Field List
______________
+--------------+----------------------------------------------+
| Field header | Explanation                                  |
+==============+==============================================+
| ``--``       | Description (Feature Code)                   |
+--------------+----------------------------------------------+
| AE            Location Indicator                            |
+--------------+----------------------------------------------+
| AF           | Azimuth format                               |
+--------------+----------------------------------------------+
| AI           | Antenna Index int (See Antenna.ini File)     |
+--------------+----------------------------------------------+
| AN           | Antenna Number int (See Antenna.ini File)    |
+--------------+----------------------------------------------+
| AO           | Azimuth Orientation                          |
+--------------+----------------------------------------------+
| AT           | Antenna Type (name of antenna)               |
+--------------+----------------------------------------------+
| AZ           | Azimuth double Geodetic Angle                |
+--------------+----------------------------------------------+
| CL           | Classification                               |
+--------------+----------------------------------------------+
| CO           | Coordinate System Option                     |
+--------------+----------------------------------------------+
| CT           | Origin center                                |
+--------------+----------------------------------------------+
| DA           | Datum Transformation Type                    |
+--------------+----------------------------------------------+
| DC           | Derivation Code                              |
+--------------+----------------------------------------------+
| DH           | HDOP from Rx                                 |
+--------------+----------------------------------------------+
| DM           | Dimensions Used                              |
+--------------+----------------------------------------------+
| DN           | Datum name                                   |
+--------------+----------------------------------------------+
| DV           | VDOP from Rx                                 |
+--------------+----------------------------------------------+
| DX           | Base line Delta X                            |
+--------------+----------------------------------------------+
| DY           | Base line Delta Y                            |
+--------------+----------------------------------------------+
| DZ           | Base line Delta Z                            |
+--------------+----------------------------------------------+
| E            | Easting                                      |
+--------------+----------------------------------------------+
| EL           | Elevation                                    |
+--------------+----------------------------------------------+
| EM           | Ellipse Name                                 |
+--------------+----------------------------------------------+
| FI           | File name                                    |
+--------------+----------------------------------------------+
| FO           | File name one                                |
+--------------+----------------------------------------------+
| FT           | File name two                                |
+--------------+----------------------------------------------+
| GF           | Geodetic Flags                               |
+--------------+----------------------------------------------+
| GM           | GPS Measure Method                           |
+--------------+----------------------------------------------+
| GN           | Geoid Model Name                             |
+--------------+----------------------------------------------+
| GO           | Grid Orientation                             |
+--------------+----------------------------------------------+
| HI           | Height of laser at GPS ref. Point            |
+--------------+----------------------------------------------+
| HO           | Horizontal Offset                            |
+--------------+----------------------------------------------+
| HP           | Horizontal Precision                         |
+--------------+----------------------------------------------+
| HR           | Height of laser target at store offset Pt.   |
+--------------+----------------------------------------------+
| HT           | Height or Ellipsoid Ht.                      |
+--------------+----------------------------------------------+
| IF           | Ellipse inverse flattening                   |
+--------------+----------------------------------------------+
| LA           | Latitude                                     |
+--------------+----------------------------------------------+
| LN           | Longitude                                    |
+--------------+----------------------------------------------+
| LX           | Translation x                                |
+--------------+----------------------------------------------+
| LY           | Translation y                                |
+--------------+----------------------------------------------+
| LZ           | Translation z                                |
+--------------+----------------------------------------------+
| MA           | Measured antenna height                      |
+--------------+----------------------------------------------+
| ME           | Measure Method                               |
+--------------+----------------------------------------------+
| N            | Northing                                     |
+--------------+----------------------------------------------+
| OO           | Orientation one                              |
+--------------+----------------------------------------------+
| OT           | Orientation two                              |
+--------------+----------------------------------------------+
| OX           | Rotation x                                   |
+--------------+----------------------------------------------+
| OY           | Rotation y                                   |
+--------------+----------------------------------------------+
| OZ           | Rotation z                                   |
+--------------+----------------------------------------------+
| PN           | Point Name                                   |
+--------------+----------------------------------------------+
| PT           | GPS Point Type                               |
+--------------+----------------------------------------------+
| PV           | Type of Vertical Adjustment                  |
+--------------+----------------------------------------------+
| RA           | Reduced antenna height                       |
+--------------+----------------------------------------------+
| RD           | Ellipsoid Radius                             |
+--------------+----------------------------------------------+
| RE           | Recording interval                           |
+--------------+----------------------------------------------+
| RH           | Horizontal RMS from Rx                       |
+--------------+----------------------------------------------+
| RS           | Rx Serial Number                             |
+--------------+----------------------------------------------+
| RT           | Rotation about origin                        |
+--------------+----------------------------------------------+
| RV           | Vertical RMS from Rx                         |
+--------------+----------------------------------------------+
| RX           | Rx Type                                      |
+--------------+----------------------------------------------+
| RY           | Rectify                                      |
+--------------+----------------------------------------------+
| SA           | Slope east                                   |
+--------------+----------------------------------------------+
| SC           | Error Scale or Scale Factor                  |
+--------------+----------------------------------------------+
| SD           | Slope Distance                               |
+--------------+----------------------------------------------+
| SF           | Scale factor at origin                       |
+--------------+----------------------------------------------+
| SG           | Setup Group                                  |
+--------------+----------------------------------------------+
| SO           | Slope north                                  |
+--------------+----------------------------------------------+
| SP           | Scale factor                                 |
+--------------+----------------------------------------------+
| SV           | Min. # of SV during obs.                     |
+--------------+----------------------------------------------+
| TA           | Tape Adjustment                              |
+--------------+----------------------------------------------+
| TE           | Translation East                             |
+--------------+----------------------------------------------+
| TH           | Translation North                            |
+--------------+----------------------------------------------+
| TM           | System Time                                  |
+--------------+----------------------------------------------+
| TP           | Type of projection                           |
+--------------+----------------------------------------------+
| TS           | Antenna Serial Number                        |
+--------------+----------------------------------------------+
| VO           | Vertical Offset                              |
+--------------+----------------------------------------------+
| VP           | Vertical Precision                           |
+--------------+----------------------------------------------+
| XX           | Variance X                                   |
+--------------+----------------------------------------------+
| XY           | Covariance X,Y                               |
+--------------+----------------------------------------------+
| XZ           | Covariance X,Z                               |
+--------------+----------------------------------------------+
| YY           | Variance Y                                   |
+--------------+----------------------------------------------+
| YZ           | Covariance Y,Z                               |
+--------------+----------------------------------------------+
| ZE           | Zenith Angle                                 |
+--------------+----------------------------------------------+
| ZG           | Zone Group (system) name                     |
+--------------+----------------------------------------------+
| ZN           | Zone name                                    |
+--------------+----------------------------------------------+
| ZZ           | Variance Z                                   |
+--------------+----------------------------------------------+

GPS Enumerated Fields List
__________________________

:AE: Location indicator for Denmark projections enum |br|
  • 1 = None |br|
  • 2 = Zeeland |br|
  • 3 = Jutland |br|
  • 4 = Bornholm

:AF: Azimuth Format enum |br|
  • 0 = Geodetic |br|
  • 1 = Grid

:AO: Azimuth Orientation WORD |br|
  • 1 = North |br|
  • 2 = South

:CL: Classification enum |br|
  • 0 = UnknownClass |br|
  • 1 = Normal |br|
  • 2 = Control |br|
  • 3 = AsBuilt |br|
  • 4 = Check |br|
  • 5 = BackSight |br|
  • 6 = Deleted Normal |br|
  • 7 = Deleted Control |br|
  • 8 = Deleted AsBuilt |br|
  • 9 = DeletedCheck |br|
  • 10 = DeletedBackSight

:CO: Coordinate System Option WORD |br|
  • 1 = None |br|
  • 2 = Scale only |br|
  • 3 = Keyed in |br|
  • 4 = Chosen from library

:CT: Origin Center enum |br|
  • 0 = Equator |br|
  • 1 = Projection center

:DA: Datum Transformation Type WORD |br|
  • 513 = csdMolodenskyDatum |br|
  • 514 = csdMultipleRegressionDatum |br|
  • 515 = csdSevenParameterDatum |br|
  • 516 = csdGridDatum |br|
  • 517 = csdWGS84Datum

:DC: Derivation Code enum |br|
  • 1 = ModeBase (Base) |br|
  • 2 = ModeRover (Rover) |br|
  • 3 = ModeGetBase (GetBase) |br|
  • 4 = ModeStatic (Static)

:DM: Number of Dimensions Used for a Calibration WORD |br|
  • 1 = 0D (None) |br|
  • 2 = 1D (Vertical only) |br|
  • 3 = 2D (Horizontal only) |br|
  • 4 = 3D (Both vertical and horizontal) |br|
  • 5 = Any

:GF: Geodetic Flags Bit Flags |br|
  • Bit 0 = GPS Base Point |br|
  • Bit 1 = GPS Horizontal Control Point |br|
  • Bit 2 = GPS Veritcal Control Point |br|
  • Bit 3 = GPS Control Point |br|
  • Bit 4 = Local Map Plane Origin (Legacy, not used in Survey Pro 3.5 and beyond) |br|
  • Bit 5 = GPS Base Coordinate Invalid

:GM: GPS Measure Method enum |br|
  • 0 = UnknownMethod |br|
  • 1 = UserInput |br|
  • 2 = Autonomous |br|
  • 3 = RTKFloat |br|
  • 4 = RTKFixed |br|
  • 5 = CopiedPoint |br|
  • 6 = RTCMCode |br|
  • 7 = WASS

:GO: Grid Orientation WORD |br|
  • 1 = NE |br|
  • 2 = SW |br|
  • 3 = NW |br|
  • 4 = SE

:ME: MeasureMethod enum |br|
  • 0 = Unknown |br|
  • 1 = True |br|
  • 2 = Uncorrected

:PT: GPS Point Type enum |br|
  • 1 = Control |br|
  • 2 = Check |br|
  • 3 = DataCollect |br|
  • 4 = Offset |br|
  • 5 = RemoteElevation |br|
  • 6 = PostProcess |br|
  • 7 = UserInput

:PV: Type of Vertical Adj. WORD |br|
  • 1 = inclined plane |br|
  • 2 = geoid model |br|
  • 3 = combined

:TP: Type of Projection WORD |br|
  • 2049 = Albers Equal Area Conic |br|
  • 2050 = Cassini |br|
  • 2051 = Krovak |br|
  • 2052 = Lambert Conformal Conic One Parallel |br|
  • 2053 = Mercator |br|
  • 2054 = New Zealand Map Grid |br|
  • 2055 = Oblique Conformal Conic |br|
  • 2056 = Oblique Mercator Azimuth |br|
  • 2057 = Oblique Stereographic |br|
  • 2058 = Plane |br|
  • 2059 = Stereographic |br|
  • 2060 = RD Stereographic |br|
  • 2062 = Transverse Mercator |br|
  • 2063 = United Kingdom National Grid |br|
  • 2064 = Denmark |br|
  • 2065 = Hungarian EOV |br|
  • 2066 = Lambert Conformal Conic Two Parallel |br|
  • 2067 = Oblique Mercator Two Points |br|
  • 2068 = Double Stereographic |br|
  • 2069 = Grid

Legacy Field List
_________________

+----------------+----------------------------+
| Field header   | Explanation                |
+================+============================+
| ``--``         | Description (Feature Code) |
+----------------+----------------------------+
| AR             | Angle right                |
+----------------+----------------------------+
| Ba             | Base Latitude              |
+----------------+----------------------------+
| BC             | Back circle                |
+----------------+----------------------------+
| Bh             | Base Ellipsoid Height      |
+----------------+----------------------------+
| Bo             | Base Longitude             |
+----------------+----------------------------+
| CS             | Coordinate System          |
+----------------+----------------------------+
| DA             | Datum                      |
+----------------+----------------------------+
| EL             | Elevation                  |
+----------------+----------------------------+
| FI             | Custome File Name          |
+----------------+----------------------------+
| GI             | Geoid model index          |
+----------------+----------------------------+
| GU             | Geoid Undulation at base   |
+----------------+----------------------------+
| Ha             | Coefficient a              |
+----------------+----------------------------+
| Hb             | Coefficient b              |
+----------------+----------------------------+
| Hc             | Coefficient c              |
+----------------+----------------------------+
| Hd             | Coefficient d              |
+----------------+----------------------------+
| HE             | Hemisphere                 |
+----------------+----------------------------+
| HT             | Height                     |
+----------------+----------------------------+
| LA             | Latitude                   |
+----------------+----------------------------+
| LN             | Longitude                  |
+----------------+----------------------------+
| ME             | Method                     |
+----------------+----------------------------+
| PN             | Backsight point            |
+----------------+----------------------------+
| RT             | Rotation                   |
+----------------+----------------------------+
| SC             | Scale                      |
+----------------+----------------------------+
| SD             | Slope Distance             |
+----------------+----------------------------+
| Va             | Coefficient a              |
+----------------+----------------------------+
| Vb             | Coefficient b              |
+----------------+----------------------------+
| Vc             | Coefficient c              |
+----------------+----------------------------+
| ZE             | Zenith                     |
+----------------+----------------------------+
| ZO             | Zone                       |
+----------------+----------------------------+

Definitions
-----------

General Raw Data
________________

Note Record
...........

Job Record
..........
:Record type: JB
:Field headers:
  NM: Job name |br|
  DT: Date |br|
  TM: Time
:Sample(s):
  ::

    “JB,NM%s,DT%s,TM%s”
  
Mode Setup Record
.................
The mode setup will be recorded at the beginning of the raw data file and whenever it is
changed.

:Record type: MO
:Field headers:
  AD: Azimuth direction (ENUM) |br|
  UN: Distance unit (ENUM) |br|
  SF: Scale factor |br|
  EC: Earth curvature (ENUM) |br|
  EO: EDM offset (inch) (Default string “0.0”) |br|
  AU: Angle unit (ENUM)
:Sample(s):
  ::

    “MO,AD%s,UN%s,SF%s,EC%s,EO0.0,AU%s”

Conventional Raw Data
_____________________

Adjusted point record
.....................
:Record type: AP
:Field headers:
  PN: Point name |br|
  N : Adjusted northing |br|
  E : Adjusted easting |br|
  EL: Adjusted elevation |br|
  ``--``: Description
:Sample(s):
  ::

    “AP,PN%s,N %s,E %s,EL%s,--%s”

Attributes
..........
:Record type: AT
:Field headers:
  TN: Attribute name |br|
  TV: Attribute value in string form
:Sample(s):
  ::

    “AT,TN%s,TV%s”

Backsight Record
................
:Record type: BK
:Field headers:
  OP: Occupy point |br|
  BP: Back point |br|
  BS: Backsight |br|
  BC: Back circle
:Sample(s):
  ::

    “BK,OP%s,BP%s,BS%s,BC%s”

Cut Sheet Record
................
:Record type: CF (cut or fill)

For an offset stakeout cut sheet.

:Field headers:
  ST: Station |br|
  OD: Offset direction (ENUM) |br|
  OL: Offset length |br|
  EL: Elevation |br|
  GD: Grade (design)
:Sample(s):
  ::

    “CF,ST%s,OD%s,OL%s,EL%s,GD%s”

For a point stakeout cut sheet.

:Field headers:
  PN: Point number |br|
  EL: Elevation |br|
  GD: Grade
:Sample(s):
  ::

    “CF,PN%s,EL%s,GD%s”

Note: From Survey Pro CE 3.5, the PN field and description field are removed from CF record for point stake out.

Design point / location record
..............................
:Record type: DE
:Field headers:
  PN: Point name (design point, may be blank) |br|
  N : Northing |br|
  E : Easting |br|
  EL: Elevation |br|
  ``--``: Description (design point description, may be blank)
:Sample(s):
  ::

    “DE,PN%s,N %s,E %s,EL%s,--%s”

Define a Location Record
........................
:Record type: DL
:Field headers:
  PN: Point name (POB) |br|
  HD: Relative horizontal distance |br|
  VD: Relative vertical distance |br|
  AZ: Azimuth |br|
  ``--`` Description of the stored point.
:Sample(s):
  ::

    “DL,PN%s,HD%s,VD%s,AZ%s,--%s”

Deleted point record
....................
:Record type: DP
:Field headers:
  PN : Point name
:Sample(s):
  ::

    “DP,PN%s”

Feature Code
............
:Record type: FC
:Field headers:
  PN: Point name |br|
  FN: Feature code name (may be blank)
:Sample(s):
  ::

    “FC,PN%s,FN%s”

Line of Sight Record
....................
:Record type: LS
:Field headers:
  HI: Height of instrument |br|
  HR: Height of rod
:Sample(s):
  ::

    “LS,HI%s,HR%s”

Multiple Distance
.................
:Record type: MD
:Field headers:
  SD: Slope distance
:Sample(s):
  ::

    “MD,SD %s:%s”

Occupy Point Record
...................
:Record type: OC
:Field headers:
  OP: Point number |br|
  N : Northing (the header is N space) |br|
  E : Easting (the header is E space)
  EL: Elevation
  ``--`` Description
:Sample(s):
  ::

    “OC,OP%s,N %s,E %s,EL%s,--%s”

Offset delta record
...................
:Record type: OE
:Field headers:
  ST: Station |br|
  OE: Offset delta (actual offset – design offset)
:Sample(s):
  ::

    “OE,ST%s,OE%s”

Off Center Shot Record
......................
:Record type: OF
:Field headers:
  AR: Angle right |br|
  ZE: Zenith |br|
  SD: Slope distance |br|
  OL: Offset length |br|
  HD: Horizontal distance |br|
  VD: Vertical distance |br|
  LR: Left/Right Offset
:Sample(s):
  ::

    “OF,AR%s,ZE%s,SD%s”
    “OF,ZE%s,--Vert Angle Offset”
    “OF,OL%s,--Right Angle Offset”
    “OF,HD%s,--Horizontal Distance Offset”
    “OF,LR%s,--Left / Right Offset”
    “OF,VD%s,--Elevation Offset”

Repeat Backsight
................
:Record type: RB (repeat backsight)
:Field headers:
  OP: Occupied point |br|
  BP: Backsight point |br|
  AR: Angle right |br|
  ZE: Zenith angle |br|
  SD: Slope distance |br|
  HR: Height of rod at the backsight |br|
  ``--`` Description
:Sample(s):
  ::

    “RB,OP%s,BP%s,AR%s,ZE%s,SD%s,HR%s,--%s”

Repeat Directional
..................
:Record type: RD
:Field headers:
  BD: Backsight direct |br|
  FD: Foresight direct |br|
  ZD: Zenith direct |br|
  FV: Foresight reverse |br|
  ZV: Zenith reverse |br|
  BV: Backsight reverse
:Sample(s):
  ::

    “RD,FD %s:%s”
    “RD,FV %s:%s”
    “RD,BD %s:%s”
    “RD,BV %s:%s”
    “RD,ZD %s:%s”
    “RD,ZV %s:%s”

The data before the colon (:) is the integer set number and the data after the colon is the angle measurement. See MO record for angle units.

Remote Elevation Record
.......................
:Record type: RE
:Field headers:
  OP: Occupied point |br|
  FE: Foresight elevation |br|
  ZE: Zenith angle |br|
  SD: Slope distance |br|
  ``--`` ( always “Remote elev”)
:Sample(s):
  ::

    “RE,OP%s,FE%s,ZE%s,SD%s,--%s”

Repeat Foresight
................
:Record type: RF (repeat foresight)
:Field headers:
  OP: Occupied point |br|
  FP: Foresight point |br|
  AR: Angle right |br|
  ZE: Zenith angle |br|
  SD: Slope distance |br|
  HR: Height of rod at the foresight |br|
  ``--`` Description
:Sample(s):
  ::

    “RF,OP%s,FP%s,AR%s,ZE%s,SD%s,HR%s,--%s”

Resection Record
................
:Record type: RS
:Field headers:
  PN: Point number |br|
  CR: Circular reading |br|
  ZE: Zenith (or VA, CE) |br|
  SD: Slope distance (or HD)
:Sample(s):
  ::

    “RS,PN%s,CR%s,ZE%s,SD%s” // A resection with angles and distance
    “RS,PN%s,CR%s” // A resection with angles only

Deltas record
.............
:Record type: SD
:Field headers:
  ND: Delta northing |br|
  ED: Delta easting |br|
  LD: Delta elevation |br|
:Sample(s):
  ::

    “SD,ND%s,ED%s,LD%s”

Stake Out Record
................
:Record type: SK
:Field headers:
  OP: Occupy point |br|
  FP: Foresight point |br|
  AR: Angle right |br|
  ZE: Zenith |br|
  SD: Slope distance
:Sample(s):
  ::

    “SK,OP%s,FP%s,AR%s,ZE%s,SD%s,--%s”

Note: FP field used to record design point name. Starting from SPCE3.5, it records the actual point name. It also may be blank if there is no actual point stored.

Slope Staking Record
....................
:Record type: SL
:Field headers:
  ST: Station |br|
  OD: Offset direction (ENUM) |br|
  EL: Actual catch point elevation |br|
  GD: Grade (design elevation of the catch point based on the slope line) |br|
  AS: Ahead on station (positive when rod is beyond design station, negative when
  before station) |br|
  HH: Horizontal distance to hinge point (always positive) |br|
  VH: Vertical distance to hinge point (positive when rod is above hinge) |br|
  HC: Horizontal distance to center line (always positive) |br|
  VC: Vertical distance to center point (positive when rod is above center point) |br|
  CF: Slope used (ENUM) |br|
  DS: Design slope |br|
  OB: Observed slope
:Sample(s):
  ::

    “SL,ST%s,OD%s,EL%s,GD%s,AS%s,HH%s,VH%s,HC%s,VC%s,CF%s,DS%s,OB%s”

Store Point Record
..................
:Record type: SP
:Field headers:
  PN: Point number |br|
  N: Northing |br|
  E: Easting |br|
  EL: Elevation |br|
  ``--`` Description
:Sample(s):
  ::

    “SP,PN%s,N %s,E %s,EL%s,--%s”

Slope Staking Reference Offset Record
.....................................
:Record type: SR
:Field headers:
  ST: Station |br|
  OD: Offset direction (ENUM) |br|
  EL: Actual elevation |br|
  GD: Grade (design elevation, corresponds to the elevation
  of the found catch point) |br|
  AS: Ahead on station (positive when rod is beyond design station, negative when
  before station) |br|
  HH: Horizontal distance to hinge point (always positive). This distance includes the
  reference offset. |br|
  VH: Vertical distance to hinge point (positive when rod is above hinge) |br|
  HC: Horizontal distance to center line (always positive). This distance includes the
  reference offset. |br|
  VC: Vertical distance to center point (positive when rod is above center point) |br|
  CF: Slope used (ENUM) |br|
  DS: Design slope |br|
  OB: Observed slope at the catch point |br|
  OL: Offset length from the catch point
:Sample(s):
  ::

    “SR,ST%s,OD%s,EL%s,GD%s,AS%s,HH%s,VH%s,HC%s,VC%s,CF%s,DS%s,OB%s,OL%s”

Sun Shot Record
...............
:Record type: SU

For a sun shot setup

:Field headers:
  GH: Greenwich hour angle (GHA 0) |br|
  GH: Greenwich hour angle (GHA 24) |br|
  DE: Declination (DECL 0) |br|
  DE: Declination (DECL 24) |br|
  SM: Semi-diameter of Sun (in DMS) |br|
  DT: Local date (See General and Conventional Field List) |br|
  TM: Local time (See General and Conventional Field List)

For the actual sun shot

:Field headers:
  BD: Backsight direct |br|
  FD: Foresight direct |br|
  FV: Foresight reverse |br|
  BV: Backsight reverse |br|
  LA: Latitude |br|
  LO: Longitude |br|
  EG0: Left trailing edge sun position |br|
  EG1: Right trailing edge sun position |br|
  EG2: Center sun position
:Sample(s):
  ::

    “SU,GH%s,GH%s,DE%s,DE%s,SM%s”
    “SU,DT%02s%02s%04s”
    “SU,LA%s,LO%s,EG%s”
    “SU,TM%s”
    “SU,%s%s%s” // Will write BD,BV or FD,FV with an angle measurement. See MO
    record for angle units.

Traverse / Sideshot / Observation Record
........................................
:Record type: TR / SS / OB
:Field headers:
  OP: Occupy point |br|
  FP: Foresight point |br|
  (one of the following) |br|
  - AZ: Azimuth |br|
  - AR: Angle right |br|
  - AL: Angle left |br|
  (one of the following pair) |br|
  - ZE: Zenith |br|
  - SD: Slope distance |br|
  (or) |br|
  - CE: Change elevation |br|
  - HD: Horizontal distance |br|
  ``--`` Description
:Sample(s):
  ::

    “TR,OP%s,FP%s,AR%s,ZE%s,SD%s,--%s”
    “SS,OP%s,FP%s,AR%s,ZE%s,SD%s,--%s”
    “OB,OP%s,FP%s,AR%s,ZE%s,SD%s,--%s”

GPS Raw Data Record Definitions
_______________________________

GPS Antenna Height
..................
:Record type: AH
:Field headers:
  DC: Derivation Code (ENUM) |br|
  MA: Measured antenna height |br|
  ME: Measure Method (ENUM) |br|
  RA: Reduced antenna height (to phase center)
:Sample(s):
  ::

    “AH,DC%s,MA%s,ME%s,RA%s”

GPS Base Line
.............
:Record type: BL
:Field headers:
  DC: Derivation |br|
  PN: Point Name |br|
  DX: Base line Delta X |br|
  DY: Base line Delta Y |br|
  DZ: Base line Delta Z |br|
  ``--``: Description (Feature Code) |br|
  GM: GPS Measure Method (ENUM) |br|
  CL: Classification |br|
  HP: Horizontal Precision |br|
  VP: Vertical Precision
:Sample(s):
  ::

    “BL,DC%s,PN%s,DX%s,DY%s,DZ%s,--%s,GM%s,CL%s,HP%s,VP%s”

Set Base Receiver Position
..........................
:Record type: BP
:Field headers:
  PN : Point Name |br|
  LA: Latitude |br|
  LN: Longitude |br|
  HT: Ellipsoid Height |br|
  SG: Setup Group (default = 0)
:Sample(s):
  ::

    “BP,PN%s,LA%s,LN%s,HT%s,SG%s”

COGO Settings record
....................
:Record type: CG
:Field headers:
  AO: Azimuth Orientation (ENUM) |br|
  GO: Grid Orientation (ENUM)
:Sample(s):
  ::

    “CG,AO%s,GO%s”

Coordinate System Identity
..........................
:Record type: CS
:Field headers:
  CO: Coordinate system option (ENUM) |br|
  ZG: Zone group (system) name |br|
  ZN: Zone name |br|
  DN: Datum name
:Sample(s):
  ::

    “CS,CO%s,ZG%s,ZN%s,DN%s”

Calibration Point
.................
:Record type: CT
:Field headers:
  PN: Point Name |br|
  DM: Dimensions used (ENUM) |br|
  RH: Horizontal residual |br|
  RV: Vertical residual
:Sample(s):
  ::

    “CT,PN%s,DM%s,RH%s,RV%s”

RMS Covariance of GPS Position
..............................
:Record type: CV
:Field headers:
  DC: Derivation (ENUM) |br|
  SV: Minimum number of SV during observation |br|
  SC: Error Scale |br|
  XX: Variance X |br|
  XY: Covariance X,Y |br|
  XZ: Covariance X,Z |br|
  YY: Variance Y |br|
  YZ: Covariance Y,Z |br|
  ZZ: Variance Z
:Sample(s):
  ::

    “CV,DC%s,SV%s,SC%s,XX%s,XY%s,XZ%s,YY%s,YZ%s,ZZ%s”

Datum Grid Record
.................
:Record type: DG
:Field headers:
  FI: File name
:Sample(s):
  ::

    “DG,FI%s”

Datum Record
............
:Record type: DT
:Field headers:
  DA: Type of datum (ENUM) |br|
  RD: Ellipsoid radius |br|
  IF: Ellipse inverse flattening |br|
  OX: Rotation x |br|
  OY: Rotation y |br|
  OZ: Rotation z |br|
  LX: Translation x |br|
  LY: Translation y |br|
  LZ: Translation z |br|
  SP: Scale factor in ppm
:Sample(s):
  ::

    “DT,DA%s,RD%s,IF%s,OX%s,OY%s,OZ%s,LX%s,LY%s,LZ%s,SP%s”

GPS Edit Point Record
.....................
:Record type: EE
:Field headers:
  GF: Geodetic Flags (ENUM) |br|
  SG: Setup Group
:Sample(s):
  ::

    “EE,GF%s,SG%s”

Geodetic position
.................
When a point is stored, its geodetic position is recorded.

:Record type: EP
:Field headers:
  TM: Time |br|
  LA: Latitude |br|
  LN: Longitude |br|
  HT: Ellipsoid Height |br|
  RH: Horizontal RMS returned from receiver |br|
  RV: Vertical RMS returned from receiver |br|
  DH: HDOP if receiver returns this info |br|
  DV: VDOP if receiver returns this info |br|
  GM: GPS Method (ENUM) |br|
  CL: Classification (ENUM)
:Sample(s):
  ::

    “EP,TM%s:%s:%s,LA%s,LN%s,HT%s,RH%s,RV%s,DH%s,DV%s,GM%s,CL%s”
    “EP,TM%s:%s:%s,LA%s,LN%s,HT%s,RH%s,RV%s,GM%s,CL%s”

Equipment Record
................
:Record type: EQ
:Field headers:
  DC: Derivation Code (ENUM) |br|
  RX: Rx Type |br|
  RS: Rx Serial Number |br|
  AN: Antenna Number (from Antenna.ini) |br|
  AI: Antenna Index (measure to index from antenna.ini) |br|
  AT: Antenna Type (name of antenna) |br|
  TS: Antenna Serial Number |br|
  TA: Tape Adjustment |br|
  HO: Horizontal Offset |br|
  VO: Vertical Offset
:Sample(s):
  ::

    “EQ,DC%s,RX%s,RS%s,AN%s,AI%s,AT%s,TS%s,TA%s,HO%s,VO%s”

Ellipsoid Record
................
:Record type: ES
:Field headers:
  RD : a - radius of semi major |br|
  IF: 1/f - inverse flattening |br|
  EM: Name - ellipse name |br|
:Sample(z:
  ::

    “ES,RD%s,IF%s,EM%s”

GPS stakeout record
...................
:Record type: GK
:Field headers:
  PN: Point name (actual point, may be blank) |br|
  N : Northing |br|
  E : Easting |br|
  EL: Elevation |br|
  ``--`` Description (actual point description, may be blank)
:Sample(s):
  ::

    “GK,PN%s,N %s,E %s,EL%s,--%s”

GPS Offset Shot Record
......................
:Record type: GO
:Field headers:
  PN: Point Name |br|
  AZ: Azimuth |br|
  ZE: Zenith Angle |br|
  SD: Slope Distance |br|
  HI: Height of laser at GPS reference point |br|
  HR: Height of laser target at store offset point |br|
  ``--`` Description
:Sample(s):
  ::

    “GO,PN%s,AZ%s,ZE%s,SD%s,HI%s,HR%s,--%s”

GPS Point Record
................
:Record type: GP
:Field headers:
  PN: Point Name |br|
  PT: Point Type (ENUM)
:Sample(s):
  ::

    “GP,PN%s,PT%s”

GPS adjusted point record
.........................
:Record type: GR
:Field headers:
  N : Northing |br|
  E : Easting |br|
  EL: Elevation |br|
  ``--``: Description
:Sample(s):
  ::

    “GR,PN%s,N %s,E %s,EL%s,--%s”

GPS Store Point
...............
The GS record is similar to the SP record, which records the coordinate of a point.
This record identifies the point is created by GPS.

:Record type: GS
:Field headers:
  PN: Point Name |br|
  N : Local Northing |br|
  E : Local Easting |br|
  EL: Local Elevation |br|
  ``--``: Description
:Sample(s):
  ::

    “GS,PN%s,N%s,E%s,EL%s,--%s”

Horizontal Calibration (Adjust)
...............................
:Record type: HA
:Field headers:
  N : Origin north |br|
  E : Origin east |br|
  TH: Translation north |br|
  TE: Translation east |br|
  RT: Rotation about origin |br|
  SF: Scale factor at origin
:Sample(s):
  ::

    “HA,N %s,E %s,TH%s,TE%s,RT%s,SC%s”

Note: all the fields may be blank if there is no adjustment done.

Extended Projection Record
..........................
:Record type: PE
:Field headers:
  TP: Type of projection (ENUM) |br|
  LA: Latitude of origin |br|
  LN: Longitude of origin |br|
  HT: Height of origin |br|
  N : Origin north |br|
  E : Origin east |br|
  EL: Origin elevation |br|
  SC: Scale factor |br|
  OO: Orientation one |br|
  OT: Orientation two |br|
  CT: Origin center (ENUM) |br|
  AF: Azimuth format (ENUM) |br|
  RY: Rectify |br|
  AE: Area (ENUM) |br|
  FO: File name one |br|
  FT: File name two
:Sample(s):
  ::

    “PE,TP%s,LA%s,LN%s,HT%s,N %s,E %s,EL%s,SC%s,OO%s,OT%s, CT%s,AF%s,RY%s,AE%s,FO%s,FT%s”

Projection Record
.................
:Record type: PJ
:Field headers:
  TP: Type of projection (ENUM) |br|
  LA: Latitude of origin |br|
  LN: Longitude of origin |br|
  HT: Height of origin |br|
  N : Origin north |br|
  E : Origin east |br|
  EL: Origin elevation |br|
  SC: Scale factor |br|
  OO: Orientation one |br|
  OT: Orientation two
:Sample(s):
  ::

    “PJ,TP%s,LA%s,LN%s,HT%s,N %s,E %s,EL%s,SC%s,OO%s,OT%s”

Local coordinates of calibration point
......................................
:Record type: RP
:Field headers:
  N : Northing |br|
  E : Easting |br|
  EL: Elevation |br|
  ``--``: Description
:Sample(s):
  ::

    “RP,PN%s,N %s,E %s,EL%s,--%s”

Receiver Setup
..............
:Record type: RX
:Field headers:
  DC: Derivation Code (ENUM) |br|
  RA: Reduced antenna height (to phase centre) |br|
  RE: Recording interval in seconds |br|
  FI: Name of post processing file opened
:Sample(s):
  ::

    “RX,DC%s,RA%s,RE%s,FI%s”

Local site settings
...................
:Record type: ST
:Field headers:
  LA: Latitude |br|
  LN: Longitude |br|
  HT: Height |br|
  SC: Scale factor |br|
  N : Northing offset |br|
  E : Easting offset
:Sample(s):
  ::

    “ST,LA%s,LN%s,HT%s,SC%s,N %s,E %s”

Vertical Calibration (Adjust)
.............................
:Record type: VA
:Field headers:
  PV: Type of vertical adjustment (ENUM) |br|
  N : Origin north (may be blank) |br|
  E : Origin east (may be blank) |br|
  LZ: Constant adjustment – translation Z (may be blank) |br|
  SO: Slope north (may be blank) |br|
  SA: Slope east (may be blank) |br|
  GN: Geoid Model Name
:Sample(s):
  ::

    “VA,PV%s,N %s,E %s,LZ%s,SO%s,SA%s,GN%s”


Legacy Raw Data Record Definitions
___________________________________

These records are not used in Survey Pro version 3.5 and beyond.

Accumulating Angle-right
........................
:Record type: AA
:Field headers:
  BC: Back circle |br|
  AR: Angle right |br|
  ZE: Zenith |br|
  SD: Slope distance
:Sample(s):
  ::

    “AA,BC%s,AR%s,ZE%s,SD%s”

Bench level, backsight
......................
:Record type: BB
:Field headers:
  PN: Backsight point |br|
  EL: BS elevation |br|
  ZE: Zenith |br|
  SD: Slope distance |br|
  ``--``: Description
:Sample(s):
  ::

    “BB,PN%s,EL%s,ZE%s,SD%s,--%s”

Base Point Geoid Model Elevation
................................
Replaced by Vertical adjustment record VA.

:Record type: BG
:Field headers:
  PN: Point Name |br|
  HT: Ellipsoid Height |br|
  GU: Geoid Undulation at base |br|
  EL: Elevation of base
:Sample(s):
  ::

    “BG,PN%s,HT%s,GU%s,EL%s”

Bench level, side shots
.......................
:Record type: BS
:Field headers:
  PN: FS point |br|
  ZE: Zenith |br|
  SD: Slope distance |br|
  ``--``: Description
:Sample(s):
  ::

    “BS,PN%s,ZE%s,SD%s,--%s”

Bench level, traverse
.....................
:Record type: BT
:Field headers:
  PN: FS point |br|
  ZE: Zenith |br|
  SD: Slope distance |br|
  ``--``: Description
:Sample(s):
  ::

    “BT,PN%s,ZE%s,SD%s,--%s”

Horizontal Control Point
........................
When solving local transformation, each control point’s lat, long and height will be
recorded.

:Record type: HC
:Field headers:
  PN: Point Name |br|
  LA: Latitude |br|
  LN: Longitude |br|
  HT: Ellipsoid Height |br|
  ``--``: Description
:Sample(s):
  ::

    “HC,PN%s,LA%s,LN%s,HT%s,--%s”

Vertical Ellipsoid Height Setup
...............................
Replaced by the vertical adjust record VA.

:Record type: LE
:Field headers:
  ``--``: Description string
:Sample(s):
  ::

    “LE,--%s”

Vertical Geoid Model Setup
..........................
Replaced by the vertical adjust record VA.

:Record type: LG
:Field headers:
  GI: Geoid model index
:Sample(s):
  ::

    “LG,GI%s”

Horizontal Mapping Plane Setup
..............................
Replaced by the projection records (ES,PJ,DT,CS).

:Record type: LM
:Field headers:
  ME: Method |br|
  CS: Coordinate System |br|
  DA: Datum |br|
  ZO: Zone |br|
  HE: Hemisphere |br|
  FI: Custom file name (cs5 or pj5)
:Sample(s):
  ::

    “LM,ME%s,CS%s,DA%s,ZO%s,HE%s,FI%s”

Local transforming coefficients for horizontal
..............................................
Replaced by Horizontal adjustment record HA.

:Record type: LH
:Field headers:
  PN: Point Name |br|
  Ha: Coefficient a |br|
  Hb: Coefficient b |br|
  Hc: Coefficient c |br|
  Hd : Coefficient d |br|
  SC: Scale |br|
  RT: Rotation
:Sample(s):
  ::

    “LH,PN%s,Ha%s,Hb%s,Hc%s,Hd%s,SC%s,RT%s”

Local transforming coefficients for vertical
............................................
Replaced by Vertical adjustment record VA.

:Record type: LV
:Field headers:
  PN: Point Name |br|
  Va: Coefficient a |br|
  Vb: Coefficient b |br|
  Vc: Coefficient c |br|
  Ba: Base Latitude |br|
  Bo: Base Longitude |br|
  Bh: Base Ellipsoid Height
:Sample(s):
  ::

    “LV,PN%s,Va%s,Vb%s,Vc%s,Ba%s,Bo%s,Bh%s”

Vertical Control point
......................
When solving local transformation, each control point’s lat, long and height will be
recorded.

:Record type: VC
:Field headers:
  PN: Control point number |br|
  LA: Latitude of control point |br|
  LN: Longitude of control point |br|
  HT: Ellipsoid height of control point |br|
  ``--``: Description
:Sample(s):
  ::

    “VC,PN%s,LA%s,LN%s,HT%s,--%s”
