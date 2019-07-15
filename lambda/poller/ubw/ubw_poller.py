import os
import xmltodict
import urllib.request
import urllib.parse
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

client = None
table = None


def lambda_handler(event, context):
    global client
    global table
    client = boto3.resource("dynamodb")
    table = client.Table("dataplattform_data_polling_status")

    last_inserted_doc = fetch_last_inserted_doc()

    ubw_datas = fetch_ubw_data()
    for ubw_data in ubw_datas:
        if should_upload_ingest(ubw_data, last_inserted_doc):
            last_doc_new = insert_new_ubw_data(ubw_data)
            if last_doc_new is not None:
                last_inserted_doc = last_doc_new

    upload_last_inserted_doc(last_inserted_doc)

    return {
        'statusCode': 200,
        'body': ''
    }


def send_request(url, data, headers):
    """
    :param url: URL.
    :param data: the data to be sent as a string.
    :param headers: the headers as a dictionary.
    :return: a list of all the weeks and their corresponding hours worked at non-billable stuff (
    fagtimer).
    """
    req = urllib.request.Request(url, data=data.encode(), headers=headers)
    response = urllib.request.urlopen(req)
    return response.read().decode()


def create_body_and_headers(template_id, username, client, password):
    """
    :param template_id: Which UBW report template should be fetched.
    :param username: UBW username
    :param client: UBW client id.
    :param password: UBW password.
    :return: This method creates and returns a body and headers for the UBW API.
    """
    body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
        xmlns:quer="http://services.agresso.com/QueryEngineService/QueryEngineV200606DotNet">
                <soapenv:Header/>
                <soapenv:Body>
                    <quer:GetTemplateResultAsXML>
                        <!--Optional:-->
                        <quer:input>
                            <quer:TemplateId>{template_id}</quer:TemplateId>
                            <!--Optional:-->
                            <quer:TemplateResultOptions>
                                <quer:ShowDescriptions>true</quer:ShowDescriptions>
                                <quer:Aggregated>true</quer:Aggregated>
                                <quer:OverrideAggregation>false</quer:OverrideAggregation>
                                <quer:CalculateFormulas>true</quer:CalculateFormulas>
                                <quer:FormatAlternativeBreakColumns>true
                                </quer:FormatAlternativeBreakColumns>
                                <quer:RemoveHiddenColumns>false</quer:RemoveHiddenColumns>
                                <!--Optional:-->
                                <quer:Filter>?</quer:Filter>
                                <quer:FirstRecord>-1</quer:FirstRecord>
                                <quer:LastRecord>-1</quer:LastRecord>
                            </quer:TemplateResultOptions>
                            <!--Optional:-->
                            <quer:SearchCriteriaPropertiesList>
                                <!--Zero or more repetitions:-->
                                <quer:SearchCriteriaProperties>
                                    <!--Optional:-->
                                    <quer:ColumnName>timecode</quer:ColumnName>
                                    <!--Optional:-->
                                    <quer:Description>Tidskode</quer:Description>
                                    <!--Optional:-->
                                    <quer:RestrictionType>!()</quer:RestrictionType>
                                    <!--Optional:-->
                                    <quer:FromValue>'X9'</quer:FromValue>
                                    <!--Optional:-->
                                    <quer:ToValue>?</quer:ToValue>
                                    <quer:DataType>10</quer:DataType>
                                    <quer:DataLength>25</quer:DataLength>
                                    <quer:DataCase>2</quer:DataCase>
                                    <quer:IsParameter>true</quer:IsParameter>
                                    <quer:IsVisible>false</quer:IsVisible>
                                    <quer:IsPrompt>false</quer:IsPrompt>
                                    <!--Optional:-->
                                    <quer:RelDateCrit>?</quer:RelDateCrit>
                                </quer:SearchCriteriaProperties>
                            </quer:SearchCriteriaPropertiesList>
                            <!--Optional:-->
                            <quer:PipelineAssociatedName>?</quer:PipelineAssociatedName>
                        </quer:input>
                        <!--Optional:-->
                        <quer:credentials>
                            <!--Optional:-->
                            <quer:Username>{username}</quer:Username>
                            <!--Optional:-->
                            <quer:Client>{client}</quer:Client>
                            <!--Optional:-->
                            <quer:Password>{password}</quer:Password>
                            <!--Optional:-->
                            <quer:AccessToken>?</quer:AccessToken>
                        </quer:credentials>
                    </quer:GetTemplateResultAsXML>
                </soapenv:Body>
            </soapenv:Envelope>"""
    headers = {
        'Accept-Encoding': 'gzip,deflate',
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction':
            'http://services.agresso.com/QueryEngineService/QueryEngineV200606DotNet'
            '/GetTemplateResultAsXML',

        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Host': 'ubw.unit4cloud.com'
    }
    return body, headers


def fetch_ubw_data():
    """
    This method fetches the data from the UBW SOAP API. This method is incredibly ugly, however the
    UBW API is very old and finicky therefore this is the cleanest I could get it working.
    :return: returns the list of all the hours used and which period this was for.
    """
    username = os.getenv("UBW_USERNAME")
    password = os.getenv("UBW_PASSWORD")
    client = os.getenv("UBW_CLIENT")
    url = os.getenv("UBW_URL")
    template_id = os.getenv("UBW_TEMPLATE_ID")

    body, headers = create_body_and_headers(template_id, username, client, password)

    xml = send_request(url, body, headers)
    # TODO: find a proper library. But for now these do seems to do the trick.
    xml = xml.replace("&gt;", ">")
    xml = xml.replace("&lt;", "<")

    dictionary = xmltodict.parse(xml)
    # I know this is very ugly, however this is where the list that we need is contained.
    return dictionary['s:Envelope']['s:Body']['GetTemplateResultAsXMLResponse'][
        'GetTemplateResultAsXMLResult']['TemplateResult']['Agresso']['AgressoQE']


def upload_last_inserted_doc(last_inserted_doc, type="UBWType"):
    """
    This method simply inserts the last_inserted_doc's reg_period into a table.
    :param last_inserted_doc: The document that is going to be uploaded.
    :param type: Which type this is.
    :return: Nothing
    """
    table.put_item(Item={
        'type': type,
        'last_inserted_doc': last_inserted_doc
    })


def fetch_last_inserted_doc(type="UBWType"):
    """
    This method fetches the last_inserted_doc from the DynamoDB table and returns the
    last_inserted_doc.
    :param type: Which type.
    :return: last_inserted_doc. or None if there was nothing saved.
    """
    response = table.query(KeyConditionExpression=Key('type').eq(type))
    items = response["Items"]
    if items:
        return items[0]["last_inserted_doc"]
    return None


def post_to_ingest_api(data):
    """
    This method uploads data to the ingest API.
    :param data: the data you want to send, as a dictionary.
    :return: a status code.
    """
    ingest_url = os.getenv("DATAPLATTFORM_INGEST_URL")
    apikey = os.getenv("DATAPLATTFORM_INGEST_APIKEY")
    data = json.dumps(data).encode()
    try:
        request = urllib.request.Request(ingest_url, data=data, headers={"x-api-key": apikey})
        response = urllib.request.urlopen(request)
        return response.getcode()
    except urllib.request.HTTPError:
        return 500


def insert_new_ubw_data(doc):
    """
    :param doc: A ubw document.
    :return: This method attempts to upload the ubw document into the ingest API and if that was
    successful it returns the reg_period of this document. (aka the last_inserted_doc)
    """
    if post_to_ingest_api(doc) == 200:
        # This method is always updating the last_inserted_doc global after uploading new data.
        return doc["reg_period"]
    return None


def should_upload_ingest(doc, last_inserted_doc):
    """
    :param doc: The doc that's about to be evaluated
    :param last_inserted_doc: This is the last inserted document. This is what we need to compare
    to.
    :return: either True if this doc should be uploaded or False if it should be skipped.
    """
    # You should always upload if there is no previous inserted doc.
    if last_inserted_doc is None:
        return True

    # The last document doesn't have either or these and should be skipped.
    if "tab" not in doc or "reg_period" not in doc:
        return False

    # Only the "B" documents are completed, the rest should be ignored.
    if doc["tab"] != "B":
        return False

    return int(doc["reg_period"]) > int(last_inserted_doc)
