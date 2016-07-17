from bs4 import BeautifulSoup
import urllib2

appStores = {
'Argentina':          143505,
'Australia':          143460,
'Belgium':            143446,
'Brazil':             143503,
'Canada':             143455,
'Chile':              143483,
'China':              143465,
'Colombia':           143501,
'Costa Rica':         143495,
'Croatia':            143494,
'Czech Republic':     143489,
'Denmark':            143458,
'Deutschland':        143443,
'El Salvador':        143506,
'Espana':             143454,
'Finland':            143447,
'France':             143442,
'Greece':             143448,
'Guatemala':          143504,
'Hong Kong':          143463,
'Hungary':            143482,
'India':              143467,
'Indonesia':          143476,
'Ireland':            143449,
'Israel':             143491,
'Italia':             143450,
'Korea':              143466,
'Kuwait':             143493,
'Lebanon':            143497,
'Luxembourg':         143451,
'Malaysia':           143473,
'Mexico':             143468,
'Nederland':          143452,
'New Zealand':        143461,
'Norway':             143457,
'Osterreich':         143445,
'Pakistan':           143477,
'Panama':             143485,
'Peru':               143507,
'Phillipines':        143474,
'Poland':             143478,
'Portugal':           143453,
'Qatar':              143498,
'Romania':            143487,
'Russia':             143469,
'Saudi Arabia':       143479,
'Schweiz/Suisse':     143459,
'Singapore':          143464,
'Slovakia':           143496,
'Slovenia':           143499,
'South Africa':       143472,
'Sri Lanka':          143486,
'Sweden':             143456,
'Taiwan':             143470,
'Thailand':           143475,
'Turkey':             143480,
'United Arab Emirates'  :143481,
'United Kingdom':     143444,
'United States':      143441,
'Venezuela':          143502,
'Vietnam':            143471,
'Japan':              143462,
'Dominican Republic': 143508,
'Ecuador':            143509,
'Egypt':              143516,
'Estonia':            143518,
'Honduras':           143510,
'Jamaica':            143511,
'Kazakhstan':         143517,
'Latvia':             143519,
'Lithuania':          143520,
'Macau':              143515,
'Malta':              143521,
'Moldova':            143523,
'Nicaragua':          143512,
'Paraguay':           143513,
'Uruguay':            143514
}





def getAppStoreRatings(store = 143460, appID = 555523050, outputfile = "guvera_australia.html"):
    # default store is AU
    # default appID is Guvera
    # default output file is "guvera_australia.html"

    with open(outputfile, "a") as myfile:
        myfile.write("<ul>")
        myfile.close()
        pageNumber = 0;
        content_type = 'application/x-apple-plist'
        user_agent = 'iTunes/12.2.1 (Macintosh; OS X 10.10.4) AppleWebKit/600.7.12'
        cookie = 'groupingPillToken=1_iphone; mz_user_info_version=0; seoReferrer=https%3A//www.google.com.au/; X-JS-SP-TOKEN=IAaT8zpzHtEhXfw1bXfD/g==; X-JS-TIMESTAMP=1437715945; mzf_in=412280; ds01=A2957FAA7D758512DD2D0F3C00A4DA168BC2DFE252A14D3516357831F2619300FCCF4A934B47B42BE51D346953899F58B0AFB0803BCD287571400E548000BD63; dslang=US-EN; itspod=41; mz_at0-8351443988=AwQAAAEBAAHViQAAAABVscSQp7grSCHsm2LVWp64wIp3if6NZgo=; mz_at_ssl-8351443988=AwUAAAEBAAHViQAAAABVscSQynQ7sIjHhSLfACHAA/Z7PhETw7c=; ns-mzf-inst=178-253-80-151-107-8129-412280-41-st13; s_fid=097D6C6F76269743-38E5AAB904FA8C45; s_vi=[CS]v1|2AB5D40985012F65-40000117000F283E[CE]; s_vnum_n2_us=4%7C1%2C19%7C3; X-Dsid=8351443988; xp_ci=3z498FN7z3TYz4UfzCx3z54QmxmnZ'

        #keep looping until there's no more reviews HACKY but works :)
        while True:
            headers = { 'User-Agent' : user_agent, 'Cookie' : cookie, 'Content-Type' : content_type, 'X-Apple-Tz': '-18000', 'X-Apple-Store-Front': store}
            iOS_url = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%d&pageNumber=%d&sortOrdering=2&type=Purple+Software" % (appID, pageNumber)
            iOS_request = urllib2.Request(iOS_url, headers=headers)
            iOS_page = urllib2.urlopen(iOS_request)
            iOS_soup = BeautifulSoup(iOS_page.read(), "html.parser")
            iOS_ratings = iOS_soup.findAll('textview', {'leftinset':'0', 'rightinset':'0', 'styleset':'normal11'})

            with open(outputfile, "a") as myfile:
                for rating in iOS_ratings:
                    a = rating.get_text().encode('utf-8').strip()
                    myfile.write("<li>" + a + "</li>")
                myfile.close()
            pageNumber += 1

            #print the page number so we can see the progress
            print pageNumber

    with open(outputfile, "a") as myfile:
        myfile.write("</ul>")
        myfile.close()

#Change these to the app & country you want the ratings for below example is spotify USA
print getAppStoreRatings(store=143441, appID=324684580, outputfile = "spotify_usa.html")


