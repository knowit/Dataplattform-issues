import ubw_poller


def test_create_body_and_headers():
    body, headers = ubw_poller.create_body_and_headers(1231, "frank", 1337, "hunter2")
    body_correct = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
        xmlns:quer="http://services.agresso.com/QueryEngineService/QueryEngineV200606DotNet">
                <soapenv:Header/>
                <soapenv:Body>
                    <quer:GetTemplateResultAsXML>
                        <!--Optional:-->
                        <quer:input>
                            <quer:TemplateId>1231</quer:TemplateId>
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
                            <quer:Username>frank</quer:Username>
                            <!--Optional:-->
                            <quer:Client>1337</quer:Client>
                            <!--Optional:-->
                            <quer:Password>hunter2</quer:Password>
                            <!--Optional:-->
                            <quer:AccessToken>?</quer:AccessToken>
                        </quer:credentials>
                    </quer:GetTemplateResultAsXML>
                </soapenv:Body>
            </soapenv:Envelope>"""
    assert body == body_correct
    headers_correct = {
        'Accept-Encoding': 'gzip,deflate',
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction':
            'http://services.agresso.com/QueryEngineService/QueryEngineV200606DotNet'
            '/GetTemplateResultAsXML',

        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Host': 'ubw.unit4cloud.com'
    }

    assert headers == headers_correct


def test_should_upload_ingest_success():
    # prev last_inserted_doc is smaller than new_doc, should upload.
    new_doc = {
        "reg_period": "201928",
        "used_hrs": "198",
        "_recno": "0",
        "_section": "D",
        "tab": "B"
    }
    last_inserted_doc = "201927"

    res = ubw_poller.should_upload_ingest(new_doc, last_inserted_doc)

    assert res


def test_should_upload_ingest_success2():
    # no prev last_inserted_doc, should upload
    new_doc = {
        "reg_period": "201928",
        "used_hrs": "198",
        "_recno": "0",
        "_section": "D",
        "tab": "B"
    }
    last_inserted_doc = None

    res = ubw_poller.should_upload_ingest(new_doc, last_inserted_doc)

    assert res


def test_should_upload_ingest_fail():
    # last_inserted has a newer doc should not upload.
    new_doc = {
        "reg_period": "201928",
        "used_hrs": "198",
        "_recno": "0",
        "_section": "D",
        "tab": "B"
    }
    last_inserted_doc = "201929"

    res = ubw_poller.should_upload_ingest(new_doc, last_inserted_doc)

    assert res is False


def test_should_upload_ingest_fail2():
    # tab == A should not upload.
    new_doc = {
        "reg_period": "201928",
        "used_hrs": "198",
        "_recno": "0",
        "_section": "D",
        "tab": "A"
    }
    last_inserted_doc = "201926"

    res = ubw_poller.should_upload_ingest(new_doc, last_inserted_doc)

    assert res is False


def test_should_upload_ingest_fail3():
    # Same reg_period should not upload
    new_doc = {
        "reg_period": "201928",
        "used_hrs": "198",
        "_recno": "0",
        "_section": "D",
        "tab": "B"
    }
    last_inserted_doc = "201928"

    res = ubw_poller.should_upload_ingest(new_doc, last_inserted_doc)

    assert res is False


def test_should_upload_ingest_fail4():
    # butchered new_doc should not upload.
    new_doc = {
        "reg_period": "201928",
        "used_hrs": "198",
        "_recno": "0",
        "_section": "D",
    }
    last_inserted_doc = "201926"

    res = ubw_poller.should_upload_ingest(new_doc, last_inserted_doc)

    assert res is False


def test_should_upload_ingest_fail5():
    # tab == A should not upload, even if there is no last_inserted_doc
    new_doc = {
        "reg_period": "201928",
        "used_hrs": "198",
        "_recno": "0",
        "_section": "D",
        "tab": "A"
    }
    last_inserted_doc = None

    res = ubw_poller.should_upload_ingest(new_doc, last_inserted_doc)

    assert res is False
