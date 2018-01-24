import uno
from ctypes import *
import datetime
from datetime import *
import time
from aas import *

def call_getAASIDByAssetID(self):
    print("call_getAASIDByAssetID was called")
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    idType = TypeToInt_Id(oSheet.getCellRangeByName("B4").String)
    result = getAASIDByAssetID(oSheet.getCellRangeByName("B2").String, oSheet.getCellRangeByName("B3").String, idType)
    print(result[0])
    oSheet.getCellRangeByName("B6").String = result[0]
    if result[0] != "AssetID not found":
      oSheet.getCellRangeByName("B8").String = IntToType_Id(result[1])
      oSheet.getCellRangeByName("B7").String = result[2]

def call_getAASEntryPointByAASID(self):
    print("call_getAASEntryPointByAASID was called")
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet
    idType = TypeToInt_Id(oSheet.getCellRangeByName("B12").String)
    oSheet = oDoc.CurrentController.ActiveSheet
    result = getAASEntryPointByAASID(oSheet.getCellRangeByName("B2").String, oSheet.getCellRangeByName("B11").String, idType)
    print(result[0])
    
    for x in range(0,4):
      for y in range(15,18):
        oSheet.getCellByPosition(y,x).String =""

    oSheet.getCellRangeByName("B14").String = result[0]
    if result[0] != "Entrypoint not found":
      i = 0;
      for element in result[1]:
        oSheet.getCellByPosition(1,14 + i).String = element
        if i==0: #KS
          protocol,ipport,path  = element.split(";")
          oSheet.getCellByPosition(0,14 + i+1).String = ("Endpoint %s" %i)
          oSheet.getCellByPosition(1,14 + i).String = "Protocol"
          oSheet.getCellByPosition(1,14 + i+1).String = protocol
          oSheet.getCellByPosition(2,14 + i).String = "Endpoint"
          oSheet.getCellByPosition(2,14 + i+1).String = ipport
          oSheet.getCellByPosition(3,14 + i).String = "Path"
          oSheet.getCellByPosition(3,14 + i+1).String = path         
        if i==2: #OPCUA
          oSheet.getCellByPosition(0,14 + i+1).String = ("Endpoint %s" %(i-1))
          endpoint,ns,identifierType,identifer = element.split(";")
          oSheet.getCellByPosition(1,14 + i).String = "Endpoint"
          oSheet.getCellByPosition(1,14 + i+1).String = endpoint
          oSheet.getCellByPosition(2,14 + i).String = "Namespace"
          oSheet.getCellByPosition(2,14 + i+1).String = ns
          oSheet.getCellByPosition(3,14 + i).String = "identifierType"
          oSheet.getCellByPosition(3,14 + i+1).String = identifierType
          oSheet.getCellByPosition(4,14 + i).String = "identifer"
          oSheet.getCellByPosition(4,14 + i+1).String = identifer
        i = i + 2

def call_createAAS(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)
    ip = oSheet.getCellRangeByName("B3").String
    AASIdSpec = oSheet.getCellRangeByName("B4").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B5").String)
    AASName = oSheet.getCellRangeByName("B6").String

    AssetIdSpec = oSheet.getCellRangeByName("B7").String
    AssetIdType = TypeToInt_Id(oSheet.getCellRangeByName("B8").String)
    StatusCall = createAAS(pathToLibrary,ip,AASIdSpec,AASIdType,AASName,AssetIdSpec,AssetIdType)
    oSheet.getCellRangeByName("B9").String = createAAS(pathToLibrary,ip,AASIdSpec,AASIdType,AASName,AssetIdSpec,AssetIdType)
    del lib
    return None

