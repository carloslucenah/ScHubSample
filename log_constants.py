# OVG

OVG_INFO_RECEIVED_OVTP_CONST = "<OVTPTemplateConsumer> INFO received"
OVG_INFO_HEADER_PARSED_VALUES_CONST_3 = " <HeaderParserOriginal> INFO header parsed values for .+?:([a-z0-9]+) are"
OVG_MESSAGE_PROCESSED_OK = "message processed ok "

OVG_MESSAGE_TYPE_TAG = "msg.DocumentType=(.+?),"
OVG_MESSAGE_HEADERHASH_TAG = "msg.headerHash=(.+?),"
OVG_MESSAGE_DISCIPLINE_TAG = "msg.Discipline=(.+?),"

OVG_allowed_lines = list()
OVG_allowed_lines.append(OVG_INFO_HEADER_PARSED_VALUES_CONST_3)
OVG_allowed_lines.append(OVG_INFO_RECEIVED_OVTP_CONST)
OVG_allowed_lines.append(OVG_MESSAGE_PROCESSED_OK)


# CEG

CEG_INFO_RECEIVED_OVTP_CONST = "OVTPTemplateConsumer> INFO received"
CEG_INFO_HEADER_PARSED_VALUES_CONST_3 = "HeaderParserOriginal> INFO header parsed values for .+?:([a-z0-9]+) are"
CEG_MESSAGE_PROCESSED_OK = "message processed ok"

CEG_MESSAGE_TYPE_TAG = "msg.DocumentType=(.+?),"
CEG_MESSAGE_HEADERHASH_TAG = "msg.headerHash=(.+?),"
CEG_MESSAGE_DISCIPLINE_TAG = "msg.Discipline=(.+?),"

CEG_allowed_lines = list()
CEG_allowed_lines.append(CEG_INFO_HEADER_PARSED_VALUES_CONST_3)
CEG_allowed_lines.append(CEG_INFO_RECEIVED_OVTP_CONST)
CEG_allowed_lines.append(CEG_MESSAGE_PROCESSED_OK)

# MOP
# Cambiada etiqueta Tracking por TrackingData
# Le agrego el mensaje de recibido
MOP_MESSAGE_RECEIVED_CONST = ".\] <TrackingData> INFO Odf message received ([a-z0-9]+)"

# MOP_MESSAGE_PROCESSED_CONST_3 = "processor-.\] <Tracking> INFO  Odf message processed OK ([a-z0-9]+)"
MOP_MESSAGE_PROCESSED_CONST_3 = ".\] <TrackingData> INFO Odf message processed OK ([a-z0-9]+)"
MOP_MESSAGE_SKIPPED_CONST = ".\] <TrackingData> INFO Message skiped. Odf message ([a-z0-9]+)"
MOP_MESSAGE_ERROR_CONST = ".\] <TrackingData> ERROR Error processing odf message ([a-z0-9]+)"

# MOP_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST = "\[topic_processor.+?<HeaderParser> INFO header parsed values for.+?:([a-z0-9]+) are"
MOP_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST = " <XMLHeaderParser> INFO header parsed values for .+?:([a-z0-9]+) are"
MOP_TRANSACTION_ID = "processor-.\] <TxRedisHandler> INFO Transacction id: \[(MODELTRANSACTION.+?)\]  Message"

MOP_allowed_lines = list()
# Le agrego el mensaje de recibido
MOP_allowed_lines.append(MOP_MESSAGE_RECEIVED_CONST)

MOP_allowed_lines.append(MOP_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST)
MOP_allowed_lines.append(MOP_MESSAGE_PROCESSED_CONST_3)
MOP_allowed_lines.append(MOP_TRANSACTION_ID)

MOP_allowed_lines.append(MOP_MESSAGE_SKIPPED_CONST)
MOP_allowed_lines.append(MOP_MESSAGE_ERROR_CONST)



# MOP_CENTRAL
# Cambiada etiqueta Tracking por TrackingData
# Le agrego el mensaje de recibido
MOP_CENTRAL_MESSAGE_RECEIVED_CONST = "\] <TrackingData> INFO Odf message received ([a-z0-9]+)"

# MOP_CENTRAL_MESSAGE_PROCESSED_CONST_3 = "processor-.\] <Tracking> INFO  Odf message processed OK ([a-z0-9]+)"
MOP_CENTRAL_MESSAGE_PROCESSED_CONST_3 = "\] <TrackingData> INFO Odf message processed OK ([a-z0-9]+)"
MOP_CENTRAL_MESSAGE_SKIPPED_CONST = "\] <TrackingData> INFO Message skiped. Odf message ([a-z0-9]+)"
MOP_CENTRAL_MESSAGE_ERROR_CONST = "\] <TrackingData> ERROR Error processing odf message ([a-z0-9]+)"

