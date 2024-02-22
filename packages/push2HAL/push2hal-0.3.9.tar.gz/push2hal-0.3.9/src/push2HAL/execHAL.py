####*****************************************************************************************
####*****************************************************************************************
####*****************************************************************************************
#### Library part of push2HAL
#### Copyright - 2024 - Luc Laurent (luc.laurent@lecnam.net)
####
#### description available on https://github.com/luclaurent/push2HAL
####*****************************************************************************************
####*****************************************************************************************


import os
import logging
import json

from . import libHAL as lib
from . import misc as m
from . import default as dflt

Logger = logging.getLogger("push2HAL")


def runJSON2HAL(
    jsonContent,
    verbose=False,
    prod="preprod",
    credentials=None,
    completion=None,
    idhal=None,
):
    """execute using arguments"""
    exitStatus = os.EX_CONFIG
    # activate verbose mode
    if verbose:
        Logger.setLevel(logging.DEBUG)

    Logger.info("Run JSON2HAL")
    Logger.info("")

    # activate production mode
    serverType = "preprod"
    testMode = True
    if prod == "prod":
        Logger.info("Execution mode: use production server (USE WITH CAUTION))")
        serverType = "prod"
        testMode = False
    elif prod == "test":
        Logger.info("Execution mode: use production server (dry-run))")
        serverType = "prod"
        testMode = True
    else:
        Logger.info("Dryrun mode: use preprod server")
        testMode = False

    #
    json_path = jsonContent
    new_xml = None
    if type(jsonContent) is dict:
        dataJSON = jsonContent
        new_xml = dflt.DEFAULT_UPLOAD_FILE_NAME_XML
    elif os.path.isfile(json_path):
        Logger.debug("JSON file: {}".format(json_path))
        dirPath = os.path.dirname(json_path)
        Logger.debug("Directory: {}".format(dirPath))
        # open and load json file
        f = open(json_path, "r")
        # Reading from file
        dataJSON = json.loads(f.read())
        new_xml = os.path.basename(json_path).replace(".json", ".xml")
    else:
        Logger.error("JSON file not found")
        exitStatus = os.EX_OSFILE
        return exitStatus

    # build XML tree from json
    xmlData = lib.buildXML(dataJSON)

    # add PDF file if provided
    pdf_path = None
    if dataJSON.get("file", None):
        # file directly found
        pdf_path = dataJSON.get("file", None)
        if not os.path.isfile(pdf_path):
            # file not found, search in the same directory
            pdf_path = os.path.join(dirPath, dataJSON["file"])
        #
        if os.path.isfile(pdf_path):
            Logger.debug("PDF file: {}".format(pdf_path))
        else:
            Logger.error("PDF file not found")
            exitStatus = os.EX_OSFILE
            return exitStatus
    # deal with specific upload options
    options = dict()
    if completion:
        Logger.info(
            "Specific completion option(s) will be used: {}".format(completion)
        )
        options["completion"] = completion
    if idhal:
        Logger.info("Deposit on behalf of: {}".format(idhal))
        options["idFrom"] = idhal
    if testMode:
        options["testMode"] = "1"
    else:
        options["testMode"] = "0"
    # prepare payload to upload to HAL
    file, payload = lib.preparePayload(
        xmlData,
        pdf_path,
        dirPath,
        xmlFileName=new_xml,
        hal_id=None,
        options=options,
    )

    # upload to HAL
    if credentials:
        id_hal = lib.upload2HAL(file, payload, credentials, server=serverType)
        return lib.manageError(id_hal)
    else:
        Logger.error("No provided credentials")
        exitStatus = os.EX_CONFIG
        return exitStatus


