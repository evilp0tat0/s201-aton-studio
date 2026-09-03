# Reference-source manifest

The public snapshot of S-201 AtoN Studio redistributes **none** of the third-party reference material listed here: the IHO and IALA publications, the S-201 Feature Catalogue XML, the IHO S-100 / S-201 schema families with the OGC, ISO and W3C schemas they import, the S-158 check tables and the S-62 producer-code data under `dev/spec-sources/`; the plain-text extracts under `dev/pdf-extracts/` derived from those publications; and `dev/tmp_verify_imgs/`. All of it is freely obtainable from its official source (the IALA publications carry no redistribution grant in their text, and the IHO copyright terms permit free-of-charge redistribution only together with an IHO-Secretariat permission statement this project does not hold), so the snapshot ships this manifest instead.

To follow a citation in the source (`FC 2.0.0 XML L11003-11023`, `r1001_ed2_full.txt L384-393`, `S-100 Pt 10b §10b-11.7`, an XSD line), obtain the named file from the source given for its folder, check that its SHA-256 matches the value below, and place it at the manifest path relative to the project root; the line numbers then resolve byte-for-byte to what the validator's citations were checked against. The extracts are regenerated from the publications, not downloaded.

The development repository keeps all of these files; `Annex_D/` (the S-201 Annex D portrayal library, © IHO / IALA) is the one third-party component the snapshot does ship, because the app cannot render without it — see NOTICE.txt.


## `dev/pdf-extracts/` (71 files)

Obtain from: Plain-text extractions of the publications above (PyMuPDF; the `.docx`-derived one by a zipfile + document.xml parse), regenerable from the originals; `MANIFEST.sha256` is the development repository's integrity manifest for them (pre-commit check #17).

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| MANIFEST.sha256 | 6,140 | `6270b6624faa879f334da9d93bf7ad7635ec2a12171c31cb1c2df70f86d6143e` |
| annex_c1_full.txt | 600,008 | `c5a09e4725429b68c5a9cc35412e3dbbbea81a623cdb7d20d97635a0fcfe231c` |
| annex_c1_pages_1_30.txt | 55,400 | `87e728ec78088284cbbc53baccb42562c035ec5a23048131193ac78c481fc137` |
| dceg_annex_a.txt | 467,151 | `bc32949b2f74da556edc3bc43ba2f68ebfce3cd1ad4c286ed3ebdb54d6c7c30b` |
| g1004_ed3_1_full.txt | 16,982 | `230e25536a4788fc065a35c9baf3859ce83b2a8aa086ff77024f1db83c8e0059` |
| g1018_ed4_0_full.txt | 59,449 | `17f79321c9e49ecaa02aa7fa4e7eacd1fa4ef3156951e4a816de661dd6bc448f` |
| g1035_ed2_1_full.txt | 82,220 | `3376e4ba7cdc8def8cd08e94355f2064a76b9729dd4f38e8a67914dd05b3dfdc` |
| g1046_ed2_1_full.txt | 16,900 | `8c6e62417ca1c5d9fb0e7b1184ce24048358a4a377359fa6d433c4dba48c0cc7` |
| g1052_ed3_2_full.txt | 55,078 | `8daf012eb288d479e7a1088dbab79c7b22e3beede6fa16a02c4c4a53b1adbfed` |
| g1054_ed2_0_full.txt | 40,482 | `e1be3392fe9c3352a6abece8537208123c28e0f017c6fe79dd3fe3af109bd206` |
| g1057_ed1_1_full.txt | 19,274 | `11db3e890c760010bd524fa5bc71325db082d312a75179f9eb3ffce1d5c4b8a8` |
| g1058_ed3_0_full.txt | 83,142 | `eb9a999c10de8f033d6c1cd8adfd037bab483dbcc9243a168e26ca2cbe07b22f` |
| g1059_ed1_0_full.txt | 13,036 | `1a855a7ea667c12091617416ab8e20508a2bff60b4a9f64cb2f0967fb5fa67db` |
| g1062_ed1_1_full.txt | 40,391 | `f0184133dec0bd5ed0b6e18b42d77dbe970e0c29bdb35956a015beb6cb1bcc88` |
| g1066_ed1_2_full.txt | 117,844 | `951c58c74c95bf1adbc1240a9d23b3ec4bebe7781aeb40a7ce8c0b07473b3bec` |
| g1081_ed2_1_full.txt | 71,808 | `96ca6190e0e2880d8672f2a2ae8dd19215d88b81c683fb46ade8904e636e8a81` |
| g1084_ed1_1_full.txt | 13,114 | `f37ea461dde815d22dda242bbf2907160d70fcdbf1aa33e0c7eda5590523a030` |
| g1085_ed1_1_full.txt | 116,342 | `b483e956434a934b4a62f2cb80f029cf310124d76c7daaffa0a1491b2ce760ea` |
| g1087_ed3_1_full.txt | 32,210 | `e9ac5fe27515156a6ca953bf3985a728fe0cadd240ac2c9b210b58563dbc74cc` |
| g1088_ed1_1_full.txt | 18,973 | `761c337e9a6848d1b2f52597f6ad967380f54bdc46769020f535fba2615fe2d9` |
| g1101_ed1_1_full.txt | 20,791 | `67e971a3749264a0807d06bfa9564bbace8122da0378ba9063cf88490b9d5a3d` |
| g1106_ed2_1_full.txt | 56,994 | `9fff6e571e101c01e123c3cbd06322e8130d7fab71064008c2a4aee878e576db` |
| g1115_ed1_1_full.txt | 44,018 | `dc3800f704e61417c767f0809093acc7f6faf4836bc34b63a4e51546050b7ad1` |
| g1121_ed1_2_full.txt | 53,313 | `110b9b19ca9cccf879766ff01e81b043dc7b9faa2c72915479b92ab71c752dca` |
| g1134_ed2_1_full.txt | 76,504 | `d265add12fd6a298747f3752e6ad80f41e030470fc18641758c5ba991a325335` |
| g1138_ed2_0_full.txt | 41,681 | `41de6dee05c9cf6ae524ac00fdccd4b1e9600b544cf4f60da0b3e1db05eba539` |
| g1143_ed3_1_full.txt | 31,947 | `a665ecdb3b7193104fbc61bffb50dafbb8c7e9d2d5b87d537dcaf9c641ea7e7e` |
| g1154_ed1_1_full.txt | 18,796 | `7ce5347bd77b16f637dfb89164b0ca578b3743a4bfa11b32ed41d938680b03f4` |
| g1162_ed1_1_full.txt | 47,977 | `441513d7e16d550654a3436b824fb6f70bdb35b072548e1b983e3aca08ebb76a` |
| g1168_ed1_1_full.txt | 63,102 | `f27300507202555b61cb6b258f477b04206698a8b3fb31231811fc903ca9a8ff` |
| g1188_ed1_0_full.txt | 48,946 | `58dad5dc83835ec09104cdf679da6725dddbe95c29f9870b119d6d0a9c7e23b5` |
| r0104_ed2_1_full.txt | 7,207 | `3230f8a7c1398172ded5c86165ab36a888091d2d40d8cce3d1ceeca65ff7bec1` |
| r0106_ed2_1_full.txt | 13,264 | `4367a425d5cd23ce67f7d36afbb5cb7c1a6a77afda03c9d6cf6521f451d20ac3` |
| r0107_ed2_1_full.txt | 3,170 | `75d9b45913887e6bc177cb50bded5d1d30781bed41deefe6104e270040c26236` |
| r0108_ed4_1_full.txt | 7,832 | `1fce0d7c40e7b1f5458258c42c68f89e7a94e10d5636247f6cd47e64a9e489cc` |
| r0109_ed1_1_full.txt | 62,940 | `0eab6dffe0a89e11bae1cff6318c3544d5bace8cb61b2f752ce9e6b2cfc0c70c` |
| r0110_ed5_full.txt | 28,251 | `7fb544de288be3600b43c4fb2d2a9a0a53494cb51067d80c151a8b48a3cb56be` |
| r0111_ed1_3_full.txt | 5,895 | `ea2b8c95f404e662c5a49933fbd1d195e79ab03f930d7dd6027e3e655b08c8ee` |
| r0112_ed1_2_full.txt | 29,454 | `d57c82fdb73dc645f6087af3ef485bac0313c39b5cbe652ab999ea853c317e26` |
| r0113_ed2_1_full.txt | 13,635 | `ae437f6e5e419efd1ced954e99738b2c3bcd29addb7fa9c937b0fbb0a264237c` |
| r0118_ed1_2_full.txt | 2,933 | `7606b80991ebee82684e9b7baf29ea19810a9994b45e1ec77e717e9950db146b` |
| r0126_ed2_0_full.txt | 72,815 | `67d18a543b85c7d6f3e25c815296dcb2915b7a18072bfb4f7803792de70e1118` |
| r0130_ed3_1_full.txt | 13,547 | `4f1ef7f349ab019c56c0e519ce7e298f81a8a9bc0034b79b53acd912ab385f65` |
| r0132_ed3_0_full.txt | 5,568 | `831d49add475b26f64c8ca0008f820f9d01211d97e1b08f9ae13a9f32551107a` |
| r0138_ed1_1_full.txt | 14,077 | `5d519627d0b17d0c09f8eaca4fb5881d668d24407d0b6b1ca28e48f6fa8822cb` |
| r0139_ed3_0_full.txt | 5,291 | `bb23d404487acc4aaeec3875a93c48040e827488120d93757a47befdfa392d54` |
| r0143_ed2_0_full.txt | 20,774 | `dd0d669852f8528cfe5345f8a926c5016be4475f3b9e1a9aaad7bed538b9e00e` |
| r0147_ed2_1_full.txt | 5,536 | `cee75bd08a17cf46086dc2fc0e3b6fb25ea569235ea5f3bbc6dd4885517efe91` |
| r0201_ed3_1_full.txt | 4,716 | `981ba6562b4672114f15dff97a089a4d5c06b9ddd32e2c14d8e0925b55c97e9b` |
| r0202_ed2_1_full.txt | 10,554 | `faf2264143f89d5bf44eccca68873a5a2b0178044edc3f147be8457fc13e568e` |
| r0203_ed2_0_full.txt | 8,875 | `b58f4386917e109836b9b95fd1e36250dd9d73a90cc82042ae8e44f2edced7bf` |
| r0204_ed3_0_full.txt | 4,474 | `8dc50bb8ca16c0056660da12f9330ba3c863f00c2f225b68fe60729ff6e481cc` |
| r0205_ed1_1_full.txt | 65,030 | `bb84a576527ca8c6d3913823cb3166a3d59371132f0af825497732deba256a60` |
| r1001_ed2_full.txt | 71,808 | `a6f2da0bdc9e30a6a5d146266e30ee97817a75c013de292809969edb9855e319` |
| r1002_ed1_1_full.txt | 3,076 | `98b9350eb37b9cdd207e791fe18b612e0b535ef67f3d0c181a52a6969472e9e7` |
| r1010_ed1_1_full.txt | 10,529 | `4e0c660303f54f563a9d1aea68782ae7181644b9a45591b758038a8bae5bf273` |
| r1015_ed1_1_full.txt | 4,431 | `e04b7f53b1e8e55cbc51fa649ca1e26ee4480b31378bb46ce3f9f71fa5ea5a97` |
| r1016_ed2_0_full.txt | 4,780 | `fb483f33caca4b0fd00f57134f00192bfb6b36c30ce27eb596734061fc91662e` |
| s100_brochure_2017_full.txt | 12,243 | `d839a6a557751619af0810df883fc79d75c50d0350426e99c68920379bc05ecc` |
| s100_ed5_2_0_full.txt | 1,909,108 | `607ea5c4f5e533bf2ebf75ead59d93261ebe270ec38be42f11bb241a4807cd50` |
| s100_roadmap_annex4_2023_full.txt | 113,901 | `3229d579621c6d3bed996a1bbacbfae6d4404f70c1589cdf08b731e183677adb` |
| s1010_ed2_full.txt | 7,927 | `c83a43d55b36085d5489b4df966d592376838a4dda3e1912f5925e3579baf99d` |
| s1020_ed2_full.txt | 8,050 | `a48714be21033eedba6f2f835e08efd8e2a1d434ebb1dc63ae3fa6e7a191d062` |
| s158_100_checks_table.txt | 112,671 | `8fb42687ea5760540f5fb9b5703a7bf741f4cb90b4a869ae4cb9553ffadecd96` |
| s158_100_full.txt | 27,221 | `1dd32cc5d56bbfbfa4f41172f739aedaa6914c1f6a56bc6ff8b6256cd97ca716` |
| s158_intro_structure_full.txt | 67,295 | `4ef4eb323868a16fdac910a5e63dfbcfb73e050e6566a07f8b6b34fce78f2dab` |
| s201_ed1_1_0_annexB2_schemas.txt | 280,656 | `118b279a7f0f16c581f727ec4eb791bab56d866d9786e122637e455a734a4730` |
| s201_ps_2_0_0_main_full.txt | 47,798 | `a24b1fa130c3f67099335d49b243a269e9d1a2bdc96b09f3339449c80a77c096` |
| s62_cumulative_changes_full.txt | 10,396 | `cead7e43bb3051cca38c517ae37bc25c2f51fe1d0783fc7cab5f12e26e1b2bc3` |
| s97_ed1_1_0_full.txt | 251,396 | `60601ae4f5b7248af03a832d650a5be0c7da275988acaf1fa604a073e56785e3` |
| s99_ed2_0_0_full.txt | 57,668 | `e6f722a5650d6316c657a5f409ed17a81d2a974c6ea1251845d782fbcb362912` |

## `dev/pdf-extracts/pdf_extract/` (18 files)

Obtain from: Plain-text extractions of the publications above (PyMuPDF; the `.docx`-derived one by a zipfile + document.xml parse), regenerable from the originals; `MANIFEST.sha256` is the development repository's integrity manifest for them (pre-commit check #17).

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| batch_01_p1-20.txt | 39,285 | `ecd698b0cc76e73fe9b43973d60cdf7feb9e45b86bc56c02c9976125a482ccdf` |
| batch_02_p21-40.txt | 24,420 | `a64b2901e5b9c1286cbd4d0d22d60cc2e4cebf402d309ac9d4188f750e1abf02` |
| batch_03_p41-60.txt | 22,810 | `b0901a2a40a35a90ae7601dfd7677802697fa9b528f211f2ee7920b32ddbe421` |
| batch_04_p61-80.txt | 24,878 | `25da80165a8f994551143836fe317b813f47a9abeebeeb763ba4a44ff8ec8320` |
| batch_05_p81-100.txt | 21,677 | `95fa2af4f99dc8eaf39c340f542bfcef62cb9133987c819f9bf616edbaa25d92` |
| batch_06_p101-120.txt | 24,639 | `7ddedc31bce30a4d6b9d986538f14630b0f5b733f1197be88de9a69d2e8af24f` |
| batch_07_p121-140.txt | 23,797 | `2cbac86ded7778ae0cd5fa64fd3cf0bbc20dbb1966844b2402f999357ae5ca51` |
| batch_08_p141-160.txt | 23,901 | `ac66510c2f855ec88806428754df506e33090b7ccf7097bd09e9348dddc25585` |
| batch_09_p161-176.txt | 18,868 | `27a7c7bb09bdf4f0c9dc3d7b1ec7b0382d35a60e248d9e2eeea96ece8462d965` |
| tables_01_p1-20.txt | 17,894 | `5e4796b1301754835f772fa0c251ec8beeb0c65b5b9cd8ad055748d946456e44` |
| tables_02_p21-40.txt | 19,617 | `2c17c2e1e60e5cc85c1946c08b31da1dd3c6b5c9cb425e26faa9d21de19a6f26` |
| tables_03_p41-60.txt | 24,419 | `f0dc160fd861a7a44048d6f9c402bc9455ed26755669ba3c574ed5296befada3` |
| tables_04_p61-80.txt | 27,199 | `b41ccd64fe545bed7b21d8b2f2f8f7c81f000e54da51763bfe268e3d885e5df7` |
| tables_05_p81-100.txt | 23,996 | `13cc87e977a12a49980d7cf8bcdd9c7d33d56efbb340b08d34cac4456d1a9e14` |
| tables_06_p101-120.txt | 23,514 | `6b558786e6ab793f2cd4f19676b60bea6bcfb7703ff4c09c99555c57de5a7bf9` |
| tables_07_p121-140.txt | 25,193 | `28c053cc05f35bb3298d671916b989ef80ee13fe58cc3e114b605e300a08e78f` |
| tables_08_p141-160.txt | 25,743 | `d575262abb235965200817a61dbd2343ac632f05f1d9b29fa0e1286ef1a3e8bf` |
| tables_09_p161-176.txt | 19,041 | `3f7dae5eee31f830c86b1a5a337939ce54826a551d988dc36d6a828bacbfccc5` |

## `dev/spec-sources/` (67 files)

