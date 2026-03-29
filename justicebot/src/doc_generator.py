"""Document Generator Module - Auto-generate bail applications"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DocumentGenerator:
    def __init__(self):
        self.templates = self.load_templates()
    
    def load_templates(self) -> Dict[str, str]:
        """Load bail application templates"""
        return {
            "436A": self.get_436a_template(),
            "167": self.get_167_template(),
            "436": self.get_436_template(),
            "437": self.get_437_template()
        }
    
    def generate_bail_application(self, case_data: Dict[str, Any], bail_section: str) -> str:
        """Generate court-ready bail application"""
        try:
            template = self.templates.get(bail_section, self.get_437_template())
            
            application = template.format(
                accused_name=case_data.get("accused_name", "Accused"),
                accused_age=case_data.get("accused_age", "Unknown"),
                father_name=case_data.get("father_name", "Unknown"),
                occupation=case_data.get("occupation", "Unknown"),
                address=case_data.get("address", "Unknown"),
                sections=", ".join(case_data.get("sections", [])),
                detention_days=case_data.get("detention_days", 0),
                max_sentence=case_data.get("max_sentence_days", 0),
                court_name=case_data.get("court_name", "MAGISTRATE"),
                state=case_data.get("state", "Unknown"),
                bail_section=bail_section
            )
            
            return application
        except Exception as e:
            logger.error(f"Document generation error: {e}")
            return f"Error generating document: {str(e)}"
    
    def get_436a_template(self) -> str:
        return """IN THE COURT OF {court_name}
{state}

BAIL APPLICATION UNDER SECTION 436A CrPC

Applicant: {accused_name}
           S/O {father_name}
           Age: {accused_age}, Occupation: {occupation}
           Resident of: {address}

Versus

RESPONDENT: THE STATE OF {state}

GROUNDS FOR BAIL:

1. The applicant has been detained in judicial custody for {detention_days} days.

2. The maximum sentence prescribed is {max_sentence} days.

3. Pursuant to Section 436A CrPC, the applicant is entitled to MANDATORY BAIL as detention has exceeded half of maximum sentence.

4. The applicant is not a flight risk and has community ties.

5. The applicant has cooperated with investigation.

RELIEF SOUGHT:

It is respectfully prayed that this Hon'ble Court grant BAIL to the applicant under Section 436A CrPC.

Dated: [Date]
[Counsel Signature]"""
    
    def get_167_template(self) -> str:
        return """IN THE COURT OF {court_name}
{state}

BAIL APPLICATION UNDER SECTION 167 CrPC (DEFAULT BAIL)

Applicant: {accused_name}

GROUNDS FOR BAIL:

1. Chargesheet has not been filed till today.

2. The prescribed period of 90 days has elapsed since arrest.

3. As per Section 167 CrPC, the applicant is entitled to DEFAULT BAIL automatically.

4. Applicant is a bona fide resident with family ties.

RELIEF SOUGHT:

It is respectfully prayed that this Hon'ble Court grant DEFAULT BAIL to the applicant.

Dated: [Date]
[Counsel Signature]"""
    
    def get_436_template(self) -> str:
        return """IN THE COURT OF {court_name}
{state}

BAIL APPLICATION UNDER SECTION 436 CrPC

Applicant: {accused_name}

GROUNDS FOR BAIL:

1. The applicant is accused of {sections} which are BAILABLE OFFENCES.

2. Maximum punishment is {max_sentence} days.

3. Applicant is entitled to bail AS OF RIGHT under Section 436 CrPC.

4. Applicant has clean criminal record and strong community ties.

RELIEF SOUGHT:

It is respectfully prayed that this Hon'ble Court grant BAIL to the applicant.

Dated: [Date]
[Counsel Signature]"""
    
    def get_437_template(self) -> str:
        return """IN THE COURT OF {court_name}
{state}

BAIL APPLICATION UNDER SECTION 437 CrPC

Applicant: {accused_name}

GROUNDS FOR BAIL:

1. The applicant is accused of {sections}.

2. The applicant is a first-time offender with strong community ties.

3. There is no flight risk or tampering risk.

4. Applicant's family and employment depend on his liberty.

5. Bail is necessary to ensure continuity of normal life.

RELIEF SOUGHT:

It is respectfully prayed that this Hon'ble Court grant BAIL to the applicant.

Dated: [Date]
[Counsel Signature]"""