def runPDF2HAL(
    pdf_path,
    verbose=False,
    prod="preprod",
    credentials=None,
    completion=None,
    halid=None,
    idhal=None,
    interaction=True,
):
    """execute using arguments"""
    exitStatus = os.EX_CONFIG
    # activate verbose mode
    if verbose:
        Logger.setLevel(logging.DEBUG)

    Logger.info("Run PDF2HAL")
    Logger.info("")

    # activate production mode
    serverType = "preprod"
    testMode = False
    if prod == "prod":
        Logger.info("Execution mode: use production server (USE WITH CAUTION))")
        serverType = "prod"
    elif prod == "test":
        Logger.info("Execution mode: use production server (dry-run))")
        serverType = "prod"
        testMode = True
    else:
        Logger.info("Dryrun mode: use preprod server")

    # check if file exists
    if os.path.isfile(pdf_path):
        Logger.debug("PDF file: {}".format(pdf_path))
        dirPath = os.path.dirname(pdf_path)
        Logger.debug("Directory: {}".format(dirPath))
        title = m.extract_info(pdf_path)
    else:
        Logger.error("PDF file not found")
        exitStatus = os.EX_OSFILE
        return exitStatus

    # show first characters of pdf file
    m.showPDFcontent(pdf_path, number=dflt.DEFAULT_NB_CHAR)

    # check title and/or provide new one
    if not halid:
        if interaction:
            title = m.checkTitle(title)
        else:
            Logger.info("Force mode: use title '{}'".format(title))

        # Search for the PDF title in HAL.science
        selected_result = dict()
        while "title_s" not in selected_result:
            archives_results = lib.getDataFromHAL(
                txtsearch=title, typeI="title", typeDB="article"
            )

            if archives_results:
                selected_result = lib.choose_from_results(
                    archives_results, not interaction
                )
                if "title_s" not in selected_result:
                    title = selected_result
            else:
                Logger.error("No result found in HAL.science")
                exitStatus = os.EX_SOFTWARE
                return exitStatus

        if selected_result:
            selected_title = selected_result.get("title_s", "N/A")
            selected_author = selected_result.get("author_s", "N/A")
            hal_id = selected_result.get("halId_s", None)

            Logger.info("Selected result in archives-ouvertes.fr:")
            Logger.info("Title: {}".format(selected_title))
            Logger.info("Author: {}".format(selected_author))
            Logger.info("HAL-id: {}".format(hal_id))
    else:
        Logger.info("Provided HAL_id: {}".format(halid))
        hal_id = halid
        # get data from HAL
        dataHAL = lib.getDataFromHAL(txtsearch=hal_id, typeI="docId", typeDB="article")

        if len(dataHAL) > 0:
            selected_title = dataHAL[0].get("title_s", "N/A")
            selected_author = dataHAL[0].get("author_s", "N/A")
            hal_id = dataHAL[0].get("halId_s", None)

            Logger.info("Title: {}".format(selected_title))
            Logger.info("Author: {}".format(selected_author))
            Logger.info("HAL-id: {}".format(hal_id))
        else:
            Logger.error("Document's ID {} not found in HAL".format(hal_id))
            exitStatus = os.EX_SOFTWARE
            return exitStatus

    if hal_id:
        # Download TEI file
        tei_content = lib.getDataFromHAL(
            txtsearch=hal_id, typeI="docId", typeDB="article", typeR="xml-tei"
        )

        if len(tei_content) > 0:
            # write TEI file
            tei_file_path = os.path.join(dirPath, hal_id + ".tei.xml")
            Logger.debug("Write TEI file: {}".format(tei_file_path))
            m.writeXML(tei_content, tei_file_path)

            options = dict()
            # deal with specific upload options
            if completion:
                Logger.info(
                    "Specific completion option(s) will be used: {}".format(completion)
                )
                options["completion"] = completion
            if idhal:
                Logger.info("Deposit on behalf of: {}".format(idhal))
                options["idFrom"] = idhal
            options["testMode"] = False
            if testMode:
                options["testMode"] = True

            # prepare payload to upload to HAL
            file, payload = lib.preparePayload(
                tei_content=tei_content, 
                pdf_path=pdf_path,
                dirPath=dirPath, 
                hal_id=hal_id, 
                options=options
            )

            # upload to HAL
            if credentials:
                retStatus = lib.upload2HAL(file, payload, credentials, server=serverType)
                return lib.manageError(retStatus)
            else:
                Logger.error("No provided credentials")
                exitStatus = os.EX_CONFIG
                return exitStatus
            
        else:
            Logger.error("Failed to download TEI file.")
            exitStatus = os.EX_SOFTWARE
            return exitStatus

    else:
        Logger.error("No result selected.")
        exitStatus = os.EX_SOFTWARE
        return exitStatus

    return exitStatus
