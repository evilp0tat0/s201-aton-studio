<?xml version="1.0" encoding="UTF-8"?>
<DataSet xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:s100_profile="http://www.iho.int/S-100/profile/s100_gmlProfile" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:S100="http://www.iho.int/s100gml/1.0" xmlns:S201="http://www.iho.int/201/gml/1.0" gml:id="GML_ID_GHKLP8">
    <gml:boundedBy>
        <gml:Envelope srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
            <gml:lowerCorner>33.1652035 124.7081621</gml:lowerCorner>
            <gml:upperCorner>34.3055553 126.4072269</gml:upperCorner>
        </gml:Envelope>
    </gml:boundedBy>
    <members>
        <LateralBuoy gml:id="NfWii">
            <categoryOfLateralMark>Starboard-Hand Lateral Mark</categoryOfLateralMark>
            <buoyShape>Pillar</buoyShape>
            <colour>Red</colour>
            <status>Permanent</status>
            <AtoNNumber>US098180522301950</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Hatteras Connector Lighted Buoy 12</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#SjgvZ" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_193DU" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.0444127 124.7081621</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LateralBuoy>
        <LightAllAround gml:id="SjgvZ">
            <colour>Red</colour>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <rhythmOfLight>
                <lightCharacteristic>Flashing</lightCharacteristic>
                <signalGroup>(1)</signalGroup>
                <signalPeriod>4</signalPeriod>
                <signalSequence>
                    <signalDuration>00.3</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>03.7</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
            </rhythmOfLight>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Hatteras Connector Lighted Buoy 12</name>
            </featureName>
            <parent xlink:href="#NfWii" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_asRqj" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.0444127 124.7081621</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <SpecialPurposeGeneralBuoy gml:id="ja0ij">
            <categoryOfSpecialPurposeMark>ODAS</categoryOfSpecialPurposeMark>
            <buoyShape>Superbuoy</buoyShape>
            <colour>Yellow</colour>
            <status>Permanent</status>
            <AtoNNumber>US099903435302030</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>NOAA Lighted Data Buoy 41025 (ODAS)</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#vJwm1" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_kpeAV" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>33.6490956 125.4876391</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </SpecialPurposeGeneralBuoy>
        <LightAllAround gml:id="vJwm1">
            <colour>Yellow</colour>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <rhythmOfLight>
                <lightCharacteristic>Flashing</lightCharacteristic>
                <signalGroup>(4)</signalGroup>
                <signalPeriod>20</signalPeriod>
            </rhythmOfLight>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>NOAA Lighted Data Buoy 41025 (ODAS)</name>
            </featureName>
            <parent xlink:href="#ja0ij" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_Hf6G5" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>33.6490956 125.4876391</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <Landmark gml:id="J0B3k">
            <categoryOfLandmark>Tower</categoryOfLandmark>
            <colour>Black</colour>
            <colour>White</colour>
            <colourPattern>Vertical Stripes</colourPattern>
            <function>Light Support</function>
            <status>Permanent</status>
            <visualProminence>Visually Conspicuous</visualProminence>
            <height>49.7</height>
            <AtoNNumber>US002806306900050</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Charleston Light</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#M5sMc" />
            <child xlink:title="StructureEquipment" xlink:href="#9Yf3F" />
            <child xlink:title="StructureEquipment" xlink:href="#u4t4W" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_6bSpc" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>33.3333865 126.1754735</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </Landmark>
        <LightSectored gml:id="M5sMc">
            <colour>White</colour>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <sectorCharacteristics>
                <lightCharacteristic>Flashing</lightCharacteristic>
                <lightSector>
                    <colour>White</colour>
                    <valueOfNominalRange>20</valueOfNominalRange>
                </lightSector>
                <signalGroup>(2)</signalGroup>
                <signalPeriod>29</signalPeriod>
            </sectorCharacteristics>
            <height>49.7</height>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Charleston Light</name>
            </featureName>
            <parent xlink:href="#J0B3k" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_acIdC" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>33.3333865 126.1754735</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightSectored>
        <LightAllAround gml:id="9Yf3F">
            <colour>White</colour>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <valueOfNominalRange>20</valueOfNominalRange>
            <rhythmOfLight>
                <lightCharacteristic>Flashing</lightCharacteristic>
                <signalGroup>(2)</signalGroup>
                <signalPeriod>32</signalPeriod>
            </rhythmOfLight>
            <height>49.7</height>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Charleston Light</name>
            </featureName>
            <parent xlink:href="#J0B3k" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_OtMwb" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>33.3333865 126.1754735</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <LightAllAround gml:id="u4t4W">
            <colour>White</colour>
            <categoryOfLight>Emergency</categoryOfLight>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <valueOfNominalRange>20</valueOfNominalRange>
            <rhythmOfLight>
                <lightCharacteristic>Flashing</lightCharacteristic>
                <signalGroup>(2)</signalGroup>
                <signalPeriod>30</signalPeriod>
            </rhythmOfLight>
            <height>49.7</height>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Charleston Light</name>
            </featureName>
            <parent xlink:href="#J0B3k" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_Cl3iN" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>33.3333865 126.1754735</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <SpecialPurposeGeneralBeacon gml:id="99BeU">
            <categoryOfSpecialPurposeMark>Mark Leading</categoryOfSpecialPurposeMark>
            <beaconShape>Lattice Beacon</beaconShape>
            <colour>White</colour>
            <status>Permanent</status>
            <AtoNNumber>US002805920600050</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Wando River Range A Rear Light</name>
            </featureName>
            <child xlink:href="#zpoeS" xlink:title="StructureEquipment" />
            <child xlink:href="#L3V5r" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_oUoUl" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.2710743 126.0814137</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </SpecialPurposeGeneralBeacon>
        <NavigationLine gml:id="Ruo1F">
            <categoryOfNavigationLine>Leading Line Bearing a Recommended Track</categoryOfNavigationLine>
            <orientation>
                <orientationValue>27</orientationValue>
            </orientation>
            <geometry>
                <S100:curveProperty>
                    <gml:Curve gml:id="GEOMETRY_ID_HByzN" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:segments>
                            <gml:LineStringSegment>
                                <gml:posList>34.2710743 126.0814137 34.2759396 126.1029669</gml:posList>
                            </gml:LineStringSegment>
                        </gml:segments>
                    </gml:Curve>
                </S100:curveProperty>
            </geometry>
        </NavigationLine>
        <LightAllAround gml:id="zpoeS">
            <colour>White</colour>
            <categoryOfLight>Subsidiary Light</categoryOfLight>
            <rhythmOfLight>
                <lightCharacteristic>Flashing</lightCharacteristic>
                <signalGroup>(1)</signalGroup>
                <signalPeriod>6</signalPeriod>
            </rhythmOfLight>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Wando River Range A Rear Light</name>
            </featureName>
            <parent xlink:title="StructureEquipment" xlink:href="#99BeU" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_IPvt1" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.2710743 126.0814137</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <LightSectored gml:id="L3V5r">
            <colour>Green</colour>
            <exhibitionConditionOfLight>Light Shown Without Change of Character</exhibitionConditionOfLight>
            <sectorCharacteristics>
                <lightCharacteristic>Isophased</lightCharacteristic>
                <lightSector>
                    <colour>Green</colour>
                </lightSector>
                <signalGroup>(1)</signalGroup>
                <signalPeriod>6</signalPeriod>
            </sectorCharacteristics>
            <height>11.6</height>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Wando River Range A Rear Light</name>
            </featureName>
            <parent xlink:title="StructureEquipment" xlink:href="#99BeU" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_KnQG1" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.2710743 126.0814137</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightSectored>
        <Pile gml:id="v1djf">
            <AtoNNumber>US06920624670646</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Bridge Light</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#ucfkA" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_E3qJ8" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.294113 126.2259339</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </Pile>
        <LightAllAround gml:id="ucfkA">
            <colour>Red</colour>
            <categoryOfLight>Air Obstruction Light</categoryOfLight>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <rhythmOfLight>
                <lightCharacteristic>Flashing</lightCharacteristic>
                <signalGroup>(1)</signalGroup>
            </rhythmOfLight>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Bridge Light</name>
            </featureName>
            <parent xlink:href="#v1djf" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_uDaVB" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.294113 126.2259339</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <Pile gml:id="atngk">
            <AtoNNumber>US057709752406465</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Bridge-RACON</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#Dt60a" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_omG2r" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.1486725 126.309401</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </Pile>
        <RadarTransponderBeacon gml:id="Dt60a">
            <categoryOfRadarTransponderBeacon>Racon, Radar Transponder Beacon</categoryOfRadarTransponderBeacon>
            <radarWaveLength>
                <radarBand>X</radarBand>
                <waveLengthValue>0.03</waveLengthValue>
            </radarWaveLength>
            <signalGroup>(B)</signalGroup>
            <status>Private</status>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Bridge-RACON</name>
            </featureName>
            <parent xlink:href="#atngk" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_gP5FZ" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.1486725 126.309401</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </RadarTransponderBeacon>
        <SafeWaterBuoy gml:id="lMTpv">
            <buoyShape>Pillar</buoyShape>
            <colour>Red</colour>
            <colour>White</colour>
            <colourPattern>Vertical Stripes</colourPattern>
            <status>Permanent</status>
            <AtoNNumber>US033467246504851</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Little River Inlet Lighted Buoy LR</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#6EvjU" />
            <child xlink:title="StructureEquipment" xlink:href="#V8W0M" />
            <topmarkPart xlink:title="BuoyTopmark" xlink:href="#7ZYc1" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_IjDL1" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.3055553 126.4072269</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </SafeWaterBuoy>
        <LightAllAround gml:id="6EvjU">
            <colour>White</colour>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <rhythmOfLight>
                <lightCharacteristic>Morse</lightCharacteristic>
                <signalGroup>(A)</signalGroup>
                <signalPeriod>8</signalPeriod>
                <signalSequence>
                    <signalDuration>00.4</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>00.6</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>02.0</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>05.0</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
            </rhythmOfLight>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Little River Inlet Lighted Buoy LR</name>
            </featureName>
            <parent xlink:href="#lMTpv" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_sgRGM" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.3055553 126.4072269</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <Topmark gml:id="7ZYc1">
            <colour>Red</colour>
            <topmarkDaymarkShape>Sphere</topmarkDaymarkShape>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Little River Inlet Lighted Buoy LR</name>
            </featureName>
            <buoyPart xlink:href="#lMTpv" xlink:title="BuoyTopmark" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_EKMmB" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.3055553 126.4072269</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </Topmark>
        <RadioStation gml:id="V8W0M">
            <categoryOfRadioStation>AIS Base Station</categoryOfRadioStation>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Little River Inlet Lighted Buoy LR</name>
            </featureName>
            <parent xlink:href="#lMTpv" xlink:title="StructureEquipment" />
            <physicalAISbroadcastBy xlink:title="PhysicalAIS" xlink:href="#dnnY0" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_UZ8Q6" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.3055553 126.4072269</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </RadioStation>
        <PhysicalAISAidToNavigation gml:id="dnnY0">
            <categoryOfPhysicalAISAidToNavigation>Physical AIS Type 1</categoryOfPhysicalAISAidToNavigation>
            <mMSICode>993672126</mMSICode>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Little River Inlet Lighted Buoy LR</name>
            </featureName>
            <physicalAISbroadcasts xlink:href="#V8W0M" xlink:title="PhysicalAIS" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_xCmEo" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.3055553 126.4072269</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </PhysicalAISAidToNavigation>
        <LateralBuoy gml:id="y3vjU">
            <categoryOfLateralMark>Port-Hand Lateral Mark</categoryOfLateralMark>
            <buoyShape>Pillar</buoyShape>
            <colour>Green</colour>
            <status>Permanent</status>
            <AtoNNumber>US011589653904107</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Cape Fear River Entrance Channel Lighted Buoy 3</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#mPt33" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_CHYDm" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.271228 126.3702744</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LateralBuoy>
        <LightAllAround gml:id="mPt33">
            <colour>Green</colour>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <rhythmOfLight>
                <lightCharacteristic>Flashing</lightCharacteristic>
                <signalGroup>(1)</signalGroup>
                <signalPeriod>4</signalPeriod>
                <signalSequence>
                    <signalDuration>00.4</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>03.6</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
            </rhythmOfLight>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Cape Fear River Entrance Channel Lighted Buoy 3</name>
            </featureName>
            <parent xlink:href="#y3vjU" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_5sFr4" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.271228 126.3702744</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <SpecialPurposeGeneralBeacon gml:id="KUvHS">
            <categoryOfSpecialPurposeMark>Leading Mark</categoryOfSpecialPurposeMark>
            <beaconShape>Pile Beacon</beaconShape>
            <colour>White</colour>
            <status>Permanent</status>
            <AtoNNumber>US011589570204107</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Southport Channel Range Front Light</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#EbC1D" />
            <child xlink:title="StructureEquipment" xlink:href="#mADmK" />
            <child xlink:title="StructureEquipment" xlink:href="#BETdU" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_TYXdy" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.1430854 126.16209</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </SpecialPurposeGeneralBeacon>
        <LightSectored gml:id="EbC1D">
            <colour>White</colour>
            <categoryOfLight>Leading Light</categoryOfLight>
            <exhibitionConditionOfLight>Daytime Light</exhibitionConditionOfLight>
            <sectorCharacteristics>
                <lightCharacteristic>Quick-Flashing</lightCharacteristic>
                <lightSector>
                    <colour>White</colour>
                    <sectorLimit>
                        <sectorLimitOne>
                            <sectorBearing>314</sectorBearing>
                        </sectorLimitOne>
                        <sectorLimitTwo>
                            <sectorBearing>325</sectorBearing>
                        </sectorLimitTwo>
                    </sectorLimit>
                </lightSector>
                <signalGroup>(1)</signalGroup>
                <signalPeriod>1</signalPeriod>
                <signalSequence>
                    <signalDuration>00.3</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>00.7</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
            </sectorCharacteristics>
            <height>22</height>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Southport Channel Range Front Light</name>
            </featureName>
            <parent xlink:href="#KUvHS" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_u0Paw" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.1430854 126.16209</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightSectored>
        <LightAllAround gml:id="mADmK">
            <colour>White</colour>
            <categoryOfLight>Leading Light</categoryOfLight>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <rhythmOfLight>
                <lightCharacteristic>Quick-Flashing</lightCharacteristic>
                <signalGroup>(1)</signalGroup>
                <signalPeriod>1</signalPeriod>
                <signalSequence>
                    <signalDuration>00.3</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>00.7</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
            </rhythmOfLight>
            <height>7</height>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Southport Channel Range Front Light</name>
            </featureName>
            <parent xlink:href="#KUvHS" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_GGOnX" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.1430854 126.16209</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <LightSectored gml:id="BETdU">
            <colour>White</colour>
            <categoryOfLight>Leading Light</categoryOfLight>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <sectorCharacteristics>
                <lightCharacteristic>Quick-Flashing</lightCharacteristic>
                <lightSector>
                    <colour>White</colour>
                    <lightVisibility>Intensified</lightVisibility>
                    <sectorLimit>
                        <sectorLimitOne>
                            <sectorBearing>318</sectorBearing>
                        </sectorLimitOne>
                        <sectorLimitTwo>
                            <sectorBearing>321</sectorBearing>
                        </sectorLimitTwo>
                    </sectorLimit>
                </lightSector>
                <signalGroup>(1)</signalGroup>
                <signalPeriod>1</signalPeriod>
                <signalSequence>
                    <signalDuration>00.3</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>00.7</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
            </sectorCharacteristics>
            <height>6.7</height>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Southport Channel Range Front Light</name>
            </featureName>
            <parent xlink:href="#KUvHS" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_1baf0" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.1430854 126.16209</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightSectored>
        <SafeWaterBuoy gml:id="Pz1f2">
            <buoyShape>Pillar</buoyShape>
            <colour>Red</colour>
            <colour>White</colour>
            <colourPattern>Vertical Stripes</colourPattern>
            <status>Permanent</status>
            <AtoNNumber>US045280074705626</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Masonboro Inlet Lighted Whistle Buoy A</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#KoZFa" />
            <child xlink:title="StructureEquipment" xlink:href="#nDZSm" />
            <topmarkPart xlink:title="BuoyTopmark" xlink:href="#J6cXB" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_NnwWK" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.0401939 125.9149188</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </SafeWaterBuoy>
        <LightAllAround gml:id="KoZFa">
            <colour>White</colour>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <rhythmOfLight>
                <lightCharacteristic>Morse</lightCharacteristic>
                <signalGroup>(A)</signalGroup>
                <signalPeriod>8</signalPeriod>
                <signalSequence>
                    <signalDuration>00.4</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>00.6</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>02.0</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>05.0</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
            </rhythmOfLight>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Masonboro Inlet Lighted Whistle Buoy A</name>
            </featureName>
            <parent xlink:href="#Pz1f2" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_tlRHG" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.0401939 125.9149188</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <Topmark gml:id="J6cXB">
            <colour>Red</colour>
            <topmarkDaymarkShape>Sphere</topmarkDaymarkShape>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Masonboro Inlet Lighted Whistle Buoy A</name>
            </featureName>
            <buoyPart xlink:href="#Pz1f2" xlink:title="BuoyTopmark" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_MrVxC" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.0401939 125.9149188</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </Topmark>
        <FogSignal gml:id="nDZSm">
            <categoryOfFogSignal>Whistle</categoryOfFogSignal>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Masonboro Inlet Lighted Whistle Buoy A</name>
            </featureName>
            <parent xlink:href="#Pz1f2" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_sLTo4" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.0401939 125.9149188</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </FogSignal>
        <Landmark gml:id="9uaEA">
            <categoryOfLandmark>Tower</categoryOfLandmark>
            <function>Light Support</function>
            <natureOfConstruction>Masonry</natureOfConstruction>
            <status>Permanent</status>
            <visualProminence>Visually Conspicuous</visualProminence>
            <verticalLength>13.7</verticalLength>
            <AtoNNumber>US006011929508644</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Race Rock Light</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#AlgxW" />
            <child xlink:title="StructureEquipment" xlink:href="#Z4Qn0" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_8jeaW" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.2765581 126.0556583</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </Landmark>
        <LightAllAround gml:id="AlgxW">
            <colour>Red</colour>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <valueOfNominalRange>14</valueOfNominalRange>
            <rhythmOfLight>
                <lightCharacteristic>Flashing</lightCharacteristic>
                <signalGroup>(1)</signalGroup>
                <signalPeriod>10</signalPeriod>
                <signalSequence>
                    <signalDuration>01.0</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>09.0</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
            </rhythmOfLight>
            <height>20.4</height>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Race Rock Light</name>
            </featureName>
            <parent xlink:href="#9uaEA" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_AM4FN" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.2765581 126.0556583</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <FogSignal gml:id="Z4Qn0">
            <categoryOfFogSignal>Horn</categoryOfFogSignal>
            <signalGroup>(2)</signalGroup>
            <signalPeriod>30</signalPeriod>
            <signalSequence>
                <signalDuration>02.0</signalDuration>
                <signalStatus>Lit/Sound</signalStatus>
            </signalSequence>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Race Rock Light</name>
            </featureName>
            <parent xlink:href="#9uaEA" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_SO1mR" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.2765581 126.0556583</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </FogSignal>
        <LateralBeacon gml:id="oiaqe">
            <categoryOfLateralMark>Starboard-Hand Lateral Mark</categoryOfLateralMark>
            <beaconShape>Stake, Pole, Perch, Post</beaconShape>
             colour>Red</colour>
            <status>Permanent</status>
            <AtoNNumber>US019371614004159</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Hatteras Inlet Channel Light 24</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#lU1pn" />
            <child xlink:title="StructureEquipment" xlink:href="#NPvJ5" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_biVc6" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>33.1652035 126.2705239</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LateralBeacon>
        <LightAllAround gml:id="NPvJ5">
            <colour>Red</colour>
            <exhibitionConditionOfLight>Night Light</exhibitionConditionOfLight>
            <valueOfNominalRange>4</valueOfNominalRange>
            <rhythmOfLight>
                <lightCharacteristic>Quick-Flashing</lightCharacteristic>
                <signalGroup>(1)</signalGroup>
                <signalPeriod>1</signalPeriod>
                <signalSequence>
                    <signalDuration>00.3</signalDuration>
                    <signalStatus>Lit/Sound</signalStatus>
                </signalSequence>
                <signalSequence>
                    <signalDuration>00.7</signalDuration>
                    <signalStatus>Eclipsed/Silent</signalStatus>
                </signalSequence>
            </rhythmOfLight>
            <height>5.8</height>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Hatteras Inlet Channel Light 24</name>
            </featureName>
            <parent xlink:href="#oiaqe" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_r9jMR" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>33.1652035 126.2705239</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
        <Daymark gml:id="lU1pn">
            <colour>Red</colour>
            <colourPattern>Border Stripe</colourPattern>
            <topmarkDaymarkShape>Triangle (Point Up)</topmarkDaymarkShape>
            <isSlatted>false</isSlatted>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Hatteras Inlet Channel Light 24</name>
            </featureName>
            <parent xlink:href="#oiaqe" xlink:title="StructureEquipment" />
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_4GX4J" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>33.1652035 126.2705239</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </Daymark>
    </members>
</DataSet>