# MOP_CENTRAL_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST = "\[topic_processor.+?<HeaderParser> INFO header parsed values for.+?:([a-z0-9]+) are"
MOP_CENTRAL_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST = "<XMLHeaderParser> INFO header parsed values for .+?:([a-z0-9]+) are"
MOP_CENTRAL_TRANSACTION_ID = "rocessor-.\] <TxRedisHandler> INFO Transacction id: \[(MODELTRANSACTION.+?)\]  Message"

MOP_CENTRAL_allowed_lines = list()
# Le agrego el mensaje de recibido
MOP_CENTRAL_allowed_lines.append(MOP_CENTRAL_MESSAGE_RECEIVED_CONST)

MOP_CENTRAL_allowed_lines.append(MOP_CENTRAL_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST)
MOP_CENTRAL_allowed_lines.append(MOP_CENTRAL_MESSAGE_PROCESSED_CONST_3)
MOP_CENTRAL_allowed_lines.append(MOP_CENTRAL_TRANSACTION_ID)

MOP_CENTRAL_allowed_lines.append(MOP_CENTRAL_MESSAGE_SKIPPED_CONST)
MOP_CENTRAL_allowed_lines.append(MOP_CENTRAL_MESSAGE_ERROR_CONST)

# CID_RT

# Cambiado en el processed Tracking por Trackingdata 
# Ahora se guarda la disciplina
CID_RT_INFO_RECEIVED_MODELTRANSACTION_CONST = "<Tracking> INFO MST \(\) \(\) \(\) \(\) \(\) \(\) \(\)  rt trx received MODELTRANSACTION"
CID_RT_INFO_PROCESSED_MODELTRANSACTION_CONST = "<Tracking> INFO MST \(\) \(\) \(\) \(\) \(\) \(\) \(\)  rt trx processed LOCKOG"
CID_RT_INFO_SENDING_PROJECT_GET_ID = "<route.+?> INFO sending project/discipline (.+?) to port .+? with trx id (.+?) and name (MODELTRANSACTION.+?)"

CID_RT_allowed_lines = list()
CID_RT_allowed_lines.append(CID_RT_INFO_RECEIVED_MODELTRANSACTION_CONST)
CID_RT_allowed_lines.append(CID_RT_INFO_PROCESSED_MODELTRANSACTION_CONST)
CID_RT_allowed_lines.append(CID_RT_INFO_SENDING_PROJECT_GET_ID)


# CID_RT_CENTRAL

# Cambiado en el processed Tracking por Trackingdata 
# Ahora se guarda la disciplina
CID_RT_CENTRAL_INFO_RECEIVED_MODELTRANSACTION_CONST = "Tracking> INFO MST \(\) \(\) \(\) \(\) \(\) \(\) \(\)  rt trx received MODELTRANSACTION"
CID_RT_CENTRAL_INFO_PROCESSED_MODELTRANSACTION_CONST = "Tracking> INFO MST \(\) \(\) \(\) \(\) \(\) \(\) \(\)  rt trx processed LOCKOG"
CID_RT_CENTRAL_INFO_SENDING_PROJECT_GET_ID = "route.+?> INFO sending project/discipline (.+?) to port .+? with trx id (.+?) and name (MODELTRANSACTION.+?)"

CID_RT_CENTRAL_allowed_lines = list()
CID_RT_CENTRAL_allowed_lines.append(CID_RT_CENTRAL_INFO_RECEIVED_MODELTRANSACTION_CONST)
CID_RT_CENTRAL_allowed_lines.append(CID_RT_CENTRAL_INFO_PROCESSED_MODELTRANSACTION_CONST)
CID_RT_CENTRAL_allowed_lines.append(CID_RT_CENTRAL_INFO_SENDING_PROJECT_GET_ID)


# CIS CLIENT

CIS_CLIENT_RECEIVED_TRANSACTION = "\{ZMQClient\} SUBS\[.+?\] Received transaction: (.+?) \("
CIS_CLIENT_PROCESSED_TRANSACTION = "\{ZMQ\}  ZMQ Message with ID:(\d+?) processed."

CIS_CLIENT_allowed_lines = list()
CIS_CLIENT_allowed_lines.append(CIS_CLIENT_RECEIVED_TRANSACTION)
CIS_CLIENT_allowed_lines.append(CIS_CLIENT_PROCESSED_TRANSACTION)


# VEG

VEG_RECEIVED_TRANSACTION = "<RedisSubscriber> INFO Processing message received: ([a-z0-9]+) from Topic:"
VEG_SENT_TRANSACTION = "<TrackingData> INFO message (.+?) sent to distributor SPHODFCentral"

VEG_allowed_lines = list()
VEG_allowed_lines.append(VEG_RECEIVED_TRANSACTION)
VEG_allowed_lines.append(VEG_SENT_TRANSACTION)


# VEG_CENTRAL

VEG_CENTRAL_RECEIVED_TRANSACTION = "RedisSubscriber> INFO Processing message received: ([a-z0-9]+) from Topic:"
VEG_CENTRAL_SENT_TRANSACTION = "TrackingData> INFO message (.+?) sent to distributor SPHODFCentral"