Obtain from: The IALA S-201 Product Specification family (main document, DCEG Annex A, Feature Catalogue Annex C1, overview) and the IALA R-, G- and S-series publications: <https://www.iala.int>. The Feature Catalogue XML `201_Feature_Catalogue_2.0.0.xml`: the IHO Geospatial Information Registry <https://registry.iho.int> (S-201 product specification entry). IHO S-100, S-97, S-99 and the S-100 Roadmap annex: <https://iho.int>.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| 201_Feature_Catalogue_2.0.0.xml | 790,060 | `74015a3d317ba1289f9dfef0934e97e2298576f56a727418aa07bad55aa5a09c` |
| IALA G1004 Ed3.1 - Level of Service (June 2017).pdf | 272,137 | `2560190719ecb7ded4488f1f2f142095091f61f14ddf4259810d31b961f58f24` |
| IALA G1018 Ed4.0 - Risk Management (June 2022).pdf | 734,301 | `5e2d4da9f0a1434d21387db63277b61ce547f1876a161e5d82f78f468d9caa71` |
| IALA G1035 Ed2.1 - Availability and Reliability of Aids to Navigation - Theory and Examples (December 2004).pdf | 843,261 | `0cdf9a8aa419ce75352b531aaaac4e59985e0ca4048b32c42a203be821976b80` |
| IALA G1046 Ed2.1 - Response Plan for the Marking of New Wrecks (June 2019).pdf | 273,348 | `9087cea4c6be948c7208be1eb8a43eedf1f6b05c4f37dd0fed921a5fb8835599` |
| IALA G1052 Ed3.2 - Quality Management Systems for Marine AtoN Service Delivery (June 2025).pdf | 855,489 | `c688e00618c36806415d0dc72606b79127a78c2d4f39de5c69c54930e99f0530` |
| IALA G1054 Ed2.0 - Preparing for an IMO Audit on AtoN Service Delivery (December 2021).pdf | 531,878 | `d91db17151c263ec039a96dd57b082a8b0b319f02dbab6d98cdde20ca85e16d7` |
| IALA G1057 Ed1.1 - The Use of Geographic Information Systems by AtoN Authorities (December 2007).pdf | 319,762 | `c7019033113505f9e4d9e30621be8152167290e6a278d7b197cf1df7b6730b6b` |
| IALA G1058 Ed3.0 - The Use of Simulation as a Tool for Waterway Design and AtoN Planning (June 2022).pdf | 1,360,122 | `f249a6e2297afe0c6bbd3f3ec63cb8a1c485cba425f09a6b1e23a405cf7bf537` |
| IALA G1059 Ed1 - Comparison of AIS Stations (June 2008).pdf | 72,431 | `610cf42070ef3e8fece0561b2c7c36f39c04fddf7b5995dcdc039ff21bb92e9b` |
| IALA G1062 Ed1.1 - The Establishment of AIS as an Aid to Navigation (December 2008).pdf | 358,577 | `3f11c0a077b14a4f7d0c5b42865294e4b7afb39f5c1ad37e2b74bfb7b9835671` |
| IALA G1066 Ed1.2 - The Design of Floating Aid to Navigation Moorings (May 2009).pdf | 3,522,330 | `d306c4d4200dd153207ba6a77ce923f5a07b0f7d8403d91e34efc9b7db9a20f2` |
| IALA G1081 Ed2.1 - Provision of Virtual Marine Aids to Navigation (June 2021).pdf | 960,480 | `398eeff29014ef45b07c809464ba7371b5c91160f173cb90c52f3eb46a5c54db` |
| IALA G1084 Ed1.1 - Authorisation of AIS AtoN (June 2011).pdf | 236,092 | `c5faf9f5e855061f367c020f7ae87f32bd98bfd82439436e74581d8d50ad3042` |
| IALA G1085 Ed1.1 - Standard Format for Electronic Exchange of AtoN Product Information (June 2012).pdf | 705,598 | `895385b948088b6ba62da342a3835f975256fe0d15e67e7b2c3a2efcafae56af` |
| IALA G1087 Ed3.1 - Procedures for the Management of the IALA Domain under the IHO GI Registry (June 2017).pdf | 408,093 | `11b8ce2127c014d4f00f7713752c8748da7ef7de923129f4659a3755d4b98bd1` |
| IALA G1088 Ed1.1 - Introduction to Preparing S-100 Product Specifications (December 2012).pdf | 342,566 | `c22e4b5fe6e046efcb5a6eecde5e226ba0c7199ea1da94d62c4112fe3d767920` |
| IALA G1101 Ed1.1 - Auditing and Assessing a VTS (January 2022).pdf | 282,380 | `652f1035fa43c14b80572ea4e3fc1cb863e76da76ad94967174e9e161c68eedf` |
| IALA G1106 Ed2.1 - Producing an IALA S-200 Series Product Specification (June 2017).pdf | 1,506,429 | `37d9835a36bcedb50caa4152a346d1c134ca59bab94aff39faac1a43cf5b6184` |
| IALA G1115 Ed1.1 - Preparing for an IMO Member State Audit Scheme (IMSAS) on VTS (January 2022).pdf | 338,588 | `bb489d6a1d355c3b8956aa7ca5d22a8e8b229a1a40fb0119705f9ccb4c7df4e9` |
| IALA G1121 Ed1.2 - Navigational Safety within Marine Spatial Planning (June 2017).pdf | 411,673 | `ef6ad20892a148a4ec1f4a1bccab8fc8c156a61199513744b9572975c13ff6ba` |
| IALA G1134 Ed2.1 - Surface Colours Used as Visual Signals on AtoN (June 2021).pdf | 2,797,188 | `9aabd6bf29fc51d655abd4635b8a78d8f878316bd31fc0f2bc36e9b016bb8cd3` |
| IALA G1138 Ed2.0 - The Use of the Simplified IALA Risk Assessment Method SIRA (December 2022).pdf | 724,115 | `24eadbecc51b0960de14e5681de59cf4bb1af8b4ebabb80b1d6f3a78adf510cd` |
| IALA G1143 Ed3.1 - Unique Identifiers for Maritime Resources (June 2021).pdf | 1,322,030 | `27b116d18028f3cb4527c76be3d4df1b0ee1c3861bf9a719e9fa6c97f56e89f2` |
| IALA G1154 Ed1.1 - Mobile AtoN (December 2020).pdf | 257,619 | `e03ffb3561773f2d8147ac5d7b6aa5b0bdffd4a6cb9d1e425b1e5f4133b755aa` |
| IALA G1162 Ed1.1 - The Marking of Offshore Man-made Structures (December 2021).pdf | 895,753 | `a15da30342ca4ebccad2f6548c6fdf93c7398e520c00ea4d95b900e984ad2521` |
| IALA G1168 Ed1.1 - Quality Control of Third-Party AtoN Service Providers (June 2022).pdf | 654,204 | `ac1fa652ecbb0edeacc22eeff264b25de260a10a2a068b7f968d64d942648541` |
| IALA G1188 Ed1.0 - Quality Management Practices for VTS Providers (December 2024).pdf | 279,801 | `772584fca8e3c15dd2ee1b4dbbfb04d6ffbd446e191bf136c3f4af896941e9a3` |
| IALA R0104 (O-104) Ed2.1 - Off Station Signals for Major Floating Aids (May 2012).pdf | 166,353 | `39d1eb2bcf6a3ac401cb993bb6a3c7c655c350d8ffac25fdbfeec63cffe43f01` |
| IALA R0106 Ed2.1 - Retroreflecting Material on AtoN Marks (June 2017).pdf | 270,147 | `8ac38845126a9b63bf833fbcf0f52e4e628e6cb299a351a8b69e2122f67a2d0e` |
| IALA R0107 (E-107) Ed2.1 - Moorings for Floating Aids to Navigation (May 2009).pdf | 134,836 | `a1497e40c63e6d982b568aa1367c418c59da75e3bf3948703bc5e0dae7a3aab5` |
| IALA R0108 (E-108) Ed4.1 - The Surface Colours used as Visual Signals on Marine AtoN (December 2017).pdf | 267,849 | `2b8db3118456c4d9a6910683fc74b51428f274331786382447cec9871ba5afd8` |
| IALA R0109 (E-109) Ed1.1 - The Calculation of the Range of a Sound Signal (June 1998).pdf | 1,413,624 | `f07d7bce619608fcb164c25f5316029c50074f3c5b0806142f64ddafdbffc861` |
| IALA R0110 Ed5.0 - Rhythmic Characters of Lights on Marine AtoN (June 2021).pdf | 400,870 | `7773374db02df20f7923af2b2996edd36f73d7b0cb30fba091751fe667c9e1cb` |
| IALA R0111 (E-111) Ed1.3 - Port Traffic Signals (December 2019).pdf | 231,240 | `d586dc453a42956a4ae8d4492258a0295752de8d44a28bc91cf3cd4c421c366e` |
| IALA R0112 (E-112) - Leading Line Design Programme v2.02 (companion spreadsheet).xls | 365,568 | `c5d2f34ee106f8e30d86dbfc2d5453593719c4203f9d3238fc9604369c58c326` |
| IALA R0112 (E-112) Ed1.2 - Leading Lights (December 2005).pdf | 551,759 | `20810b829cbacb31eb675618813e13c231ddc08226a5f6d7a380f01dd7c2604f` |
| IALA R0113 (O-113) Ed2.1 - The Marking of Fixed Bridges and Other Structures over Navigable Waters (December 2011).pdf | 442,335 | `8219d81d1eccba7b17cba8349a0375570fd00b71e2a9c147d3250c659b27c241` |
| IALA R0118 (O-118) Ed1.2 - The Recording of Aids to Navigation Positions (December 2005).pdf | 138,280 | `9959567e344a593e169a91301923df77938bf851552cd2ef199f8987ae6a1e7d` |
| IALA R0126 (A-126) Ed2.0 - The Use of AIS in Marine AtoN Services (December 2021).pdf | 585,465 | `1c7710578b6eb4bff280342d1da82b3615131191a9fb64236205630aa99241a1` |
| IALA R0130 Ed3.1 - Categorisation and Availability Objectives for Short Range AtoN (June 2017).pdf | 250,519 | `5489f9c394704a668613f38c50f3f1edb7fa527e6e7ca2204aaa976d0961fd51` |
| IALA R0132 Ed3.0 - Quality Management for Marine AtoN Authorities (December 2024).pdf | 159,049 | `5d95331f1d8290064b9a00e76c8b0d8c2c1f1e9b7032c336133097b187a8d6d0` |
| IALA R0138 Ed1.1 - The Use of GIS and Simulation by AtoN Authorities (December 2007).pdf | 212,522 | `f233d989702a84d93b0a3c0519441e6232a59e3ac0fd88b9bc78d90701c2b07d` |
| IALA R0139 (O-139) Ed3.0 - The Marking of Man-made Structures (December 2021).pdf | 189,801 | `57d9289596e8d2641b57499108137970639db6a142b20fab880d39b38aa4ee96` |
| IALA R0143 Ed2.0 - Provision of Virtual Aids to Navigation (June 2021).pdf | 235,149 | `209db3a7399708fa57d3fb85bad4f729b88740bac00a4a45933dfea7bde1dea8` |
| IALA R0147 (e-NAV-147) Ed2.1 - Product Specification Development and Management (June 2017).pdf | 140,601 | `a56b88944dfb5cf9bc40f492785752a03a9b573e287a9485bd73d820d8eaeff4` |
| IALA R0201 (E200-1) Ed3.1 - Marine Signal Lights Colours (December 2018).pdf | 246,407 | `e8288b258e05158861568da4c3a18d2191cde2eb580f18443a00cf1b4848c2a2` |
| IALA R0202 Ed2.1 - Marine Signal Lights Luminous Range (Dec 2017).pdf | 752,802 | `cc4fe408e6b32f000525c46c00e722b8a401b8f3d25ef90036b0d2e016f5765f` |
| IALA R0203 Ed2.0 - Definition of Marine Signal Lights Terms and Measurement.pdf | 823,831 | `b5e220ab0074e97eb78b21e1735b69e5ede7a885eb3c3827bc9aa6889f42aec6` |
| IALA R0204 Ed3.0 - Marine Signal Lights Determination and Calculation of Effective Intensity (June 2022).pdf | 246,305 | `f3982942c882e8fb79160c603b9f4946e905ca04cb665b9db68368c2cedd0d60` |
| IALA R0205 (E-200-5) Ed1.1 - Marine Signal Lights Part 5 Estimation of the Performance of Optical Apparatus (December 2008).pdf | 1,431,753 | `e03e9284a11a306b26de164e274af590ab8d3b0c33e3d6ed1ba2a2292a7f2b3e` |
| IALA R1001 Ed2.0 - The IALA Maritime Buoyage System (June 2023).pdf | 1,836,975 | `2e085b09d226747ed50162a7977674979f95a3bd4f502a696161d9901db1b115` |
| IALA R1002 Ed1.1 - Risk Management for Marine Aids to Navigation (June 2017).pdf | 134,527 | `6e664cfa909888e617e16ab18a13249d2337bb328b5aa0aa641eafa54def9aa1` |
| IALA R1010 Ed1.1 - The Involvement of Maritime Authorities in Marine Spatial Planning (June 2017).pdf | 277,420 | `099728b0e62905e18a3e9e01159983cb40a636c9c9070bd2156e2504283133a9` |
| IALA R1015 Ed1.1 - Marking of Hazardous Wrecks (December 2017).pdf | 182,780 | `18f95665814649173e69ba1076fb53be7f0ca0f9c021d1dc5a175bbd5154396a` |
| IALA R1016 Ed2.0 - Mobile Marine Aids to Navigation MAtoN (December 2020).pdf | 193,655 | `8f59a90859b5bfddb783acd2d4dd9b5f281e4963cd8f9f1eee56ecd04b23cd34` |
| IALA S-1010 Ed2.0 - Marine AtoN Planning and Service Requirements (June 2023).pdf | 243,989 | `1091fec4d0e5e67023089930d704dd8a3fc4ffc5d0f47990ad5cfc3d5960eb8a` |
| IALA S-1020 Ed2.0 - Marine AtoN Design and Delivery (June 2023).pdf | 203,957 | `42a8f45ab869b2f5cfb59b8e6735af2ad3f47b55ba3fed12b3973c0a35e8ea25` |
| IHO S-100 - Universal Hydrographic Data Model (informational brochure, May 2017).pdf | 3,460,974 | `ba579fdb762aa84daedfcf3253c206f1e0f91435b3a885bd8db3635066289071` |
| IHO S-100 Roadmap Annex 4 v1.0 - Dual Fuel Concept for S-100 ECDIS (May 2023).pdf | 846,666 | `6c002b1fcfaab39948b76d17ec378fcecbbbafa799289652b958eb261f7f8571` |
| IHO S-97 Ed1.1.0 - Guidelines for Creating S-100 Product Specifications (June 2020).pdf | 3,034,504 | `8e23f1ec1a5d0b316bd69350f2c726328440de5960d59f5ac23876c55a6abad9` |
| IHO S-99 Ed2.0.0 - Operational Procedures for the Organization and Management of the IHO Geospatial Information Registry (October 2022).pdf | 747,212 | `c3ba085f2c9454476c5eeef511471b830112d918fe66383e271f671be1e7a9be` |
| S-100 Ed5.2.0 - Universal Hydrographic Data Model (June 2024).pdf | 20,973,318 | `dd5ab86a3f6b5a26f32f7468a2eb3023e7d87a63423c8567c44657e8d3373732` |
| S-201 2.0.0 overview-1.pdf | 193,946 | `ee4d727767b31d3b554952e5e1dcd7d3133af40d09587e545020be190faae301` |
| S-201 DCEG - Annex A-1.pdf | 2,325,005 | `f4fdcbf8486104a0350f9ba3156ded29d9ae255e1bb98e90542488871cf6ab28` |
| S-201 Feature Catalogue - Annex C1.pdf | 2,069,301 | `875a58415a178eece41138919b7adee83e38f2267ea7c6eecae156de6e383d83` |
| S-201 Product Specification - 2.0.0 May 2025 - main document-1.pdf | 2,557,659 | `f75283e7968ffc20ee9afac6b266a830535949c94faf6902ff297d80f374dff5` |

## `dev/spec-sources/iala-additional/` (6 files)

Obtain from: IALA guidelines and recommendations: <https://www.iala.int>.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| G1085-Ed1.1-Standard-Format-for-Electronic-Exchange-of-AtoN-Product-Information-June-2012.pdf | 705,598 | `895385b948088b6ba62da342a3835f975256fe0d15e67e7b2c3a2efcafae56af` |
| G1087-Ed3.1-Procedures-for-the-Management-of-the-IALA-Domain-under-the-IHO-GI-Registry-June-2017.pdf | 408,093 | `11b8ce2127c014d4f00f7713752c8748da7ef7de923129f4659a3755d4b98bd1` |
| G1088-Ed1.1-Introduction-to-Preparing-S-100-Product-Specifications-December-2012 (1).pdf | 342,566 | `c22e4b5fe6e046efcb5a6eecde5e226ba0c7199ea1da94d62c4112fe3d767920` |
| G1106-Ed2.1-Producing-an-IALA-S-200-Series-Product-Specification-June-2017 (3).pdf | 1,506,429 | `37d9835a36bcedb50caa4152a346d1c134ca59bab94aff39faac1a43cf5b6184` |
| IALA_G1059_Ed1.0_Comparison_of_AIS_Stations_June_2008.pdf | 72,431 | `610cf42070ef3e8fece0561b2c7c36f39c04fddf7b5995dcdc039ff21bb92e9b` |
| R0147-Ed2.1-Product-Specification-Development-and-Management-e-NAV-147-June-2017 (1).pdf | 140,601 | `a56b88944dfb5cf9bc40f492785752a03a9b573e287a9485bd73d820d8eaeff4` |

## `dev/spec-sources/iho-additional/` (14 files)

Obtain from: IHO S-62 producer-code register and the other IHO documents: <https://iho.int> and <https://registry.iho.int>. `S-62_ProducerCodes.csv` / `.json` are extracted from the S-62 register snapshot by `extract_producer_codes.py` (the development repository's own script, listed here because it lives in this folder).

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| IHO_S-100brochure_final_11-5-17-compressed (1).pdf | 3,460,974 | `ba579fdb762aa84daedfcf3253c206f1e0f91435b3a885bd8db3635066289071` |
| IHO_Technical-documents-Catalogue_Ed-10.0_December-2025.pdf | 14,289,340 | `5bf24c0e402bd37e94f300f256618c46ce20f97233e728356370f7c51ad24819` |
| Relationships of S101-S124-S125-S-201_v2.pdf | 3,370,363 | `ba87cbb7335adb212cba300b104dba406e555543d891a2a07497b9ea638b7c52` |
| S-100 Roadmap_Annex4_v1.0_May2023-compressed (1).pdf | 846,666 | `6c002b1fcfaab39948b76d17ec378fcecbbbafa799289652b958eb261f7f8571` |
| S-100WG2_8.5_S-100_ProducerCodes_Rev1.pdf | 203,633 | `d3e761ccd404fd8a1d4032661d43c648a750acb91dbf655905d42282a25232dc` |
| S-200 Annex A Data classification Encoding Guide-Minsu .pdf | 1,698,487 | `883e253ea578bdd0ac78ff2268f6b6a27162929cd4f9bd2c3f043706ca582bf9` |
| S-62_Cumulative_List_of_Changes.pdf | 112,237 | `a23b791c69b2bf8075106bc53ea95cf6db043a6b82f165d2a202e6f4ad21bcfd` |
| S-62_ProducerCode_registry_snapshot_20260421.pdf | 278,775 | `647a6d1b379adb6a039d6f4ce67f84348316995823eab55223f4db944d36e6b9` |
| S-62_ProducerCodes.csv | 31,359 | `82a6241457bf5c562de9409e5651bf0d95b29c8f6e699ee0640b9775f4f6ae95` |
| S-62_ProducerCodes.json | 99,416 | `49f95ab71f64bb6f145872311381935cf2df73cc04656871230127ec08aa2e63` |
| S-97 Ed 1.1.0_EN_Guidance for PS Developers_Final (1).pdf | 3,034,504 | `8e23f1ec1a5d0b316bd69350f2c726328440de5960d59f5ac23876c55a6abad9` |
| S-99 Ed 2.0.0_Final (1).pdf | 747,212 | `c3ba085f2c9454476c5eeef511471b830112d918fe66383e271f671be1e7a9be` |
| Understanding S-100’s Use of GML as a Subset of ISO 19136.pdf | 974,864 | `69428dc4c47f6f5220655aa76a8d9763283fe342bc7d39389e5268319a443269` |
| extract_producer_codes.py | 5,095 | `e4f2d6881c999e2248d493660b1022a4237f63db3f9ba775620f7dbda27f4fa8` |

## `dev/spec-sources/iso-xsd/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ISO_LICENCE.TXT | 547 | `29c6aca06082138896010f8405c5077d741d00109d10fe8bc254c62d7699ebbb` |

## `dev/spec-sources/iso-xsd/19110/-/fcc/2.1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| abstract.xsd | 2,030 | `658604396bba85e5f71cf5be6aa3b58cbf73908deb88683bda48b138e4d40823` |
| fcc.xsd | 586 | `85fb5ee0486e7421cedcfb15d7aab7d201d35a0583655c38c31a9a3b3460775f` |

