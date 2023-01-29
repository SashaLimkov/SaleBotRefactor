"""Инициализирует все необходимые компоненты бота"""
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from pyrogram import Client
import pyrogram

from core import settings

API_ID = 27325512
API_HASH = "9ac037990583f0f80406cdfb62ef92c5"
pyrogram = Client("maryia2", API_ID, API_HASH, parse_mode=pyrogram.enums.ParseMode.HTML)

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
storage = JSONStorage(f'{Path.cwd()}/{"fsm_data.json"}')
dp = Dispatcher(bot, storage=storage)
all_users = {
    878849282: 974,
    925173547: 21,
    1998290591: 0,
    1271488810: 21,
    384781475: 55,
    955038431: 25,
    1723884169: 0,
    381247707: 4,
    972333380: 21,
    833510785: 0,
    544032510: 0,
    792817144: 3,
    597523009: 41,
    541218313: 3,
    359894143: 5,
    5178109399: 0,
    549828043: 0,
    5557454676: 66,
    1088768435: 4,
    677564653: 63,
    1585871690: 0,
    1355263614: 12,
    282475273: 23,
    506991649: 2,
    917350852: 0,
    1372700543: 21,
    1001201519: 84,
    1278592948: 0,
    1341325974: 0,
    5096707931: 0,
    638257606: 0,
    1600729304: 51,
    884725943: 0,
    463117267: 0,
    527737890: 0,
    639679112: 0,
    5208805131: 21,
    410406132: 0,
    674697924: 25,
    1348771193: 0,
    1354186174: 25,
    1019792241: 59,
    556963108: 81,
    541463414: 9,
    5521651393: 0,
    220164566: 41,
    1235266976: 0,
    1030607056: 5,
    376514116: 954,
    1035093682: 25,
    484278530: 82,
    394251572: 51,
    815651680: 0,
    431544305: 71,
    592102104: 4,
    1776748725: 0,
    827707915: 0,
    320481228: 1,
    324998402: 0,
    384369235: 7,
    475036682: 0,
    440803406: 0,
    2015865780: 0,
    390959255: 806,
    693334372: 0,
    277393634: 64,
    526382906: 36,
    1125641966: 0,
    425138470: 21,
    5569743952: 25,
    1038795158: 84,
    1846473481: 0,
    303526035: 0,
    232982980: 53,
    378498610: 36,
    892324107: 0,
    569993217: 18,
    392459647: 3,
    2108204303: 7,
    1073852406: 29,
    245446557: 0,
    509967157: 0,
    373971927: 81,
    142664249: 11,
    251385630: 17,
    836531721: 0,
    1163066314: 0,
    1045170793: 0,
    1006331940: 3,
    367848386: 17,
    943862940: 0,
    680983628: 21,
    398420982: 49,
    1227397664: 0,
    875566746: 59,
    5024081326: 0,
    1255991463: 0,
    1086236048: 0,
    1531054004: 2,
    1305787576: 12,
    888139493: 0,
    1111533987: 21,
    5372572345: 4,
    2052269006: 13,
    1274019370: 0,
    1059933562: 0,
    1888121645: 0,
    755766441: 41,
    119855329: 1,
    1902485394: 4,
    398019953: 0,
    722521634: 0,
    519881679: 0,
    451705776: 948,
    389128508: 0,
    545496867: 0,
    945504115: 3,
    1644093138: 0,
    712718882: 13,
    5348743153: 0,
    612780121: 0,
    989375571: 0,
    378240838: 1,
    293847991: 25,
    625742104: 2,
    767144125: 0,
    1174365434: 22,
    361432834: 27,
    728794607: 0,
    289225849: 27,
    851578703: 0,
    655967127: 6,
    1170116207: 0,
    1262101155: 0,
    835880401: 50,
    696363570: 0,
    629017286: 0,
    1191363595: 87,
    303317193: 87,
    972741746: 0,
    945440018: 87,
    999689807: 0,
    1484061177: 0,
    1846204030: 26,
    968784177: 0,
    335694535: 0,
    926116603: 12,
    538952422: 0,
    525989464: 0,
    5221369550: 0,
    760127: 0,
    922903946: 28,
    5493233063: 0,
    966732541: 0,
    384115924: 0,
    1176299598: 0,
    5608293604: 0,
    349649949: 0,
    1333284026: 0,
    734682326: 3,
    388133695: 28,
    876725468: 0,
    1702807065: 1,
    1050212282: 0,
    81351325: 22,
    1302467907: 0,
    718740021: 29,
    150486206: 0,
    130249950: 0,
    323470085: 29,
    423668207: 3,
    576965421: 0,
    684961476: 0,
    472331295: 0,
    883097234: 0,
    1117843463: 0,
    764363090: 25,
    439913678: 0,
    301564787: 0,
    149254611: 0,
    57303626: 0,
    206986025: 0,
    1280732115: 0,
    390485107: 0,
    361031475: 0,
    1043094716: 0,
    522813418: 0,
    1148754283: 0,
    564355124: 27,
    871194270: 60,
    887339615: 1,
    899582076: 27,
    1107055655: 0,
    972952241: 0,
    342961626: 25,
    843646445: 0,
    1060929275: 1,
    136540331: 28,
    848351294: 5,
    1661233713: 0,
    525896151: 0,
    1020892136: 1,
    450317017: 1,
    916443034: 0,
    1873328868: 1,
    2088503450: 0,
    841940435: 1,
    364206312: 61,
    391028284: 0,
    5720248681: 0,
    1001805173: 0,
    1278939458: 0,
    5169859077: 0,
    705812435: 0,
    587377129: 2,
    428225529: 0,
    723528682: 0,
    248106764: 0,
    1333853388: 3,
    395199173: 0,
    1363126387: 0,
    544508725: 0,
    846984764: 0,
    1141336018: 2,
    1364361255: 0,
    448559711: 2,
    874234511: 2,
    320810355: 0,
    549332009: 17,
    892518305: 0,
    769082915: 58,
    1029404407: 0,
    1479178173: 0,
    163663259: 3,
    5248078715: 3,
    491874539: 18,
    793407201: 4,
    485221265: 0,
    1487904018: 0,
    1018193212: 0,
    1278396077: 0,
    740871541: 0,
    727901374: 0,
    714355604: 0,
    482588378: 4,
    334407459: 5,
    652625174: 0,
    1354916591: 0,
    385263178: 1,
    801306784: 0,
    1400916023: 0,
    1137183301: 60,
    1627395635: 0,
    471716840: 13,
    1933819575: 0,
    1311088539: 0,
    898041860: 0,
    738763563: 0,
    1078598814: 0,
    5796698376: 0,
    2017661847: 0,
    491849194: 2,
    834846800: 6,
    730461508: 5,
    431554181: 0,
    765789176: 0,
    5439188679: 0,
    2084703529: 0,
    508336199: 0,
    1175667415: 0,
    1328001127: 7,
    1954608985: 0,
    5177760097: 4,
    273296846: 0,
    1233347309: 4,
    1280178074: 0,
    371203608: 0,
    175251098: 0,
    715443213: 0,
    1570625393: 0,
    499967169: 11,
    962011938: 0,
    325503251: 12,
    5599448592: 10,
    882838975: 23,
    889112666: 0,
    864610722: 0,
    1098455849: 6,
    1136938146: 0,
    1509245614: 0,
    723599346: 0,
    168371123: 0,
    548785081: 9,
    1173764692: 10,
    205870713: 21,
    663104370: 14,
    328724155: 0,
    861277069: 0,
    515891088: 74,
    535686630: 0,
    5736296669: 87,
    201509454: 0,
    292486321: 0,
    703481080: 0,
    1804761174: 0,
    1748297660: 0,
    860445406: 0,
    5325426124: 0,
    441738785: 0,
    731508344: 0,
    1050791658: 17,
    427157479: 0,
    1640369829: 0,
    898173264: 0,
    671192327: 0,
    738724470: 0,
    263099518: 0,
    297983232: 0,
    656112382: 18,
    754239889: 1,
    5347351754: 0,
    901570142: 0,
    354521735: 0,
    909840949: 0,
    1030873686: 18,
    1959458346: 0,
    150984599: 78,
    914623936: 20,
    1388393231: 78,
    1051603973: 21,
    537965532: 0,
    919187809: 0,
    590450575: 21,
    443098688: 0,
    5172020006: 0,
    287484041: 0,
    937246563: 0,
    297955574: 0,
    1151281801: 0,
    2123054687: 0,
    544510368: 0,
    284548139: 0,
    638951043: 0,
    21242242: 0,
    1002311954: 0,
    1055165439: 0,
    5167135284: 0,
    340490146: 0,
    917695152: 22,
    400872753: 0,
    673058546: 0,
    1321431829: 0,
    965277142: 0,
    1607205597: 0,
    1918754406: 0,
    915106819: 0,
    1060496138: 0,
    455958865: 0,
    149943334: 0,
    5819054629: 84,
    225788801: 0,
    841969921: 0,
    568002388: 0,
    643446220: 0,
    553979900: 0,
    2083888251: 0,
    438562645: 0,
    802885842: 0,
    400412720: 28,
    932591272: 0,
    1281416082: 0,
    1763136405: 0,
    386515723: 27,
    1220424586: 0,
    745666348: 86,
    791451271: 0,
    694277889: 2,
    2034700772: 0,
    1480232494: 27,
    180717501: 0,
    471364890: 1,
    276611590: 3,
}

helper_inviter = {
    1388393231: 150984599,
    5736296669: 150984599,
    754239889: 119855329,
    887339615: 119855329,
    378240838: 899582076,
    769082915: 871194270,
    764363090: 342961626,
    564355124: 289225849,
    423668207: 1006331940,
    945440018: 303317193,
    451705776: 376514116,
    1902485394: 5372572345,
    330759037: 755766441,
    5178109399: 1888121645,
    875566746: 1019792241,
}
