import requests

session = requests.session()

data = {
    "userpasswordcredentials.domain": "xxxxxxx",
	"userpasswordcredentials.domainType": "name",
	"userpasswordcredentials.username": "xxxxxxx",
	"userpasswordcredentials.password": "xxxxxxx",
	"userpasswordcredentials.userInfoType": "name",

}

session.post('https://auth.huaweicloud.com/authui/validateUser.action?service=https://auth.huaweicloud.com/idp/sso/SAML2/Unsolicited?entityId=https://ocbiam.inhuawei.com:31943&type=xfederation', 
             data=data)
response = session.get("https://auth.huaweicloud.com/idp/sso/SAML2/Unsolicited?entityId=https://ocbiam.inhuawei.com:31943&type=xfederation")

from HTMLParser import HTMLParser

class MyParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
	    if len(attrs) == 3 and attrs[1][1] == 'SAMLResponse':
		    self.SAMLResponse = attrs[2][1]
			
	def getSAML(self):
	    return self.SAMLResponse
		
mp = MyParser()
mp.feed(response.content)
SAMLResponse = mp.getSAML()

headers = {"Content-Type": "application/x-www-form-urlencoded",
           "X-Idp-Id": "@ALLY_HUAWEICLOUD"}
response = requests.post("https://ocbiam.inhuawei.com:31943/v3.0/OS-FEDERATION/tokens", headers=headers,
                         data={"SAMLResponse": SAMLResponse},
						 verify=False)

print response.headers