## `dev/spec-sources/iso-xsd/19110/-/fcc/2.2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| abstract.xsd | 2,034 | `10df77ff5fd2a08baffbcce5bb637ca4dd886eb406f99ce6b4a671d09e514ab0` |
| fcc.xsd | 586 | `6add2114d93dec7553a04a44b9e2df89bf32898ca7ce987c0c59f38a4184479e` |

## `dev/spec-sources/iso-xsd/19110/-/gfc/1.0/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| gfc.xsd | 24,888 | `cd427ea2046a89c8c096cfcc619d3901ee7c9a3da137b0789e3a8713b81c35be` |

## `dev/spec-sources/iso-xsd/19110/-/gfc/2.1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| featureCatalogue.xsd | 36,149 | `aae01692ff70b620876ae890f8f99ba46e6888cb7efe835b935bba86d04a001b` |
| gfc.xsd | 1,182 | `7593fedde4723c9572fa3f26162cef9dde00515777740e2ee992188f849ee5dd` |

## `dev/spec-sources/iso-xsd/19110/-/gfc/2.2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| featureCatalogue.xsd | 37,241 | `ecd18ba8819a597a78547bbaa83fdeda208cb0f6ea1f57adddfca1e5b7e45acf` |
| gfc.xsd | 1,188 | `407fa59f4b4c94727fd6ef3fb0ebb34b6bf7d559ea1492e78a2752b94d3b8aa2` |

## `dev/spec-sources/iso-xsd/19110/fcc/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| abstract.xsd | 2,129 | `783de4459d264c875d9bd6b0b7bd0341456e860b9b0625f8f810fe6a71bb11e3` |
| fcc.xsd | 514 | `276d79402d8c69573b13f7d6e8cb1009cdf2c2f2ebac5ec2f2e519d5ad255c2d` |

## `dev/spec-sources/iso-xsd/19110/gfc/1.1/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| featureCatalogue.xsd | 36,114 | `2765f0b705bb369d7ac399960029eaa98d79631a598f5921aff5b12d4a003e02` |
| gfc.xsd | 1,176 | `186afb75cee00b214454595faa4f77389b4e9a98a23279c4ad694e3b3563bcee` |

## `dev/spec-sources/iso-xsd/19111/-/rbc/3.1.0/` (8 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| commonClasses.xsd | 6,545 | `1dd1587783ddd377f863861c2f6cba31ea6c46f7fe326514efd5bac4b7c59272` |
| coordOps.xsd | 39,141 | `7367a2260714b00952863d78ddd5535fbb1ba634054f6e3caa1f72122f1aa64e` |
| coordRefSys.xsd | 27,583 | `e510c11cffcc1a2eeeeb7cc345d041948517604f3a3ef567c4992a9e07a3411a` |
| coordSys.xsd | 46,020 | `adfdf50519bbd85329ab5a8a0701c22123754da2b745299782f6d372510221aa` |
| coordinates.xsd | 6,088 | `8a6c3f6cceafddbb8bc814b4452cb3dbf9fb6b0964ba2d27ec3650abd0a2af3a` |
| datum.xsd | 26,886 | `22bca06703cbe28c3cbbf4b62d835df709bbedeeb8051abb7fd677d92653b49c` |
| rbc.xsd | 1,035 | `f4a85662b30950bd0bf719543d8f0745a33693b6741420d9e9f8a61e31ed5d41` |
| rbcStubs.xsd | 8,500 | `0ef255cb5584086c980000f3597ae148e836747c79d25f7ff12b169d3ba009a7` |

## `dev/spec-sources/iso-xsd/19111/-/rbc/3.1.1/` (8 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| AbstractCommonClasses.xsd | 12,067 | `0f92ebbb5148334cb14ea720fc206f4a997621ca52d1faa6b7ced3889f8d7060` |
| commonClasses.xsd | 6,942 | `4cb957cd17ba69701403f625ec5f2722d941630deed9f03fbea050ce27b4900b` |
| coordOps.xsd | 39,221 | `9d53ae6f4c777344b8abea5170071ec648bf2c83ef5108ab9199970a9bcb23ff` |
| coordRefSys.xsd | 27,455 | `0c4564f3946b3c01103812195959fc8ad401a9eb54be6efa21f00efeaa2dc687` |
| coordSys.xsd | 45,980 | `bdc9f673442c5fbac2cfe14f7b5dad883b4ee278bf109f852be9852eb6d90c38` |
| coordinates.xsd | 5,969 | `160db6115078076bc64feac7bc71801095083eefe7a73438901ec49c9a3b51a6` |
| datum.xsd | 26,882 | `95afde76b5a78e7e1e434174527c59502f8fb220b7dbc3f0791399b5940aaa39` |
| rbc.xsd | 1,124 | `ad48e206356e683b9f03457f4faa0c0e6b1244c1150b8ed198dfe8a7d3935006` |

## `dev/spec-sources/iso-xsd/19115/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| 19115.sch | 81,052 | `c8d21bb5281c525d33dc6e837ba2514b3f1e40b90ecced6fdcd6343b5e1bc405` |

## `dev/spec-sources/iso-xsd/19115/-1/cit/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| cit.sch | 5,197 | `3fec1952c85c8cd4e477a72c7f651abb47b215ef097facfbda0f69a55e6283cd` |
| cit.xsd | 539 | `8e51e769a10d476836e81e3a4517b7b934e4dc0a5a9f110939d2410b011bfd7b` |
| citation.xsd | 29,894 | `9670a4e99f073666c5d0faccb728b1e8f48568edc2dbb4edc2ef1fb126519e11` |
| codelists.xml | 439,701 | `9d9e82c1345d25a15eb405914cc1e56cbd0c5e870382e7b47c2ede61d4af334b` |

## `dev/spec-sources/iso-xsd/19115/-1/gex/1.3.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| extent.xsd | 15,424 | `cf7c652591f9c54255e760c221b6aaa9c646f915eebd9432b8b3ca5ad5dfb5ff` |
| gex.sch | 8,255 | `107eb11e3bda060959df7a4766a335aefc01f3d8335ed1caebf3c727a2b414ce` |
| gex.xsd | 809 | `e26e2477e98ea8aef34d3651fb4bc685754ba9eb8e97d284ba90ae1d3fe20c7c` |

## `dev/spec-sources/iso-xsd/19115/-1/lan/1.3.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| lan.xsd | 848 | `8b2b7d0a8025fda417a947d8df0697cea8f5f615b6f83c98c9bc021dddd034d5` |
| language.xsd | 8,119 | `646c371f6c64cadb7d91fec3c211ddb488297591d0c356e40827ff9efe568d2e` |

## `dev/spec-sources/iso-xsd/19115/-1/mas/1.3.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| applicationSchema.xsd | 4,134 | `ae929455402e581ff12560e89d617253e514c4d5506679bf6ff9a4053270110c` |
| mas.xsd | 1,007 | `c5f13c55268b45bfbcbc34c9efeb2eb5f70c5439c207b179ea34e60e31b34843` |

## `dev/spec-sources/iso-xsd/19115/-1/mcc/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| AbstractCommonClasses.xsd | 15,428 | `674ea571d2a9c49db49e1a15fb1a7d33ec80c910857be21790219cd8d1b4e023` |
| codelists.xml | 47,124 | `a21abf2ad632b702e08ecdace212f13077bcea9d290d318c99924567cc7932ae` |
| commonClasses.xsd | 13,186 | `88c48f8533ae2be0d2b7c82e3b69fa846e36e98ee4fee0cce41eaf97c2afcac3` |
| mcc.xsd | 802 | `aa5dabcc70704e124e420e46e63eb897418c56929de9eaee25c7ddd0aafcfc62` |

## `dev/spec-sources/iso-xsd/19115/-1/mco/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 27,287 | `7c45ea148ad3a78bd853b5adb9cff7d72c7107f0a6d9dcbec78a80c05e8c30dc` |
| constraints.xsd | 12,287 | `2e7bfc8dd12dfae7299cb424dfd310e6a2d73c23f6e8ebed61d1a521b0a5de02` |
| mco.sch | 8,577 | `ec9fc6131bf42d2ff03960a2798063dd7a515d224961e16e10b1aad0bed27dcc` |
| mco.xsd | 808 | `19c70194cdce538e6b8fc1f8633d0bbf84ad48c1123e4562976ffbc7dea09900` |

## `dev/spec-sources/iso-xsd/19115/-1/mda/1.3.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mda.xsd | 790 | `54cdc434c1c15d1c5ae5b60b1146c3be2f0f284f8cdf2faccbe7a9f67a12e0af` |
| metadataApplication.xsd | 9,304 | `2697a815e76981a95d1c6c3be674060110fb49d9ba8bd1bb0465967697c6acdb` |

## `dev/spec-sources/iso-xsd/19115/-1/mdb/1.3.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mdb.sch | 10,636 | `52b43e72b48260f2c10105e6546b21ac8d7adc4e83642f8d4047fe8d0adb8067` |
| mdb.xsd | 1,903 | `0414916a3f896cd616bac7b30612e982dc1e5013b766e0e950f4ed634c81fee5` |
| metadataBase.xsd | 9,763 | `81e951903215359a96a8d04c8da49036db967e16e686c027b4348c827f9f7194` |

## `dev/spec-sources/iso-xsd/19115/-1/mex/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 19,527 | `2475d83981380b31de7a4b6a2c0e008870b99a9537e684a04c5e9de31514e12c` |
| metadataExtension.xsd | 9,816 | `55db612e705f204a7de8e60ad772bbc6869e652abce7a26be493c188ad792b0d` |
| mex.sch | 12,276 | `416e8cbec31181add3af2659523c4d510e0311c1270631962b5e695a05c96d17` |
| mex.xsd | 806 | `b9f04241b832954a92029ab5099f679f59f80f3a57068af5a6a1d5ca5952efbf` |

## `dev/spec-sources/iso-xsd/19115/-1/mmi/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 15,480 | `7c30723aff961f40ec6f474139f22303a204824212385958fcf082e31184b035` |
| maintenance.xsd | 5,201 | `cd418d27e40437e265ed1a89a1a99488fba7c9b8c01a0bc5680eae90c17a411d` |
| mmi.sch | 3,388 | `401713507f6abb1c90b138d52a4b87dd35b3e567d821c4e5df061a1749f6a677` |
| mmi.xsd | 821 | `95e2d379e2d4eb6fe506117a922e65ca982d6f61861c2c6aa8d8939eb1105bb8` |

## `dev/spec-sources/iso-xsd/19115/-1/mpc/1.3.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mpc.xsd | 883 | `f392b0188152df1ccb1a00e8e509770e41f35cd35a7b4abb3f254f1a6ec57ad8` |
| portrayalCatalogue.xsd | 2,295 | `c7b5d58223e68d758ea3697d0b8438c9501f24d2ab4c6badd13c4dd490508bea` |

## `dev/spec-sources/iso-xsd/19115/-1/mrc/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 21,760 | `4eac0e98453d1594070ce618a0c8d75a648b58dd061e356cd81acacda7aa8cb1` |
| content.xsd | 26,176 | `091f9d78cd8cbdec4d6e1af377a73e53a2b121cd27138e3406eaa5e1793da299` |
| mrc.sch | 5,941 | `1c5b27c39366678f9181e6a823efa25565532c644761860b42509008417b8e24` |
| mrc.xsd | 1,294 | `dc0890634a23ea4c9759f846422f1db8c0b5950a9a6cf36247727fdf70c0f6cf` |

## `dev/spec-sources/iso-xsd/19115/-1/mrc/2.1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| content.xsd | 26,130 | `06d112e79c77f6770ee1ad11300c75ef50ac6c4d2dba1345ff5d22909b0b3dab` |
| mrc.xsd | 1,263 | `61515058660b271b86b9be5b5487e09725e5f635328c1783f8db82ff5bd58600` |

## `dev/spec-sources/iso-xsd/19115/-1/mrd/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 8,422 | `e1ac00a61e53e381a04aae84455203ccb51d30e552082f60e9986e502e3efb29` |
| distribution.xsd | 16,309 | `e4715bc10ea4a383e5f027e6f3254c3e6a4059ce9e3d2cc0aea9c52dab2f6f93` |
| mrd.sch | 2,109 | `e19f716b8472d94ce0bd58ea177cca2fff624d4d99049df994e0924d32b0b13b` |
| mrd.xsd | 821 | `d3cc92d233a97242674389ca3990edac0c2f26043f8fcab1e61e3853553f75eb` |

## `dev/spec-sources/iso-xsd/19115/-1/mri/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 63,667 | `9f950747ca0f798d3a297044b2e986f2e9f7f5838cd9b52f83e5b42b12dde18e` |
| identification.xsd | 33,627 | `900f828a1ec737f5ab4ba2642a91abe755b33d59c7054b01786ad06ce25c083a` |
| mri.sch | 17,175 | `8a53f8827c99359968268a4334b7af8f8016c23fc0e8c0e4b572827a305b870e` |
| mri.xsd | 990 | `77c13fe5dac73f6e575fc07b4e810ecc59b1017eeb666b31de202f7841288a97` |

## `dev/spec-sources/iso-xsd/19115/-1/mrl/1.3.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| lineage.xsd | 9,407 | `4261bcaf78b0614a314a4e234384fad44b4357db63dac212a31c466bb642954e` |
| mrl.sch | 2,775 | `1f7a25eacce809599253289de2ea424a7b92175a0bb783fc78bab2f751ca51f3` |
| mrl.xsd | 866 | `fee6057a9372b4d38d2eb3d996895a0fb90d5789972170e33259f96a7c0c384e` |

## `dev/spec-sources/iso-xsd/19115/-1/mrs/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 34,687 | `bfbf3bed207e67c53d2822a4035af5be309132b5ec6b83c427612c1a89774ee6` |
| mrs.sch | 577 | `157ce6545b32d549bf2c87d43cfdb592ed6363bce01933df954bd6844fd30611` |
| mrs.xsd | 860 | `61d78d3ccbff206063a88b27224317ef0a6c30a2c2029166fbb05d6abddd5a65` |
| referenceSystem.xsd | 4,721 | `ff52e7aa3126f571a66cc71a50bca341a8a8ee441059763d26a89524420f20b9` |

## `dev/spec-sources/iso-xsd/19115/-1/mrs/1.3.1/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 34,687 | `bfbf3bed207e67c53d2822a4035af5be309132b5ec6b83c427612c1a89774ee6` |
| mrs.sch | 577 | `157ce6545b32d549bf2c87d43cfdb592ed6363bce01933df954bd6844fd30611` |
| mrs.xsd | 860 | `61d78d3ccbff206063a88b27224317ef0a6c30a2c2029166fbb05d6abddd5a65` |
| referenceSystem.xsd | 5,067 | `68cd99def730ccbbd720baedf2e772903156ae8bc7ae83e39e5e74e0c5167a20` |

## `dev/spec-sources/iso-xsd/19115/-1/mrs/1.3.2/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 34,687 | `bfbf3bed207e67c53d2822a4035af5be309132b5ec6b83c427612c1a89774ee6` |
| mrs.sch | 577 | `157ce6545b32d549bf2c87d43cfdb592ed6363bce01933df954bd6844fd30611` |
| mrs.xsd | 860 | `61d78d3ccbff206063a88b27224317ef0a6c30a2c2029166fbb05d6abddd5a65` |
| referenceSystem.xsd | 5,219 | `6246165369f29608b3df01d1e6c48b3b7b2316f65a03b7f698515097832dfda7` |

## `dev/spec-sources/iso-xsd/19115/-1/msr/1.3.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| msr.xsd | 1,117 | `273381ff5f86d5d993f79225d7eba0fea746ad782e1f2a9880e719c23acee4eb` |
| spatialRepresentation.xsd | 22,886 | `529174095ba70ae81ea6d9a7a6a502e10ad1231534a9d1efb106bc4ba7a8d4c2` |

## `dev/spec-sources/iso-xsd/19115/-1/msr/1.3.1/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| msr.xsd | 1,117 | `273381ff5f86d5d993f79225d7eba0fea746ad782e1f2a9880e719c23acee4eb` |
| spatialRepresentation.xsd | 22,886 | `529174095ba70ae81ea6d9a7a6a502e10ad1231534a9d1efb106bc4ba7a8d4c2` |

## `dev/spec-sources/iso-xsd/19115/-1/srv/1.3.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 17,880 | `6a98d501f6859ccc0f35d493ad8bc90c0581850d1db7e13267ea8e59b2bc6f13` |
| serviceInformation.xsd | 18,739 | `4170ef2ecd4ae87de0f1e1b930768fc7b2fc93fa5f7c95ea69f94b3be72f0b18` |
| srv.sch | 14,419 | `ecf9650a086963c235f2e0b2b075ae0856bf7fe927d421d396ce69c3c5305643` |
| srv.xsd | 794 | `fe88b6509af9d84f9a480c2fb1f66f54c00561062ca960bc2cd5d192d65fe980` |

## `dev/spec-sources/iso-xsd/19115/-2/gmi/1.0/` (6 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| acquisitionInformation.xsd | 23,092 | `6b6bad6dea08e0c260338d7b39e10b3fbca970ca25a54cfeceebc981526d348f` |
| contentInformation.xsd | 8,275 | `233773f79e7a25e1f500e4af7969b2329a72fd68f99c783285a08367fc651936` |
| dataQualityInformation.xsd | 11,740 | `00f00f8c2b209876d41396305c067f74a33064faf45968416e894e79b4984073` |
| gmi.xsd | 1,537 | `8cbc73c0ff578b0cf822dc19a38d5d53d372c3210f862d236bddb3ea99dc9c73` |
| metadataEntitySet.xsd | 2,360 | `615845a1284b1a87ce59ab24ff5b430bc5536a55742ffdb7ccd58f2815f31496` |
| spatialRepresentationInformation.xsd | 7,204 | `809f2320f3ad68b743e043ee76f450be7eb178b2e147ce2cec1557b9b00982ed` |

## `dev/spec-sources/iso-xsd/19115/-2/mac/2.2.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| acquisitionInformationImagery.xsd | 60,250 | `2ae94a988044db44da7a3a040563455b12a322a846826647b7a131d2cdbcd783` |
| mac.sch | 7,341 | `79c51cfc6342f5c0840e27292eeff1a7ae7102d8f510403d8a9e4270fca30db6` |
| mac.xsd | 495 | `87f759c65a5a71ec51ea90d5af4e7097949f6b4db3aa1acaf9e1cc24326f3419` |

## `dev/spec-sources/iso-xsd/19115/-2/mrc/2.2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 21,640 | `b7b9460b3a1d7d5bba5f65c9e1203dd082c0f01248804b8e81a84195c22c6235` |
| contentInformationImagery.xsd | 10,814 | `70b06696d40d54d050aa8a18aeb7d070011d4052841c46c2b6b483fb49ed54e2` |