VEG_CENTRAL_allowed_lines = list()
VEG_CENTRAL_allowed_lines.append(VEG_CENTRAL_RECEIVED_TRANSACTION)
VEG_CENTRAL_allowed_lines.append(VEG_CENTRAL_SENT_TRANSACTION)



# CLIENT MULTICAST

# [159] 2019-03-13 01:54:10.174 {ZMQClient} SUBS[OG TEN] Received transaction: 8 (1381 bytes); Loading Time: 00:00.000
# Group 1 = The discipline name
# Group 2 = The transaction ID
# CLIENT_MULTICAST_RECEIVED_TRANSACTION = " Received transaction: (\d+?) \(\d+? bytes\); Loading Time:"
CLIENT_MULTICAST_RECEIVED_TRANSACTION = "--> \[(.+?)\]--Received Tx:(\d+?) Content: \d+? bytes"

# [161] 2019-03-13 01:54:10.174 {ZMQ}  ZMQ Message with ID:8 processed. [*READY* 9 (12932 bytes)][No next]
# Group 1 = the transaction ID, Group 2 = The ready transaction ID
# CLIENT_MULTICAST_PROCESSED_TRANSACTION = "ZMQ Message with ID:((?!0_INIT)\d+?) processed\. \[\*READY\* ([a-zA-Z0-9]+?) \(\d+? bytes\)\]"
# CLIENT_MULTICAST_PROCESSED_TRANSACTION = "ZMQ Message with ID:((?!0_INIT)\d+?) processed\. \[\*READY\* ([a-zA-Z0-9]+?) \(\d+? bytes\)\]"

# [395] 2019-03-13 01:54:47.442 {DEC} Times for 34 Decode 0ms Total 30 ms (Source:ZMQ)
# Group 1 = Discipline name
# Group 2 = The ready transaction ID
# Group 3 = Decode time
# Group 4 = Total time  (the last seconds one will not be used to count how much time takes to process the message. It will be taken from the log timestamp at the beginning of the line.)
CLIENT_MULTICAST_TIMES_TRANSACTION = " Times for \[(.+?)\]ID:(\d+?) Decode (\d+?)ms Total (\d+?) ms \(Source:ZMQ\)"


CLIENT_MULTICAST_allowed_lines = list()
CLIENT_MULTICAST_allowed_lines.append(CLIENT_MULTICAST_RECEIVED_TRANSACTION)
# CLIENT_MULTICAST_allowed_lines.append(CLIENT_MULTICAST_PROCESSED_TRANSACTION)
CLIENT_MULTICAST_allowed_lines.append(CLIENT_MULTICAST_TIMES_TRANSACTION)


# CLIENT UNICAST

# [159] 2019-03-13 01:54:10.174 {ZMQClient} SUBS[OG TEN] Received transaction: 8 (1381 bytes); Loading Time: 00:00.000
# Group 1 = The discipline name
# Group 2 = The transaction ID
# CLIENT_UNICAST_RECEIVED_TRANSACTION = " Received transaction: (\d+?) \(\d+? bytes\); Loading Time:"
CLIENT_UNICAST_RECEIVED_TRANSACTION = "-> \[(.+?)\]--Received Tx:(\d+?) Content: \d+? bytes"

# [161] 2019-03-13 01:54:10.174 {ZMQ}  ZMQ Message with ID:8 processed. [*READY* 9 (12932 bytes)][No next]
# Group 1 = the transaction ID, Group 2 = The ready transaction ID
# CLIENT_UNICAST_PROCESSED_TRANSACTION = "ZMQ Message with ID:((?!0_INIT)\d+?) processed\. \[\*READY\* ([a-zA-Z0-9]+?) \(\d+? bytes\)\]"
# CLIENT_UNICAST_PROCESSED_TRANSACTION = "ZMQ Message with ID:((?!0_INIT)\d+?) processed\. \[\*READY\* ([a-zA-Z0-9]+?) \(\d+? bytes\)\]"

# [395] 2019-03-13 01:54:47.442 {DEC} Times for 34 Decode 0ms Total 30 ms (Source:ZMQ)
# Group 1 = Discipline name
# Group 2 = The ready transaction ID
# Group 3 = Decode time
# Group 4 = Total time  (the last seconds one will not be used to count how much time takes to process the message. It will be taken from the log timestamp at the beginning of the line.)
CLIENT_UNICAST_TIMES_TRANSACTION = "Times for \[(.+?)\]ID:(\d+?) Decode (\d+?)ms Total (\d+?) ms \(Source:ZMQ\)"


CLIENT_UNICAST_allowed_lines = list()
CLIENT_UNICAST_allowed_lines.append(CLIENT_UNICAST_RECEIVED_TRANSACTION)
# CLIENT_UNICAST_allowed_lines.append(CLIENT_UNICAST_PROCESSED_TRANSACTION)
CLIENT_UNICAST_allowed_lines.append(CLIENT_UNICAST_TIMES_TRANSACTION)