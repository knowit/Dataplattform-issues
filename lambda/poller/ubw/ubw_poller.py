import os
import xmltodict
import urllib.request
import urllib.parse


def lambda_handler(event, context):
    ubw_datas = fetch_ubw_data()
    for ubw_data in ubw_datas:
        print(ubw_data)
        if should_upload(ubw_data):
            upload_data(ubw_data)


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


def fetch_ubw_data():
    username = os.getenv("UBW_USERNAME")
    password = os.getenv("UBW_PASSWORD")
    client = os.getenv("UBW_CLIENT")
    url = os.getenv("UBW_URL")
    template_id = os.getenv("UBW_TEMPLATE_ID")
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
    xml = send_request(url, body, headers)
    # TODO: find a proper library. But for now these do seems to do the trick.
    xml = xml.replace("&gt;", ">")
    xml = xml.replace("&lt;", "<")

    dictionary = xmltodict.parse(xml)
    # I know this is very ugly, however this is where the list that we need is contained.
    return dictionary['s:Envelope']['s:Body']['GetTemplateResultAsXMLResponse'][
        'GetTemplateResultAsXMLResult']['TemplateResult']['Agresso']['AgressoQE']


def upload_data(doc):
    pass


def should_upload(doc):
    """
    :param doc: The doc that's about to be evaluated
    :return: either True if this doc should be uploaded or False if it should be skipped.
    """
    return True


if __name__ == '__main__':
    lambda_handler(None, None)