## `dev/spec-sources/iso-xsd/19115/-2/mrl/2.2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| lineageImagery.xsd | 22,906 | `011b7b1fad8e786d722976a878b86920a91d714d6a3114ab7c26d91981e83b0f` |
| mrlExt.sch | 2,775 | `96ccb8806d81c5152ffce12028b343c1bc1295bdf278400a6242f5fbd1133eb6` |

## `dev/spec-sources/iso-xsd/19115/-2/msr/2.2.0/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| spatialRepresentationImagery.xsd | 8,012 | `84f1608168dd4b24a708350b80fb1b03b618833627c904642814ca7a567d0e00` |

## `dev/spec-sources/iso-xsd/19115/-3/cat/1.0/` (5 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| cat.xsd | 1,098 | `a6278879cc9a81d17e562376318d1ac0aa37336c78953b856b9057d678a159a3` |
| catalogues.xsd | 3,157 | `fdfaf62941d2c9700456403bb5550f1fe0b5899f58e71e918ee334fda3ba230e` |
| codelistItem.xsd | 2,539 | `566325e1584915a5ea8989bbec47735e021c9987c71d0a46df639f6510e4aeef` |
| crsItem.xsd | 7,826 | `7574bc769415fcfb835cfc4e03d4db208e6963e74c6c40308e26fa39e2572405` |
| uomItem.xsd | 1,887 | `d9110ddaf61131e86f7b189d404a677b77e374ca5d584b6d287bbb1afc2b659a` |

## `dev/spec-sources/iso-xsd/19115/-3/cit/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| cit.sch | 4,778 | `e347c54baf80b6b082d9c76f88a7c173b7a5cbc641695b27a74865a3cc928602` |
| cit.xsd | 561 | `cbb45764ab5191dd8ae6a3f1eb3bc2a4d84323a51355b335fc858a34f368fa26` |
| citation.xsd | 23,667 | `683661efc1de6e2947c514a554a060b2ec789d389dc69638c34b088911c00310` |
| codelists.xml | 69,602 | `9955c9f25fd5bde9ea49786a228c14a24e292d8b030d1177694c86ec322c72bd` |

## `dev/spec-sources/iso-xsd/19115/-3/cit/2.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| cit.xsd | 526 | `922282d94f512119bfcfbf01808139466e440e3a17cef8458ac63e0de9c347b9` |
| citation.xsd | 23,969 | `9dc33c62b6cd55ebe4dd06e52c0bc068da597b8594eda74fd5eb705f90a77d21` |
| codelists.xml | 69,602 | `9955c9f25fd5bde9ea49786a228c14a24e292d8b030d1177694c86ec322c72bd` |

## `dev/spec-sources/iso-xsd/19115/-3/gco/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| baseTypes.xsd | 28,080 | `c9a7c4b8b0ada4527f547cb994e50e9b7f6f3fbad99356544e523e3a7d9b0683` |
| baseTypes2014.xsd | 28,040 | `80ed7e7d913f821b0bca6f1eb53234c1a85db50290d8b2691bc49e5e1a6ca11c` |
| gco.xsd | 1,484 | `11b52eb6b9564965f99bf6a1755c09c3ffb45161ae5252167c96cbf1133d42b3` |

## `dev/spec-sources/iso-xsd/19115/-3/gcx/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| extendedTypes.xsd | 5,365 | `dbdc2779abfd748987b7472895a97bc3352acb331f7bc185c274abbb2383382a` |
| gcx.xsd | 657 | `75f047243007c2ff5267b886c78504c4598d7af25a1de2d2af1ead7b2d4f3d07` |

## `dev/spec-sources/iso-xsd/19115/-3/gex/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| extent.xsd | 11,554 | `12614e8d6efc1d84b88350ef048dd3a7207c8d7818ce8f7a5b3c02747cd56e4d` |
| gex.sch | 7,966 | `7ad25f9f6731b08ba23f4e43c5447f4e678bf0bf0e6a0020a54586f97d75cfb4` |
| gex.xsd | 778 | `717b067d3648cc46e3a58f7cc680a0989a7548e2a2db6f35cd3edd71da2e4670` |

## `dev/spec-sources/iso-xsd/19115/-3/gmw/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| gmlWrapperTypes.xsd | 7,829 | `eb68f89f638d344e999b6152f091a5ac436abf13fc0d53049fec2ef8262f059c` |
| gmlWrapperTypes2014.xsd | 7,807 | `fa04ff2c10764a4f116a9bf8d93e6ef49a2edd7137066286fa17e37fba8d9872` |
| gmw.xsd | 1,643 | `7d02701e00334155a17bd5952c29f612036e6fe170a15cf2071100d7b8a4c9a6` |

## `dev/spec-sources/iso-xsd/19115/-3/lan/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| lan.xsd | 839 | `d8b7d176a716e69bafc559bc7729802dd1d55a733f132b21cc159d86f07387a9` |
| language.xsd | 6,387 | `289dcd3b0d3aa152692db7d2123940689ef6300a94935e4581ce267616703b66` |

## `dev/spec-sources/iso-xsd/19115/-3/mac/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| acquisitionInformationImagery.xsd | 27,134 | `a9ff302de2b2e49459a0bf07422ddb4417f48aaa9ac903e6a8505be366c6430f` |
| mac.xsd | 518 | `5697e424d8f5b48ebf6511524a50228a40d3f1ee32beea17b6526278c277ec64` |

## `dev/spec-sources/iso-xsd/19115/-3/mac/2.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| acquisitionInformationImagery.xsd | 30,911 | `5fb75b2fbb838fe19dc2f5e9fc20657beab70d36833599ca34673fcc88276def` |
| event.xsd | 6,305 | `6bbe73391bcba640b6d6b4a2c006e4929866bbdff4c3e1c770d7e1ad3156b6a5` |
| mac.xsd | 617 | `d977f3e8bdd2b56187bcef68b084dae4000605ce12b8c9627f349ec3e0299a6e` |
| metadataEntitySet.xsd | 2,724 | `d19759d46f6dfaca085d0d8df19d0ac87bb9dbdc007259a3b214bc250d384597` |

## `dev/spec-sources/iso-xsd/19115/-3/mas/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| applicationSchema.xsd | 3,457 | `90b537d84b36ebe6e003a811b98cf3a349d73723e3385061d1da7fdc0c110d1a` |
| mas.xsd | 988 | `d9de4f9fe08fbc56cd45820e615abf6ad66fd290c5e65df0bb6e94e70b6430a6` |

## `dev/spec-sources/iso-xsd/19115/-3/mcc/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| AbstractCommonClasses.xsd | 15,047 | `55043118dc1f7f9324442b91472f110e37328bfd6d319afbfdb8b3bb0167f215` |
| codelists.xml | 47,117 | `e2e123cbce8ea9c27c61cd3da1249c45430580f5f38ec055c30f0a502142e21d` |
| commonClasses.xsd | 10,076 | `c689087807d81c3f564aa8da9c253a3b423bd5ca85536d12b900f9a4ac99aee4` |
| mcc.xsd | 765 | `0d15506ec1fb89a863261de11ec09a90d2ae9192f4f49063788bdedb0e32580f` |

## `dev/spec-sources/iso-xsd/19115/-3/mco/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 27,272 | `f84fb68acb05a083ea5ae803f04b3e87accd7e3286a8bef7f5eb20ffe967e391` |
| constraints.xsd | 9,703 | `7c3521ec2e16aa326b626de8250862a9b3c06617f2f1c861ff82b11ca4b9448b` |
| mco.sch | 8,402 | `be7d43138c177a2d0042237cca3609bac7abe9a5ca3a43f91c1c6b0fac51e65a` |
| mco.xsd | 781 | `363d592cfd59e839bfc087221993f45fb1e62ef8eca49d3ff36adc9c47f68677` |

## `dev/spec-sources/iso-xsd/19115/-3/md1/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| md1.xsd | 1,233 | `bd85d736bb08a2872b9018c9dd08353463508e117236450aee192aba3f80edd9` |
| metadataWExtendedType.xsd | 381 | `c864d53ce22cc199b999ed1a34cd9df5c05035c69a997d0fd4bb15983e8745a7` |

## `dev/spec-sources/iso-xsd/19115/-3/md1/2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| md1.xsd | 1,245 | `1c2cea158132faa5e47d5a9a366af6cdaa4a75bc5733427706392f979ae78443` |
| metadataWExtendedType.xsd | 385 | `2e85217c713008463c45d65d27c13ac50b347f96d5a1f9457d9932b45a10a613` |

## `dev/spec-sources/iso-xsd/19115/-3/md2/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| md2.xsd | 2,210 | `aa620fdc2193b394950dbbfeb3a5c75fbf24c7c5fe9abceecac97d4ca1b66b82` |
| metadataWithExtensions.xsd | 381 | `47c2fe5df357213713faf6e0f9d81db7b42effd8d3adae7e2d3d8d9f321890f1` |

## `dev/spec-sources/iso-xsd/19115/-3/md2/2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| md2.xsd | 2,229 | `e71de80bea17791ca9e8243a86f6768b334c9247da33a71c58ca0e002f92aab3` |
| metadataWithExtensions.xsd | 385 | `197ccdf62918be978cfb7b29cf78b09b590a81ab93c3d593b1f6b06462351b94` |

## `dev/spec-sources/iso-xsd/19115/-3/mda/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mda.xsd | 817 | `73cb0cda566fd1ed68f7453dcf07f136aaa9b0522e6d0ced2cf8b9b782d7297c` |
| metadataApplication.xsd | 7,887 | `2f8d1bbc4fb5d14609c08dc2ef52509b92ed484113893cd055fc4495e7a13dcc` |

## `dev/spec-sources/iso-xsd/19115/-3/mda/2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mda.xsd | 824 | `3062fbf56dc1f01b30a910a23ed4310ea259c9906369b816b83a06f503b6383a` |
| metadataApplication.xsd | 7,909 | `17e52504c83b0142b250989246120d1187902dba1f5d008c758098529acb30b0` |

## `dev/spec-sources/iso-xsd/19115/-3/mdb/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mdb.sch | 10,733 | `7a97720a0e49b1165fc0cc5ed6597a4a25b9c4cb58b50e963b16eda5514b83e3` |
| mdb.xsd | 1,745 | `cddd3394fc0200d7b1795e955b36099dabcea06ea595e2aac59d4c1f81a352cc` |
| metadataBase.xsd | 7,243 | `5ff757d0e06b99c1b9b11fb19c5c6f6021280c11f0db940805515cf64d32d7f9` |

## `dev/spec-sources/iso-xsd/19115/-3/mdb/2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mdb.xsd | 1,760 | `18db21baab39daf8a6e8adcec4837ae119060e170032655c9c9c85908154eea2` |
| metadataBase.xsd | 7,990 | `e8a53d0f9bbee0fe351264f1a23ab14ac15f60d1939437e3e96bfc026d2bcd0d` |

## `dev/spec-sources/iso-xsd/19115/-3/mds/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mds.xsd | 3,719 | `f66e61528f3042fd231c8616dc0210b44ab27cc8ef99ec831dce59130bae0af9` |
| metadataDataServices.xsd | 381 | `cf0f184d7097006825d1cc0c13d8d47df3d8acee35e71b92139fcdbf5b855f40` |

## `dev/spec-sources/iso-xsd/19115/-3/mds/2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mds.xsd | 4,095 | `2936ef8c7e2b6ada2e12e37f850cd427bbe83d6058a3a90b63f5cfcc66d9594b` |
| metadataDataServices.xsd | 381 | `fc14b6b0b0d8d142342360749f2a6beb63ce0d3e8217e3f0527dcdf28a3e6721` |

## `dev/spec-sources/iso-xsd/19115/-3/mdt/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 7,373 | `684e0ae69d31104f2f388ff583809aca8fefa749c9f2dccb00cb61caad06db16` |
| mdt.xsd | 1,253 | `2ffa10477a79b6b5056c578221eec5f9bab20490112910aba34e55785b45bdce` |
| metadataTransfer.xsd | 5,438 | `573e73282409e702d69490b8de4a8a7bd1ce4f245231c7952f7e6ed19bd35c56` |

## `dev/spec-sources/iso-xsd/19115/-3/mdt/2.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 7,373 | `684e0ae69d31104f2f388ff583809aca8fefa749c9f2dccb00cb61caad06db16` |
| mdt.xsd | 1,256 | `5766b875ac9a93063b404967fec94f13624ac78df4123d0bef4ae73a910f2768` |
| metadataTransfer.xsd | 5,447 | `221ec41ff798df222bdeea323d500579d291d35c72b5cc2abec7db9ee21a5989` |

## `dev/spec-sources/iso-xsd/19115/-3/mex/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 19,520 | `af0552da9b3b1f76ac2456d82571bbe50b6690def55797cf8a0d78dab314ea86` |
| metadataExtension.xsd | 7,789 | `ec00309d0c04ec27b1b15c83b4eb3c929f3d6237a425575e5005d8d9f5762f4e` |
| mex.sch | 12,263 | `ee93f68435eaa43b80d0f8df2c22bd1b2a6310a3bf5d843a8338a9d6cbd86a79` |
| mex.xsd | 779 | `490862c4bb39e6af4eb65fa397208dbd65086415c1e17656ac58fb42a315e9d9` |

## `dev/spec-sources/iso-xsd/19115/-3/mmi/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 15,465 | `c06551542ef5f6f5106299a48de84a6d703f168d464f72d7e8bb2aad0ff01d45` |
| maintenance.xsd | 4,336 | `cbbda43da0ae3caf11e8332d957b8f1205455b71162d8638d6e84ba0e7d2aadf` |
| mmi.sch | 3,375 | `aff4c824025ae516efba55fdcb27d9b55de9c380f8a7404cc2ab6866e035adf9` |
| mmi.xsd | 794 | `aacaf52c8f84aff4752c5bb878ee86f3957b0205a09d6e78a8364cf3b48f0278` |

## `dev/spec-sources/iso-xsd/19115/-3/mpc/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| mpc.xsd | 849 | `0d50824242af821f3e1cc2b9f73ed7a2d913100493fac57211d669a22f66ce9b` |
| portrayalCatalogue.xsd | 1,891 | `b4733bc3c93376aca19f1db13f011aa8151321af4381c40ce5176563a7d34b4b` |

## `dev/spec-sources/iso-xsd/19115/-3/mrc/1.0/` (5 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 21,637 | `fc2240fe495ec55406b9eaeb7b57be45a9082b2e891cbc539cd42385dfadaa1c` |
| content.xsd | 21,127 | `c540cfddb1387de72da731cd749b7cf3f4d0de22232203b90605e71770734d2a` |
| contentInformationImagery.xsd | 8,335 | `0c68edd9dbd21a867f1b323c144c56a90a68d69800478e28e57fb493ef30781b` |
| mrc.sch | 5,941 | `58bae553f25513cdb4f9197ae65be815d6c4565ef1082527e0c2651fb99914dd` |
| mrc.xsd | 1,239 | `1198f48a43a6634c3e2f43b697333ace0e468615e7fbf01e8688b9fc8f6ddbc1` |

## `dev/spec-sources/iso-xsd/19115/-3/mrc/2.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 21,637 | `fc2240fe495ec55406b9eaeb7b57be45a9082b2e891cbc539cd42385dfadaa1c` |
| content.xsd | 21,520 | `44098a810ad6b8b0baf826f386f4ee72b888892204099b34fb4d1e529151e492` |
| contentInformationImagery.xsd | 8,754 | `164e7110a456c832843109db94e31f0324bdcae89e9dd613bb59ad319379e525` |
| mrc.xsd | 1,440 | `f74f9212451eef2c1f2fb9cef31a15ec66cfa568db636722416c10fe77250b37` |

## `dev/spec-sources/iso-xsd/19115/-3/mrd/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 8,415 | `d0d40b5f248be30d5f2a6d275ee90b672c86236f53444d6b9d69c28fc69d54c9` |
| distribution.xsd | 13,346 | `19a8c27fd4c42de9611efa77d80b9557b26affa1f0b3f205a800eb0de4c6d2af` |
| mrd.sch | 2,095 | `9ebc4b0c0a46076f0f4a52920e67c89802b4355a3e8832da603e4364920cf536` |
| mrd.xsd | 813 | `f8a44a325090c25154f55cd93d17ce9c262da9fcf42c2f0b2c5ef8c247ada9b0` |

## `dev/spec-sources/iso-xsd/19115/-3/mri/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 63,656 | `6d6dfa128d35172e913a86d6b86a1dcdc39c7a6aef46ca094d62f603ce24cb70` |
| identification.xsd | 28,108 | `166b59e485374e32d64ab1d731372a6f68e03dee3f9db6feef1a43361e28e958` |
| mri.sch | 15,133 | `bb4266a038dbf9cc0195d7ac5bb4ba2e3b9232319c34cb75165483962df70983` |
| mri.xsd | 991 | `ad80f80cd9a05809f3f7630f0f7a0c5848027c11350c6089ce0380d5d196a1bf` |

## `dev/spec-sources/iso-xsd/19115/-3/mrl/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| lineage.xsd | 7,655 | `4237454f8fef9fa4b1a51172cbae5267333914dbf6fbd2aa714c3efc3348d738` |
| lineageImagery.xsd | 10,210 | `e74c0f9707460241f74cb90668ad7e1c7fe06db880269ddde206fefdfdc27683` |
| mrl.xsd | 824 | `58fbb9919ff57bf368f498cc2abe5fa084d472b4e73bf9671ebd458b55f7598d` |

## `dev/spec-sources/iso-xsd/19115/-3/mrl/2.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| lineage.xsd | 7,697 | `408dbc2de532522502f645e4486667ed99306df9584af76513ad8b716948a414` |
| lineageImagery.xsd | 15,910 | `19aae4b17b9e75d572aa475be1d34d94089360b35d8ef654773422a36e954b36` |
| mrl.xsd | 828 | `e8becb8f7e30c8ccbd43eaf84ad874aae81a12a63149987b82fbe3a0f38ac5eb` |

## `dev/spec-sources/iso-xsd/19115/-3/mrs/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 34,660 | `e1dfd98b1de525d6860dcbd020fd010449e1cfb96eb41d5196b5fdb248d5e82f` |
| mrs.sch | 577 | `6920f908107a321330a2f5649388a591af57468b98c12b2753fcd4be0f3de136` |
| mrs.xsd | 824 | `79c1cd7178371191aeade967302f7737888be7408bf401991d2acafb15039646` |
| referenceSystem.xsd | 2,517 | `a51044474bf532a5184d7bcbdc70208663dea87942dff3fa5024a63365ec89f6` |

## `dev/spec-sources/iso-xsd/19115/-3/msr/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| msr.xsd | 1,091 | `49c31390ed73d33f47cfbf6aa1864240d685af8ceaa1d27665c02c8c2ad51aa0` |
| spatialRepresentation.xsd | 18,623 | `40fc148773b4def80d00e181fa189a9143f3f63f046c0dcb59b5915ad4caa845` |
| spatialRepresentationImagery.xsd | 5,738 | `040d5e4784f1a3a79a684a06ed0851584438dbb6bd9afa4bcced04c48014bf2c` |

