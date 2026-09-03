<?xml version="1.0" encoding="UTF-8"?>
<DataSet xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:s100_profile="http://www.iho.int/S-100/profile/s100_gmlProfile" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:S100="http://www.iho.int/s100gml/1.0" xmlns:S201="http://www.iho.int/201/gml/1.0" gml:id="GML_ID_GHKLP8">
    <gml:boundedBy>
        <gml:Envelope srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
            <gml:lowerCorner>33.1652035 124.7081621</gml:lowerCorner>
            <gml:upperCorner>34.3055553 126.4072269</gml:upperCorner>
        </gml:Envelope>
    </gml:boundedBy>
    <members>
        <Pile gml:id="v1djf">
            <AtoNNumber>US06920624670646</AtoNNumber>
            <featureName>
                <displayName>false</displayName>
                <language>ENG</language>
                <name>Bridge Light</name>
            </featureName>
            <child xlink:title="StructureEquipment" xlink:href="#ucfkA"/>
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_E3qJ8" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.294113 126.2259339</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        <rhythmOfLight><signalPeriod>1</signalPeriod></rhythmOfLight></Pile>
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
            <parent xlink:href="#v1djf" xlink:title="StructureEquipment"/>
            <geometry>
                <S100:pointProperty>
                    <S100:Point gml:id="GEOMETRY_ID_uDaVB" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2">
                        <gml:pos>34.294113 126.2259339</gml:pos>
                    </S100:Point>
                </S100:pointProperty>
            </geometry>
        </LightAllAround>
    </members>
</DataSet>
