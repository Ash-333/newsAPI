import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup

# Your XML content
xml_content = """
<rss version="2.0"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:atom="http://www.w3.org/2005/Atom"
	xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
	xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
	>
	<channel>
		<title>Online Khabar</title>
		<atom:link href="https://www.onlinekhabar.com/feed" rel="self" type="application/rss+xml" />
		<link>https://www.onlinekhabar.com</link>
		<description>No 1 News Portal from Nepal in Nepali.</description>
		<lastBuildDate>Wed, 13 Sep 2023 17:21:36 +0000</lastBuildDate>
		<language>en-US</language>
		<sy:updatePeriod>
	hourly	</sy:updatePeriod>
		<sy:updateFrequency>
	1	</sy:updateFrequency>
		<generator>https://wordpress.org/?v=6.2.2</generator>
		<image>
			<url>https://www.onlinekhabar.com/wp-content/uploads/2017/05/logo-mobile1-50x50.png</url>
			<title>Online Khabar</title>
			<link>https://www.onlinekhabar.com</link>
			<width>32</width>
			<height>32</height>
		</image>
		<item>
			<content:encoded>
				<![CDATA[<p style="text-align: justify;">२८ भदौ, काठमाडौं । लिबियामा बाढीमा परी ५ हजार बढीको मृत्यु भएको एक जना मन्त्रीले बताएका छन् ।</p><p style="text-align: justify;">लिबियाका एकजना मन्त्री हिशाम चकियोतले ५ हजार ३०० जनाको मृत्यु भएको बीबीसीसँग बताएका हुन् । आपतकालीन उद्धारमा खटिएका अधिकारीहरुले १० हजार जना बेपत्ता भएको र ३० हजार जना मानिस विस्थापित भएको बताएका छन् ।</p><p style="text-align: justify;">डेनियल नामको आँधीका कारण आइतबार राति डेर्नामा सुनामी जस्तो बाढी आएको थियो । उक्त बाढीले करिब एक लाख जनसंख्या रहेको डेर्ना शहरको धेरै इलाकालाई बगाएर समुद्रमा पुर्&#x200d;याएको समाचार एजेन्सीहरुले जनाएका छन् ।</p><p style="text-align: justify;">डेर्नाको तटीय क्षेत्रमा बाढीले दुईवटा बाँध र चारवटा पुलहरु भत्काएको छ । त्यसपछि बस्तीमा बाढी पसेर क्षति पुगेको बीबीसीले जनाएको छ ।</p><p><img decoding="async" loading="lazy" class="size-full wp-image-1365542 aligncenter" src="https://www.onlinekhabar.com/wp-content/uploads/2023/09/Libya-Flood_death-Body.jpg" alt="" width="1230" height="692" srcset="https://www.onlinekhabar.com/wp-content/uploads/2023/09/Libya-Flood_death-Body.jpg 1230w, https://www.onlinekhabar.com/wp-content/uploads/2023/09/Libya-Flood_death-Body-500x281.jpg 500w, https://www.onlinekhabar.com/wp-content/uploads/2023/09/Libya-Flood_death-Body-1024x576.jpg 1024w, https://www.onlinekhabar.com/wp-content/uploads/2023/09/Libya-Flood_death-Body-768x432.jpg 768w" sizes="(max-width: 1230px) 100vw, 1230px" /></p><p style="text-align: justify;">बाढीले सबैभन्दा बढी क्षति डेर्ना शहरमा पुगेको छ । त्यहाँ फेला परेका लाशहरुलाई मेसिनको सहायताले ठूलो खाल्डो खनेर एकै ठाउँ गाडिएको छ । बोरा र कम्बलहरुमा बेरिएका शवहरुलाई सामूहिक चिहानमा समाधिस्थ गरिएको हृदयविदारक दृष्य देखिएको बीबीसीले जनाएको छ ।</p><p style="text-align: justify;">जनजीवन अस्तव्यस्त भएका कारण क्षतिको विवरण संकलन गर्नसमेत उद्धारकर्तालाई हम्मेहम्मे परेको बीबीसीले जनाएको छ । विवरण संकलनको काम जारी रहेकाले बाढीमा परी मृत्यु हुनेको संख्या बढ्न सक्ने अनुमान छ ।</p>
]]>
			</content:encoded>
		</item>
	</channel>
</rss>
"""

# Parse the XML content
root = ET.fromstring(xml_content)

# Find the <content:encoded> element and its text content within CDATA
encoded_content = root.find(".//{http://purl.org/rss/1.0/modules/content/}encoded")

# Check if encoded_content exists
if encoded_content is not None:
    # Extract the text content within CDATA
    cdata_content = encoded_content.text.strip() if encoded_content.text else ""

    # Parse the HTML content within CDATA using BeautifulSoup
    soup = BeautifulSoup(cdata_content, 'html.parser')

    # Find all <img> tags within the HTML content
    img_tags = soup.find_all('img')

    # Extract the 'src' attribute from the first <img> tag (you can loop through all if needed)
    img_src = img_tags[0]['src'] if img_tags else None

    # Print the image URL
    print("Image Source (img_src):", img_src)
else:
    print("No content:encoded element found.")