## `dev/spec-sources/iso-xsd/19115/-3/msr/2.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| msr.xsd | 1,104 | `826661f279211b1bf02a9fa2841bf012409e53a5e8d65c6650d54b7f16a087d7` |
| spatialRepresentation.xsd | 18,943 | `67e2f7d53c1c748e0011e92dfbce5dc13dc44e39a9e116d430cc8cf676af11f7` |
| spatialRepresentationImagery.xsd | 5,794 | `f396dc96a8764695371577abec0179b96779cb44f2a204a71950de485de2efb5` |

## `dev/spec-sources/iso-xsd/19115/-3/srv/2.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 17,869 | `2052a1ede6a991ecbe1be61d2a3f000ea04bf5c5c1ace57c80c631f51b181799` |
| serviceInformation.xsd | 14,083 | `a139c8765eb1170c5e72bb573958462706cc3166e204a38ae014b23f922bc19a` |
| srv.sch | 14,405 | `0dab53d8963ea6bc182e8a9aa50293c8f81b8f6c27366dda93ae8b00ce09f052` |
| srv.xsd | 794 | `c2dc784cf1d4417894e033a4a2fad5edd782b6e6b9f4697b978d411ea0d19aed` |

## `dev/spec-sources/iso-xsd/19115/resources/Codelist/cat/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 342,990 | `292c92c538dd74f2acf44439b6775938e1d8ca09d509b6f2e8273fad4b4b2053` |

## `dev/spec-sources/iso-xsd/19115/resources/Codelist/gml/` (50 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| CD_PixelinCell.xml | 1,273 | `a117e7c8952e2fb3bfb83b895c77c6fe33dd139a4eb28aef59f4e71079aa28d2` |
| CI_DateTypeCode.xml | 5,368 | `a837f49bac27d922d698d3cf011be41b68d91ee76ce5903d7ef180dcae85a3f6` |
| CI_OnLineFunctionCode.xml | 3,596 | `dd4ec67318906cbb4b4491e1988d0b02287cb9d2fbb8338e6a78d43d7910e830` |
| CI_PresentationFormCode.xml | 7,481 | `49f655700dee1ddedef64dbf032c25017652a235da47a58b00029032a7db6d46` |
| CI_RoleCode.xml | 6,273 | `a2ecd038200e72e3faae90a3d522333fddbfc76ebd6e24464c8a3994120abada` |
| CI_TelephoneTypeCode.xml | 1,331 | `e29f64377312bc2a6d4b98650f905b1072c8373961a287013af38829c724d86c` |
| CS_AxisDirection.xml | 9,130 | `fb073a0037bb193b74f63139a2e23b618a4fa7e061d919a5e9fea486d8996562` |
| CS_RangeMeaning.xml | 1,258 | `5dce9b184d63c59990f978d7338a0ef93b74f82ac09c4e3723aba1e2bf54dfb5` |
| CodelistDictionary-v32.xsl | 2,965 | `d1497f45aab8c7478fcf597cbf9f97026315f9dc15b2d658d9a92a4a394c1cee` |
| DCPList.xml | 3,093 | `06ca445278cbe98e9fcb32f1ac0a7f6b797b83e9311ede0276457dfc129abc6d` |
| DS_AssociationTypeCode.xml | 3,244 | `0f5cc6e1768756dda2b8548e8105c8abe60814865a71cafb67f7021a9df53ec6` |
| DS_InitiativeTypeCode.xml | 4,686 | `0a26b7b44b6fed17447f80470192f06bac9e232ad6f0c16c1e3235ac7ebdd78f` |
| FC_RoleType.xml | 1,370 | `f02384b4f7c02b096dea7668ebf9e6803537e306ef5570d5caf512fa9a2b8368` |
| MD_CellGeometryTypeCode.xml | 1,728 | `fdfa016a0d38e620cc9959e40f858710882c41c1b1209f9ce25132ab56913f9c` |
| MD_ClassificationCode.xml | 3,056 | `df1c4171f17e031e79d4684e55012e2adf23d4fd853b108e33d4faec504cc39c` |
| MD_CoverageContentTypeCode.xml | 3,429 | `e866fc4fcc907e052b26f9dd9d7df04709d221c5da633a03dcf279aaf60f60c2` |
| MD_DatatypeCode.xml | 5,104 | `36d403a306a347dfc6d156af458ec221c151754c9b1d1029790b6100b17ea6f0` |
| MD_DimensionNameTypeCode.xml | 2,557 | `94d569228139d392844e6f765e353eb2e3aaec3f9f099ecfbb84ef1d73037615` |
| MD_GeometricObjectTypeCode.xml | 2,573 | `77b5661c41af8ddcc3dd31adb4dbe16ddfd4c13841dd2d5966cb99628debd29a` |
| MD_ImagingConditionCode.xml | 3,822 | `984a81ce97e68ffb4f7166a6546b2ac3447b247483464f5c821bf311dae3f9bd` |
| MD_KeywordTypeCode.xml | 4,991 | `7156a543495a0231730dc4a781512690546f6a3ed1aa068ea4a3759b8e6e9b2d` |
| MD_MaintenanceFrequencyCode.xml | 4,670 | `e89977654f0f5d50fb97e03509ad803ab55ccb47285f847ddeaddeef2cf3f1c4` |
| MD_MediumFormatCode.xml | 2,412 | `d29d3318c3c2b8af2165c2e8b08c1dbfc549583c78ed48262a485eeead9a2955` |
| MD_ObligationCode.xml | 1,358 | `c6d699ebc59c7388ae9cd9121c07bab4d001718eba2e31e102f7d6700c9c2de2` |
| MD_PixelOrientationCode.xml | 2,076 | `9ee51dec4a84d560c16e998fb2838fb0daf774f57f25f2cfa2610246a634f3ca` |
| MD_ProgressCode.xml | 5,404 | `d0b4ffede5b8032202866c582c4594b0dcb1af99cbb608bdea704f11d3dfa729` |
| MD_ReferenceSystemTypeCode.xml | 13,066 | `fd4d6f59eb653d3c4bb3b8140419937117f73e88eb467f39a1a31e072c5e3e22` |
| MD_RestrictionCode.xml | 5,959 | `1dd786ba4689da32a6cfb62241585e02869392ee922bda2e1c8b369a31b424e3` |
| MD_ScopeCode.xml | 7,865 | `de3765721deb43b0e5cd0bb57e0e00473c107e70cfbfa34e784c11ad404519af` |
| MD_SpatialRepresentationTypeCode.xml | 2,301 | `316a8a87b4078ef4dfc6523ba92fd9b0973bb020c54568eb8af1433c19325ce3` |
| MD_TopicCategoryCode.xml | 9,087 | `d0f0d4a0cebc184828f627a40078e91525a559e02024bb3375f78b3ea107c7f1` |
| MD_TopologyLevelCode.xml | 3,706 | `c855245697829cc3e10abf51a516a82731e11e0f8c05302117115223904048f4` |
| MI_BandDefinition.xml | 2,377 | `eecdb0d02ef81430ff523b25b3427a3e85bd18fb2fc8ed9809c4ef6bf71e3873` |
| MI_ContextCode.xml | 1,431 | `6bb06662a40a3fa528a465856a2bbf84a5bf31c66b751a40d6589946ee8f81b8` |
| MI_GeometryTypeCode.xml | 1,701 | `7f943de1350a0cb8204ae69521dae3904e325f54a1ede39d98bcc544bb9c557c` |
| MI_ObjectiveTypeCode.xml | 1,463 | `94286294021a306eb72e37c61df6b53593e578573c007cd588c0fbdf25e137df` |
| MI_OperationTypeCode.xml | 1,208 | `2019193dbee09d0ebb8e52ff687b1e978dc6ed9f22686f6234e4116aae4587e8` |
| MI_PolarisationOrientationCode.xml | 2,187 | `23347b8d6822519f49927bb2291b03a56530de8e9ab9bb46009cb35b0c27025f` |
| MI_PriorityCode.xml | 1,736 | `800ceab41d0062a6117e2a2a10b62f77f470ba5707a5b9b3077318aff80f4c28` |
| MI_SensorTypeCode.xml | 810 | `598878964d03f8ac543838d8ad5f1bf4cca5e2dec81c0bc5d2eedaf9131f9410` |
| MI_SequenceCode.xml | 1,416 | `6e52a6188f0bf3f37ab40c8d0a7ecaefb8e18043682c7c737527c6dd7c712446` |
| MI_TransferFunctionTypeCode.xml | 1,427 | `922a4b2e96d355c30e8aebc93c7d6a4345d60021b8c99d32c7884e8cf42f73a2` |
| MI_TriggerCode.xml | 1,421 | `3d69ecefa7264d61249d9df1505108d7397d439163c0f075df1ae4225cd09ec0` |
| RE_AmendmentType.xml | 1,235 | `238f7a037a24281f30cc3d9b4a30906df8aea9fb5915179ec88a7b6ac2917edb` |
| RE_DecisionStatus.xml | 1,467 | `fa7e4a50fcef4fd0928283468cdf1c044ff7e1b744ea012782668d622c80bec2` |
| RE_Disposition.xml | 1,253 | `458f8511187dc136e41b3a61dc9ca36d31cd88862af9a7d84fd4e925614da73c` |
| RE_ItemStatus.xml | 1,713 | `2631b86fbee11d78d904f5754c61a3684b757cdeda7401b00c3700dab87f0214` |
| SC_DerivedCRSType.xml | 2,246 | `8879bde24d83473df72c0f014650d7d8fdc90d2f75b3d7ecad493dd0947d2b3a` |
| SV_CouplingType.xml | 1,729 | `c79c0fd3782ff169bbccd6fed9cafd71fc89fe40978879ceb07ced0863cd02b0` |
| SV_ParameterDirection.xml | 1,467 | `271d3a90ae389e8542b45037ebdead4f6849adfd7995526318c950c4454b8669` |

## `dev/spec-sources/iso-xsd/19115/resources/namespaceInformationAndTools/` (5 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ISONamespaceInformation.xml | 53,190 | `8f5c3f2273315798788bb2901429a726e2b913ea3f314543b674a87ac7be4340` |
| NamespaceUpdates.md | 7,332 | `2a257d2394da3b6d67724a563267e23ae4d693b25e5363819f91f2bdb2987b2f` |
| makeNamespaceTable.xsl | 11,984 | `268af39a6088fa70a3a330c6afe0a8a0e491b7afabf32530aa61967c1051c407` |
| sortISONamespaceInformation.xsl | 590 | `8d0aaca99bdb946a551034ba3b259df5cc78baeabc07f76cf9cf96923d3ea062` |
| writeHTMLFiles.xsl | 15,398 | `8982b9fd76f19d66ab831a371e0da8c9c08bd4467d388aaa72c8331ab3053ac4` |

## `dev/spec-sources/iso-xsd/19115/resources/transforms/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| CT_CodelistCatalougue2HTML.xsl | 7,204 | `855e24c6ce499409cb85a5435c7cbd1f79ef8646b0e456a8c7ce2375018e2b5c` |
| dataconcepts83108.xml | 104,634 | `90825bf3ab6e7e1ea7397584654f35a294e51a4e8e720bcd10776ad0f6a8041a` |
| serviceConcepts2.0-83108.xml | 111,499 | `e91f888e762e5315fa5bd5eeb983910eb5bc4db40a71dbdcb1110c3d5b97c123` |
| serviceConcepts83108.xml | 108,615 | `a8e469bd9975ccad1d6b8aa4172141bd7676bc58c8819f10ee781ff4a5cd1a78` |

## `dev/spec-sources/iso-xsd/19115/resources/transforms/ISO19139/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| fromISO19139.xsl | 7,408 | `889b352e81af002d4a7d15fd93fb7fff4ffa72107d9a87e3e82d8469859f5d98` |
| toISO19139.xsl | 38,582 | `7cc20f1278fb670d37966187fa5e722f7a5812a8517550938aff8af5a487d40e` |

## `dev/spec-sources/iso-xsd/19115/resources/transforms/ISO19139/mapping/` (6 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| CI_Citation.xsl | 6,929 | `7167c1b972eddc2bffa64a65db3f64932e352d99ff55d5d8ef33a007e8b326ff` |
| CI_ResponsibleParty.xsl | 12,011 | `6c34041fd6164748bee66e3063288665daaa277b98058fd004185a4dfb454f1c` |
| DQ.xsl | 16,438 | `b75d1a3639e14b0ebf935491cd15b38c68d6846d5254b6fb53c2cf0e6665eca5` |
| SRV.xsl | 5,765 | `66d4a166eeb0222ecaaad64d30060cdbcac4e8874910cf427742ad37d6258fe8` |
| core.xsl | 34,694 | `cad781077d812e6bad5c73f1e66bfe701c90416875f292dcff72090361721ca7` |
| defaults.xsl | 14,446 | `4893c1b07420a693c6ea49d33d94f77180273bba6a7a6c580e3045b786bac533` |

## `dev/spec-sources/iso-xsd/19115/resources/transforms/ISO19139/utility/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| create19115-3Namespaces.xsl | 4,204 | `2bf401cb524eec311ebcb3cc1612bce3e0c02770c75d271991c78dd394603726` |
| dateTime.xsl | 3,084 | `778286e33f51b5d736df139a42a93e41404c6df14a537dff62de3dfbee814ad0` |
| multiLingualCharacterStrings.xsl | 6,168 | `870c26322b9be145a7d339beda9f32d1db986e6bd07a62107ae48764df4bde49` |

## `dev/spec-sources/iso-xsd/19139/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 1,106 | `45ec95e8e5786a97b19afee6f851e6a33a7088dae8f62c210f51f6d1505d68f8` |

## `dev/spec-sources/iso-xsd/19139/-/cat/1.1.0/` (5 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| cat.xsd | 1,229 | `b173bc7de3304acac6bb6efe00b9303c773a7ce58e1a052cb7a3c979abad0cf7` |
| catalogues.xsd | 4,066 | `034745664e430f3e5e8842be3b9b4e0ceeeab993da4ea17f7e8a5dbdab80b2ad` |
| codelistItem.xsd | 2,905 | `574e2bc5c0ad8d17dd2fad4d2848833dda15ffe752d6755c3ee2f77dd4e11a82` |
| crsItem.xsd | 9,606 | `567bb941e670a64c8c19a09e5faaa886efddb9f9ae1bfe1ec4676dd29d5de745` |
| uomItem.xsd | 2,386 | `c1df7ab17759d93211fd188264519010fe8a46f3f135e3aa60f7e5365b24010a` |

## `dev/spec-sources/iso-xsd/19139/-/cat/1.2.0/` (5 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| cat.xsd | 1,226 | `2676102f87638b319673d2f85b395dc0d39e64f923cbd5a636e5dea208577618` |
| catalogues.xsd | 4,058 | `954884fb38d8cb76a446d4f16f58a96562969a9af6387723a7b2640c44c8cef3` |
| codelistItem.xsd | 2,904 | `a4aa1242b2e5e8fa971a585d78e7a6fe548e5850a18f197da03c1bf0a423844d` |
| crsItem.xsd | 9,603 | `951324577d713f3161f7cd3c14286406924b9ba1239d738069630e20d5a994cc` |
| uomItem.xsd | 2,382 | `02b8d68dcabbbb4b64f2508d4a719b46e2459d658f34c0fd9530545da673f478` |

## `dev/spec-sources/iso-xsd/19139/-/gco/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,697 | `6f13240904a9fa144b09e4c6e8fb55b72e521ae4cb5f5cffb7058910757d0258` |
| basicTypes.xsd | 22,214 | `4bb46d0376ef1f3a0f23466f2a350c6d81923343e4e5483e2d03a6500f2f9a98` |
| gco.xsd | 1,186 | `fb631cdc64b6438930b5de8e83bb72efc3aca55a028af8b0497e3e63878acddf` |
| gcoBase.xsd | 4,258 | `1db3380d491bdc095f186c82a7291b0d43678bb438c349801439c19c12a6f97c` |

## `dev/spec-sources/iso-xsd/19139/-/gmd/1.0/` (18 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,541 | `e02de9578f78e165ea2a3a44c70ef828648cee4ffdf9aa64ea724a28dee224d5` |
| applicationSchema.xsd | 3,214 | `97a77189bf8e33960f96f2fcf67141cab56a54b4c816a506b73d2299bddd12be` |
| citation.xsd | 15,547 | `467b02e9c06a4273c8126fb38530ed5052d220cbe510a3bf9988efcfdb143b8d` |
| constraints.xsd | 6,581 | `4bcf49dbeba599f58e248a592ed9c0af92c806476b48a96868033c882c4df343` |
| content.xsd | 11,449 | `21b02047850f08c03235acda9204a12e4db63037790a17fd5a282e5bbf1a031f` |
| dataQuality.xsd | 30,962 | `5aeaff61c0da8f09ed287dc001501b50fa92ff67900e7be2cdaa62c58595ffa3` |
| distribution.xsd | 11,762 | `78a1e4734d649d2c783f1060de411da5cbb443470f5e44f56969aefd7fb88d45` |
| extent.xsd | 11,395 | `a640a29d93ca78cbea67416bec43972e866d13488861b48b8f3e96b26a24445c` |
| freeText.xsd | 7,187 | `5a2ddcea226a79736354af94063be109791e8a42b67639d5631a9f0256343cd2` |
| gmd.xsd | 1,197 | `ac50e24660c12dc5109a074066db8267c0b6938827e67186978b3de18e7db3e5` |
| identification.xsd | 19,777 | `f43616fa742ef7185f045dabca1806e950b2b6003a3eca7c16a1bbd9da3016ad` |
| maintenance.xsd | 6,051 | `94b7d896c3d1b9035c719f923e5ec8891b1383e79e81969d3798268f69e75c35` |
| metadataApplication.xsd | 9,358 | `07e6715a1df909a10d422f7cd10f92fe08d9d7a5146f66af669f1223d209680e` |
| metadataEntity.xsd | 5,903 | `d49957de1e0c8e885aa55d8fddce2fcee96cf321e598ac6ad800acf78c860182` |
| metadataExtension.xsd | 6,455 | `7136df62315d11a7073b95603d68bab924a3ddeb9ea1852d80b5c1ebfc78e5cf` |
| portrayalCatalogue.xsd | 2,690 | `2f1a9162213cb1533971207e59a006406c05693e60c893ec52b640ad9009faea` |
| referenceSystem.xsd | 5,749 | `c928ef3043bf92f7030e31443d45f3ee0ad52c205fc11ddc4cf6a414ee96555c` |
| spatialRepresentation.xsd | 13,951 | `b6f98d1ae61beede20ac04ad843fe4bec7a4d793b2aa42d3a2b5a574f7785f33` |

