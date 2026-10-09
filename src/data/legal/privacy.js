// Privacy Policy — document content
//
// Body copy in this file was ported VERBATIM from the live site
// (https://withotter.com/privacy-policy) on 2026-10-08 by extracting the
// rendered DOM of <main id="main"> — no paraphrasing, summarising,
// rewriting or added clauses. The `<br>` / " - " pseudo-list structure of
// the original is preserved exactly (see CONTENT NOTES below).
//
// ⚠️  This is operative legal text. It MUST be reviewed and signed off by
//     whoever owns legal/content at With Otter before any real deployment.
//     Do not edit it to "clean it up" — edit it only as a deliberate
//     content decision.
//
// CONTENT NOTES / deliberate deviations from the live DOM:
//  - The live page fakes every list inside a single <p> using <br> separators
//    and " - " prefixes (zero <ul>/<ol>/<li>/<table> on the page). That
//    structure is reproduced as-is here to preserve the original's exact
//    vertical rhythm.
//  - Inline run model: a plain string is a text run, BR is a <br>, and an
//    object { tag, children, href?, target?, id? } is an inline element
//    (<strong>, <em>, <a>, …).
//
// Shape:
//   intro:    { eyebrowTag, eyebrow: Run[], paragraphs: Run[][] }
//   sections: { heading, paragraphs: Run[][] }[]

/** Marker object for a <br> inside an inline run list. */
export const BR = { br: true }

