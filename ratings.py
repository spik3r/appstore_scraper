__author__ = 'Kai'
from bs4 import BeautifulSoup
import urllib2

#iOS
iTunesStores = {
        "143441": "United States",
        "143505": "Argentina",
        "143460": "Australia",
        "143446": "Belgium",
        "143503": "Brazil",
        "143455": "Canada",
        "143483": "Chile",
        "143465": "China",
        "143501": "Colombia",
        "143495": "Costa Rica",
        "143494": "Croatia",
        "143489": "Czech Republic",
        "143458": "Denmark",
        "143443": "Deutschland",
        "143506": "El Salvador",
        "143454": "Espana",
        "143447": "Finland",
        "143442": "France",
        "143448": "Greece",
        "143504": "Guatemala",
        "143463": "Hong Kong",
        "143482": "Hungary",
        "143467": "India",
        "143476": "Indonesia",
        "143449": "Ireland",
        "143491": "Israel",
        "143450": "Italia",
        "143466": "Korea",
        "143493": "Kuwait",
        "143497": "Lebanon",
        "143451": "Luxembourg",
        "143473": "Malaysia",
        "143468": "Mexico",
        "143452": "Nederland",
        "143461": "New Zealand",
        "143457": "Norway",
        "143445": "Osterreich",
        "143477": "Pakistan",
        "143485": "Panama",
        "143507": "Peru",
        "143474": "Phillipines",
        "143478": "Poland",
        "143453": "Portugal",
        "143498": "Qatar",
        "143487": "Romania",
        "143469": "Russia",
        "143479": "Saudi Arabia",
        "143459": "Schweitz/Suisse",
        "143464": "Singapore",
        "143496": "Slovakia",
        "143499": "Slovenia",
        "143472": "South Africa",
        "143486": "Sri Lanka",
        "143456": "Sweden",
        "143470": "Taiwan",
        "143475": "Thailand",
        "143480": "Turkey",
        "143481": "United Arab Emirates",
        "143444": "United Kingdom",
        "143502": "Venezuela",
        "143471": "Vietnam",
        "143462": "Japan"
    }

def getAppStoreRatings(allStores = False):
        #get app store ratings
        # getAppStoreRatings(allStores = False) - gets AU ratings
        # getAppStoreRatings(allStores = True) - gets World wide ratings
        #setup stuff
        iOSRatings = {}
        appID = "555523050" #Guvera appID
        content_type = 'application/x-apple-plist'
        user_agent = 'iTunes/12.2.1 (Macintosh; OS X 10.10.4) AppleWebKit/600.7.12'
        cookie = 'groupingPillToken=1_iphone; mz_user_info_version=0; seoReferrer=https%3A//www.google.com.au/; X-JS-SP-TOKEN=IAaT8zpzHtEhXfw1bXfD/g==; X-JS-TIMESTAMP=1437715945; mzf_in=412280; ds01=A2957FAA7D758512DD2D0F3C00A4DA168BC2DFE252A14D3516357831F2619300FCCF4A934B47B42BE51D346953899F58B0AFB0803BCD287571400E548000BD63; dslang=US-EN; itspod=41; mz_at0-8351443988=AwQAAAEBAAHViQAAAABVscSQp7grSCHsm2LVWp64wIp3if6NZgo=; mz_at_ssl-8351443988=AwUAAAEBAAHViQAAAABVscSQynQ7sIjHhSLfACHAA/Z7PhETw7c=; ns-mzf-inst=178-253-80-151-107-8129-412280-41-st13; s_fid=097D6C6F76269743-38E5AAB904FA8C45; s_vi=[CS]v1|2AB5D40985012F65-40000117000F283E[CE]; s_vnum_n2_us=4%7C1%2C19%7C3; X-Dsid=8351443988; xp_ci=3z498FN7z3TYz4UfzCx3z54QmxmnZ'

        if not allStores:
            store = 143460 #set default store to AU
            headers = { 'User-Agent' : user_agent, 'Cookie' : cookie, 'Content-Type' : content_type, 'X-Apple-Tz': '-18000', 'X-Apple-Store-Front': store}
            iOS_url = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&pageNumber=0&sortOrdering=2&type=Purple+Software" % appID
            iOS_request = urllib2.Request(iOS_url, headers=headers)
            iOS_page = urllib2.urlopen(iOS_request)
            iOS_soup = BeautifulSoup(iOS_page.read(), "html.parser")
            iOS_ratings = iOS_soup.findAll('textview', {'leftinset':'5'})
            iOS_ratings = iOS_ratings[0:5]
            iOS_ratings.reverse()
            print "\n iOS Ratings Australia"
            for i, v in enumerate(iOS_ratings):
                iOSRatings[str(i+1)+"star"] = v.string
            version = getiOSVersion()
            iOSRatings['version'] = version


        else:
            #global ratings - hacky!
            oneStar = 0
            twoStar = 0
            threeStar = 0
            fourStar = 0
            fiveStar = 0
            numStars = 0

            globalRatings = [oneStar, twoStar, threeStar, fourStar, fiveStar]
            for country in iTunesStores:
                headers = { 'User-Agent' : user_agent, 'Cookie' : cookie, 'Content-Type' : content_type, 'X-Apple-Tz': '-18000', 'X-Apple-Store-Front': country}
                iOS_url = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&pageNumber=0&sortOrdering=2&type=Purple+Software" % appID
                iOS_request = urllib2.Request(iOS_url, headers=headers)
                iOS_page = urllib2.urlopen(iOS_request)
                iOS_soup = BeautifulSoup(iOS_page.read(), "html.parser")
                iOS_ratings = iOS_soup.findAll('textview', {'leftinset':'5'})
                iOS_ratings = iOS_ratings[0:5]
                iOS_ratings.reverse()
                for i, v in enumerate(iOS_ratings):
                    if numStars > len(globalRatings) - 1:
                        numStars = 0
                    globalRatings[numStars]  += int(v.string)
                    numStars += 1

            print "\n iOS Global Ratings"
            for i, rating in enumerate(globalRatings):
                iOSRatings[str(i+1)+"star"] = str(rating)
            version = getiOSVersion()
            iOSRatings['version'] = version
        return iOSRatings