## `dev/spec-sources/iso-xsd/19139/-/gmx/1.0/` (8 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,683 | `6186f8ce76439d963cab18ff909d4333112eb528ebb65202f49839a41151385d` |
| catalogues.xsd | 7,270 | `e85fde61e378b6ff4d524b5b4b5a3ac0b85541c9eb55be61a69afc20f3160a16` |
| codelistItem.xsd | 9,478 | `77c93ad7285898c7d17d7d9ac963b4cd2daab126a45790bfbec3a5c95f0f7b18` |
| crsItem.xsd | 50,099 | `3778b77d10f02d7446e6477de8d6615f6dbed74b1edf1ac99e71634250c93195` |
| extendedTypes.xsd | 4,637 | `a72d800db468716851774c4eb73f3143c5ab1ec0c88467f3ea743c91e8e6a0d5` |
| gmx.xsd | 1,171 | `c6d35e2e12ae568325130da97dd475fa9065640c534b862c7668ce170f3a63cb` |
| gmxUsage.xsd | 7,344 | `13a4bc60d228d8131bc42f289b00198d9def7e352c80cea83664e6506ddd267c` |
| uomItem.xsd | 9,172 | `60b5342254093b90c4223b860bda8974d6d32b74b3def6d7cb779020c43101b7` |

## `dev/spec-sources/iso-xsd/19139/-/gsr/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,553 | `39d6d19213e8aa94692c222b81bb27bcad837072797ab083cedb54aeb26f43e8` |
| gsr.xsd | 1,207 | `b1c36f3254176669919e61979abe12bf2d2d4969622338929674d6184efcba8a` |
| spatialReferencing.xsd | 2,335 | `592eb4b77c9034e5c19e6dc2d9a62e730913f654b1db0c61592816dd8a20a9e1` |

## `dev/spec-sources/iso-xsd/19139/-/gss/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,550 | `9b4f1f0d2ef7b09c81efac11cd81ace5c14c172ae1d75f944faa70f6dac4454c` |
| geometry.xsd | 2,868 | `b83ed221d77da17008056aece068859ba70db6f4d490621d2999eb067e8ff0bf` |
| gss.xsd | 1,193 | `48a0bda09825caed9b7a517ea34bead8f7d923ec5e165165242d17fee7b21efd` |

## `dev/spec-sources/iso-xsd/19139/-/gts/1.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,547 | `c6534a8223405cc90b7ed6240f3338394295e38f0a1f33a949c5c29c0b76fa7b` |
| gts.xsd | 1,200 | `09132b1a45cdb51a01efeb333f0c70544fe05410f01f3bcf6c5c714db0b66587` |
| temporalObjects.xsd | 2,956 | `2742d53cffb6d6fdf56f7907cc48ee5115be68ff7e4dacdcbcc8b08e4a53b918` |

## `dev/spec-sources/iso-xsd/19139/-/resources/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 1,162 | `fd3727a3cef75690c2ac41990387a9e9d5f9f66db07bc5b9b7de443400996983` |

## `dev/spec-sources/iso-xsd/19139/-/resources/codelist/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ML_gmxCodelists.xml | 44,014 | `511666b677a9e8233fd20aa67017f8fd71c587a4a01044f05f0b6e5c61512efa` |
| gmxCodelists.xml | 95,363 | `1491d5d933b73406cd3c42418b409d30ad26e4ba9161661399b8c7f5c709e652` |
| tcCodelists.xml | 3,699 | `b8990c33eee67a86f3f4bfa4cb428d3c67d9fe26a8d11aef98b238fbdfcabe91` |

## `dev/spec-sources/iso-xsd/19139/-/resources/crs/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ML_gmxCrs.xml | 8,516 | `ed15ec074c2f408e160d215428f5149de7575b50a055030deb44886864b1f759` |
| gmxCrs.xml | 15,107 | `971ac57cd28fc6bf0160aecd63d3d7446950195e70d1350fb96e1635ac7a2348` |

## `dev/spec-sources/iso-xsd/19139/-/resources/example/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| fr-fr.xml | 3,777 | `22e96cba116caa858c1b085a0a9a8b4d54b3067c6ab1b0e2e656112d99b0f8b8` |

## `dev/spec-sources/iso-xsd/19139/-/resources/uom/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ML_gmxUom.xml | 7,043 | `780d72c8423f72bf4b58d62f8cf27e197d395a8d7922ea38e629d19edb2e7e0a` |
| gmxUom.xml | 3,706 | `b96deedd0d87fc036495f38cf3aef0766f5d3f4172a283f3ee405585279ab917` |

## `dev/spec-sources/iso-xsd/19157/-/dqc/1.2.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| abstract.xsd | 1,917 | `d7474ee2c0299bef1ca5b567ebd6d56d570e10b9d490dd3ef718b3c84cd664e0` |
| dqc.xsd | 971 | `f9f6c4a886e59a0680d24d6808c4315a44f68b5fa8f53db72033d2a13bc5cb7c` |

## `dev/spec-sources/iso-xsd/19157/-/dqm/1.2.0/` (3 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| dqm.sch | 4,380 | `da8f48ef0fac6b2d4185f77992dbefd4f82d0b3c13284ccbc0ac5bee8efaa37d` |
| dqm.xsd | 1,153 | `bedc78a3212c1f80ef0370ea8c5e3b9a1735b4e1bf6731abd4e9d84a63e44e2f` |
| qualityMeasures.xsd | 14,412 | `3edd96a33c3e9ff1e506e9855ff0a0194a98c6f92863d00ef66fda68ddd0b3c2` |

## `dev/spec-sources/iso-xsd/19157/-/mdq/1.2.0/` (7 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| dataQualityElement.xsd | 24,433 | `e817a1cfe077b1c69a37b295aa88841f2264a9576925ec9f47e4ea5c6ac15752` |
| dataQualityEvaluation.xsd | 8,447 | `bcb050ebce5cf5644f67e84071a882cc168315bb9f21758f77140d6ac65d64ef` |
| dataQualityImagery.xsd | 3,765 | `ac9fd3fee0a0262c1b51b5c01cf3b38331b7088c5252263d0f5377c7cd0558c8` |
| dataQualityResult.xsd | 6,603 | `3dabcb5ecc1d677ed952e25f1790b8502a958709d013dbbba8a38b5205d0b79a` |
| mdq.sch | 2,115 | `db9a2843d1ebe587c60771c101a01659662e9366d2b9c62571f5b013e7e38252` |
| mdq.xsd | 1,258 | `37ce9bd4e12456b8f5f2f400a59c72e111744bc65591893c8c3504c8ac33fcf1` |
| metaquality.xsd | 3,697 | `9fbf51e9adc962a49e024afc549425e207e61a9c1b5679678021429cd28f10c0` |

## `dev/spec-sources/iso-xsd/19157/-1/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 19,399 | `ee0fc6da6f8c57074875edceb9647fbab2651466cefc849f8e2d909535ac66ce` |

## `dev/spec-sources/iso-xsd/19157/-1/dqc/1.0.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| dataQualityCommon.xsd | 1,594 | `4d1a5d7e28c639675382d796b22edc10e154b93fbcc7c02a0bb9b59fdf1d9436` |
| dqc.xsd | 788 | `356a9f0f805fd81906c2845d0a760933f70f93ea26287b96dd7d5647f0eb1376` |

## `dev/spec-sources/iso-xsd/19157/-1/dqm/1.0.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| dataQualityMeasure.xsd | 15,616 | `f2d95bc8c8a14b5f2aad8524d364a7e2ac859f8faae83482943be9534274855d` |
| dqm.xsd | 502 | `94a3186ca07dcb3e929bcd94254c3b077af9c3296c0991528574030f44ec2d9a` |

## `dev/spec-sources/iso-xsd/19157/-1/mdq/1.0.0/` (5 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| dataMetaQuality.xsd | 5,191 | `f4bc0aa177604285411c347f34883a0ea837fd8dda20dd4e9b9308dfff58d33c` |
| dataQualityElement.xsd | 30,691 | `1164d4b55e5a0aa747392f623ce5c3acf65c689f25f77b5784343b3d0ded1811` |
| dataQualityEvaluation.xsd | 12,513 | `50243c0e86cc756247bf30a3256a667c1c4eb41f17642170c9cb17322f0bb5fc` |
| dataQualityResult.xsd | 10,130 | `0a4b8af7dd517eb4a9ecb69c4f3f3b6e94130b0282795a315373ea3bd8eb28e1` |
| mdq.xsd | 714 | `afb789d9f53d6df6f69c886e3d2b19cf301a5c0946d69ed545e25fe5c53f80b1` |

## `dev/spec-sources/iso-xsd/19157/-2/dqc/1.0/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| abstract.xsd | 1,926 | `9a334e56cb1d74c157ada114722ad638ca54c1f2140eedfd9d2e006b73841ec2` |
| dqc.xsd | 1,002 | `d547a03344f7ef1cc913037ada17dc87133cfd791a77778aa241fa18798fe24a` |

## `dev/spec-sources/iso-xsd/19157/-2/dqm/1.0/` (4 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 6,175 | `b48adc6697031d59835f2dd7bc541f92a68a7bee193ad9e4cde28117d5ed8f61` |
| dqm.sch | 4,382 | `6d57819bd8b184c7aeb224daea22520b4045c12e17b7e31e44d0806601e78ef7` |
| dqm.xsd | 990 | `49d03d4ab581b9b52e5caf03b2bb282e45534802c283d743fcc54028c8958818` |
| qualityMeasures.xsd | 14,004 | `b0daf9a28b47b824ad95ce98f2dd96406da804d0df7bb025c6de832f0bad7e17` |

## `dev/spec-sources/iso-xsd/19157/-2/mdq/1.0/` (8 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 4,679 | `ac201b23fdf57bcdda14a0fa6596af867df88ebea22a9eac4c1279fbe1725d0e` |
| dataQualityElement.xsd | 24,109 | `80c67e1225f4357901008d9d1d5e56c5ec08bed6b84eef7c7e040243b3e50b50` |
| dataQualityEvaluation.xsd | 8,263 | `0d04308198f1c93cc44dc48bb615ed9ec3454134bf99be6c9e026dfa1accec3d` |
| dataQualityImagery.xsd | 3,728 | `478bc9f4debc1b6a0cd6b057e4deff6eca944bff2f8416766603ad6d138a01a2` |
| dataQualityResult.xsd | 6,438 | `da60ec977c9fdc11b8b097ecf25e14da194d32a667f2a665714b622947dd4568` |
| mdq.sch | 2,117 | `2075825b3c3b5938ae195f99a499031cf8691655939e54f46a4a43529cdd0126` |
| mdq.xsd | 1,286 | `c807cfce6cd4b52c5b507faac4fe5a1671aefadc9e907fd2932b93182dff1678` |
| metaquality.xsd | 3,652 | `b3184cddeb1ee9a80cba5bdb105488648e02e6da22529f5aaa7ccfc065151b92` |

## `dev/spec-sources/iso-xsd/19157/resources/Codelists/cat/` (1 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 12,201 | `75628d7d44f8320215812de1b5984fa9519578f198c51763ae6fe54aa8fa9504` |

## `dev/spec-sources/iso-xsd/19157/resources/Codelists/gml/` (2 files)

Obtain from: ISO/TC 211 XML schemas (ISO 19110, 19111, 19115, 19139, 19157): <https://schemas.isotc211.org/> and <https://schemas.opengis.net/iso/19139/>; the terms are in the folder's ISO_LICENCE.TXT, listed below.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| DQM_ValueStructure.xml | 2,577 | `45dcef8d7be89242e8d040f539c08f3ae176b670e29ca6d31249f43c5c01be30` |
| DQ_EvaluationMethodTypeCode.xml | 1,646 | `1ea81de2d58fd20af461366049f22bddad9c225470308071c7631b37f2dd6e99` |

## `dev/spec-sources/ogc-gml/` (1 files)

Obtain from: OGC GML 3.2 schemas: <https://schemas.opengis.net/gml/> (OGC document and software licence).

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| SchematronConstraints.xml | 5,552 | `ed6698d09477a0d956a4ad242db3791046fcf21d28541443763b7c564b8c4f74` |

## `dev/spec-sources/ogc-gml/gml-3.2.2/` (30 files)

Obtain from: OGC GML 3.2 schemas: <https://schemas.opengis.net/gml/> (OGC document and software licence).

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| basicTypes.xsd | 14,905 | `2e37d858bd5be1307892add40826632e4e16d5c44b032ba668c510f09588da5c` |
| coordinateOperations.xsd | 33,344 | `d9a96671453711b98301d8f796ba1bb47990b7ab4ea83e8a1803c27110bbc434` |
| coordinateReferenceSystems.xsd | 18,420 | `0b38a6d9a82b698307215be446cfbec18682f1edcdbdf531d0e9fadb88e3017e` |
| coordinateSystems.xsd | 18,701 | `50658a9b0cd0e8887dab3a54d0e66ea9d74e7737ac15b87fb3a88f6d578c884b` |
| coverage.xsd | 20,827 | `8861ca287202f3da462b3d78c71065dc78b3d24ac37304297601bd6599e8362f` |
| datums.xsd | 15,923 | `a5ac13d8015f8d9c0947e5ad614c482a0f2c632d168f87c631d953273bdeb30d` |
| defaultStyle.xsd | 19,385 | `88ddc067143b88010887564883c8fad51bea16e46bd1892480dd93a30367cdc0` |
| deprecatedTypes.xsd | 34,674 | `cd02f14a1f83be529cb5d7ba8ce6a4089ebf26dcb3e287e4b81488cb6bf6dd5b` |
| dictionary.xsd | 7,137 | `fb5f633e6b441ed19bd17433e28efedfb7a335bdbde04b4e5383582a763beae5` |
| direction.xsd | 4,161 | `fed7bb5e0fcc13b78add0bdb4b603a278452b70617a207ee084d2427daa17011` |
| dynamicFeature.xsd | 6,807 | `457e07361d175c8c344d20fbed203f051b07dc13f7c637576247872fcf294c43` |
| feature.xsd | 5,584 | `aa8434aa6b38fe00ab9dd1a1e84c9288b4828484c783c04c8caf4ea5650ecb07` |
| geometryAggregates.xsd | 11,523 | `d1cb25b4e923d06c44d6930ced39848ea0e938e197f95a8794e73692d0ff425b` |
| geometryBasic0d1d.xsd | 18,929 | `b1f9e4c1714546cd1df6f03f459926c3714f6b4346bba58de7950eddedcc7d6c` |
| geometryBasic2d.xsd | 6,625 | `2fc0914ecd7ca02d41ec090d8202e754d67e40890d8846382e7e25446bf4b181` |
| geometryComplexes.xsd | 5,824 | `26e936aa53efe6e56bbcadd5528967c2b9ac2b08b869252703c757e7ffb9711c` |
| geometryPrimitives.xsd | 42,649 | `ddde612ddaa13fe8313ac5e0d70090d52459c83777e394b3d3917a205469b2af` |
| gml.xsd | 1,076 | `eb1e652fdc10fa70352c3fc554cd3bfacc5a863e964a4e64c76f25c762b80a3f` |
| gmlBase.xsd | 12,756 | `36825875b089ee8f69f42103d31ce52f6eb9489d2f40e11516495f7c152cc79d` |
| gml_32_geometries.rdf | 13,659 | `e203bae3295172e3e85e9cebed777a792f046811e1f9a888c1498fb3beceb917` |
| grids.xsd | 4,132 | `c317678414da9a28e0be87bb1544b875875746bc219aa0b7f6c31f32efd0c5f0` |
| measures.xsd | 3,104 | `3faae40533a200b6999278678ef43c90a508fd7f8ded474f50475b4c3f19f152` |
| observation.xsd | 5,530 | `514b7489b2aeaf58303e24c0180cba92654f2201e87a6aa7c2fe8e1c73ceff99` |
| referenceSystems.xsd | 4,680 | `5bbeb1210ead8b6fba6516c4a5b9e80c1b811b48ec9f3293bbaaa5346aeec0e8` |
| temporal.xsd | 15,598 | `e6336faf79732dd8cc79b4f18595a4ccf93ab9d7c55e9f6517b79f4f44572fdd` |
| temporalReferenceSystems.xsd | 12,679 | `f7671997af4fbd098ff53db1f025df3d1a678f707560a9bca83ca54d4ef61e7c` |
| temporalTopology.xsd | 7,795 | `ee8fd1e816cb41746c16443e47a0206f71ab77a621d49778dc565a9d6eff4352` |
| topology.xsd | 22,790 | `aa4e2db656a1dfad2fe50c23cccf5ab0f3bba5894087dca75e7bd25faf31ba12` |
| units.xsd | 12,283 | `b3e2b8f364b9b844dccc0d8314f9c6c952db5155bccfe7316a1742a63dcc29fe` |
| valueObjects.xsd | 11,438 | `ddf0c234b66363f596492f59b92e307d2d7d864a122c28abc32bcdf87ce7485e` |

