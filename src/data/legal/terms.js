// Terms of Use — document content
//
// Body copy in this file was ported VERBATIM from the live site
// (https://withotter.com/terms-of-use) on 2026-10-08 by extracting the
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

export const termsOfUse = {
  intro: {
    eyebrowTag: "div",
    eyebrow: [
      "Effective date: October 10, 2021",
      BR,
      "‍",
      BR,
      "‍",
      {
        tag: "strong",
        children: [
          "IMPORTANT NOTICE: THIS AGREEMENT CONTAINS A BINDING ARBITRATION PROVISION AND CLASS ACTION WAIVER. IT AFFECTS YOUR LEGAL RIGHTS AS DETAILED IN THE ARBITRATION AND CLASS ACTION WAIVER SECTION BELOW. PLEASE READ CAREFULLY.",
          BR,
          BR,
          "PLEASE NOTE THAT YOUR USE OF AND ACCESS TO THE PLATFORM (DEFINED BELOW) ARE SUBJECT TO THE FOLLOWING TERMS; IF YOU DO NOT AGREE TO ALL OF THE FOLLOWING, YOU MAY NOT USE OR ACCESS THE PLATFORM IN ANY MANNER."
        ]
      },
      BR
    ],
    paragraphs: []
  },
  sections: [
    {
      heading: "Acceptance of Terms",
      paragraphs: [
        [
          "Thank you for using Otter! Our mission is to create a world in which every child has access to quality childcare and stay-at-home parents are empowered to access new economic opportunity for their family. These Terms of Use (“Terms”) are a binding legal agreement between you and With Otter, Inc. (“Otter,” “we,” “us,” or “our”). Otter offers an online platform that connects users offering childcare (“Care Providers”) with users seeking and using childcare (“Care Seekers”). A person who completes Otter’s account registration process, including Care Seekers and Care Providers, is a “Member.” These Terms govern your use of the websites, applications, and other offerings from Otter (collectively, the “Platform”). ",
          BR,
          BR,
          "By using or otherwise accessing the Platform, or clicking to accept or agree to these Terms where that option is made available, you (1) accept and agree to these Terms, and (2) consent to the collection, use, disclosure and other handling of information as described in our ",
          {
            tag: "a",
            children: [
              "Privacy Policy"
            ],
            href: "https://withotter.com/privacy",
            target: "_blank"
          },
          ".",
          BR,
          BR,
          "All references to “you” or “your,” as applicable, mean the person who accesses, uses, and/or participates in the Platform in any manner, and each of your heirs, assigns, and successors. If you use the Platform on behalf of an entity, you represent and warrant that you have the authority to bind that entity, your acceptance of the Terms will be deemed an acceptance by that entity, and “you” and “your” herein shall refer to that entity, its directors, officers, employees, and agents.",
          BR
        ]
      ]
    },
    {
      heading: "The Otter Platform",
      paragraphs: [
        [
          "Except for Section 21, providing for binding arbitration and waiver of class action rights, Otter reserves the right, at its reasonable and sole discretion, to modify or replace these Terms at any time. The most current version of these Terms will be accessible through the Platform. You shall be responsible for reviewing and becoming familiar with any such modifications. If a revision to the Terms, in our sole discretion, is material, we will notify you by contacting you either through the email address associated with your Account or another messaging system you have associated with our Account. Use of the Platform by you after any modification to the Terms constitutes your acceptance of the Terms as modified.",
          BR,
          BR,
          "Otter reserves the right at any time to modify, suspend, discontinue, or terminate, temporarily or permanently, the Platform or associated services (or any part thereof), with or without notice. Except for refunds for Bookings expressly available to you under these Terms (or as required by law), you agree that Otter shall not be liable to you or any third party for any modification, suspension or discontinuance of the Platform or associated services.",
          BR
        ]
      ]
    },
    {
      heading: "Eligibility",
      paragraphs: [
        [
          "You hereby represent and warrant that you are fully able and competent to enter into the terms, conditions, obligations, affirmations, representations and warranties set forth in these Terms and to abide by and comply with these Terms. Only individuals who are at least 18 years old and can form legally binding contracts under applicable law are permitted to access the Platform or be a Member. Parents may provide us with personal information about their children, but if we learn we have collected personal information from children under 13, we will delete that information in accordance with our legal requirements. If you believe that a child under 13 may have provided us personal information, please contact us in writing through Otter’s ",
          {
            tag: "a",
            children: [
              "Help Center"
            ],
            href: "http://help.withotter.com/"
          },
          ".",
          BR,
          BR,
          "By registering as a Care Provider, Care Providers represent and warrant that they, and the employees, agents, contractors, and subcontractors who may perform work for them, are properly and fully qualified and experienced, and licensed and insured as required by applicable laws or regulations to which they may be subject in the jurisdiction(s) in which they offer Childcare Services.Otter may, for transparency or fraud prevention or detection purposes (directly or through third parties) ask a Member to provide a form of government identification (for example, a driver’s license or passport), date of birth, and other information, or undertake additional checks and processes designed to help verify or check the identities or backgrounds of Members and/or screen Member information against third party databases or other sources. However, we do not make any representations about, confirm, or endorse any Member or the Member’s purported identity or background.",
          BR
        ]
      ]
    },
    {
      heading: "Account Creation",
      paragraphs: [
        [
          "You must create an account (“Account”) to access certain features of the Platform, such as booking Childcare Services or creating a Listing. To create an Account and become a Member, you must select a username and password. You may not select as your username a name that you don’t have the right to use, or another person’s name with the intent to impersonate that person. You agree to provide accurate, current, and complete information during the Account registration process and at all other times when you use the Platform, and to update information to keep it accurate, current, and complete. You are solely responsible for safeguarding your Account password. You are solely responsible for all activity that occurs on your Account, and you will notify Otter immediately of any unauthorized use. For clarity, Otter is not liable for any losses by any party caused by an unauthorized use of your Account. Your Account is nontransferable except with Otter’s written permission and in line with Otter policies and procedures.",
          BR,
          BR,
          "If and as permitted by applicable law, we may, but have no obligation (unless required by law) to (i) ask you to provide identification or other information, (ii) undertake checks designed to help verify your identity or background, (iii) screen you against third-party databases or other sources and request reports from service providers, (iv) obtain reports from public records of criminal convictions or sex offender registrations or their local equivalents, and (v) otherwise request information or obtain information about you (including through an interview if required by applicable law) to protect the safety and security of the Platform, Otter, our users, and the public.",
          BR
        ]
      ]
    },
    {
      heading: "Rules and Prohibitions",
      paragraphs: [
        [
          "As a condition of use, you agree you will not use the Platform for any purpose that is unlawful or prohibited by these Terms, or any other purpose not reasonably intended by Otter. By way of example, and not as a limitation, you agree not to:",
          BR,
          "- create multiple Accounts on the Platform;",
          BR,
          "- use methods to disguise your location or otherwise circumvent Otter’s tools to ensure the safe and efficient operation of the Platform;",
          BR,
          "- use another individual’s account to access the Platform;",
          BR,
          "- abuse, harass, impersonate, intimidate or threaten Members or others;",
          BR,
          "- post or transmit, or cause to be posted or transmitted, any User Content (defined below) that are infringing, libelous, defamatory, abusive, offensive, obscene, pornographic or otherwise violates any law or right of any third party;",
          BR,
          "- use the Platform for any unauthorized purpose, or in violation of any applicable law, including intellectual property laws;post or transmit, or cause to be posted or transmitted, any communication or solicitation designed or intended to obtain password, account, or private information from any Member or other Platform user;",
          BR,
          "- infringe upon the intellectual property rights of Platform, its users, or any third party;submit comments linking to affiliate programs, multi-level marketing schemes, sites repurposing existing stories or off-topic content;",
          BR,
          "- post, email, transmit, upload, or otherwise make available any material that contains software viruses or any other computer code, files or programs designed or functioning to interrupt, destroy, or limit the functionality of any computer software or hardware or telecommunications equipment;",
          BR,
          "- scrape, access, monitor, index, frame, link, or copy any Content or information on the Platform by accessing the Platform in an automated way, using any robot, spider, scraper, web crawler, or using any method of access other than manually accessing the publicly-available portions of the Platform through a browser or accessing the Platform through any approved mobile application, application programming interface, or client application;",
          BR,
          "- violate the restrictions in any robot exclusion headers of the Platform, if any, or bypass or circumvent other measures employed to prevent or limit access to the Platform;",
          BR,
          "- download or use the Platform if you are under the age of 18, regardless of any age rating that is given to the Platform by any third party;",
          BR,
          "- post material that advocates illegal activity or discusses illegal activities with the intent to commit them (in either case as determined by Otter in its sole discretion);",
          BR,
          "- post or otherwise make available any material that contains any software, device, instructions,  computer code, files, programs and/or other Content or feature that is designed to interrupt, destroy or limit the functionality of any computer software or hardware or telecommunications equipment (including without limitation any time bomb, virus, software lock, worm, self-destruction, drop-device, malicious logic, Trojan horse, trap door, \"disabling,\" \"lock out,\" \"metering\" device or any malicious code);",
          BR,
          "- falsely state or otherwise misrepresent your affiliation with a person or entity, or impersonate any person or entity in a manner that does not constitute parody;",
          BR,
          "- through misrepresentation or otherwise, solicit personal or sensitive information from other users such as credit card or financial account information;",
          BR,
          "- violate the law or encourage conduct that would constitute a criminal offense or give rise to civil liability;decompile, reverse engineer, or otherwise attempt to obtain the source code or underlying ideas or information of or relating to the Platform;",
          BR,
          "- as a Care Provider, circumvent a Care Provider’s obligation to collect Fees through the Platform for any care arrangement originally found or arranged through the platform;",
          BR,
          "- as a Care Seeker, circumvent a Care Seeker’s obligation to pay Fees through the Platform for any care arrangement originally found or arranged through the platform;",
          BR,
          "- sign up for, negotiate a price for, use, or otherwise solicit services of a Care Provider with no intention of following through with your use of or payment for the Childcare Services;",
          BR,
          "- falsely imply Otter endorsement, partnership, or otherwise mislead others as to your affiliation with Otter;",
          BR,
          "- use the Platform in a way that violates or facilitates violations of these Terms, any other agreement or any guidelines or policies posted by Otter; orattempt to do any of the foregoing directly or indirectly.",
          BR,
          BR,
          "If you believe that a Member, Listing, or User Content (as defined below) poses an imminent risk of harm to a person or property, you should immediately contact local authorities before contacting Otter. In addition, if you believe that a Member, Listing, or User Content has violated our Terms, you should report your concerns to Otter. If you reported an issue to local authorities, Otter may request a copy of that report. Except as required by law, you agree that we are not obligated to take action in response to any report, though we generally will make efforts to do so.",
          BR,
          BR,
          "Violation of our rules and these Terms may result in the removal of your User Content from the Platform, and/or termination of your Account. You acknowledge and agree that Otter may remove any User Content and terminate any Account at any time for any reason (including, but not limited to, upon receipt of claims or allegations from third parties or authorities relating to such User Content). Otter further reserves the right to report unlawful activity to law enforcement or other regulatory authorities.",
          BR,
          BR,
          "You acknowledge that Otter has the right, but does not have any obligation, to monitor the use of the Platform and verify information provided by our Members. For example, we may review, disable access to, remove, or edit User Content to: (i) operate, secure and improve the Platform (including for fraud prevention, risk assessment, investigation and customer support purposes); (ii) ensure Members’ compliance with these Terms; (iii) comply with applicable law or the order or requirement of a court, law enforcement or other administrative agency or governmental body; (iv) address User Content that we determine is harmful or objectionable; (v) take actions set out in these Terms; and (vi) maintain and enforce any reasonable quality or eligibility criteria, including by removing Listings that don’t meet such reasonable quality and eligibility criteria. Members agree to cooperate with and assist Otter in good faith, and to provide Otter with such information and take such actions as may be reasonably requested by Otter with respect to any investigation undertaken by Otter regarding the use or abuse of the Platform. ",
          BR
        ]
      ]
    },
    {
      heading: "User Content",
      paragraphs: [
        [
          "You may be able to post, upload, publish, submit or transmit information to or through the Platform (“User Content”). Some User Content may be viewable by Members and/or other users. Except as explicitly limited herein, by making available any User Content on or through the Platform, you hereby grant to Otter a worldwide, irrevocable, perpetual, non-exclusive, transferable, royalty-free, sub-licensable license, with the right to sublicense, to use, copy, adapt, modify, distribute, license, sell, transfer, publicly display, publicly perform, transmit, stream, broadcast, access, view, and otherwise exploit such User Content on, through, by means of or to promote, market, or advertise Otter, Listings, or the Platform, or for any other purpose in our reasonable and sole discretion. This license shall survive termination of the Platform, these Terms, or your Account. Otter does not claim ownership rights in your User Content and nothing in these Terms will be deemed to restrict rights that you may have to use and exploit any such User Content submitted, posted, uploaded, published, or transmitted on or through the Platform by you.",
          BR,
          BR,
          "Any information or content publicly posted or privately transmitted through the Platform is the sole responsibility of the person from whom such content originated, and you access all such information and content at your own risk, and we aren’t liable for any errors or omissions in that information or content or for any damages or loss you might suffer in connection with it. We cannot control and have no duty to take any action regarding how you may interpret and use the User Content or what actions you may take as a result of having been exposed to the User Content, and you hereby release us from all liability for you having acquired or not acquired User Content through the Platform. While we may try to do so, we can’t guarantee the identity of any users with whom you interact in using the Platform and are not responsible for which users gain access to the Platform.",
          BR,
          BR,
          "You are responsible for all User Content you contribute, in any manner, to the Platform, and you represent and warrant you have all rights necessary to do so, in the manner in which you contribute it. You will keep all your registration information accurate and current. You are responsible for all your activity in connection with the Platform.",
          BR
        ]
      ]
    },
    {
      heading: "Notice and Procedure for Making Claims of Copyright Infringement",
      paragraphs: [
        [
          "Otter may, in appropriate circumstances and at its discretion, disable and/or terminate the Accounts of users who infringe the intellectual property of others. If you believe that your copyright or the copyright of a person on whose behalf you are authorized to act has been infringed, please provide Otter’s Copyright Agent a written Notice containing the following information:",
          BR,
          "- an electronic or physical signature of the person authorized to act on behalf of the owner of the copyright or other intellectual property interest;",
          BR,
          "- a description of the copyrighted work or other intellectual property that you claim has been infringed;",
          BR,
          "- a description of where the material that you claim is infringing is located on the Platform;",
          BR,
          "- your address, telephone number, and email address;a statement by you that you have a good faith belief that the disputed use is not authorized by the copyright owner, its agent, or the law;",
          BR,
          "- a statement by you, made under penalty of perjury, that the above information in your Notice is accurate and that you are the copyright or intellectual property owner or authorized to act on the copyright or intellectual property owner's behalf.",
          BR,
          BR,
          "Otter’s Copyright Agent can be reached by sending an email to DMCA@withotter.com.To be valid, a Notice must be in writing and must follow the instructions above. You also may use the contact information in this Section to notify us of alleged violations of other intellectual property rights.",
          BR
        ]
      ]
    },
    {
      heading: "Feedback",
      paragraphs: [
        [
          "We welcome your feedback about Otter and the Platform. By sending us any feedback, comments, questions, or suggestions concerning Otter or the Platform (collectively, “Feedback”) you represent and warrant (a) that you have the right to disclose the Feedback, (b) that the Feedback does not violate the rights of any other person or entity, and (c) that your Feedback does not contain the confidential or proprietary information of any third party or parties. By sending us any Feedback, you further (i) agree that we are under no obligation of confidentiality, express or implied, with respect to the Feedback, (ii) acknowledge that we may have something similar to the Feedback already under consideration or in development, (iii) grant us an irrevocable, non-exclusive, royalty-free, perpetual, worldwide license to use, modify, prepare derivative works, publish, distribute and sublicense the Feedback, and (iv) irrevocably waive, and cause to be waived, against Otter and its users any claims and assertions of any moral rights contained in such Feedback. This Feedback section shall survive any termination of your Account or the Platform.",
          BR
        ]
      ]
    },
    {
      heading: "Bookings, Fees, and Taxes",
      paragraphs: [
        [
          "When you book Childcare Services offered through a Listing (a “Booking”), you are agreeing to pay all itemized charges for the Booking, including the price of the Childcare Services, applicable fees like Otter’s service fee, taxes, and any other items identified during checkout (collectively, the “Fees”). When you receive the Booking confirmation, a contract for Childcare Services is formed directly between the applicable Care Seeker and Care Provider (each, a “Childcare Services Contract”). The ",
          {
            tag: "a",
            children: [
              "Otter Cancellation Policy"
            ],
            href: "https://help.withotter.com/hc/en-us/articles/4410166870413-Cancellations"
          },
          " and ",
          {
            tag: "a",
            children: [
              "Parent Handbook"
            ],
            href: "https://help.withotter.com/hc/en-us/categories/4410166453645-Parent-Handbook"
          },
          " become part of the applicable Childcare Services Contract. ",
          BR,
          "‍",
          BR,
          "Care Seekers must pay Fees for Childcare Services through the Platform. Care Provider agrees not to seek or accept payments from Care Seekers outside of the Platform, and Members who fail to comply with this provision may lose access to the Platform. ",
          BR,
          BR,
          "Payment of Fees on Otter are through our payment processing partner, Stripe. Care Providers who receive payment for Childcare Services agree to the ",
          {
            tag: "a",
            children: [
              "Stripe Connected Account Agreement"
            ],
            href: "https://stripe.com/connect-account/legal"
          },
          ", which includes the ",
          {
            tag: "a",
            children: [
              "Stripe Services Agreement"
            ],
            href: "https://stripe.com/legal"
          },
          ", as may be modified by Stripe from time to time. As a condition of receiving payment processing services through Stripe, you agree to provide Otter with accurate and complete information about you and your business, and you authorize Otter to share this information and transaction information related to your use of the payment processing services provided by Stripe. As a Care Seeker making payments through Stripe, you authorize Stripe to charge your payment method for Fees.",
          BR
        ]
      ]
    },
    {
      heading: "Cancellations, Care Access Issues, Refunds, and Booking Modifications",
      paragraphs: [
        [
          "Please review the Otter ",
          {
            tag: "a",
            children: [
              "Cancellation Policy"
            ],
            href: "https://help.withotter.com/hc/en-us/articles/4410166870413-Cancellations"
          },
          " for information detailing what happens when you cancel or modify a Booking. Booking modifications and cancellations may be subject to additional Fees and/or charges, and by cancelling or making the modification, the applicable Care Seeker and Care Provider agree to such Fees and charges.",
          BR
        ]
      ]
    },
    {
      heading: "Additional Obligations of Sitters",
      paragraphs: [
        [
          {
            tag: "em",
            children: [
              "Contracting with Care Seekers"
            ]
          },
          ". When you accept a Booking request, or receive a Booking confirmation through the Platform, you are entering into a contract directly with the Care Seeker, and are responsible for delivering your Childcare Services under the terms and at the price specified in your Listing. Any terms, policies or conditions that you include in any supplemental contract with Care Seekers must  be consistent with these Terms, our policies, and the information provided in your Listing.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Independence of Care Providers"
            ]
          },
          ". Your relationship with Otter is not that of an employee, agent, joint venturer, or partner of Otter. Otter does not and has no right to direct or control your Childcare Services, and you agree that you have complete discretion whether and when to provide Childcare Services, and on what terms to offer them.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Accuracy of Listings"
            ]
          },
          ". The Platform provides tools that enable you to create and manage a Listing. Your Listing must include complete and accurate information about your Childcare Services, your price, and any rules or requirements that apply to your Care Seeker, their dependents, or the Listing. You are responsible for keeping your Listing information (including calendar availability) and content (like photos, if any) up-to-date and accurate at all times. By posting a Listing, you represent and warrant that such Listing or a Care Seeker’s Booking or use of Childcare Services (i) will not breach any agreements you have entered into with any third parties, such as homeowners association, condominium, or other third party agreements, (ii) will be in compliance with all applicable laws (such as zoning laws), tax requirements, intellectual property laws, and rules and regulations that may apply to Childcare Services included in a Listing (including having all required permits, licenses and registrations), and (iii) not conflict with the rights of third parties.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Insurance"
            ]
          },
          ". By posting a Listing, you represent and warrant that you have obtained appropriate insurance for your Childcare Services. You are solely responsible for reviewing any insurance policy that you may have for the Childcare Services carefully, and in particular you must make sure that you are familiar with and understand any exclusions to, and any deductibles that may apply for, such insurance policy, including, but not limited to, whether or not such insurance policy will cover the actions or inactions of or relating to Care Seekers and their children while you are performing Childcare Services.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Compliance with Applicable Laws"
            ]
          },
          ". You are responsible for understanding and complying with any laws, rules, regulations, and contracts with third parties that apply to your Listing or Childcare Services. For example, applicable laws may (1) restrict or prohibit childcare in specific circumstances; (2) require registration, permitting, or licensing before you may offer or provide Childcare Services; or (3) require registration of Care Seekers and their dependents that use your Childcare Services. You are solely responsible for complying with these applicable laws. To the extent Otter provides guidance on local requirements, you understand such guidance is not legal advice, is for informational purposes only, and you will independently confirm your obligations. You are responsible for handling and using personal data of Care Seekers and their dependents and others in compliance with applicable privacy laws and these Terms. If you have questions about how local laws apply you should always seek legal advice.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Taxes"
            ]
          },
          ". Care Providers are responsible for any and all applicable federal, state and local taxes, duties, tariffs, levies, withholdings, and similar assessments (including without limitation, sales, use, and value added taxes) relating to the subject matter hereunder, excluding taxes based on Otter’s income.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Disputes"
            ]
          },
          ". Otter reserves the right to cancel confirmed Bookings, including in situations where a Care Seeker has provided evidence of a material concern with a Care Provider’s Childcare Services. Material concerns include, without limitation, overenrollment of Childcare Services that affect safety, material misrepresentations in the Childcare Services as compared to the Listing, and complaints about the behavior of Care Provider or Care Provider’s employees or agents. Where Otter cancels a confirmed Booking due to a material concern of a Care Seeker, we may request, and you agree to provide, a refund of Fees collected for the applicable child, to be calculated in Otter’s reasonable discretion.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Assumption of Risk"
            ]
          },
          ". You acknowledge that providing Childcare Services carries inherent risks and agree that you assume the entire risk arising out of your access to and use of the Platform, offering Childcare Services, or any interaction you have with other Members whether in person or online. You agree that you have had the opportunity to investigate the Platform and any laws, rules, regulations, or obligations that may be applicable to your Listings or Childcare Services and that you are not relying upon any statement of law made by Otter.",
          BR
        ]
      ]
    },
    {
      heading: "Additional Obligations of Parents",
      paragraphs: [
        [
          "You agree to pay applicable fees like Otter’s service fee (and applicable taxes) for each Booking. Otter will charge those itemized fees when you also pay the Care Provider. Care Seekers agree that a confirmed Booking only allows the Care Seeker to use the Childcare Services in the Listing for the limited duration described therein or elsewhere by the Care Provider and for the number of children identified in the Booking. Care Seekers further agree to pick up their children from the Care Provider no later than the pickup time that the Care Provider specifies in the Listing or such other time as mutually agreed upon between the Care Seeker and the Care Provider. If a Care Seeker picks up a child past the agreed upon pickup time without the Care Provider’s consent, the Care Seeker may be charged an additional fee. Care Providers may also impose additional fees on Care Seekers, such as for meals or special activities, in accordance with the Listing. Care Seekers shall pay such fees.",
          BR,
          BR,
          "Assumption of Risk. You acknowledge that receiving Childcare Services carries inherent risks and agree that you assume the entire risk arising out of your access to and use of the Platform, receiving Childcare Services, or any interaction you have with other Members whether in person or online. You agree that you have had the opportunity to investigate the Platform and any laws, rules, regulations, or obligations that may be applicable to Childcare Services and that you are not relying upon any statement of law made by Otter.",
          BR
        ]
      ]
    },
    {
      heading: "Reviews",
      paragraphs: [
        [
          "The Platform may offer Care Providers and Care Seekers to submit and publish reviews of each other (a “Review”). Your Review must be accurate and may not contain any discriminatory, offensive, defamatory, or other language that violates these Terms. Reviews are not verified by Otter for accuracy and may be incorrect or misleading.",
          BR
        ]
      ]
    },
    {
      heading: "Term and Termination",
      paragraphs: [
        [
          {
            tag: "em",
            children: [
              "Term"
            ]
          },
          ". The agreement between you and Otter reflected by these Terms is effective when you access the Platform (for example to create an Account) and remains in effect until either you or we terminate the agreement in accordance with these Terms.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Termination"
            ]
          },
          ". You may terminate this agreement at any time by contacting us in writing through Otter’s ",
          {
            tag: "a",
            children: [
              "Help Center"
            ],
            href: "http://help.withotter.com/"
          },
          " or by deleting your Account. Otter may terminate this agreement and your Account for any reason by giving you notice via email or using any other contact information you have provided for your Account. Otter may also terminate this agreement immediately and without notice and stop providing access to the Platform if you breach these Terms, you violate our policies, you violate applicable laws, or we reasonably believe termination is necessary to protect Otter, its Members, or third parties. If you have not engaged in any activity with your Account for more than two years, we may terminate your Account for any reason without prior notice.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Member Violations"
            ]
          },
          ". Without limiting any other rights available to Otter, if (i) you breach these Terms, (ii) you violate applicable laws, regulations, or third-party rights, or (iii) Otter believes it is reasonably necessary to protect Otter, its Members, or third parties; Otter may, with or without prior notice:",
          BR,
          "- suspend or limit your access to or use of the Platform and/or your Account;",
          BR,
          "- suspend or remove Listings, Reviews, or other User Content;",
          BR,
          "- cancel pending or confirmed Bookings; or",
          BR,
          "- suspend or revoke any special status associated with your Account.",
          BR,
          BR,
          "You may appeal actions taken by us under this Section by contacting customer service. If a Booking is cancelled under this Section, the amount paid to the Care Provider will be reduced by the amount we refund or otherwise provide to the Care Seeker, and by any other costs we incur as a result of the cancellation, subject to any limitations imposed by applicable law. Please review our ",
          {
            tag: "a",
            children: [
              "Cancellation Policy"
            ],
            href: "https://help.withotter.com/hc/en-us/articles/4410166870413-Cancellations"
          },
          " for more details on cancellations.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Effect of Termination"
            ]
          },
          ". If you are a Care Provider and terminate your Account, any confirmed Booking(s) will be automatically cancelled, and your Care Seekers will receive a full refund of any amounts pre-paid for such Booking, subject to any limitations imposed by applicable law. If you terminate your Account as a Care Seeker, any confirmed Booking(s) will be automatically cancelled, and any refund will depend upon eligibility pursuant to our ",
          {
            tag: "a",
            children: [
              "Cancellation Policy"
            ],
            href: "https://help.withotter.com/hc/en-us/articles/4410166870413-Cancellations"
          },
          ". You are not entitled to a restoration of your Account or any of your Content if you terminate your Account, though you may create a new Account unless prohibited by these Terms. If your access to or use of the Platform has been limited, or your Account has been suspended, or this agreement has been terminated by us, you may not register a new account or access or use the Platform through an account of another Member.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Survival"
            ]
          },
          ". Parts of these Terms that by their nature survive termination, will survive termination of this agreement, including Sections 2 through 28.",
          BR
        ]
      ]
    },
    {
      heading: "Indemnity and Release",
      paragraphs: [
        [
          "You agree to release and to indemnify, defend and hold harmless Otter and its parents, subsidiaries, affiliates and agents, as well as the officers, directors, employees, shareholders and representatives of any of the foregoing entities, from and against any and all losses, liabilities, expenses, damages, costs (including attorneys’ fees and court costs) claims, actions, inquiries, or investigations of any kind whatsoever arising out of or resulting from your use of the Platform or the Childcare Services made available through the Platform, your violation of these Terms, and any of your acts or omissions that implicate publicity rights, defamation or invasion of privacy. Otter reserves the right, at its own expense, to assume exclusive defense and control of any matter otherwise subject to indemnification by you and, in such case, you agree to cooperate with Otter in the defense of such matter.",
          BR,
          BR,
          "In the event that you have a dispute with one or more other users, you release Otter, its officers, employees, agents, and successors from claims, demands, and damages of every kind or nature, known or unknown, suspected or unsuspected, disclosed or undisclosed, arising out of or in any way related to such disputes and/or our Platform. If you are a California resident, you waive California Civil Code Section 1542, which provides:",
          BR,
          BR,
          "A general release does not extend to claims that the creditor or releasing party does not know or suspect to exist in his or her favor at the time of executing the release and that, if known by him or her, would have materially affected his or her settlement with the debtor or released party.",
          BR,
          BR,
          "If you are not a California resident, you waive your rights under any statute or common law principle similar to Section 1542 that governs your rights in the jurisdiction of your residence.",
          BR
        ]
      ]
    },
    {
      heading: "Disclaimers",
      paragraphs: [
        [
          "Neither Otter nor its licensors or suppliers make any representations or warranties concerning any content contained in or accessed through the Platform, and we will not be responsible or liable for the accuracy, copyright compliance, legality, or decency of material contained in or accessed through the Platform. We (and our licensors and suppliers) make no representations or warranties regarding suggestions or recommendations of services or products offered or purchased through the Platform. Products and services purchased or offered (whether or not following such recommendations and suggestions) through the Platform are provided “AS IS” and without any warranty of any kind from Otter or others. ",
          BR,
          BR,
          "YOU ACKNOWLEDGE AND AGREE THAT OTTER DOES NOT HAVE AN OBLIGATION, BUT RESERVES THE RIGHT FOR ANY REASON, TO (A) MONITOR, REVIEW, AND/OR REMOVE USER CONTENT; OR (B) FOR ANY PERMISSIBLE PURPOSE, CONDUCT IDENTITY VERIFICATION, BACKGROUND (INCLUDING CRIMINAL BACKGROUND) OR REGISTERED SEX OFFENDER CHECKS ON ANY MEMBER. THE PLATFORM AND CONTENT ARE PROVIDED BY OTTER (AND ITS LICENSORS AND SUPPLIERS) ON AN “AS-IS” BASIS, WITHOUT WARRANTIES OR ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING, WITHOUT LIMITATION, IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, OR THAT USE OF THE PLATFORM WILL BE UNINTERRUPTED, TIMELY, SECURE OR ERROR-FREE OR THAT THE RESULTS OR CONTENT THAT MAY BE OBTAINED FROM THE PLATFORM WILL BE ACCURATE OR RELIABLE OR THAT THE QUALITY OF ANY PRODUCTS, SERVICES, INFORMATION OR OTHER MATERIAL PURCHASED OR OBTAINED BY YOU THROUGH THE PLATFORM WILL MEET YOUR EXPECTATIONS. NO ADVICE OR INFORMATION, WHETHER ORAL OR WRITTEN, OBTAINED FROM OTTER OR THROUGH THE PLATFORM, WILL CREATE ANY WARRANTY NOT EXPRESSLY MADE HEREIN.",
          BR,
          BR,
          "YOU ARE SOLELY RESPONSIBLE FOR ALL OF YOUR COMMUNICATIONS AND INTERACTIONS WITH OTHER USERS OR MEMBERS OF THE PLATFORM AND WITH OTHER PERSONS WITH WHOM YOU COMMUNICATE OR INTERACT AS A RESULT OF YOUR USE OF THE PLATFORM, INCLUDING BUT NOT LIMITED TO ANY CARE PROVIDER OR CARE SEEKER. YOU UNDERSTAND THAT OTTER DOES NOT MAKE ANY ATTEMPT TO VERIFY THE STATEMENTS OF MEMBERS OR TO REVIEW OR VET ANY LISTINGS. OTTER MAKES NO REPRESENTATIONS OR WARRANTIES AS TO THE CONDUCT OF USERS OF THE PLATFORM OR THEIR COMPATIBILITY WITH ANY CURRENT OR FUTURE USERS OF THE PLATFORM. YOU AGREE TO TAKE REASONABLE PRECAUTIONS IN ALL COMMUNICATIONS AND INTERACTIONS WITH OTHER USERS OF THE PLATFORM AND WITH OTHER PERSONS WITH WHOM YOU COMMUNICATE OR INTERACT AS A RESULT OF YOUR USE OF THE PLATFORM, PARTICULARLY IF YOU DECIDE TO MEET OFFLINE OR IN PERSON AND GIVE OR RECEIVE CHILDCARE SERVICES. OTTER EXPLICITLY DISCLAIMS ALL LIABILITY FOR ANY ACT OR OMISSION OF ANY USERS OR THIRD PARTIES.",
          BR,
          BR,
          "SOME STATES DO NOT ALLOW LIMITATIONS ON HOW LONG AN IMPLIED WARRANTY LASTS, SO THE ABOVE LIMITATIONS MAY NOT APPLY TO YOU.",
          BR
        ]
      ]
    },
    {
      heading: "Limitation of Liability",
      paragraphs: [
        [
          "TO THE FULLEST EXTENT ALLOWED BY APPLICABLE LAW, UNDER NO CIRCUMSTANCES AND UNDER NO LEGAL THEORY (INCLUDING, WITHOUT LIMITATION, TORT, CONTRACT, STRICT LIABILITY, OR OTHERWISE) SHALL OTTER (OR ITS LICENSORS OR SUPPLIERS) BE LIABLE TO YOU OR TO ANY OTHER PERSON FOR (A) ANY INDIRECT, SPECIAL, INCIDENTAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES OF ANY KIND, INCLUDING DAMAGES FOR LOST PROFITS, LOSS OF GOODWILL, WORK STOPPAGE, ACCURACY OF RESULTS, OR COMPUTER FAILURE OR MALFUNCTION, OR (B) ANY AMOUNT, IN THE AGGREGATE, HIGHER THAN THE GREATER OF (I) $100 OR (II) THE AMOUNTS PAID BY YOU TO OTTER IN CONNECTION WITH THE PLATFORM IN THE TWELVE (12) MONTH PERIOD PRECEDING THE EVENT GIVING RISE TO THE APPLICABLE CLAIM. THE LIMITATIONS ON DAMAGES SET FORTH ABOVE ARE FUNDAMENTAL ELEMENTS OF THE BASIS OF THE BARGAIN AND ARE MATERIAL TO OTTER’S DECISION TO ENTER INTO THE AGREEMENT BETWEEN OTTER AND YOU. SOME STATES DO NOT ALLOW THE EXCLUSION OR LIMITATION OF CERTAIN DAMAGES, SO THE ABOVE LIMITATION AND EXCLUSIONS MAY NOT APPLY TO YOU.",
          BR,
          BR,
          "THE LIMITATION OF LIABILITY DESCRIBED ABOVE SHALL APPLY FULLY TO RESIDENTS OF NEW JERSEY.",
          BR
        ]
      ]
    },
    {
      heading: "Arbitration and Class Action Waiver",
      paragraphs: [
        [
          {
            tag: "strong",
            children: [
              "PLEASE READ THIS SECTION CAREFULLY – IT MAY SIGNIFICANTLY AFFECT YOUR LEGAL RIGHTS, INCLUDING YOUR RIGHT TO FILE A LAWSUIT IN COURT.",
              BR,
              BR,
              "Initial Dispute",
              BR,
              "‍"
            ]
          },
          "Our Customer Support Department is available through the Otter ",
          {
            tag: "a",
            children: [
              "Help Center"
            ],
            href: "http://help.withotter.com/"
          },
          " to address any concerns you may have regarding the Platform. Our Customer Service Department can resolve most concerns quickly to our users’ satisfaction. The parties shall use their best efforts through this Customer Service process to settle any dispute, claim, question, or disagreement and engage in good faith negotiations which shall be a condition to either party initiating a lawsuit or arbitration. Failure to engage in this process could result in the award of fees against you in arbitration.",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "Binding Arbitration",
              BR,
              "‍"
            ]
          },
          "If the parties do not reach an agreed upon solution within a period of 30 days from the time informal dispute resolution begins under the Initial Dispute Resolution provision, then either party may initiate binding arbitration as the sole means to resolve claims, subject to the terms set forth below. This agreement to arbitrate is a contract governed by the Federal Arbitration Act, 9 U.S.C. section 1, et seq., and evidences a transaction involving commerce.  Specifically, all claims arising out of or relating to these Terms (including their formation, performance and breach), the parties’ relationship with each other and/or your use of the Platform and any services made available through the Platform shall be finally settled by binding arbitration administered by JAMS in accordance with the provisions of its Streamlined Arbitration Rules and Procedures, excluding any rules or procedures governing or permitting class or representative actions and except that each party will be permitted at least one deposition unless forbidden by JAMS. If for any reason JAMS is unable to administer arbitration, either party may apply to a court to appoint an arbitrator pursuant to 9 U.S.C. section 5.",
          BR,
          BR,
          "Except as explicitly set forth in this Section 21, the arbitrator, and not any federal, state or local court or agency, shall have exclusive authority to resolve all disputes arising out of or relating to the interpretation, applicability, enforceability or formation of these Terms, including, but not limited to any claim that all or any part of these Terms are void or voidable, whether a claim is subject to arbitration, and any dispute regarding the payment of JAMS administrative or arbitrator fees (including the timing of such payments and remedies for nonpayment). The arbitrator shall be empowered to grant whatever relief would be available in a court under law or in equity. The parties agree that the arbitrator may allow the filing of dispositive motions if they are likely to efficiently resolve or narrow issues in dispute. The arbitrator’s award shall be written, and binding on the parties and may be entered as a judgment in any court of competent jurisdiction. No arbitration award or decision will have any preclusive effect as to issues or claims in any dispute with anyone who is not a named party to the arbitration.",
          BR,
          BR,
          "The Streamlined Arbitration Rules governing the arbitration may be accessed at ",
          {
            tag: "a",
            children: [
              "www.jamsadr.com"
            ],
            href: "#"
          },
          " or by calling JAMS at (800) 352-5267. If you commence arbitration in accordance with these Terms, you will be required to pay $250 to initiate the arbitration. To the extent the filing fee for the arbitration exceeds the cost of filing a lawsuit, the arbitrator may require Otter to pay the additional cost. You are responsible for your own attorneys’ fees unless the arbitration rules and/or applicable law provide otherwise. If the arbitrator finds the arbitration to be non-frivolous, Otter will pay the remaining filing and arbitrator fees for the arbitration, provided your claim does not exceed $75,000. For claims above $75,000, fees and costs will be determined in accordance with applicable JAMS rules. The arbitration rules permit you to recover attorney’s fees in certain cases.",
          BR,
          BR,
          "Any arbitration demand or counterclaim asserted by either party must contain sufficient information to provide fair notice to the other party of the asserting party’s identity, the claims being asserted, and the factual allegations on which they are based. The arbitrator and/or JAMS may require amendment of any demand or counterclaim that does not satisfy these requirements. The arbitrator has the right to impose sanctions in accordance with JAMS Rule 24 for any claims the arbitrator determines to be frivolous or improper (under the standard set forth in Federal Rule of Civil Procedure 11).",
          BR,
          BR,
          "The parties agree that JAMS has discretion to modify the amount or timing of any administrative or arbitration fees due under JAMS’s Rules where it deems appropriate, provided that such modification does not increase the costs to you, and you waive any objection to such fee modification. The parties also agree that a good-faith challenge by either party to the fees imposed by JAMS does not constitute a default, waiver, or breach of this Section 21 while such challenge remains pending before JAMS, the arbitrator, and/or a court of competent jurisdiction.",
          BR,
          BR,
          "The parties understand that, absent this mandatory provision, they would have the right to sue in court and have a jury trial. They further understand that, in some instances, the costs of arbitration could exceed the costs of litigation and the right to discovery may be more limited in arbitration than in court.",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "Location",
              BR,
              "‍"
            ]
          },
          "If you are a resident of the United States, arbitration will take place at any reasonable location within the United States convenient for you. You and Otter agree to submit to the personal jurisdiction of any federal or state court in New Castle County, Delaware, in order to compel arbitration, to stay proceedings pending arbitration, or to confirm, modify, vacate or enter judgment on the award entered by the arbitrator.",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "Class Action Waiver",
              BR,
              "‍"
            ]
          },
          "The parties further agree that any arbitration shall be conducted in their individual capacities only and not as a class action or other representative action, and the parties expressly waive their right to file a class action or seek relief on a class basis. YOU AND OTTER AGREE THAT EACH MAY BRING CLAIMS AGAINST THE OTHER ONLY IN YOUR OR ITS INDIVIDUAL CAPACITY, AND NOT AS A PLAINTIFF OR CLASS MEMBER IN ANY PURPORTED CLASS OR REPRESENTATIVE PROCEEDING.  Notwithstanding any other provision of these terms, disputes regarding the interpretation, applicability, or enforceability of the Class Action Waiver may be resolved only by a court and not by an arbitrator.  If there is a final judicial determination that applicable law precludes enforcement of this paragraph’s limitations as to a particular remedy, then that remedy (and only that remedy) must be severed from the arbitration and may be sought in court. The parties agree, however, that any adjudication of remedies not subject to arbitration shall be stayed pending the outcome of any arbitrable claims and remedies.  ",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "Exception - Litigation of Intellectual Property and Small Claims Court Claims",
              BR,
              "‍"
            ]
          },
          "Notwithstanding the parties’ decision to resolve all disputes through arbitration, either party may bring an action in state or federal court to protect its intellectual property rights (“intellectual property rights” means patents, copyrights, moral rights, trademarks, and trade secrets, but not privacy or publicity rights). Either party may also elect to have disputes or claims resolved in a small claims court that are within the scope of that court’s jurisdiction. Either party may also seek a declaratory judgment or other equitable relief in a court of competent jurisdiction regarding whether a party’s claims are time-barred or may be brought in small claims court in your state and county of residence. Seeking such relief shall not waive a party’s right to arbitration under this agreement.",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "30-Day Right to Opt Out",
              BR,
              "‍"
            ]
          },
          "You have the right to opt-out and not be bound by the arbitration and class action waiver provisions set forth above by sending written notice of your decision to opt-out to the following email address: opt-out@withotter.com. The notice must be sent within 30 days of ",
          {
            tag: "strong",
            children: [
              "October 10, 2021"
            ]
          },
          " or your first use of the Platform, whichever is later, otherwise you shall be bound to arbitrate disputes in accordance with the terms of those paragraphs. If you opt-out of these arbitration provisions, Otter also will not be bound by them.",
          BR,
          BR,
          {
            tag: "strong",
            children: [
              "Changes to this Section",
              BR,
              "‍"
            ]
          },
          "Otter will provide 30 days’ notice of any changes affecting the substance of this Section 21. Changes will become effective on the 30th day. If you continue to use the site after the 30th day, you agree that any unfiled claims of which Otter does not have actual notice are subject to the revised clause.",
          BR
        ]
      ]
    },
    {
      heading: "Venue and Governing Law",
      paragraphs: [
        [
          "For any dispute not subject to arbitration or under the jurisdiction of a small claims court, you and Otter agree to submit to the personal and exclusive jurisdiction of and venue in the federal and state courts located in New Castle County, Delaware. You further agree to accept service of process by mail, and hereby waive any and all jurisdictional and venue defenses otherwise available.",
          BR,
          BR,
          "The Terms and the relationship between you and Otter shall be governed by the laws of the State of Delaware without regard to conflict of law provisions.",
          BR
        ]
      ]
    },
    {
      heading: "Links",
      paragraphs: [
        [
          "The Platform may provide, or third parties may provide, links to other World Wide Web sites, applications or resources. Because Otter has no control over such sites, applications and resources, you acknowledge and agree that Otter is not responsible for the availability of such external sites, applications or resources, and does not endorse and is not responsible or liable for any content, advertising, products or other materials on or available from such sites or resources. You further acknowledge and agree that Otter shall not be responsible or liable, directly or indirectly, for any damage or loss caused or alleged to be caused by or in connection with use of or reliance on any such content, goods or services available on or through any such site or resource.",
          BR
        ]
      ]
    },
    {
      heading: "Application License",
      paragraphs: [
        [
          "Subject to your compliance with these Terms, Otter grants you a limited non-exclusive, non-transferable license to download and install a copy of Otter mobile app on a device that you exclusively control and to run such copy of the app solely for your own personal use. Otter reserves all rights in and to the app not expressly granted to you under these Terms. You will not run any version of the app on a jailbroken device.",
          BR,
          BR,
          "If you have downloaded our app, you agree to promptly download and install any new version that we make available through the iTunes App Store or Google Play store, as applicable. Some new versions may contain updated Terms. Some new versions may contain security fixes and service improvements, whether or not we disclose that they do; accordingly, failure to promptly update your version of the App may in some cases expose you to increased security risks or Platform malfunctions.",
          BR
        ]
      ]
    },
    {
      heading: "General",
      paragraphs: [
        [
          {
            tag: "em",
            children: [
              "Entire Agreement"
            ]
          },
          ". These Terms (and any additional terms, contracts, rules and conditions that Otter may post on the Platform) constitute the entire agreement between you and Otter with respect to the Platform and supersedes any prior agreements, oral or written, between you and Otter. In the event of a conflict between these Terms and additional terms, contracts, rules and conditions that Otter may post on the Platform, the latter will prevail over the Terms to the extent of the conflict.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Waiver and Severability of Terms"
            ]
          },
          ". The failure of Otter to exercise or enforce any right or provision of the Terms shall not constitute a waiver of such right or provision. If any provision of the Terms is found by an arbitrator or court of competent jurisdiction (as applicable) to be invalid, the parties nevertheless agree that the arbitrator or court should endeavor to give effect to the parties’ intentions as reflected in the provision, and the other provisions of the Terms remain in full force and effect.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Statute of Limitations"
            ]
          },
          ". You agree that regardless of any statute or law to the contrary, any claim or cause of action arising out of or related to the use of the Platform or the Terms must be filed within one (1) year after such claim or cause of action arose or be forever barred. This statute of limitations provision does not apply to residents of New Jersey.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Notice"
            ]
          },
          ". Otter may give notice by any means of communication reasonably anticipated to notify you of the information provided. You agree that all notices, disclosures, and other communications that we provide to you electronically satisfy any legal requirement that such communications be in writing or be delivered in a particular manner. You agree that you have the ability to store such electronic communications such that they remain accessible to you in an unchanged form. By way of example only, such communication may be a general notice on the Platform or via email to the email address listed on your Account. It is your obligation to update your Account information so that we may contact you as may be necessary. Such notice shall be deemed to have been given 48 hours after dispatch. If physical notice (e.g., US Mail) is used, then such notice shall be deemed to have been given 7 days after dispatch.Except as explicitly described in the “Arbitration and Class Action Waiver” section, you may give notice to Otter (such notice shall be deemed given when received by Otter) at any time by contacting us in writing through Otter’s ",
          {
            tag: "a",
            children: [
              "Help Center"
            ],
            href: "http://help.withotter.com/"
          },
          ".",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "Section Titles"
            ]
          },
          ". The section titles in the Terms are for convenience only and have no legal or contractual effect.",
          {
            tag: "em",
            children: [
              "Assignment"
            ]
          },
          ". These Terms are personal to you, and are not assignable, transferable or sublicensable by you except with our prior written consent. We may assign, transfer or delegate any of our rights and obligations hereunder without consent.",
          BR,
          BR,
          "‍",
          {
            tag: "em",
            children: [
              "No Third-Party Beneficiaries."
            ]
          },
          " You agree that, except as otherwise expressly provided in these Terms, there shall be no third-party beneficiaries to these Terms.",
          BR
        ]
      ]
    },
    {
      heading: "Contact Us",
      paragraphs: [
        [
          "If you have questions about these Terms, please contact us in writing through Otter’s ",
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
      heading: "iOS Terms",
      paragraphs: [
        [
          "You acknowledge and agree that (i) these Terms are binding between you and Otter only, and Apple is not a party hereto, and (ii) as between Otter and Apple, it is Otter that is responsible for the app and the content thereof. You must use the iOS app only on an Apple-branded product that runs iOS. Your use of the app must comply with the terms of use applicable to the Apple source from which you obtain it (including the Usage Rules set forth in the Apple App Store Terms of Service). You acknowledge that Apple has no obligation to furnish you with any maintenance and support services with respect to the app.",
          BR,
          BR,
          "You acknowledge that Apple is not responsible for addressing any claims you have or any claims of any third party relating to the app or your possession and use of the app, including, but not limited to (i) product warranty or liability claims; (ii) any claim that the app fails to conform to any applicable legal or regulatory requirement; (iii) claims arising under consumer protection or similar legislation; or (iv) claims that the app infringes a third party’s intellectual property rights.",
          BR,
          BR,
          "In the event of any failure of the iOS version of the app to conform to any applicable warranty that has not been effectively disclaimed by these Terms, you may notify Apple, and Apple will refund the purchase price for the app (if any) to you; to the maximum extent permitted by applicable law, Apple will have no other warranty obligation whatsoever with respect to the app, and, as between Apple and Otter, any other claims, losses, liabilities, damages, costs or expenses attributable to any failure to conform to any warranty will be Otter’s responsibility, but only to the extent provided by these Terms. Please read the entire Terms, as other sections of these Terms limit Otter’s liability in this regard.",
          BR,
          BR,
          "Apple, and Apple’s subsidiaries, are third-party beneficiaries of these Terms. Upon your acceptance of the Terms, Apple will have the right (and will be deemed to have accepted the right) to enforce the Terms against you as a third-party beneficiary thereof. ",
          BR
        ]
      ]
    },
    {
      heading: "California Civil Code § 1812.5095",
      paragraphs: [
        [
          "This Section 28 applies to Care Providers, and as referenced below, Care Seekers, in the State of California. In California, Otter acts as an “Employment Agency” under Cal. Civil Code § 1812.501(a)(1)(C) for Care Providers. Otter helps Care Providers find work, but Care Providers are free to also find work through other Employment Agencies and/or work for individuals seeking care who are not found through Otter. As a Care Provider, you may be obligated to obtain business permits or licenses, where required by any state or local law, ordinance, or regulation, and you are not eligible for unemployment insurance, state disability insurance, social security, or workers’ compensation benefits through Otter. If you are self-employed, you will also need to pay self-employment tax, state tax, and federal income taxes.",
          BR,
          BR,
          "Care Provider and Otter also agree as follows:",
          BR,
          "- Care Provider, and not Otter, has the sole right to dictate any restrictions on hours, location and conditions of the work Care Provider will accept, and Care Provider is free to select or reject any work opportunity procured, offered, referred, or provided by Otter through the Platform or otherwise.",
          BR,
          "- Care Provider is free to renegotiate with the Care Seeker the amount to be paid in connection with any Listing.",
          BR,
          "- Otter shall not and has no right to provide any training to Care Provider with respect to the performance of the childcare services Care Provider provides to Care Seeker, but Otter may offer a voluntary orientation session to outline these Terms and the relationship between Otter and Care Provider.",
          BR,
          "- Otter shall not, and has no right to, direct, control or supervise Care Provider in the performance of services to Care Seekers.",
          BR,
          "- Otter does not provide tools, supplies or equipment necessary to perform Care Provider’s childcare services to Care Seekers.",
          BR,
          "- Notwithstanding any other provision of these Terms, Care Provider is not obligated to pay Otter any fee and Otter is not obligated to remit any sums to Care Provider, if Care Seeker fails or refuses to pay for Care Provider’s services.",
          BR,
          "- Payments from Care Seekers for Care Provider’s services shall be paid directly to the Care Provider, as described herein.",
          BR,
          "- Notwithstanding any other provision of these Terms, only the Care Seeker or Care Provider, and not Otter, may terminate a relationship between the Care Seeker and Care Provider. However, Otter may in its reasonable and sole discretion decline to permit Care Provider further use of the Platform.",
          BR,
          BR,
          "Care Seekers in California should know, pursuant to California law, that Otter is not the employer of the domestic worker (Care Provider) it refers to you. Depending on your arrangement with the domestic worker (Care Provider), you may have employer responsibilities.   ",
          BR
        ]
      ]
    }
  ]
}

export default termsOfUse
