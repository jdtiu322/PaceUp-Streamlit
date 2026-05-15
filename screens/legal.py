from __future__ import annotations

import html

import streamlit as st


LAST_UPDATED = "May 15, 2026"


def _route_href(page: str) -> str:
    return f"?page={page}"


def _route_link(label: str, page: str, css_class: str) -> None:
    st.markdown(
        (
            f'<a class="{html.escape(css_class, quote=True)}" '
            f'href="{html.escape(_route_href(page), quote=True)}" target="_self">'
            f"{html.escape(label)}</a>"
        ),
        unsafe_allow_html=True,
    )


def _render_legal_nav() -> None:
    with st.container(key="landing_nav"):
        brand_col, spacer_col, actions_col = st.columns([1.35, 2.85, 1.5], gap="small")
        with brand_col:
            st.markdown(
                """
                <a class="landing-brand-link" href="?page=home" target="_self">
                    <div class="landing-brand">
                        <span class="landing-brand-mark">↗</span>
                        <span>PaceUp</span>
                    </div>
                </a>
                """,
                unsafe_allow_html=True,
            )
        with spacer_col:
            st.markdown('<div class="landing-nav-spacer"></div>', unsafe_allow_html=True)
        with actions_col:
            with st.container(key="landing_nav_actions"):
                login_col, start_col = st.columns([.76, 1.24], gap="small")
                with login_col:
                    _route_link("Log in", "login", "landing-route-link landing-login-link")
                with start_col:
                    _route_link("Start training  →", "register", "landing-route-link landing-start-link")