## `dev/spec-sources/s-100-xsd/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S-100_Schemas_README.pdf | 450,214 | `addf8756f2bef65a9e162592134e909834e4044528109df7467f8f3ad5cdc6f3` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100CSL/20220331/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100CSL.xsd | 11,642 | `a7f43222e9caac51ed185d61d006f5648fe27bb924468d9cd1ac0eca706b85f2` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100Catalog/20220705/` (7 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ISOTS19139A1Constraints_v1.4.sch | 35,744 | `5beb6692e087609fd1afc30ebc8cd638d8b03be283211bab7df7af16410e2e3b` |
| S100_ExchangeCatalogue.xsd | 58,956 | `b589b44c7fdab3d6a17a9c1eed4bb81c8271051167069dad1cbe9353c954d28b` |
| S100_XC.sch | 20,841 | `1ffa3eab9cf9d2803f127d2f7291dd63f8bc33a01724f286f8b7adf94a258106` |
| maintenance.xsd | 4,017 | `22e06f46e9de194d0fb5b66661e101b28e52a137bb4851b9988ecc06e354c734` |
| mmi.xsd | 784 | `d65775aa199eb44ae50ee20f3b8097d7638a24f0e44247c709df3461500d9ba5` |
| s100mds.xsd | 4,853 | `65782f452c22c6b9a7baf96a1d162e0963ddfb08d4b42b8a38c67be48f1e61ab` |
| serviceIdentification.xsd | 5,802 | `3c99bc9919552adda821aea972ad791421b52cb8044f1eb53805f4fd25e9ad3a` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100Catalog/20230105/` (7 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ISOTS19139A1Constraints_v1.4.sch | 35,744 | `5beb6692e087609fd1afc30ebc8cd638d8b03be283211bab7df7af16410e2e3b` |
| S100_ExchangeCatalogue.xsd | 59,991 | `965efbdd1b6c6ae2321f9d909807071b61e95c8f2577d67db8db2bc2c12d0d02` |
| S100_XC.sch | 20,933 | `cd338b141f6f811ec487c0a02a8655b10dfb326c41c08134b9399cdf93fc4331` |
| maintenance.xsd | 4,017 | `22e06f46e9de194d0fb5b66661e101b28e52a137bb4851b9988ecc06e354c734` |
| mmi.xsd | 784 | `d65775aa199eb44ae50ee20f3b8097d7638a24f0e44247c709df3461500d9ba5` |
| s100mds.xsd | 4,953 | `01c51932f3ac49da93a3387b0415b805d409115f109acd7eefd17122b37cb075` |
| serviceIdentification.xsd | 5,908 | `c35f3016c5ff8104b12125dc0820beb3995b6a8d23e2f78baac4e7a84508e022` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100FC/20220610/` (5 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100Base.xsd | 7,811 | `181378d88ffc21fb2e9d6dcf6669708713c7a6aea6e0ef34161868db84ffb0c8` |
| S100CD.xsd | 12,663 | `e84e8ae1c056d08e1fe177c73d616e8e0f0a136bef950476ff23b526953ac05e` |
| S100CI.xsd | 47,160 | `47d1c7690db2536649309174c8d2b9b05cff713c8a6d038a20311e8186aeb373` |
| S100FC.xsd | 30,308 | `37dffd3b6345e3e3136102969c49651fd0244900b97da5e0c6b197c6feb47db9` |
| S100_FC.sch | 5,293 | `a152024de2f3ac711bd5b3b94aa67ca3ade138ea8a19ba1af7d701f1f5b35146` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100GML/20220620/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100_gmlProfile.xsd | 77,689 | `7a7a3ae69bdfbf095701e78a100cb5544b6c82dbc3eab6e9f45fc3a84c455163` |
| S100_gmlProfileLevels.xsd | 3,398 | `a6602346c05212d8598e9bc96d31d7b1d8db5af4a8f496fff17347348fe3b930` |
| s100gmlbase.xsd | 43,000 | `d73af785782498434cb398b519f86812dae12dfb672b9d133583daac63b0fe10` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100IC/20220828/` (2 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100_IC.sch | 7,039 | `16c3c98624a01b37b29bcf47966e4ebe52d17b5029cdcb93f9b01969bbe593a6` |
| S100_IC.xsd | 30,962 | `e8ae2abe5b8990ca138930ad78f3be3472ed3959d721d2dd86b4e6dc58d57357` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100LA/20220331/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| multi_language_support.xsd | 8,423 | `7068c2adba7efb83fdd6ff9e4e0ef22c2b93097df627110175157ac387040dfb` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100LA/20220728/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| multi_language_support.xsd | 8,537 | `ddf4cdfe2b4b00e5b2e053c471306a283396b8bd1c5576585b0e7d5b5a8cbe1a` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100PC/20220705/` (11 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100AlertCatalog.xsd | 9,747 | `bf5fcc522a2feb8d0dff4b9233e96348af22e68978c759fb9062523fdd5a3f46` |
| S100AreaFill.xsd | 2,978 | `938e6bb7e9bf27e9329be0a29fc4da707fe61a77f774f9387aa7c1b0eba14e2b` |
| S100BaseModel.xsd | 12,142 | `e34d841c0b1d3d490a7ed980b2f84070abd0386be0314e3881865537b421e774` |
| S100ColorProfile.xsd | 6,378 | `05291ad0cfd04d9cd76a916aae2179a79111cc5ac1a4b7d78560e31662067e4b` |
| S100LineStyle.xsd | 2,823 | `d0a85e392e67c64ff62c6dd6e1d7b84b8a4d39887619fae6c1d7164d665b5e96` |
| S100Pixmap.xsd | 4,647 | `f98dc380dd3239de9580919ff5c9c759d9a169292a1719b78ced4f31bc4428b8` |
| S100PortrayalCatalog.xsd | 20,494 | `04b522168c47be3afaa489060f1c4eac152c8cf4f46bd4b9d5685f8c7894f775` |
| S100Presentation.xsd | 10,677 | `4a84c016df74e29f05e3cfda3dee3bfcd1dcd355c5440465af2556fb2c7878a2` |
| S100SVG.xsd | 5,600 | `cd981c2952136374fee76b71d6561bff4b8759a41976b0d5b2f0654a47f8491e` |
| S100SVG1.xsd | 2,918 | `f26c73033e57c898c7081377473e08bc5ce383ddef80201acda5856f858a51cf` |
| S100SymbolDefinition.xsd | 23,088 | `e83e006c8ae39dbe0d8c84641a2701c6510a7028981f6b9fd2b4660542fadfd1` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100SE/20220610/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| Part15.xsd | 20,582 | `0dfd80fc1eac98f39b37771ad95941f2c7de3a6b15f845054ee2a38b63f65944` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/S100SE/20220728/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| Part15.xsd | 20,677 | `e67a7ad01e4369efaad3e924523865598bec67ee30ce852ba0b53452c4e4ef30` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/resources/Codelists/cat/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 74,118 | `52bbaa797462f6e6076473e492bf9168dbf9471be850afc0473e504eacafa650` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/resources/Codelists/gml/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| README.TXT | 47 | `2209cb2e059812f18e841f8d20bf9ef11c8bafb8686f69ceec2ca74a3c389bd4` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/resources/XMLCatalogs/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| XMLCatalog.xml | 4,338 | `3f60a2cdcad22bb9d4bdeed829346a8a52a012cc95db5fb008f3552f6e2e04fa` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/w3c/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| LICENCE.TXT | 2,526 | `0787a37000cfa7310803c0a160e0c19d0f234d6b5d25f3085fd2a5b4975171e4` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/w3c/XML/2001/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| xml.xsd | 11,374 | `0853f3f40a4eb194e4705659f2868810fcd0a03c767e9db6d656d27722d19ca3` |

## `dev/spec-sources/s-100-xsd/S100/5.0.0/w3c/XML/2008/06/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| xlink.xsd | 9,093 | `4dfb09c21df578c1699e231d8b5a44ae6de2dac1645a2c834197c7d89532c834` |

## `dev/spec-sources/s-100-xsd/S100/5.1.0/S100Catalog/20230327/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ISOTS19139A1Constraints_v1.4.sch | 35,744 | `5beb6692e087609fd1afc30ebc8cd638d8b03be283211bab7df7af16410e2e3b` |
| S100_ExchangeCatalogue.xsd | 59,147 | `856087ab383ada1f9e1c03a5d84b865ff7520d0231c984cb85b29b56b9a93b2a` |
| S100_XC.sch | 21,783 | `3ac3066155492c297144c3d1b819c7e3c0c1df168e3cc9760c4d214fcd35d35e` |

## `dev/spec-sources/s-100-xsd/S100/5.1.0/S100PC/20230327/` (8 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100AlertCatalog.xsd | 16,668 | `7f84925aaae3cc93ae9ed6c03b0786a3a2b6ce2d393b86d91689af87d8010eee` |
| S100AreaFill.xsd | 3,177 | `245c9c9e81e6daa6fc7d2d24ca271a586fd72499245ffdbdd2d1583e22123f61` |
| S100ColorProfile.xsd | 6,619 | `737cd73e596a701a8c7ec4b37e3429981c3a938421727b7b13aedc98904bb9ba` |
| S100LineStyle.xsd | 3,024 | `1001ad1112b13883fe26866832e3993e2f41cff7b026cae0f2d63fe0efc04ce9` |
| S100Pixmap.xsd | 4,841 | `df8fa27ce80cc54a086384e1ee5252f7c893cfbd474f09514d9af0d76ee95482` |
| S100PortrayalCatalog.xsd | 27,713 | `2b8a917da9d6500ebab6652cfe72cd41eb75f57548e329f3bbee90774fe72cd2` |
| S100Presentation.xsd | 18,360 | `a92f46b9e65ac218613cd143ab3a05eac5ad6ca8c458f24a3e3552e2d3567f77` |
| S100SymbolDefinition.xsd | 55,046 | `16361445cbfbc9793c3a560c79eb1b9476aa7d4a33ad46106c44c129310448ff` |

## `dev/spec-sources/s-100-xsd/S100/5.1.0/S100SE/20230327/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| Part15.xsd | 21,370 | `ba6b63533e9ea2029d69987cc9615d897e0a08db3d2ec435b4d9da7579e3f86e` |

## `dev/spec-sources/s-100-xsd/S100/5.1.0/resources/Codelists/cat/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 64,596 | `96d73abfabe743ce43dc2354d3451444cbd865b4f3ddc20f55a905b66f0657c2` |

## `dev/spec-sources/s-100-xsd/S100/5.1.0/resources/Codelists/gml/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| README.TXT | 47 | `2209cb2e059812f18e841f8d20bf9ef11c8bafb8686f69ceec2ca74a3c389bd4` |

## `dev/spec-sources/s-100-xsd/S100/5.1.0/resources/XMLCatalogs/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| XMLCatalog.xml | 4,338 | `3f60a2cdcad22bb9d4bdeed829346a8a52a012cc95db5fb008f3552f6e2e04fa` |

## `dev/spec-sources/s-100-xsd/S100/5.2.0/S100Catalog/20240415/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ISOTS19139A1Constraints_v1.4.sch | 35,744 | `5beb6692e087609fd1afc30ebc8cd638d8b03be283211bab7df7af16410e2e3b` |
| S100_ExchangeCatalogue.xsd | 59,390 | `6687f9463be98a42a4af1e22428f491adca82d544da4a9244f97260a30884e5d` |
| S100_XC.sch | 25,047 | `a91d0edbad2720de90889b8224af7bbfa5c0f6a036076cc264559dbe5910160d` |

## `dev/spec-sources/s-100-xsd/S100/5.2.0/S100FC/20231214/` (2 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100FC.xsd | 31,991 | `322bad958bf8af10636eefbc435dd832fd56796e1448ce1ecadaf29163fb6662` |
| S100_FC.sch | 5,588 | `df1b0a134c0c225505bdd71516eb59aef224e9a329c7456437a06ff62fab39f1` |

## `dev/spec-sources/s-100-xsd/S100/5.2.0/S100FC/20240515/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100_FC.sch | 17,410 | `c59e521dce819954270e4cbcc826eece80d002aea7c704cfe30e86a386fc06e7` |

## `dev/spec-sources/s-100-xsd/S100/5.2.0/S100PC/20240415/` (9 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100AlertCatalog.xsd | 16,922 | `6677cf6094bdf17109a5e3aedc401d3be5695a295b39ad1ec386a562f7f4ba80` |
| S100AreaFill.xsd | 3,431 | `da8ca823907fcbf853ea330bd1eef24feec4d5ad13d6f2a502d302d9c03c16c6` |
| S100LineStyle.xsd | 3,278 | `e4260d2062c6f4e9bbb78e3478f5ec8b24b24cdc269e41f1e9ca2dbe1b8b6903` |
| S100Pixmap.xsd | 5,095 | `0d1f1aeac9791247d737bb523bd707cec5e612a1ab57561fb9aa74c4f2c7352b` |
| S100PortrayalCatalog.xsd | 27,967 | `9c58b1c4f53bb7d1519a08a93e321e01daae480b1a135091bee8a8bdee713f92` |
| S100Presentation.xsd | 18,756 | `91a539dde69cead9b6b9f097e67f107d8e3a3540bda5f2d349f44bf0aac9c763` |
| S100SVG.xsd | 11,070 | `b2a77892d883a741efe48dd6f0ab9ffd7d1bea6e1d3c15ab1d5636ded4acd97d` |
| S100SVGMeta.xsd | 3,154 | `75f6663d691bf889997aaf5701051fc6f02f9fa3633db4bceb5930f3422bce16` |
| S100SymbolDefinition.xsd | 55,317 | `540ce723be4bf0d46ea68cfeb06255b8004d878a549d96090738d4420d87dbab` |

## `dev/spec-sources/s-100-xsd/S100/5.2.0/S100SE/20240415/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| Part15.xsd | 21,620 | `f43cd7e8d9758fbefc1f939967c6ed67e834225ea16da495d2995c1bdac8e01b` |

## `dev/spec-sources/s-100-xsd/S100/5.2.0/resources/Codelists/cat/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 68,678 | `8df0d0a62be97e634cd8303053b4136b210ae47a4766b70632f634a1793a97c8` |

## `dev/spec-sources/s-100-xsd/S100/5.2.0/resources/Codelists/gml/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| README.TXT | 47 | `2209cb2e059812f18e841f8d20bf9ef11c8bafb8686f69ceec2ca74a3c389bd4` |

## `dev/spec-sources/s-100-xsd/codelist-schema/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100CSL.xsd | 11,642 | `a7f43222e9caac51ed185d61d006f5648fe27bb924468d9cd1ac0eca706b85f2` |

## `dev/spec-sources/s-100-xsd/codelists/cat/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| codelists.xml | 68,678 | `8df0d0a62be97e634cd8303053b4136b210ae47a4766b70632f634a1793a97c8` |

## `dev/spec-sources/s-100-xsd/codelists/gml/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| README.TXT | 47 | `2209cb2e059812f18e841f8d20bf9ef11c8bafb8686f69ceec2ca74a3c389bd4` |

## `dev/spec-sources/s-100-xsd/exchange-catalogue/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ISOTS19139A1Constraints_v1.4.sch | 35,744 | `5beb6692e087609fd1afc30ebc8cd638d8b03be283211bab7df7af16410e2e3b` |
| S100_ExchangeCatalogue.xsd | 59,390 | `6687f9463be98a42a4af1e22428f491adca82d544da4a9244f97260a30884e5d` |
| S100_XC.sch | 25,047 | `a91d0edbad2720de90889b8224af7bbfa5c0f6a036076cc264559dbe5910160d` |

## `dev/spec-sources/s-100-xsd/exchange-catalogue/legacy-5.0.0/` (4 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| maintenance.xsd | 4,017 | `22e06f46e9de194d0fb5b66661e101b28e52a137bb4851b9988ecc06e354c734` |
| mmi.xsd | 784 | `d65775aa199eb44ae50ee20f3b8097d7638a24f0e44247c709df3461500d9ba5` |
| s100mds.xsd | 4,853 | `65782f452c22c6b9a7baf96a1d162e0963ddfb08d4b42b8a38c67be48f1e61ab` |
| serviceIdentification.xsd | 5,802 | `3c99bc9919552adda821aea972ad791421b52cb8044f1eb53805f4fd25e9ad3a` |

## `dev/spec-sources/s-100-xsd/feature-catalogue/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100_FC.sch | 17,410 | `c59e521dce819954270e4cbcc826eece80d002aea7c704cfe30e86a386fc06e7` |

## `dev/spec-sources/s-100-xsd/feature-catalogue/legacy-5.0.0/` (4 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100Base.xsd | 7,811 | `181378d88ffc21fb2e9d6dcf6669708713c7a6aea6e0ef34161868db84ffb0c8` |
| S100CD.xsd | 12,663 | `e84e8ae1c056d08e1fe177c73d616e8e0f0a136bef950476ff23b526953ac05e` |
| S100CI.xsd | 47,160 | `47d1c7690db2536649309174c8d2b9b05cff713c8a6d038a20311e8186aeb373` |
| S100FC.xsd | 30,308 | `37dffd3b6345e3e3136102969c49651fd0244900b97da5e0c6b197c6feb47db9` |

## `dev/spec-sources/s-100-xsd/gml-profile/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100_gmlProfile.xsd | 77,689 | `7a7a3ae69bdfbf095701e78a100cb5544b6c82dbc3eab6e9f45fc3a84c455163` |
| S100_gmlProfileLevels.xsd | 3,398 | `a6602346c05212d8598e9bc96d31d7b1d8db5af4a8f496fff17347348fe3b930` |
| s100gmlbase.xsd | 43,000 | `d73af785782498434cb398b519f86812dae12dfb672b9d133583daac63b0fe10` |

## `dev/spec-sources/s-100-xsd/information-catalogue/` (2 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100_IC.sch | 7,039 | `16c3c98624a01b37b29bcf47966e4ebe52d17b5029cdcb93f9b01969bbe593a6` |
| S100_IC.xsd | 30,962 | `e8ae2abe5b8990ca138930ad78f3be3472ed3959d721d2dd86b4e6dc58d57357` |

## `dev/spec-sources/s-100-xsd/logical-application/20220331/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| multi_language_support.xsd | 8,423 | `7068c2adba7efb83fdd6ff9e4e0ef22c2b93097df627110175157ac387040dfb` |

## `dev/spec-sources/s-100-xsd/logical-application/20220728/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| multi_language_support.xsd | 8,537 | `ddf4cdfe2b4b00e5b2e053c471306a283396b8bd1c5576585b0e7d5b5a8cbe1a` |

## `dev/spec-sources/s-100-xsd/portrayal-catalogue/` (9 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100AlertCatalog.xsd | 16,922 | `6677cf6094bdf17109a5e3aedc401d3be5695a295b39ad1ec386a562f7f4ba80` |
| S100AreaFill.xsd | 3,431 | `da8ca823907fcbf853ea330bd1eef24feec4d5ad13d6f2a502d302d9c03c16c6` |
| S100LineStyle.xsd | 3,278 | `e4260d2062c6f4e9bbb78e3478f5ec8b24b24cdc269e41f1e9ca2dbe1b8b6903` |
| S100Pixmap.xsd | 5,095 | `0d1f1aeac9791247d737bb523bd707cec5e612a1ab57561fb9aa74c4f2c7352b` |
| S100PortrayalCatalog.xsd | 27,967 | `9c58b1c4f53bb7d1519a08a93e321e01daae480b1a135091bee8a8bdee713f92` |
| S100Presentation.xsd | 18,756 | `91a539dde69cead9b6b9f097e67f107d8e3a3540bda5f2d349f44bf0aac9c763` |
| S100SVG.xsd | 11,070 | `b2a77892d883a741efe48dd6f0ab9ffd7d1bea6e1d3c15ab1d5636ded4acd97d` |
| S100SVGMeta.xsd | 3,154 | `75f6663d691bf889997aaf5701051fc6f02f9fa3633db4bceb5930f3422bce16` |
| S100SymbolDefinition.xsd | 55,317 | `540ce723be4bf0d46ea68cfeb06255b8004d878a549d96090738d4420d87dbab` |

## `dev/spec-sources/s-100-xsd/portrayal-catalogue/legacy-5.0.0/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S100BaseModel.xsd | 12,142 | `e34d841c0b1d3d490a7ed980b2f84070abd0386be0314e3881865537b421e774` |
| S100ColorProfile.xsd | 6,378 | `05291ad0cfd04d9cd76a916aae2179a79111cc5ac1a4b7d78560e31662067e4b` |
| S100SVG1.xsd | 2,918 | `f26c73033e57c898c7081377473e08bc5ce383ddef80201acda5856f858a51cf` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| OGC_LICENCE.TXT | 15,254 | `5536c203639ae6b9ac97c1de891cb7a707700c1b0bb220af54336b36d887383d` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/gml/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 5,138 | `5704e231833f53db77120289a42f7280a30dd71692a04ecf1a75500132621cda` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/gml/3.2.1/` (32 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| SchematronConstraints.xml | 5,552 | `ed6698d09477a0d956a4ad242db3791046fcf21d28541443763b7c564b8c4f74` |
| basicTypes.xsd | 14,894 | `66d64862f65a8bd877f111845412df4bd24b14167dd13656002ec9981ad2da72` |
| coordinateOperations.xsd | 33,333 | `7d4a38dc37aceac1a8cffd44fa9e536623056e7e667f0067390c8b51210e42e1` |
| coordinateReferenceSystems.xsd | 18,409 | `4ea24d2fea10b07304de9619797159c215c01503f4c5cbd547a63504e24b5236` |
| coordinateSystems.xsd | 18,690 | `bebce49b8a3e112accd2a8ecd9bbc8980d0042dadc1b74efa059d0140c1cfd1e` |
| coverage.xsd | 20,816 | `3c1b0306a16bfbbe9a796148d36ea4faed0b8acb165c5242eb1f1caa9c4aae18` |
| datums.xsd | 15,912 | `1a1829ecf0f3cdceea38a90fa3d1d18aa9036a424fdac14873a489c54f22baed` |
| defaultStyle.xsd | 19,374 | `a62c2047f1a33505b43f4d75452fd297aaecfc6bc7a2c73a7f93c3893d07c7a6` |
| deprecatedTypes.xsd | 34,663 | `9be6206a496428c62f14834826cc2ee7c3da84051874afeedd459e04d0b409cd` |
| dictionary.xsd | 7,126 | `9695905cc674f6799b33c9846c42b063c90fa27c40b9f0ef0ae607f7fcfe8c84` |
| direction.xsd | 4,150 | `19761fcbccb1ad7b2d0d9d820af19d4ed33de823a65edaafc1ded623045ab986` |
| dynamicFeature.xsd | 6,796 | `2c4f365c226f0ae7c70c498eb258f6db6f9669fdf6b05d26135888be1b7f5f42` |
| feature.xsd | 5,573 | `fd37ae133fd8ae6501c4ee6a47c964646a5a5d8ef234fe5b4a78d35a66f4e34c` |
| geometryAggregates.xsd | 11,512 | `e863a94c0d18274c791a66ae0a7931713a00f9e112f1be930d10b41d155115da` |
| geometryBasic0d1d.xsd | 18,918 | `f121d01bc9fddf0c7a9203445344b901839645d21d0fb4e7371c1db182d0a46d` |
| geometryBasic2d.xsd | 6,514 | `48d54f181173ff227fe706ab6886623d2c012f001a445e5de75732d71a508039` |
| geometryComplexes.xsd | 5,813 | `c05e013423560ec3fd8e2b9719d2d76a315cc6f29cdf353d82bfb1502f2d01d4` |
| geometryPrimitives.xsd | 42,528 | `f037b5819cc4feea4e2942a047dc4cb7837c10a6ce7ab871d1feba122195fa01` |
| gml.xsd | 1,065 | `2edff80d73b7a7c40b37d70744b92edd27c58fb243098deba1e42437f259df94` |
| gmlBase.xsd | 12,760 | `ef4fdffe24702716acbbf1056ec234cc419ef3933a4d08c8aae1ac9a56b67b95` |
| gml_32_geometries.rdf | 13,659 | `e203bae3295172e3e85e9cebed777a792f046811e1f9a888c1498fb3beceb917` |
| gml_3_2_1-ReadMe.txt | 2,437 | `7ee2984abe236be048d3883a1d28cc064d66427959aac65ead6aec6663a9d7ed` |
| grids.xsd | 4,121 | `6c65245aeef0a01c363344a8a58bf21c253468fa0d6d025159bcad74430a3eb6` |
| measures.xsd | 3,093 | `02d9b98b945b2b42fce8b4143af9278c6460cc1ea361dc38a571465bd684725d` |
| observation.xsd | 5,519 | `6f47fdfc4bf883e64fce4085a27a292f24f4dcd88480cb1825b19a5fddc034a3` |
| referenceSystems.xsd | 4,669 | `7b2218695020cc8a5ef009486d85e6738f90f99baf48ced1f7491f048cb70d72` |
| temporal.xsd | 15,587 | `f465ee38c1bebaac5c939cc9e37d0a404ef54828e748b4e74e10e11a5b158f97` |
| temporalReferenceSystems.xsd | 12,668 | `39ca20c93bf41130fb3b0a07902adc9cc36b2039a3a0b49140106e88596b2d05` |
| temporalTopology.xsd | 7,784 | `a9395fe5764d6a58e27bfc267e12ee66a3ae7bd682c2d63bcfa989d6108f052e` |
| topology.xsd | 22,779 | `37f6e0cfe8d91c5be0b078467daf7c0f8eca9c6a63cedce18b2b60d16b5ed142` |
| units.xsd | 12,272 | `7d42dfce5451bc8c379e7935a41b3941b70c063eef08b58ca6a1c51b4e210a0b` |
| valueObjects.xsd | 11,427 | `7a89532a885b5d17cf5123a0808230ca7945e791cf953e86eca8e3a85d496f86` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 1,253 | `115fa0f332bb85be932c5b9aea80f3660053d094ca6f6af9e090b3509dd5abfa` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/gco/` (4 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,293 | `7f71059a833e4c1e8c280fa7443216ed913001d0b15dff6a7ea3ca8d8fa1f0df` |
| basicTypes.xsd | 22,050 | `5ac7545eedc0ebea9ee2788197ffc54eb32797cfde015239f33400f8527ff7f4` |
| gco.xsd | 1,159 | `bc3ea300204f6b99e696976aeb32207d604295f8e4c1d397cf5bb7b9e59bdabf` |
| gcoBase.xsd | 4,087 | `bc6ef613238a37d0cfcdcbb43df751de7c81ebe46e67b185bae477f530b3f9ab` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/gmd/` (18 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,138 | `b7d7c0532b64dd7a80f2fcf3498914dee8563c54d2a465d0dd8339b2939595ee` |
| applicationSchema.xsd | 3,188 | `bd5b9f294f42dbe0d78e7f760fae008fb061c8a23d6c45b34bef0bf1427b1ed5` |
| citation.xsd | 15,521 | `dfdef7355c21e8780cb3d50b28dd6d4c556ef83a1082c3059fffe41e357ba97d` |
| constraints.xsd | 6,555 | `b1f9c2971bbd1bf641f23a82ec87c0728bc19446b86ad490b5d3e917b096193e` |
| content.xsd | 11,423 | `e2c31ad9e56c6682f137b200db430b11ea89ee667379615c6498c4267c129eda` |
| dataQuality.xsd | 30,936 | `a1c97293e7966bf67ad4635894a5479c3e3f7044ad6253d3e87b74b3c34739cb` |
| distribution.xsd | 11,736 | `1759a0d820644e07ed442b8385a87585cf62c68a7a257dcff109fb469109bb28` |
| extent.xsd | 11,372 | `a1e35e7730774fd7c4229699ade5cd29a8449997452d6a017f8a797f2a0a8c41` |
| freeText.xsd | 7,160 | `79fcacb8fe5d0000fce05bef5e6430c61af9c151edf50542de4f4d90f4d1d306` |
| gmd.xsd | 1,170 | `62c01b7ac3a6d283a2ea4ac72891bc1b912ff43016367b8df30ec7a8dfa583b1` |
| identification.xsd | 19,751 | `a9cbc54f0774b804a7e49e0713502d49ed051e2ad43d138b7ba840b7868ea937` |
| maintenance.xsd | 6,026 | `49e16597d6ce1bf039db46ac6d4c0069b2c6297bfc8da3fdb28a4d2e717766f9` |
| metadataApplication.xsd | 9,332 | `215e4f0e39b73c98c30e2c799b3c47448b420b481bed91087f983faf42074b6c` |
| metadataEntity.xsd | 5,877 | `e780e56e534c58140df94625293f535827b966a662b01014802288c349f31a3a` |
| metadataExtension.xsd | 6,429 | `2a59d200fbd0cf1229f908fa5ddfee71c7b2be273d6f2d9402e386390e2d1012` |
| portrayalCatalogue.xsd | 2,664 | `e8b1086c78ef4474be9091839d3fa9aee3d9481c465fe5aa4372e2e2d3c2090a` |
| referenceSystem.xsd | 5,723 | `320bf5301f0fc40fc028a5428133ee66ed2b5b99ea5b74544ebf0642a1083f06` |
| spatialRepresentation.xsd | 13,926 | `3e4d2886b7816e1bc67fa23d82201e473162c5110aa6e6bd34478ad606c0b73c` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/gmx/` (8 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,279 | `cdca86834c3d280c8f63798cf56a06d8a0b369eae2cdf71b081e0fb7b272b498` |
| catalogues.xsd | 7,244 | `692ce4027255fe9b0955ad6551258b978ce1454756aef351911622acd31891b1` |
| codelistItem.xsd | 9,310 | `0031f74c26214203f366f6b9029473397d7de66e92b600903049cdd2c36bc3d9` |
| crsItem.xsd | 49,931 | `c3909a0a8f259f817f530703d51b76f6ddd4e84e82f0dafe98b97ede75718d35` |
| extendedTypes.xsd | 4,608 | `d4edf77dad90cdce549e3d47e6128d0124c65bb8dfb72302e60e1c904f918c9b` |
| gmx.xsd | 1,143 | `fbcacc647e177d02acb3efb98ec5684c1ea85d909a9bbff6175bc27a681d7ba8` |
| gmxUsage.xsd | 7,318 | `a50d91c32491cdbefc67c4d466a66742a95dbffbfb2dece6284d1816c5ff505e` |
| uomItem.xsd | 9,004 | `543a3d882015b025c3b7fff076c542e359d36105fd9b0ada20d1e10f992f325c` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/gsr/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,149 | `c996e5f4aaffa4343020c14f4538ca746aaf1b56809908b85f15d0d83eb8e908` |
| gsr.xsd | 1,180 | `5066cfe4d0488b89cf7a15a990cd2e05f3dcdbb11c95df1ec73a1e714101161d` |
| spatialReferencing.xsd | 2,166 | `19dcdbf1fcc296598dd5def55338bdf604e2ddd62358f7a3a9caa62bd7a6833b` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/gss/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,146 | `64e13d0624800a9595ffde07434d47554ea3d67645a72a28508c5859a0e80ce4` |
| geometry.xsd | 2,700 | `fabf3df4d5d7098944494e4932426e4bfd7d56d73ac535edfcf5ef67292ad767` |
| gss.xsd | 1,166 | `1cb5492d7cb110ced0d46e8bc858dc3b340e1350b0b16f99772318c7df4d3906` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/gts/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 2,143 | `095c8e505f07842ac8a4bf0b6c19a2686919a13a6d63f0410431a360635dc0af` |
| gts.xsd | 1,173 | `bef7c0ed6e63cd2be4b54defe994125783491a4a750c675cd28ca01382c9b273` |
| temporalObjects.xsd | 2,787 | `22d2c593d31cd6c91e245bebd44240bd89046cc45c8e7f3a79b22442d9ee2595` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/resources/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 719 | `965ba566a8f00a1450511f230f028b914998320fd68dc3dd79d4d7b552ea666c` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/resources/codelist/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ML_gmxCodelists.xml | 43,856 | `b951ab1dd33cf2af2f913d9c761224644c088766b7cebba4c5f5d0441f50dcf7` |
| gmxCodelists.xml | 95,237 | `40b2bf5744027a86a8fb5e949064457f3fa8bd2485b33799be2adfa6c2918675` |
| tcCodelists.xml | 3,574 | `7f2364d2a7b205f4d324f52cbae9b5a18d7ba25f126b33ddabe0f7ca8f249190` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/resources/crs/` (2 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ML_gmxCrs.xml | 8,362 | `73e4eff354b5c69a3f884771ca2fb9f4ca70fc4c63846e97b5cd43d95452827f` |
| gmxCrs.xml | 14,953 | `6f8d6893046dff3407279daa5f863bea8f82915bb80fda023cc940ab56980b92` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/resources/example/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| fr-fr.xml | 3,651 | `fc411c34429b31e2e74139a99ce6c22e89285eacb51d5d6554bbe4ed26e7415f` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/resources/uom/` (2 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ML_gmxUom.xml | 6,911 | `8dfccdad9502ed9854a4c10fb66ebe4a2a57e4f5e82af8971319d3d07bb4a208` |
| gmxUom.xml | 3,580 | `55bb6bf0cde17d5f8a5ed23345191c24c947e749e632970fc6094385d7e51d4e` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/srv/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| ReadMe.txt | 1,616 | `ebf109acde473ef6c32093c26d47ad6505ea4ee34d57b0bd6f1261e214d671cb` |

## `dev/spec-sources/s-100-xsd/schemas.opengis.net/iso/19139/20070417/srv/1.0/` (3 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| serviceMetadata.xsd | 14,070 | `07f9c0c53406242a72a553db5d377a9f73802c9baac082a234ce4ea41c381395` |
| serviceModel.xsd | 13,218 | `7d90b28c1cfc06475e46e3c9242edc6136a4a730e3c6012fe149810ecb8571a3` |
| srv.xsd | 1,941 | `ddda752cbd7ddf2dbac0c17b523ed154d3723bc822d36c6bebccf334678ed92a` |

## `dev/spec-sources/s-100-xsd/security/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| Part15.xsd | 21,620 | `f43cd7e8d9758fbefc1f939967c6ed67e834225ea16da495d2995c1bdac8e01b` |

## `dev/spec-sources/s-100-xsd/xml-catalog/` (1 files)

Obtain from: IHO S-100 Ed 5.2.0 schema package (GML profile, exchange, feature and information catalogues, codelists, the ISO 19139 codelists it imports): the IHO Geospatial Information Registry <https://registry.iho.int>. The package's own README and licence files are listed with it.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| XMLCatalog.xml | 4,338 | `3f60a2cdcad22bb9d4bdeed829346a8a52a012cc95db5fb008f3552f6e2e04fa` |

## `dev/spec-sources/s-158/` (12 files)

Obtain from: IHO S-158 validation-check publications and check tables: <https://iho.int> (S-158 series) and the S-100 Validation Checks working repository <https://github.com/iho-ohi/S-100-Validation-Checks>.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| (KRISO) Data Validation.pdf | 275,502 | `b6bf178193fcaf5cbc08020da43b2de8d66632fda07fa9c1ae6bfbc2b3ee0351` |
| S-158-101_Validation_Checks_Ed_1.0.0.xlsx | 118,490 | `9e1a6392c087cf34b05752c2a78b4bc055161904ea9cf10ab09195c6e1145553` |
| S-158-102_Validation_Checks_Ed_1.0.0.xlsx | 40,943 | `3a57f7d567ab74f4ad0f84d31b066b40505f0bba0dbd98ac92c14d3a80b0ea4f` |
| S-158_100_1_0_0_20250224.xlsx | 66,850 | `5ada6c451653572258da3926a663353d355157c3f94b5ddcac998c372c91b310` |
| S-158_100_Universal_Hydrographic_Data_Model_Validation_Checks_Ed_1.0.0.pdf | 405,203 | `a624d7b02b48bb9cd9589bc3b50b8e3a656101c6b712b9fad8659f40ed53157f` |
| S-158_101_ENC_Validation_Checks_Introduction_Ed 1.0.0.pdf | 374,842 | `d68044776732943d4ddc622dc949d14371bf96545a505b8c7315689e0d0d806c` |
| S-158_102_ENC_Validation_Checks_Introduction_Ed 1.0.0.pdf | 409,990 | `6db2944c3da8e6661be39e0179669705e5430e3aa7268bf34bce1dd0877b34ff` |
| S-158_130_1_1_0_20251031.xlsx | 40,383 | `ffbf3f886a0631d822b3e4d9fc5f0739b0996804fc20593039198f033add04e2` |
| S-158_130_Polygonal_Demarcations_of_Global_Sea_AreasValidation_Checks_Introduction_Ed_1.1.0.pdf | 389,319 | `e8f6cdff1941ec3c4039a59bea638b6624521f3588f0e8aadbad997fa938c760` |
| S-158_98_1_0_0_20250224.xlsx | 42,465 | `d30d0b735b52286ab543a4523c318aecb16a29859ebb369d7a8b21184aa94b46` |
| S-158_98_Data_Product_Interoperability_Validation_Checks_Introduction_Ed_1.0.0.pdf | 428,747 | `dc4223441f8bebf2fe068210080483b224552b9a3ce3980710bcc1b4fd72787b` |
| S-158_Validation_Checks_Introduction_and_Structure_Ed_1.0.0.pdf | 795,954 | `e228594612b4c8ae11f13f54c54c4b762d9657c45d2fb18925581014c18e78ae` |

## `dev/spec-sources/s-201-xsd/` (2 files)

Obtain from: IALA S-201 Ed 1.1.0 Annex B1 data-product-format schema: <https://www.iala.int> and the IHO Geospatial Information Registry <https://registry.iho.int>.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| S-201_Ed1.1.0_Annex_B1_DataProductFormatSchemas.xsd | 434,822 | `4d2d7310e6db99400de2c14656a7762ac834f6417fe256c8058ceadcb44a2d4d` |
| S-201_Ed1.1.0_Annex_B2_DataProductFormatSchemas_Document.docx | 2,825,696 | `53a84bede2648ecd18b37f3b0123d8db8229b370433dbdf89e7a58685f2dbb17` |

## `dev/spec-sources/w3c-xsd/` (3 files)

Obtain from: W3C `xml.xsd` and `xlink.xsd`: <https://www.w3.org/2001/xml.xsd>, <https://www.w3.org/1999/xlink.xsd> (W3C software and document licence, LICENCE.TXT listed below).

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| LICENCE.TXT | 2,526 | `0787a37000cfa7310803c0a160e0c19d0f234d6b5d25f3085fd2a5b4975171e4` |
| xlink.xsd | 9,093 | `4dfb09c21df578c1699e231d8b5a44ae6de2dac1645a2c834197c7d89532c834` |
| xml.xsd | 11,374 | `0853f3f40a4eb194e4705659f2868810fcd0a03c767e9db6d656d27722d19ca3` |

## `dev/tmp_verify_imgs/` (8 files)

Obtain from: Courseware-derived verification scratch; not a source.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| _g_mechanics.txt | 8,762 | `ce6dc33fa239ab83d59642fe7efc274d22012919e846beea6445f8c5b8b54f06` |
| _g_symbols.txt | 9,294 | `c31bc0d08bc773eeb4346e9a685e43b8568b3c9e7240b5b5ec1d99ffa54a89ae` |
| day3p8_0_Image83.jpg | 366,138 | `f93ab20cc882328a632ac3bd7ff32c0263df461ca71d4f654ec92f631954da8f` |
| day4p13_0_Image70.jpg | 52,702 | `c8f4b0f1211f6380173eef02cbd06f65f92dbf288ea9ce01d5680d5406098272` |
| day4p13_1_Image71.png | 2,360 | `8f5e44e596b6644e81942e31aa2fe6fb225428af35e0a0b4d2b01b8adf0366da` |
| day4p13_2_Image73.jpg | 124,146 | `214aa1923d0adb029a9da4da6430c6d868659b09fe9e52e1a61a7febae7886ec` |
| day4p13_3_Image74.png | 1,735 | `e29817f0969638e3677d19362bbe46d16991c755b11a5ccde199f8a4141f13f1` |
| day4p13_4_Image76.png | 199,386 | `20773e40dd8922d8693837c95b36c093fa26213fb7ec5fb103bc6ae2b6cf092f` |

---

**Total: 835 files, 126,041,876 bytes.** Regenerate this manifest with `python dev/scripts/generate-spec-sources-manifest.py` whenever a file under these folders is added, replaced or removed.