def call_deleteAAS(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
 

    ip = oSheet.getCellRangeByName("B16").String
    AASIdSpec = oSheet.getCellRangeByName("B17").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B18").String)


    oSheet.getCellRangeByName("B19").String = deleteAAS(pathToLibrary, ip, AASIdSpec, AASIdType)
    
    return None



def call_createSubModel(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String

    endpointStr = oSheet.getCellRangeByName("B3").String
    AASIdSpec = oSheet.getCellRangeByName("B4").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B5").String)

    localID = oSheet.getCellRangeByName("B7").String
    

    ModelIdSpec = oSheet.getCellRangeByName("B8").String
    ModelIdType = TypeToInt_Id(oSheet.getCellRangeByName("B9").String)

    ModelName = oSheet.getCellRangeByName("B10").String
    Revision = int(oSheet.getCellRangeByName("B11").String)
    Version = int(oSheet.getCellRangeByName("B12").String)

    oSheet.getCellRangeByName("B13").String = createSubModel(pathToLibrary, endpointStr, AASIdSpec, AASIdType,  localID, ModelIdSpec, ModelIdType, ModelName, Revision, Version)
    return None

def call_deleteSubModel(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)

    ip = oSheet.getCellRangeByName("B19").String
    AASIdSpec = oSheet.getCellRangeByName("B20").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B21").String)

    localID = oSheet.getCellRangeByName("B24").String

    ip_c = ip.encode('utf-8')
    AASIdSpec_c = AASIdSpec.encode('utf-8')
    AASIdType_c = c_int(AASIdType)

    print(ip)
    StatusCall = deleteSubModel(pathToLibrary,ip, AASIdSpec, AASIdType,localID)
    print(StatusCall)
    if(StatusCall!=0):
      status_str = "failed"
    else:
      status_str = "good"
    oSheet.getCellRangeByName("B25").String = status_str;
    del lib
    return None


def call_createLCE(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)

    ip = oSheet.getCellRangeByName("B3").String
    AASIdSpec = oSheet.getCellRangeByName("B4").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B5").String)
    #oSheet.getCellRangeByName("B6").String = AASIdType

    creatingInstanceIdSpec = oSheet.getCellByPosition(1,8).String #i starts with 0, i+7 is the first entry
    creatingInstanceIdType = TypeToInt_Id(oSheet.getCellByPosition(0,8).String)
    writingInstanceIdSpec = oSheet.getCellByPosition(3,8).String
    writingInstanceIdType = TypeToInt_Id(oSheet.getCellByPosition(2,8).String)

    eventClass = oSheet.getCellByPosition(4,8).String
    subject = oSheet.getCellByPosition(5,8).String

    valueType = TypeToInt_valueType(oSheet.getCellByPosition(7,8).String)
    value = oSheet.getCellByPosition(8,8).String


    #type conversion
    ip_c = ip.encode('utf-8')
    AASIdSpec_c = AASIdSpec.encode('utf-8')
    AASIdTypeInt_c = c_int(AASIdType)

    creatingInstanceIdSpec_c = creatingInstanceIdSpec.encode('utf-8')
    creatingInstanceIdType_c = c_int(creatingInstanceIdType)
    writingInstanceIdSpec_c = writingInstanceIdSpec.encode('utf-8')
    writingInstanceIdType_c = c_int(writingInstanceIdType)

    eventClass_c = eventClass.encode('utf-8')
    subject_c = subject.encode('utf-8')

    value_c = value.encode('utf-8')
    valueType_c = c_int(valueType)
    dtTicks = c_int64((time.time()*10000000+116444736000000000))

    StatusCall = lib.call_CreateLCE(c_char_p(ip_c), c_char_p(AASIdSpec_c), AASIdTypeInt_c, c_char_p(creatingInstanceIdSpec_c), creatingInstanceIdType_c, c_char_p(writingInstanceIdSpec_c), writingInstanceIdType_c, c_char_p(eventClass_c), c_char_p(subject_c), dtTicks, c_char_p(value_c), valueType_c)
    #time string
    oSheet.getCellByPosition(6,7).String = str(datetime.utcnow())
    if(StatusCall!=0):
      status_str = "failed"
    else:
      status_str = "good"
    oSheet.getCellRangeByName("K8").String = status_str;

    del lib
    return None

def call_deleteLCE(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)

    ip = oSheet.getCellRangeByName("M16").String
    AASIdSpec = oSheet.getCellRangeByName("M17").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("M18").String)

    LCEId = oSheet.getCellRangeByName("M19").String
    ip_c = ip.encode('utf-8')
    AASIdSpec_c = AASIdSpec.encode('utf-8')
    AASIdType_c = c_int(AASIdType)
    LCEId_c = c_longlong(int(LCEId))

    StatusCall = lib.call_DeleteLCE(c_char_p(ip_c), c_char_p(AASIdSpec_c), AASIdType_c,LCEId_c)
    if(StatusCall!=0):
      status_str = "failed"
    else:
      status_str = "good"
    oSheet.getCellRangeByName("M20").String = status_str;
    del lib
    return None

def call_createLCE1(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)

    ip = oSheet.getCellRangeByName("B3").String
    AASIdSpec = oSheet.getCellRangeByName("B4").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B5").String)

    creatingInstanceIdSpec = oSheet.getCellRangeByName("A8").String
    creatingInstanceIdType = TypeToInt_Id(oSheet.getCellRangeByName("B8").String)
    writingInstanceIdSpec = oSheet.getCellRangeByName("C8").String
    writingInstanceIdType = TypeToInt_Id(oSheet.getCellRangeByName("D8").String)

    eventClass = oSheet.getCellRangeByName("E8").String
    subject = oSheet.getCellRangeByName("F8").String
    #time string conversion?

    valueType = TypeToInt_valueType(oSheet.getCellRangeByName("H8").String)

    value = oSheet.getCellRangeByName("I8").String


    #type conversion
    ip_c = ip.encode('utf-8')
    AASIdSpec_c = AASIdSpec.encode('utf-8')
    AASIdType_c = c_int(AASIdType)

    creatingInstanceIdSpec_c = creatingInstanceIdSpec.encode('utf-8')
    creatingInstanceIdType_c = c_int(creatingInstanceIdType)
    writingInstanceIdSpec_c = writingInstanceIdSpec.encode('utf-8')
    writingInstanceIdType_c = c_int(writingInstanceIdType)

    eventClass_c = eventClass.encode('utf-8')
    subject_c = subject.encode('utf-8')
    timeStamp_c = c_int64(int((time.time())*10000000+116444736000000000))

    value_c = value.encode('utf-8')
    valueType_c = c_int(valueType)
    print(valueType_c)
    StatusCall = lib.call_CreateLCE(c_char_p(ip_c), c_char_p(AASIdSpec_c), AASIdType_c, c_char_p(creatingInstanceIdSpec_c), creatingInstanceIdType_c, c_char_p(writingInstanceIdSpec_c), writingInstanceIdType_c, c_char_p(eventClass_c), c_char_p(subject_c), timeStamp_c, c_char_p(value_c), valueType_c)
    StatusCall = 1
    if(StatusCall!=0):
      status_str = "failed"
    else:
      status_str = "good"
    oSheet.getCellRangeByName("K8").String = status_str;
    del lib
    return None


def call_createPVSL(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)

    ip = oSheet.getCellRangeByName("B3").String

    AASIdSpec = oSheet.getCellRangeByName("B4").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B5").String)

    listName = oSheet.getCellRangeByName("B6").String

    carrierIdSpec = oSheet.getCellRangeByName("B7").String
    carrierIdType = TypeToInt_Id(oSheet.getCellRangeByName("B8").String)

    parentIdSpec = oSheet.getCellRangeByName("B11").String


   
    oSheet.getCellRangeByName("B13").String = createPVSL(pathToLibrary,ip,AASIdSpec,AASIdType,listName,carrierIdSpec,carrierIdType,parentIdSpec)




def call_deletePVSL(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet
    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    ip = oSheet.getCellRangeByName("B3").String
    AASIdSpec = oSheet.getCellRangeByName("B16").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B17").String)

    listIdSpec =  oSheet.getCellRangeByName("B19").String

    oSheet.getCellRangeByName("B21").String = deletePVSL(pathToLibrary,ip,AASIdSpec,AASIdType,listIdSpec)
    return None



def call_createPVS(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

#ipAddress,
#char* AASIdSpec,
#int AASIdType,
#char* ListIdSpec,
#int ListIdType,
#char* PVSName,
#char* Value,
#int ValueType,
#int mask,
#char* CarrierIdSpec,
#int CarrierIdType,
#int ExpressionLogic,
#int ExpressionSemantic,
#char* propertyIdSpec,
#int propertyIdType,
#int view,
#int visibility

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)

    ip = oSheet.getCellRangeByName("B3").String
    AASIdSpec = oSheet.getCellRangeByName("B4").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B5").String)

    #SubModelIdSpec   =  oSheet.getCellRangeByName("G2").String
    #SubModelIdType   = TypeToInt_Id(oSheet.getCellRangeByName("G3").String)


    ListIdType   = TypeToInt_Id("URI")
    ListIdSpec   =  oSheet.getCellRangeByName("B6").String
    #PVSLName = oSheet.getCellRangeByName("B6").String
    #PVSLName_c = PVSLName.encode('utf-8')

    ip_c = ip.encode('utf-8')
    AASIdSpec_c = AASIdSpec.encode('utf-8')
    AASIdType_c = c_int(AASIdType)

    #SubModelIdSpec_c = SubModelIdSpec.encode('utf-8')
    #SubModelIdType_c = c_int(SubModelType)

    ListIdSpec_c = ListIdSpec.encode('utf-8')
    ListIdType_c = c_int(ListIdType)

    #dont use the carrier Id in this case
    CarrierIdSpec_c = ListIdSpec_c  # dummy
    CarrierIdType_c = ListIdType_c  # dummy

    mask = 1 | 2 | 4 | 8 | 16 | 32
    offsetY = 8

    for i in range(5):

        #hierarchy
        PVSName = oSheet.getCellByPosition(0,i+offsetY).String
        if len(PVSName)==0:
            break
        PRIdType = oSheet.getCellByPosition(2,i+offsetY).String
        if len(PRIdType)==0:
            break
        PRIdSpec = oSheet.getCellByPosition(1,i+offsetY).String
        if len(PRIdSpec)==0:
            break
        #definition: get from website?
        #unit = oSheet.getCellByPosition(5,i+offsetY).String
        valueType = oSheet.getCellByPosition(3,i+offsetY).String
        if len(valueType)==0:
            break
        #valuelist
        Value = oSheet.getCellByPosition(4,i+offsetY).String
        if len(Value)==0:
            break
        expressionLogic = oSheet.getCellByPosition(5,i+offsetY).String
        if len(expressionLogic)==0:
            break
        expressionSemantic = oSheet.getCellByPosition(6,i+offsetY).String
        if len(expressionSemantic)==0:
            break
        view = oSheet.getCellByPosition(7,i+offsetY).String
        if len(view)==0:
            break
        visibility = oSheet.getCellByPosition(8,i+offsetY).String
        if len(visibility)==0:
            break

        PVSName_c = PVSName.encode('utf-8')
        expressionLogic_c = c_int(TypeToInt_EL(expressionLogic))
        expressionSemantic_c = c_int(TypeToInt_ES(expressionSemantic))
        print("expression Semantic %s" % expressionSemantic_c)
        Value_c = Value.encode('utf-8')
        valueType_c = c_int(TypeToInt_valueType(valueType))
        #unit_c = unit.encode('utf-8')
        PRIdSpec_c = PRIdSpec.encode('utf-8')
        PRIdType_c = c_int(TypeToInt_Id(PRIdType))
        view_c = c_int(TypeToInt_view(view))
        visibility_c = c_int(TypeToInt_VIS(visibility))
        mask_c = c_int(mask)
        print(mask_c)
#ipAddress,
#char* AASIdSpec,
#int AASIdType,
#char* ListIdSpec,
#int ListIdType,
#char* PVSName,
#char* Value,
#int ValueType,
#int mask,
#char* CarrierIdSpec,
#int CarrierIdType,
#int ExpressionLogic,
#int ExpressionSemantic,
#char* propertyIdSpec,
#int propertyIdType,
#int view,
#int visibility


        StatusCall = lib.call_CreatePVS(c_char_p(ip_c), c_char_p(AASIdSpec_c),AASIdType_c,c_char_p(ListIdSpec_c),ListIdType_c, c_char_p(PVSName_c), c_char_p(Value_c),valueType_c,mask_c,c_char_p(CarrierIdSpec_c),CarrierIdType_c,expressionLogic_c,expressionSemantic_c,c_char_p(PRIdSpec_c),PRIdType_c,view_c,visibility_c)
        if(StatusCall!=0):
          break
        oSheet.getCellRangeByName("B16").Value = i+1
    del lib
    return None

def call_deletePVS(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)

    ip = oSheet.getCellRangeByName("L6").String
 
    AASIdSpec = oSheet.getCellRangeByName("L7").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("L8").String)
    
    PVSName = oSheet.getCellRangeByName("L9").String
    PVSName_c = PVSName.encode('utf-8')



    ip_c = ip.encode('utf-8')
    AASIdSpec_c = AASIdSpec.encode('utf-8')
    AASIdType_c = c_int(AASIdType)

    StatusCall = lib.call_DeletePVS(c_char_p(ip_c), c_char_p(AASIdSpec_c), AASIdType_c,c_char_p(PVSLName_c),c_int(0))
    if(StatusCall!=0):
      status_str = "failed"
    else:
      status_str = "good"
    oSheet.getCellRangeByName("R12").String = status_str

    del lib
    return None




def getPVS(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    ip = oSheet.getCellRangeByName("B22").String
    AASIdSpec = oSheet.getCellRangeByName("B23").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B24").String)
    listId = oSheet.getCellRangeByName("B25").String
    print_start_x = 0
    print_start_y = 28
    pvsl = getPVSL(ip,listId)
    if (pvsl==None):
      return None
      
    i = 0
    print(pvsl.Name)
    #clear
    for x in range(0,15):
      for y in range(26,50):
        oSheet.getCellByPosition(x,y).String = ""
        oSheet.getCellByPosition(x,y).CharWeight = 100
        
    oSheet.getCellByPosition(0,25).String = "Local Name"
    oSheet.getCellByPosition(0,25).CharWeight = 150
    oSheet.getCellByPosition(1,25).String = pvsl.Name
 
    
    line = 26
    if hasattr(pvsl, 'CarrierID'):
      oSheet.getCellByPosition(0,line).String = "Carrier ID Spec"
      oSheet.getCellByPosition(0,line).CharWeight = 150
      oSheet.getCellByPosition(1,line).String = pvsl.CarrierID.IDSpec  
      line = line + 1
      oSheet.getCellByPosition(0,line).String = "Carrier ID Type"
      oSheet.getCellByPosition(0,line).CharWeight = 150
      oSheet.getCellByPosition(1,line).String = pvsl.CarrierID.IDType  
      line = line + 1
    if hasattr(pvsl, 'PropertyID'):
      oSheet.getCellByPosition(0,line).String = "Property ID Spec"
      oSheet.getCellByPosition(0,line).CharWeight = 150
      oSheet.getCellByPosition(1,line).String = pvsl.PropertyID.IDSpec 
      line = line + 1
      oSheet.getCellByPosition(0,line).String = "Property ID Type"
      oSheet.getCellByPosition(0,line).CharWeight = 150
      oSheet.getCellByPosition(1,line).String = pvsl.PropertyID.IDType  
      line = line + 1   
    if hasattr(pvsl, 'ExpressionLogic'):
      oSheet.getCellByPosition(0,line).String = "ExpressionLogic"
      oSheet.getCellByPosition(0,line).CharWeight = 150
      oSheet.getCellByPosition(1,line).String = pvsl.ExpressionLogic
      line = line + 1
    if hasattr(pvsl, 'ExpressionSemantic'):
      oSheet.getCellByPosition(0,line).String = "ExpressionSemantic"
      oSheet.getCellByPosition(0,line).CharWeight = 150
      oSheet.getCellByPosition(1,line).String = pvsl.ExpressionSemantic
      line = line + 1
    
    if hasattr(pvsl, 'View'):
      oSheet.getCellByPosition(0,line).String = "View"
      oSheet.getCellByPosition(0,line).CharWeight = 150
      oSheet.getCellByPosition(1,line).String = pvsl.View
      line = line + 1       
    if hasattr(pvsl, 'Visibility'):
      oSheet.getCellByPosition(0,line).String = "Visibility"
      oSheet.getCellByPosition(0,line).CharWeight = 150
      oSheet.getCellByPosition(1,line).String = pvsl.Visibility
    line = line + 2    
    oSheet.getCellByPosition(0,line).String  = "Statements"
    oSheet.getCellByPosition(0,line).CharWeight = 150
    line = line + 1
    firstPVS = True
    i=0
    firstLine = line
    line = line + 1
    for pvs in pvsl.statements:
      print(i)
      i=i+1
      col = 0;
      if firstPVS:
        oSheet.getCellByPosition(col,firstLine).String = "(preferred)Name"
        oSheet.getCellByPosition(col,firstLine).CharWeight = 150
      oSheet.getCellByPosition(col,line).String = pvs.Name
      col = col + 1 
      
  
      if hasattr(pvs, 'PropertyID'):
        if firstPVS:
          oSheet.getCellByPosition(col,firstLine).String = "Property ID Spec"
          oSheet.getCellByPosition(col,firstLine).CharWeight = 150
        oSheet.getCellByPosition(col,line).String = pvs.PropertyID.IDSpec 
        col = col + 1
        
        if firstPVS:
          oSheet.getCellByPosition(col,firstLine).String = "Property ID Type"
          oSheet.getCellByPosition(col,firstLine).CharWeight = 150
        oSheet.getCellByPosition(col,line).String = pvs.PropertyID.IDType
        col = col + 1 
         
      if hasattr(pvs, 'Value'):       
        if firstPVS:
          oSheet.getCellByPosition(col,firstLine).String = "Value"
          oSheet.getCellByPosition(col,firstLine).CharWeight = 150
        oSheet.getCellByPosition(col,line).String = pvs.Value
        col = col + 1 
        
      if hasattr(pvs, 'CarrierID'):
        if firstPVS:
          oSheet.getCellByPosition(col,firstLine).String = "Carrier ID Spec"
          oSheet.getCellByPosition(col,firstLine).CharWeight = 150
        oSheet.getCellByPosition(col,line).String = pvs.CarrierID.IDSpec 
        col = col + 1
        
        if firstPVS:
          oSheet.getCellByPosition(col,firstLine).String = "Property ID Type"
          oSheet.getCellByPosition(col,firstLine).CharWeight = 150
        oSheet.getCellByPosition(col,line).String = pvs.CarrierID.IDType    
        
      if hasattr(pvs, 'ExpressionLogic'):
        if firstPVS:
          oSheet.getCellByPosition(col,firstLine).String = "ExpressionLogic"
          oSheet.getCellByPosition(col,firstLine).CharWeight = 150
        oSheet.getCellByPosition(col,line).String = pvs.ExpressionLogic 
        col = col + 1
        
      if hasattr(pvs, 'ExpressionSemantic'):
        if firstPVS:
          oSheet.getCellByPosition(col,firstLine).String = "ExpressionSemantic"
          oSheet.getCellByPosition(col,firstLine).CharWeight = 150
        oSheet.getCellByPosition(col,line).String = pvs.ExpressionSemantic 
        col = col + 1  
        
      if hasattr(pvs, 'View'):
        if firstPVS:
          oSheet.getCellByPosition(col,firstLine).String = "View"      
          oSheet.getCellByPosition(col,firstLine).CharWeight = 150
        oSheet.getCellByPosition(col,line).String = pvs.View 
        col = col + 1    
        
      if hasattr(pvs, 'Visibility'):
        if firstPVS:
          oSheet.getCellByPosition(col,firstLine).String = "Visibility"
          oSheet.getCellByPosition(col,firstLine).CharWeight = 150
        oSheet.getCellByPosition(col,line).String = pvs.Visibility 
        print("found Visibility %s" %pvs.Visibility)
        col = col + 1    
        
      line = line + 1;
      firstPVS = False

    return None


def call_getLastLCEs(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    ip = oSheet.getCellRangeByName("B12").String
    AASIdSpec = oSheet.getCellRangeByName("B13").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B14").String)
    lceCountToReturn = int(oSheet.getCellRangeByName("B15").String)
    lib = CDLL(pathToLibrary)

    ip_c = ip.encode('utf-8')
    AASIdSpec_c = AASIdSpec.encode('utf-8')
    AASIdTypeInt_c = c_int(AASIdType)
    lceCountToReturn_c = c_int(lceCountToReturn)
    lifeCycleEntries = c_void_p()
    count = lib.call_GetLastLCEs(c_char_p(ip_c), c_char_p(AASIdSpec_c), AASIdTypeInt_c,lceCountToReturn_c, byref(lifeCycleEntries))
    #oSheet.getCellByPosition(0,42).String = count


    if count > 0:
        LCEArray = POINTER(LCE * count)
        lce_array = LCEArray.from_address(addressof(lifeCycleEntries))
        print_start_x = 0
        print_start_y = 18
        n = 0
        while (len(oSheet.getCellByPosition(print_start_x+0,print_start_y+n).String) > 0):
          n = n + 1
        for i in range(n):
          for j in range(10):
            oSheet.getCellByPosition(print_start_x+j,print_start_y+i).String=""
        for i in range(count):
            oSheet.getCellByPosition(print_start_x+1,print_start_y+i).String = lce_array.contents[i].creatingInstanceSpec
            oSheet.getCellByPosition(print_start_x+0,print_start_y+i).String = IntToType_Id(lce_array.contents[i].creatingInstanceType)

            oSheet.getCellByPosition(print_start_x+3,print_start_y+i).String = lce_array.contents[i].writingInstanceSpec
            oSheet.getCellByPosition(print_start_x+2,print_start_y+i).String = IntToType_Id(lce_array.contents[i].writingInstanceType)

            oSheet.getCellByPosition(print_start_x+4,print_start_y+i).String = lce_array.contents[i].eventClass
            oSheet.getCellByPosition(print_start_x+5,print_start_y+i).String = lce_array.contents[i].subject
            if lce_array.contents[i].timestamp > 116444736000000000:
              ticks = (lce_array.contents[i].timestamp-116444736000000000)/10000000
              dt = datetime.fromtimestamp(ticks);
              oSheet.getCellByPosition(print_start_x+6,print_start_y+i).String = dt.strftime('%Y-%m-%d %H:%M:%S%f')
              print(dt.strftime('%Y%m%d%H%M%S%f'))
            else:
              oSheet.getCellByPosition(print_start_x+6,print_start_y+i).String = "not defined"
            oSheet.getCellByPosition(print_start_x+7,print_start_y+i).String = IntToType_valueType(lce_array.contents[i].dataType)
            oSheet.getCellByPosition(print_start_x+8,print_start_y+i).String = lce_array.contents[i].data
            oSheet.getCellByPosition(print_start_x+9,print_start_y+i).String = lce_array.contents[i].id
    del lib
    return None

def call_triggerGetCoreData(self):
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    ip = oSheet.getCellRangeByName("B3").String
    srcAASIdSpec = oSheet.getCellRangeByName("B4").String
    srcAASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B5").String)
    dstAASIdSpec = oSheet.getCellRangeByName("B6").String
    dstAASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B7").String)

    lib = CDLL(pathToLibrary)

    ip_c = ip.encode('utf-8')
    srcAASIdSpec_c = srcAASIdSpec.encode('utf-8')
    srcAASIdTypeInt_c = c_int(srcAASIdType)

    dstAASIdSpec_c = dstAASIdSpec.encode('utf-8')
    dstAASIdTypeInt_c = c_int(dstAASIdType)

    count = lib.call_triggerGetCoreData(c_char_p(ip_c), c_char_p(srcAASIdSpec_c), srcAASIdTypeInt_c,c_char_p(dstAASIdSpec_c), dstAASIdTypeInt_c)

def call_startGetAssetLCEData(self):

    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)

    ip = oSheet.getCellRangeByName("B3").String

    AASIdSpec = oSheet.getCellRangeByName("B4").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B5").String)
    AssetIp = oSheet.getCellRangeByName("B6").String
    AssetIdSpec = oSheet.getCellRangeByName("B7").String
    AssetIdType = TypeToInt_Id(oSheet.getCellRangeByName("B8").String)

    ip_c = ip.encode('utf-8')
    AASIdSpec_c = AASIdSpec.encode('utf-8')
    AASIdType_c = c_int(AASIdType)

    AssetIdSpec_c = AssetIdSpec.encode('utf-8')
    AssetIdType_c = c_int(AASIdType)

    AssetIp_c = AssetIp.encode('utf-8')

    StatusCall = lib.call_startGetAssetLCEData(c_char_p(ip_c), c_char_p(AASIdSpec_c), AASIdType_c, c_char_p(AssetIp_c), c_char_p(AssetIdSpec_c), AssetIdType_c)
    if(StatusCall!=0):
      oSheet.getCellRangeByName("B9").String = "failed"
    else:
      oSheet.getCellRangeByName("B9").String = "good"
    del lib
    return None

def call_stopGetAssetLCEData(self):

    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    pathToLibrary = oSheet.getCellRangeByName("B2").String
    lib = CDLL(pathToLibrary)

    ip = oSheet.getCellRangeByName("B3").String

    AASIdSpec = oSheet.getCellRangeByName("B4").String
    AASIdType = TypeToInt_Id(oSheet.getCellRangeByName("B5").String)

    ip_c = ip.encode('utf-8')
    AASIdSpec_c = AASIdSpec.encode('utf-8')
    AASIdType_c = c_int(AASIdType)

    StatusCall = lib.call_stopGetAssetLCEData(c_char_p(ip_c), c_char_p(AASIdSpec_c), AASIdType_c)
    if(StatusCall!=0):
      oSheet.getCellRangeByName("B9").String = "failed"
    else:
      oSheet.getCellRangeByName("B9").String = "good"
    del lib
    return None
    
def call_serializeAAS(self): 
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet

    #Parameter parsing
    endpointStr = oSheet.getCellRangeByName("B27").String
    identifierType = "String"
    identifer = oSheet.getCellRangeByName("B28").String
    namespaceIndex = oSheet.getCellRangeByName("B29").String
    filename = oSheet.getCellRangeByName("B30").String
    
    StatusCall = serialize_AAS(endpointStr, identifierType,identifer,int(namespaceIndex),filename)
    if(StatusCall!=0):
      oSheet.getCellRangeByName("B9").String = "failed"
    else:
      oSheet.getCellRangeByName("B9").String = "good"

    return None   
