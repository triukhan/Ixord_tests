ENDPOINT = "https://stage.ixord.com/api/api/"
ENDPOINT_TAG = "https://stage.ixord.com/api/api/tags/addTag?workspaceId="
ENDPOINT_GTAG = "https://stage.ixord.com/api/api/tags/getTags?workspaceId="
ENDPOINT_LIST = "https://stage.ixord.com/api/api/executions/runOnce"
ENDPOINT_SID = "https://stage.ixord.com/api/api/executions/getExecutionByKey?secureKey="
REFRESH = "&skip=0&count=100&showOnlyUsersExecutions=false&respectToAdminRole=true&type=1&sortByModif=false&respectToSort=true"
ENDPOINT_REFRESH = "https://stage.ixord.com/api/api/executions/getExecutionsByTagIds?status=2&workspaceId="
ENDPOINT_EXECUTE = "https://stage.ixord.com/api/api/defaultExecuteExecution/executeSteps?executionId="
ENDPOINT_EX = "https://stage.ixord.com/api/api/execution/"
ENDPOINT_EXS = "https://stage.ixord.com/api/api/executions/"
ENDPOINT_PRF = "https://stage.ixord.com/api/api/profileEdit/"
ENDPOINT_TMP = "https://stage.ixord.com/api/api/execution/saveAsChecklist?executionId="
ENDPOINT_UP_TMP = "https://stage.ixord.com/api/api/search/searchWorkspaceChecklists?search=&workspaceId="
UP_END = "&skip=0&count=100&allowExecuteOnly=true&loadRelatedData=false&type=1"
END_START = "https://stage.ixord.com/api/api/defaultStartExecution/start?checklistId="


IMAGES = {
        "value": "{\"blocks\":[{\"type\":\"image\",\"data\":{\"file\":{\"url\":\"images/ChecklistImages/64186f053f3bf5c"
        "ec5c134a9/content/Pikachu-SVG-File-Free_b18c57e12c1847d2a14831d0070f0ecc.png\",\"title\":\"png\"}}},{\"type\":"
        "\"image\",\"data\":{\"file\":{\"url\":\"images/ChecklistImages/64186f053f3bf5cec5c134a9/content/maxresdefault_"
        "6ec46c5586ba4819b1602dfadf5595d5.jpg\",\"title\":\"jpg\"}}},{\"type\":\"image\",\"data\":{\"file\":{\"url\":\""
        "images/ChecklistImages/64186f053f3bf5cec5c134a9/content/a2b770611ea9b7b8_d5256f69ecc04aa2be5a8119a14bdfd1"
        ".gif\",\"title\":\"gif\"}}},{\"type\":\"image\",\"data\":{\"file\":{\"url\":\"images/ChecklistImages/64186f053"
        "f3bf5cec5c134a9/content/harry-potter-and-the-goblet-of-fire-yule-ball_7b101ee4cd084a57839f233407fe8ee1.webp\","
        "\"title\":\"webp\"}}}]}"}
ALL_ELEMENTS = {
     "value": "{\"blocks\":[{\"type\":\"attaches\",\"data\":{\"file\":{\"url\":\"images/ChecklistImages/64187b0e0029bae"
     "bb1f21475/content/Pikachu-SVG-File-Free_0d08c7a9430b490e8f6259ccfb9311f8.png\",\"title\":\"Pika\"},\"title\":"
     "\"Pika\"}},{\"type\":\"paragraph\",\"data\":{\"text\":\"PIKA\"}},{\"type\":\"step\",\"data\":{\"title\":\"PIKA\","
     "\"done\":false}},{\"type\":\"header\",\"data\":{\"text\":\"PIKA\",\"level\":2}},{\"type\":\"list\",\"data\":"
     "{\"style\":\"ordered\",\"items\":[\"PIKA\",\"PIKA\",\"PIKA\"]}},{\"type\":\"image\",\"data\":{\"file\":{\"url\":"
     "\"images/ChecklistImages/64187b0e0029baebb1f21475/content/Pikachu-SVG-File-Free_2cca3351acf74ff99350b1017940a"
     "597.png\",\"title\":\"Pika\"}}},{\"type\":\"table\",\"data\":{\"withHeadings\":false,\"content\":[]}}]}"}
PRF_TOKEN = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMzciLCJqdGkiOiI1YzQwYzhlNC0zZTNm"
                              "LTQ4NTMtYmMyMi0xOWI5Y2ZiZTE1NmIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYv"
                              "aWRlbnRpdHkvY2xhaW1zL3JvbGUiOiIxIiwiZXhwIjoxNjg0NjU2OTMwLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0"
                              "OjUwMDAiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAifQ._UWQD4T3CB67Ta_LcfpTUV8dniO0zk0_SyJxZ"
                              "tM3dXQ"}
ERR_EMAIL = "The specified string is not in the form required for an e-mail address."
CONNECTION = "mssql+pyodbc://autotest:8sXxyLO@ixs-stage-vm\SQLEXPRESS"