def _render_legal_page(title: str, subtitle: str, sections: list[tuple[str, str]], *, kicker: str) -> None:
    st.markdown('<div class="landing-page-bg"></div>', unsafe_allow_html=True)
    _render_legal_nav()

    section_html = "".join(
        f'<section class="legal-section"><h2>{heading}</h2>{body}</section>'
        for heading, body in sections
    )
    st.markdown(
        f"""
        <div class="legal-page">
            <header class="legal-header">
                <div class="legal-kicker"><span></span> {kicker}</div>
                <h1 class="legal-title">{title}</h1>
                <div class="legal-sub">{subtitle}</div>
                <div class="legal-meta">Last updated &middot; {LAST_UPDATED}</div>
            </header>
            <div class="legal-body">
                {section_html}
            </div>
            <footer class="legal-footer">
                <div class="legal-footer-brand">PaceUp</div>
                <div class="legal-footer-copy">&copy; 2026 PaceUp. All rights reserved.</div>
                <div class="legal-footer-links">
                    <a href="?page=privacy" target="_self">Privacy Policy</a>
                    <a href="?page=terms" target="_self">Terms of Service</a>
                    <a href="?page=contact" target="_self">Contact</a>
                </div>
            </footer>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_terms() -> None:
    sections: list[tuple[str, str]] = [
        (
            "1. Acceptance of these Terms",
            """
            <p>These Terms of Service (the &ldquo;Terms&rdquo;) constitute a binding
            legal agreement between you (the &ldquo;User&rdquo;) and PaceUp
            (&ldquo;PaceUp,&rdquo; &ldquo;we,&rdquo; &ldquo;us,&rdquo; or
            &ldquo;our&rdquo;) governing your access to and use of the PaceUp
            platform, including any associated software, websites, content, and
            related services (collectively, the &ldquo;Service&rdquo;). By
            registering for an account or otherwise accessing or using the
            Service, you acknowledge that you have read, understood, and agree
            to be bound by these Terms. If you do not accept these Terms in
            their entirety, you are not authorized to use the Service.</p>
            <p>You represent and warrant that you are at least sixteen (16)
            years of age. Users who are minors under the age of majority in
            their jurisdiction of residence must obtain the prior consent of a
            parent or legal guardian, who shall be deemed to have accepted
            these Terms on the minor&rsquo;s behalf.</p>
            """,
        ),
        (
            "2. Nature of the Service",
            """
            <p>The Service is an artificial-intelligence-assisted application
            designed to generate informational training guidance, pacing
            recommendations, and educational content relating to recreational
            running, based upon the profile data and inquiries submitted by the
            User.</p>
            <p>The Service does not constitute, and shall not be construed as,
            medical advice, diagnosis, treatment, or professional health
            consultation. PaceUp is not a medical device, healthcare provider,
            or licensed practitioner. The User is strongly advised to consult a
            qualified medical professional prior to commencing, modifying, or
            discontinuing any training, exercise, or rehabilitation program,
            particularly where any pre-existing medical condition, injury, or
            symptom is present.</p>
            <p>The User acknowledges that physical activity, including running,
            entails inherent risks of injury and assumes full and sole
            responsibility for any consequences arising from reliance upon the
            information furnished by the Service.</p>
            """,
        ),
        (
            "3. User Accounts",
            """
            <p>The User is responsible for maintaining the accuracy and
            currency of all information submitted to the Service and for
            preserving the confidentiality of any credentials associated with
            the account. The User shall promptly notify PaceUp of any
            unauthorized access to, or use of, the account.</p>
            <p>PaceUp reserves the right, in its sole discretion, to suspend,
            restrict, or terminate any account that it determines, on
            reasonable grounds, to be in breach of these Terms or to be
            employed in a manner detrimental to the Service or its users.</p>
            """,
        ),
        (
            "4. Acceptable Use",
            """
            <p>The User shall not, and shall not permit any third party to:</p>
            <ul>
              <li>use the Service for any unlawful, fraudulent, or otherwise
              prohibited purpose, or in contravention of any applicable law,
              regulation, or judicial order;</li>
              <li>reverse-engineer, decompile, disassemble, scrape, or
              otherwise attempt to derive the source code, underlying ideas,
              or algorithms of the Service or interfere with the systems on
              which it operates;</li>
              <li>transmit, upload, or otherwise make available content that
              infringes intellectual-property rights, violates privacy rights,
              or is harmful, harassing, defamatory, or deceptive; or</li>
              <li>employ automated means to access the Service in excess of
              what is reasonably required for ordinary personal use.</li>
            </ul>
            """,
        ),
        (
            "5. AI-Generated Output",
            """
            <p>The outputs generated by the Service are produced by large
            language models in combination with retrieval mechanisms operating
            over a curated corpus of training literature. Such outputs may be
            incomplete, inaccurate, or outdated, and shall not be relied upon
            as authoritative directives. The User is expected to exercise
            independent judgment in evaluating and applying any output.</p>
            <p>As between the parties, the User retains ownership of the
            prompts submitted to the Service and is granted a personal,
            non-exclusive licence to use the corresponding outputs for
            non-commercial training purposes. PaceUp reserves the right to
            process de-identified and aggregated usage data for the purposes
            of operating, securing, and improving the Service.</p>
            """,
        ),
        (
            "6. Intellectual Property Rights",
            """
            <p>All right, title, and interest in and to the Service, including
            without limitation the PaceUp name, logo, software, design,
            documentation, and content (excluding User-submitted inputs),
            shall remain the exclusive property of PaceUp or its licensors.
            Subject to the User&rsquo;s continued compliance with these Terms,
            PaceUp grants the User a limited, non-exclusive, non-transferable,
            non-sublicensable, revocable licence to access and use the Service
            solely for personal, non-commercial purposes.</p>
            """,
        ),
        (
            "7. Subscriptions and Fees",
            """
            <p>The Service is presently made available at no cost to the User.
            PaceUp reserves the right to introduce paid plans or premium
            features in the future. Any such fees, together with their
            applicable terms, shall be communicated to the User in advance,
            and no charge shall be incurred without the User&rsquo;s express
            consent.</p>
            """,
        ),
        (
            "8. Disclaimers of Warranties",
            """
            <p>The Service is provided on an &ldquo;as is&rdquo; and &ldquo;as
            available&rdquo; basis, without representation, warranty, or
            condition of any kind, whether express, implied, or statutory,
            including without limitation any implied warranties of
            merchantability, fitness for a particular purpose, title, and
            non-infringement. PaceUp does not warrant that the Service will
            be uninterrupted, secure, or error-free, nor that the use of any
            recommendation will produce any particular result.</p>
            """,
        ),
        (
            "9. Limitation of Liability",
            """
            <p>To the fullest extent permitted by applicable law, in no event
            shall PaceUp, its affiliates, officers, employees, or agents be
            liable for any indirect, incidental, special, consequential,
            exemplary, or punitive damages, or for any loss of profits,
            revenue, data, goodwill, or other intangible losses, arising out
            of or in connection with the User&rsquo;s use of, or inability to
            use, the Service. The aggregate liability of PaceUp arising out of
            or relating to the Service shall not exceed the greater of (a)
            the total amount paid by the User to PaceUp in the twelve (12)
            months preceding the event giving rise to the claim, or (b)
            twenty United States dollars (USD $20).</p>
            """,
        ),
        (
            "10. Modifications to the Service and Terms",
            """
            <p>PaceUp reserves the right, at its sole discretion, to modify,
            suspend, or discontinue the Service, or to amend these Terms, at
            any time. Where any such amendment is material, PaceUp shall
            provide reasonable notice through the Service or by electronic
            mail. Continued use of the Service following the effective date
            of any revision shall constitute the User&rsquo;s acceptance of
            the amended Terms.</p>
            """,
        ),
        (
            "11. Termination",
            """
            <p>The User may terminate this agreement at any time by ceasing
            use of the Service and requesting deletion of the account through
            the profile settings or by written notice to PaceUp. PaceUp may
            terminate or suspend access to the Service, without prior notice,
            in the event of a material breach of these Terms or where required
            by applicable law. Provisions which by their nature are intended
            to survive termination shall continue in effect.</p>
            """,
        ),
        (
            "12. Governing Law and Jurisdiction",
            """
            <p>These Terms shall be governed by and construed in accordance
            with the laws of the jurisdiction in which PaceUp is operated,
            without regard to its conflict-of-laws principles. Any dispute,
            controversy, or claim arising out of or relating to these Terms or
            the Service shall be submitted to the exclusive jurisdiction of
            the competent courts of that jurisdiction, save where mandatory
            consumer-protection legislation provides otherwise.</p>
            """,
        ),
        (
            "13. Contact",
            """
            <p>Any questions, notices, or correspondence relating to these
            Terms should be directed to
            <a href="mailto:hello@paceup.app">hello@paceup.app</a>.</p>
            """,
        ),
    ]
    _render_legal_page(
        title="Terms of Service",
        subtitle="The terms and conditions governing your access to and use of the PaceUp platform.",
        kicker="Legal &middot; Terms",
        sections=sections,
    )


def show_privacy() -> None:
    sections: list[tuple[str, str]] = [
        (
            "1. Identity of the Data Controller",
            """
            <p>PaceUp (&ldquo;PaceUp,&rdquo; &ldquo;we,&rdquo; &ldquo;us,&rdquo;
            or &ldquo;our&rdquo;) operates the artificial-intelligence-assisted
            running coach platform (the &ldquo;Service&rdquo;) and acts as the
            data controller in respect of the personal information processed
            in connection therewith. This Privacy Policy describes the
            categories of personal information collected, the purposes and
            legal bases of processing, and the rights afforded to the User
            under applicable data-protection legislation.</p>
            """,
        ),
        (
            "2. Categories of Personal Information Collected",
            """
            <p><strong>Account information.</strong> Upon registration, PaceUp
            collects the User&rsquo;s electronic-mail address, an authentication
            credential (stored exclusively in the form of a cryptographic
            one-way hash by Firebase Authentication), and the display name
            selected by the User.</p>
            <p><strong>Training profile.</strong> Information voluntarily
            provided by the User during onboarding or via the settings
            interface, including without limitation fitness level, goal
            distance, target race date, current weekly training volume,
            preferred long-run day, recent race performance, and self-declared
            injury status. Such information may be amended or removed by the
            User at any time.</p>
            <p><strong>Conversation data.</strong> The inquiries submitted to
            the Service, the responses generated in reply, and the citations
            to retrieved source materials, retained in order to permit the
            User to review prior conversations.</p>
            <p><strong>Usage telemetry.</strong> Pseudonymous event data
            describing the User&rsquo;s interaction with features of the
            Service, processed for the purposes of analytics and product
            improvement.</p>
            <p><strong>Technical data.</strong> Standard request metadata,
            including internet-protocol address, user-agent identifier, and
            timestamps, processed for the purposes of security, fraud
            prevention, and service integrity.</p>
            <p>PaceUp does <em>not</em> collect biometric information,
            geolocation data, contact lists, payment-card details, or data
            obtained from third-party fitness platforms, save where the User
            expressly authorizes such integration in a future release of the
            Service.</p>
            """,
        ),
        (
            "3. Purposes and Legal Bases of Processing",
            """
            <ul>
              <li>to provide and administer the Service, including
              authentication, personalization of coaching outputs, and the
              persistence of training profiles and conversation histories;</li>
              <li>to improve the Service through analysis of aggregated and
              de-identified usage data;</li>
              <li>to safeguard the Service, including the detection of abuse,
              the enforcement of the Terms of Service, and the protection of
              accounts and infrastructure; and</li>
              <li>to communicate with the User in respect of administrative
              matters and, subject to prior consent, in respect of product
              updates.</li>
            </ul>
            """,
        ),
        (
            "4. Processing by Artificial-Intelligence Systems",
            """
            <p>When the User submits an inquiry to the Service, the text of
            the inquiry, together with such contextual information from the
            User&rsquo;s training profile and prior conversation as is
            reasonably necessary to formulate a response, is transmitted to
            our language-model provider (Google&rsquo;s Gemini API) acting in
            the capacity of a data processor. The provider processes such
            data on PaceUp&rsquo;s behalf and, in accordance with its
            contractual obligations, does not employ such data for the
            training of its general-purpose models. PaceUp does not sell or
            otherwise commercialize User conversations.</p>
            """,
        ),
        (
            "5. Data Storage and International Transfers",
            """
            <p>Account information and conversation data are stored within
            Google Firebase (Firestore and Firebase Authentication) and may
            be processed in jurisdictions in which Google operates data-centre
            infrastructure. Our service providers maintain industry-standard
            organizational and technical security measures, and PaceUp
            applies additional access controls and encryption in transit. Any
            international transfer of personal data is effected in reliance
            upon appropriate safeguards as required by applicable law.</p>
            """,
        ),
        (
            "6. Retention Periods",
            """
            <ul>
              <li>Account and profile information: retained until deletion of
              the account by the User.</li>
              <li>Conversation history: retained until the relevant
              conversation or the account itself is deleted; individual
              conversations may be removed at any time from the sidebar.</li>
              <li>Usage telemetry: retained for a period not exceeding
              twenty-four (24) months, after which it is aggregated or
              irreversibly deleted.</li>
              <li>Backups: retained securely for a period not exceeding
              thirty (30) days following deletion, after which they are
              overwritten in the ordinary course.</li>
            </ul>
            """,
        ),
        (
            "7. Disclosure of Personal Information",
            """
            <p>PaceUp discloses personal information solely to the following
            categories of recipients:</p>
            <ul>
              <li>service providers acting in the capacity of data processors
              on PaceUp&rsquo;s behalf (including, without limitation, Google
              Firebase, Google Gemini, and our electronic-mail provider),
              each of which is bound by contractual data-protection
              obligations;</li>
              <li>competent governmental, regulatory, or judicial authorities,
              where disclosure is required by applicable law or is necessary
              to protect rights, safety, or the integrity of the Service; and</li>
              <li>a successor entity in the event of a merger, acquisition,
              reorganization, or sale of assets, subject to prior notice to
              the User.</li>
            </ul>
            <p>PaceUp does not sell personal information and does not display
            third-party advertising within the Service.</p>
            """,
        ),
        (
            "8. Rights of the Data Subject",
            """
            <p>Subject to applicable law, the User may have the right to
            access, rectify, port, restrict the processing of, or request the
            erasure of personal information, and to object to certain
            processing activities. The User may exercise such rights through
            the following means:</p>
            <ul>
              <li>amendment of profile information via the settings interface;</li>
              <li>deletion of individual conversations through the chat
              sidebar; and</li>
              <li>submission of a written request for account deletion or
              other data-subject rights to
              <a href="mailto:privacy@paceup.app">privacy@paceup.app</a>.</li>
            </ul>
            <p>PaceUp shall respond to verified requests within the time
            period prescribed by applicable law, ordinarily not exceeding
            thirty (30) days.</p>
            """,
        ),
        (
            "9. Children",
            """
            <p>The Service is not directed to children under the age of
            thirteen (13), and PaceUp does not knowingly collect personal
            information from such children. Where PaceUp becomes aware that
            personal information has been provided by a child without
            appropriate parental consent, such information shall be deleted
            without undue delay.</p>
            """,
        ),
        (
            "10. Cookies and Similar Technologies",
            """
            <p>PaceUp utilizes a limited number of strictly necessary cookies
            and local-storage entries for the purpose of maintaining
            authenticated sessions. PaceUp does not employ advertising or
            cross-site tracking technologies.</p>
            """,
        ),
        (
            "11. Information Security",
            """
            <p>PaceUp implements reasonable administrative, technical, and
            organizational measures designed to protect personal information
            against unauthorized access, alteration, disclosure, or
            destruction, including encryption in transit and authentication
            safeguards. Notwithstanding such measures, no system of electronic
            transmission or storage can be guaranteed to be entirely secure.
            In the event of a personal-data breach affecting the User,
            PaceUp shall provide notification in accordance with applicable
            law.</p>
            """,
        ),
        (
            "12. Amendments to this Policy",
            """
            <p>PaceUp reserves the right to amend this Privacy Policy from
            time to time. Material amendments shall be communicated through
            the Service or by electronic mail to the address associated with
            the User&rsquo;s account. The date appearing under
            &ldquo;Last updated&rdquo; reflects the date of the most recent
            revision.</p>
            """,
        ),
        (
            "13. Contact",
            """
            <p>Any inquiry, request, or complaint relating to this Privacy
            Policy or to PaceUp&rsquo;s processing of personal information
            should be addressed to
            <a href="mailto:privacy@paceup.app">privacy@paceup.app</a>.</p>
            """,
        ),
    ]
    _render_legal_page(
        title="Privacy Policy",
        subtitle="The terms governing the collection, use, and protection of personal information processed by PaceUp.",
        kicker="Legal &middot; Privacy",
        sections=sections,
    )