export const privacyPolicy = {
  intro: {
    eyebrowTag: "h2",
    eyebrow: [
      "Effective date: October 10, 2021"
    ],
    paragraphs: [
      [
        "Thank you for using Otter! Our mission is to create a world in which every child has access to quality childcare and stay-at-home parents are empowered to access new economic opportunity for their family. With Other, Inc. (“Otter,” “we,” “us,” or “our”) knows you care about how your personal information is used and shared, and we take your privacy seriously. In this Privacy Policy (“Policy”), we describe the information we collect, how we use it, when and with whom we share it, and your choices. This Policy applies to all sites, mobile applications, and other online services (collectively, “Platform”) made available by Otter. Undefined capitalized terms used herein shall have the definitions as set forth in our Terms of Use.",
        BR,
        BR,
        "By using or accessing the Platform in any manner, you acknowledge that you accept the practices and policies outlined in this Policy, and you hereby consent that we will collect, use, and share your information in the following ways. If you do not agree to this Policy, please do not access or use the Platform."
      ]
    ]
  },
  sections: [
    {
      heading: "The information we collect",
      paragraphs: [
        [
          "How we collect and store information depends on how you access and use the Platform. We collect information in multiple ways including when you provide information directly to us, when you permit third parties to provide information to us, and when we passively collect information from you, such as information collected from your browser or device.",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "a. Information You Provide Directly to Us",
              BR
            ]
          },
          "We may collect information that you provide directly to us, such as when:",
          BR,
          "- You register for an Account on the Platform;",
          BR,
          "- You use the Platform, such as when you view available Listings, enroll in Childcare Services, or offer Childcare Services;",
          BR,
          "- You participate in surveys or fill out forms;",
          BR,
          "- You subscribe to newsletters;",
          BR,
          "- You register for promotions;",
          BR,
          "- You transmit User Content to us;",
          BR,
          "- You request customer support and/or technical assistance; and",
          BR,
          "- You otherwise communicate with us or with others through the Platform.",
          BR,
          BR,
          "The information you provide directly to us may concern you or others and may include, but is not limited to:",
          BR,
          "- Account Information: We may collect information associated with your creation of an Account, such as your name, email address, phone number, birthdate, address, social security number, driver’s license number, immunization records, and occupation.",
          BR,
          "- Information Regarding Children: We may collect the name of your child(ren), birth date, and other information regarding your child(ren), including without limitation immunization records and health information.",
          BR,
          "- Communications: We may collect communications you make on or through the Platform, including communications between you and other users of the Platform.",
          BR,
          "‍",
          BR,
          "You are not required to provide us with such information, but certain features of the Platform may not be accessible or available, absent the provision of the requested information.",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "b. Information From Affiliates and Non-Affiliated Third Parties",
              BR
            ]
          },
          "We may collect information about you or others through our affiliates or through non-affiliated third parties. For example, to the extent permitted by law, we may, in our sole discretion, ask for and collect supplemental information from third parties, such as information about your credit from a credit bureau, or information to verify your identity or trustworthiness, or for other fraud or safety protection purposes. We may combine information that we collect from you through the Platform with information that we obtain from such third parties and information derived from any other products or services we provide.",
          BR,
          BR,
          {
            tag: "em",
            children: [
              "Social Networks"
            ]
          },
          ". We may also allow you to access the Platform through a social networking account, such as Facebook. If you access the Platform through your Facebook account, you may allow us to have access to certain information in your Facebook profile. This may include your name, profile picture, gender, networks, user IDs, list of friends, location, date of birth, email address, photos, videos, people you follow and/or who follow you, and/or your posts or \"likes.\" Social networking sites, such as Facebook, have their own policies for handling your information. For a description of how these sites may use and disclose your information, including any information you make public, please consult the sites' privacy policies. We have no control over how any third-party site uses or discloses the personal information it collects about you.",
          BR,
          BR,
          {
            tag: "em",
            children: [
              "Text Messages Between Members"
            ]
          },
          ". If you send text messages with a Member (i.e. Care Seeker or Care Provider) using the telephone number for that Member available on the Platform, we may use a third-party service provider to track these text messages. We track these text messages for fraud prevention, to ensure appropriate charging of Fees, to enforce our Terms of Use, and for quality and training purposes. As part of this process, Otter and its service provider will receive in real time and store data about your text message, including the date and time of the text message, your phone number, and the content of the text message.",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "c. Information We Collect Automatically",
              BR
            ],
            id: "information-we-collect-automatically"
          },
          {
            tag: "em",
            children: [
              "Device/Usage Information"
            ]
          },
          ". We and our third-party service providers, which include ad networks and analytics companies such as Google Analytics, may use cookies, web beacons, and other tracking technologies to collect information about the computers or devices (including mobile devices) you use to access the Platform. As described further below, we may collect and analyze information including but not limited to (a) browser type; (b) ISP or operating system; (c) domain name; (d) access time; (e) referring or exit pages; (f) page views; (g) IP address; (h) unique device identifiers (e.g. IDFA or Android ID); and (i) the type of device that you use. We may also track when and how frequently you access or use the Platform, including how you engage with or navigate our website or mobile application. We use this information (including the information collected by our third-party service providers) for analytics (including to determine which portions of the Platform are used most frequently and what our users like/do not like), to assist in determining relevant advertising (both on and off the Platform), to evaluate the success of our advertising campaigns and our Platform, and as otherwise described in this Policy.",
          BR,
          BR,
          {
            tag: "em",
            children: [
              "Cookies and Other Electronic Technologies"
            ]
          },
          ". We and our third-party service providers may use cookies, clear GIFs, pixel tags, and other technologies that help us better understand user behavior, personalize preferences, perform research and analytics, and improve the Platform. These technologies, for example, may allow us to tailor the Platform to your needs, save your password in password-protected areas, track the pages you visit, help us manage content, and compile statistics about usage of our Platform. We or our third-party service providers also may use certain of these technologies in emails to our customers to help us track email response rates, identify when our emails are viewed, and track whether our emails are forwarded.",
          BR,
          BR,
          "You can choose to accept or decline cookies. Most web browsers automatically accept cookies, but your browser may allow you to modify your browser settings to decline cookies if you prefer. If you disable cookies, you may be prevented from taking full advantage of the Platform, because the Platform may not function properly. As we adopt additional technologies, we may also gather additional information through other methods.",
          BR,
          BR,
          {
            tag: "em",
            children: [
              "Location Information"
            ]
          },
          ". When you use the Platform, we may collect general location information (such as general location inferred from an IP address). If you install our mobile app, we may ask you to grant us access to your mobile device's geolocation data. If you grant such permission, we may collect information about your precise geolocation, and we may use that information in accordance with this Policy, including to improve the Platform, and providing you with location-based features. If you access the Platform through a mobile device and you do not want your device to provide us with location-tracking information, you can disable the GPS or other location-tracking functions on your device, provided your device allows you to do this. See your device manufacturer's instructions for further details. If you disable certain functions, you may be unable to use certain parts of the Platform.",
          BR
        ]
      ]
    },
    {
      heading: "How We Use the Information We Collect",
      paragraphs: [
        [
          "We use your information for business and commercial purposes, such as the following reasons:",
          BR,
          "- For the purposes for which you provided it;",
          BR,
          "- To enable you to use the services available through the Platform, including registering you for an Account;",
          BR,
          "- To verify your identity and authority to use our Platform;",
          BR,
          "- For customer support and to respond to your inquiries;",
          BR,
          "- To communicate with you, including to send you emails about products and services that may interest you;",
          BR,
          "- For internal record-keeping purposes;",
          BR,
          "- To analyze and improve the Platform or any other products and services we provide;",
          BR,
          "- To administer surveys, sweepstakes, promotions, or contests;",
          BR,
          "- To improve and maintain the Platform and for product development;",
          BR,
          "- To protect the safety and/or integrity of our users, employees, third parties, members of the public, and/or the Platform;",
          BR,
          "- With your consent, to contact you by text message regarding certain services or information you have requested;",
          BR,
          "- To manage and remember your preferences and personalize the Platform;",
          BR,
          "- To track fees and process billing and payment including sharing with third-party payment gateways and payment service providers in connection with the Platform;",
          BR,
          "- To comply with our legal obligations or as permitted by law;",
          BR,
          "- To administer and troubleshoot the Platform;",
          BR,
          "- For other research and analytical purposes; ",
          BR,
          "- To resolve disputes, or to protect ourselves, members of the public, or other users of the Platform; and ",
          BR,
          "- To enforce any legal terms that govern your use of the Platform.",
          BR,
          BR,
          "We may combine information that we collect from you through the Platform with information that we obtain from affiliated and nonaffiliated third parties, and information derived from any other products or services we provide.",
          BR,
          BR,
          "We may aggregate and/or de-identify information collected through the Platform. We may use de-identified or aggregated data for any purpose, including without limitation for research and marketing purposes and may also share such data with any third parties at our discretion.",
          BR,
          BR,
          "We may, either directly or through third parties we engage to provide services to us, review, scan, or analyze your communications with other users exchanged via the Platform or as otherwise described in this Policy for fraud prevention, risk assessment, regulatory compliance, investigation, product development, research, and customer support purposes. For example, as part of our fraud prevention efforts, we may scan and analyze messages to prevent fraud or improper actions. We may also scan, review, or analyze messages for research and product development purposes, as well as to debug, improve and expand product offerings. By using the Platform or engaging in off-Platform communications tracked by Otter, you consent that Otter, in its sole discretion, may, either directly or through third parties we engage to provide services to us, review, scan, analyze, and store your communications, whether done manually or through automated means.",
          BR,
          BR,
          BR,
          BR
        ]
      ]
    },
    {
      heading: "When Otter Shares Your Information",
      paragraphs: [
        [
          "We may share or disclose information in the following ways:",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Affiliates"
            ]
          },
          ". We may share your information with any of our affiliates.",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Consent/At Your Direction"
            ]
          },
          ". We may disclose your information to nonaffiliated third parties based on your consent to do so. Such consent includes the disclosure of your information (a) in order to facilitate inquiries or Bookings for Childcare Services, including sharing your profile information that is publicly available; (b) when we have your permission; or (c) as described in this Policy, the Terms of Use, or any other legal terms governing your use of the Platform.",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Vendors"
            ]
          },
          ". We provide access to or share your information with select third parties who perform services on our behalf. They provide a variety of services to us, including data storage, analytics, billing, marketing, product content and features, customer service, data storage, security, fraud prevention, and legal services.",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Protection of Otter and Others"
            ]
          },
          ". We may share or disclose certain information if we believe in good faith that doing so is necessary or appropriate to (i) protect or defend the rights, safety, or property of Otter or third parties, including to defend or enforce this Policy, our Terms of Use, or any other contractual arrangement or (ii) respond to your requests for customer service; and/or (iii) protect the rights, property or personal safety of Otter, its agents and affiliates, its employees, users and/or the public.",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Legal Requirements"
            ]
          },
          ". We may share or disclose certain information if we believe in good faith that doing so is necessary or appropriate to comply with any law enforcement, legal, or regulatory process, such as to respond to a warrant, subpoena, court order, or other applicable laws and regulations.",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Business Transfer"
            ]
          },
          ". We may share or disclose certain information, in connection with or during negotiations of any merger, sale of company assets, financing, or acquisition of all or a portion of our business to another company.",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Aggregate/Anonymous Information"
            ]
          },
          ". From time to time, we may share aggregate/anonymous information about use of the Platform, such as by creating reports on usage trends. The sharing of such data is unrestricted.",
          BR,
          "‍",
          BR,
          "We invite you to post User Content on or through our Platform, including, but not limited to, your comments, pictures, profile, and any other information. However, please be careful and responsible whenever you are online. If you choose to post User Content on or through the Platform, such as through Member-to-Member messaging or through our review boards, forums, blogs, or other postings, that information: (a) may be or may become publicly available; (b) may be collected and used by third parties with or without our knowledge; and (c) may be used in a manner that may violate this Policy, the law, or your personal privacy.",
          BR,
          BR,
          BR,
          BR
        ]
      ]
    },
    {
      heading: "Online Analytics and Tailored Advertising",
      paragraphs: [
        [
          {
            tag: "strong",
            children: [
              "a. Analytics",
              BR
            ]
          },
          "We may use third-party web analytics services on the Platform, such as those of Google Analytics. These service providers use the sort of technology described in the ",
          {
            tag: "a",
            children: [
              "“Information We Collect Automatically”"
            ],
            href: "#"
          },
          " section above to help us analyze how users use the Platform, including by noting the third-party website from which you arrive. The information collected by the technology will be disclosed to or collected directly by these service providers, who use the information to evaluate your use of the Platform. We may also use Google Analytics for certain purposes related to advertising, as described in the following section. To prevent Google Analytics from using your information for analytics, you may install the ",
          {
            tag: "a",
            children: [
              "Google Analytics Opt-Out Browser Add-on"
            ],
            href: "https://tools.google.com/dlpage/gaoptout"
          },
          ".",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "b. Tailored Advertising",
              BR
            ]
          },
          "Third parties whose products or services are accessible or marketed via the Platform may also place cookies or other tracking technologies on your computer, mobile phone, or other device to collect information about your use of the Platform in order to (a) inform, optimize, and serve marketing content based on past visits to our websites and other sites and (b) report how our marketing content impressions, other uses of marketing services, and interactions with these marketing impressions and marketing services are related to visits to our websites. We also allow other third parties (e.g., ad networks and ad servers such as Google Analytics, DoubleClick, Facebook and others) to serve tailored marketing to you and to access their own cookies or other tracking technologies on your computer, mobile phone, or other device you use to access the Platform. We neither have access to, nor does this Policy govern, the use of cookies or other tracking technologies that may be placed on your computer, mobile phone, or other device you use to access the Platform by non-affiliated, third-party ad technology, ad servers, ad networks or any other non-affiliated third parties. Those parties that use these technologies may offer you a way to opt out of targeted advertising as described below. You may receive tailored advertising on your computer through a web browser. Cookies may be associated with de-identified data linked to or derived from data you voluntarily have submitted to us (e.g., your email address) that we may share with a service provider in hashed, non-human-readable form.",
          BR,
          BR,
          "If you are interested in more information about tailored browser advertising and how you can generally control cookies from being put on your computer to deliver tailored marketing, you may visit the ",
          {
            tag: "a",
            children: [
              "Network Advertising Initiative's Consumer Opt-Out Link"
            ],
            href: "http://www.networkadvertising.org/choices"
          },
          " and/or the",
          {
            tag: "a",
            children: [
              " Digital Advertising Alliance's Consumer Opt-Out Link"
            ],
            href: "http://www.aboutads.info/choices"
          },
          " to opt-out of receiving tailored advertising from companies that participate in those programs. To opt out of Google Analytics for Display Advertising or customize Google Display Network ads, you can visit the ",
          {
            tag: "a",
            children: [
              "Google Ads Settings page"
            ],
            href: "https://www.google.com/settings/ads"
          },
          ". Please note that to the extent advertising technology is integrated into the Platform, you may still receive advertising content even if you opt out of tailored advertising. In that case, the advertising content will just not be tailored to your interests. Also, we do not control any of the above opt-out links and are not responsible for any choices you make using these mechanisms or the continued availability or accuracy of these mechanisms. If your browsers are configured to reject cookies when you visit this opt-out page, or you subsequently erase your cookies, use a different computer or change web browsers, your NAI or DAA opt-out may no longer be effective. Additional information is available on NAI's and DAA's websites, accessible by the above links.",
          BR,
          BR,
          "When using a mobile application you may also receive tailored in-application advertising content. Each operating system-iOS for Apple devices, Android for Android devices, and Windows for Microsoft devices-provides its own instructions on how to prevent the delivery of tailored in-application marketing content. You may review the support materials and/or the privacy settings for the respective operating systems in order to opt-out of tailored in-application advertising. For any other devices and/or operating systems, please visit the privacy settings for the applicable device or contact the applicable platform operator.",
          BR,
          BR,
          BR
        ]
      ]
    },
    {
      heading: "Children's privacy",
      paragraphs: [
        [
          "While we may collect information about children under 13 from their parents, guardians, and/or caregivers, the Platform is not designed for minors under the age of 18. As noted in the Terms of Use, we do not knowingly collect or solicit personal information from anyone under the age of 13. If you are under 13, please do not attempt to register for the Platform or send any personal information to us. If we learn that we have collected personal information from a child under age 13, we will delete that information as required by law. If you believe that a child under 13 may have provided us personal information, please contact us in writing through Otter’s ",
          {
            tag: "a",
            children: [
              "Help Center"
            ],
            href: "http://help.withotter.com/"
          },
          ".",
          BR
        ]
      ]
    },
    {
      heading: "Security of Your Information",
      paragraphs: [
        [
          "Otter implements technical, administrative, and physical safeguards to protect the information provided via the Platform from loss, misuse, and unauthorized access, disclosure, alteration, or destruction. However, no Internet or email transmission is ever fully secure or error free. Therefore, we do not promise and cannot guarantee, and thus you should not expect, that your personal information or communications will not be collected, disclosed and/or used by others. You should take steps to protect against unauthorized access to your password, phone, and computer by, among other things, signing off after using a shared computer, choosing a robust password that nobody else knows or can easily guess, keeping your log-in and password private, and not recycling passwords from other websites or accounts. Otter is not responsible for the unauthorized use of your information nor for any lost, stolen, or compromised passwords, or for any activity on your Account via unauthorized password activity.",
          BR
        ]
      ]
    },
    {
      heading: "Links to External Sites and Services",
      paragraphs: [
        [
          "The Platform may contain links to third-party websites or services. We are not responsible for the content or practices of those websites or services. The collection, use, and disclosure of your information will be subject to the privacy policies of the third-party websites or services, and not this Policy. We urge you to read the privacy and security policies of these third parties.",
          BR
        ]
      ]
    },
    {
      heading: "Your Choices",
      paragraphs: [
        [
          "You have certain rights or choices with respect to your information such as:",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Account Information"
            ]
          },
          ": You may access your Account to access and, in some cases, edit or remove certain information. This may include your (1) name and password; (2) email address; (3) phone number; (4) address; and (5) other user profile information. The information you can view, update, and remove may change as the features of the Platform change. Some of the information in your Account such as your location, phone number, address, email address, and user profile information, may be visible to other user with whom you have Bookings.",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Marketing Communications"
            ]
          },
          ". You can unsubscribe from marketing emails by following the directions in those emails. Please note that it may take up to 10 business days for us to process opt-out requests. If you opt out of receiving emails about recommendations or other information we think may interest you, we may still send you emails about your Account or any services you have requested or received from us.",
          BR,
          "- ",
          {
            tag: "em",
            children: [
              "Cookies & Analytics"
            ]
          },
          ": You can opt out of certain cookie-related and analytics processing by following the instructions in this Policy.",
          BR
        ]
      ]
    },
    {
      heading: "California Do-Not-Track Disclosure",
      paragraphs: [
        [
          "Otter is committed to providing you with meaningful choices about the information collected on our Platform for third party purposes. That is why we have provided links (above) to the NAI opt-out link, the DAA opt-out link, and a Google opt-out link. However, Otter does not currently recognize or respond to browser-initiated Do-Not-Track signals, as the Internet industry is currently still working on Do-Not-Track standards, implementations, and solutions.",
          BR
        ]
      ]
    },
    {
      heading: "Consent to Transfer",
      paragraphs: [
        [
          "Our computer systems are currently based in the United States, so your personal information will be processed by us in the United States, where data protection and privacy regulations may not offer the same level of protection as in other parts of the world. By using the Platform, you agree to this Policy and you consent to the transfer of all such information to the United States, which may not offer a level of protection equivalent to that required in the European Union or certain other countries, and to the processing of that information as described in this Policy.",
          BR
        ]
      ]
    },
    {
      heading: "Changes to This Privacy Policy",
      paragraphs: [
        [
          "We may change this Policy to reflect changes in the law, our information practices, or the features of the Platform. The Policy will indicate the date of the most recent update. If we make a material change to the Policy, you will be provided with appropriate notice in accordance with legal requirements. By continuing to use the Platform, you are confirming that you have read and understood the latest version of this Policy.",
          BR
        ]
      ]
    },
    {
      heading: "Contact Us",
      paragraphs: [
        [
          "If you have any questions about the Policy or the Platform, please contact us in writing through Otter’s ",
          {
            tag: "a",
            children: [
              "Help Center"
            ],
            href: "http://help.withotter.com/"
          },
          ".",
          BR
        ]
      ]
    }
  ]
}

export default privacyPolicy