def getiOSVersion():
        #determine what version Guvera is up too on the iOS App Store
        #returns string

        iOSRatings = {}
        appID = "555523050" #Guvera appID
        content_type = 'application/x-apple-plist'
        user_agent = 'iTunes/12.2.1 (Macintosh; OS X 10.10.4) AppleWebKit/600.7.12'
        cookie = 'groupingPillToken=1_iphone; mz_user_info_version=0; seoReferrer=https%3A//www.google.com.au/; X-JS-SP-TOKEN=IAaT8zpzHtEhXfw1bXfD/g==; X-JS-TIMESTAMP=1437715945; mzf_in=412280; ds01=A2957FAA7D758512DD2D0F3C00A4DA168BC2DFE252A14D3516357831F2619300FCCF4A934B47B42BE51D346953899F58B0AFB0803BCD287571400E548000BD63; dslang=US-EN; itspod=41; mz_at0-8351443988=AwQAAAEBAAHViQAAAABVscSQp7grSCHsm2LVWp64wIp3if6NZgo=; mz_at_ssl-8351443988=AwUAAAEBAAHViQAAAABVscSQynQ7sIjHhSLfACHAA/Z7PhETw7c=; ns-mzf-inst=178-253-80-151-107-8129-412280-41-st13; s_fid=097D6C6F76269743-38E5AAB904FA8C45; s_vi=[CS]v1|2AB5D40985012F65-40000117000F283E[CE]; s_vnum_n2_us=4%7C1%2C19%7C3; X-Dsid=8351443988; xp_ci=3z498FN7z3TYz4UfzCx3z54QmxmnZ'
        store = 143460 #set default store to AU
        headers = { 'User-Agent' : user_agent, 'Cookie' : cookie, 'Content-Type' : content_type, 'X-Apple-Tz': '-18000', 'X-Apple-Store-Front': store}
        iOS_url = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&pageNumber=0&sortOrdering=2&type=Purple+Software" % appID
        iOS_request = urllib2.Request(iOS_url, headers=headers)
        iOS_page = urllib2.urlopen(iOS_request)
        iOS_soup = BeautifulSoup(iOS_page.read(), "html.parser")

        iOS_version = iOS_soup.findAll('setfontstyle', {'normalstyle':'textColor'})
        iOS_version = iOS_version[4].string
        iOS_version = iOS_version[26:31]
        return iOS_version


def getPlayStoreRatingsGlobal():
    #returns global play store ratings
    androidRatings = {}
    versionString = ""
    url = "https://play.google.com/store/apps/details?id=com.guvera.android"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")

    stars = soup.findAll('span',{'class': 'bar-label'})
    ratings = soup.findAll('span',{'class': 'bar-number'})
    version = soup.findAll('div', {'itemprop': 'softwareVersion'})
    versionString = version[0].string
    versionString = str(versionString)
    print versionString
    num_ratings = 5
    ratings.reverse()
    print "Android Global Ratings"
    for i, v in enumerate(ratings):
        androidRatings[str(i+1)+"star"] = v.string

    androidRatings['version'] = versionString
    return androidRatings

print "starting"

print getAppStoreRatings()
print getPlayStoreRatingsGlobal()